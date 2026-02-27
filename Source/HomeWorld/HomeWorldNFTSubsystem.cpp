// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldNFTSubsystem.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "Misc/ConfigCacheIni.h"

void UHomeWorldNFTSubsystem::LoadMiladyConfig()
{
	GConfig->GetString(TEXT("Milady"), TEXT("RemiliaContractAddress"), RemiliaContractAddress, GGameIni);
	GConfig->GetString(TEXT("Milady"), TEXT("EthereumRPCURL"), EthereumRPCURL, GGameIni);
	GConfig->GetString(TEXT("Milady"), TEXT("IPFSGateway"), IPFSGateway, GGameIni);
	if (IPFSGateway.IsEmpty())
	{
		IPFSGateway = TEXT("https://ipfs.io/ipfs/");
	}
}

bool UHomeWorldNFTSubsystem::VerifyMiladyOwnership(const FString& WalletAddress)
{
	// Stub: requires Web3 plugin eth_call to balanceOf(contract, wallet). Return false until integrated.
	(void)WalletAddress;
	return false;
}

void UHomeWorldNFTSubsystem::FetchMetadataFromURL(const FString& MetadataURL, int32 TokenId)
{
	PendingMetadataTokenId = TokenId;
	const FString ResolvedURL = ResolveIPFSUrl(MetadataURL);
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(ResolvedURL);
	Request->SetVerb(TEXT("GET"));
	Request->OnProcessRequestComplete().BindUObject(this, &UHomeWorldNFTSubsystem::OnMetadataResponse);
	Request->ProcessRequest();
}

void UHomeWorldNFTSubsystem::OnMetadataResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
	const int32 TokenId = PendingMetadataTokenId;
	FMiladyTokenMetadata Meta;
	Meta.TokenId = TokenId;
	if (!bSuccess || !Response.IsValid() || Response->GetResponseCode() != 200)
	{
		OnMetadataReceived.Broadcast(false, Meta);
		return;
	}
	const FString Content = Response->GetContentAsString();
	TSharedPtr<FJsonObject> Json;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Content);
	if (!FJsonSerializer::Deserialize(Reader, Json) || !Json.IsValid())
	{
		OnMetadataReceived.Broadcast(false, Meta);
		return;
	}
	Meta.TokenURI = Request->GetURL();
	if (Json->HasField(TEXT("image")))
	{
		Meta.ImageURI = this->ResolveIPFSUrl(Json->GetStringField(TEXT("image")));
	}
	if (Json->HasField(TEXT("name")))
	{
		Meta.Name = Json->GetStringField(TEXT("name"));
	}
	OnMetadataReceived.Broadcast(true, Meta);
}

void UHomeWorldNFTSubsystem::DownloadMiladyPNG(const FString& ImageURI, int32 TokenId)
{
	PendingPNGTokenId = TokenId;
	const FString ResolvedURL = ResolveIPFSUrl(ImageURI);
	TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
	Request->SetURL(ResolvedURL);
	Request->SetVerb(TEXT("GET"));
	Request->OnProcessRequestComplete().BindUObject(this, &UHomeWorldNFTSubsystem::OnPNGResponse);
	Request->ProcessRequest();
}

void UHomeWorldNFTSubsystem::OnPNGResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess)
{
	const int32 TokenId = PendingPNGTokenId;
	FString LocalPath;
	if (!bSuccess || !Response.IsValid() || Response->GetResponseCode() != 200)
	{
		OnPNGDownloaded.Broadcast(false, LocalPath);
		return;
	}
	const FString CacheDir = FPaths::ProjectSavedDir() / TEXT("MiladyCache");
	IFileManager::Get().MakeDirectory(*CacheDir, true);
	LocalPath = FPaths::Combine(CacheDir, FString::Printf(TEXT("%d.png"), TokenId));
	const TArray<uint8>& Payload = Response->GetContent();
	if (!FFileHelper::SaveArrayToFile(Payload, *LocalPath))
	{
		OnPNGDownloaded.Broadcast(false, FString());
		return;
	}
	OnPNGDownloaded.Broadcast(true, LocalPath);
}

FString UHomeWorldNFTSubsystem::GetCachedPNGPath(int32 TokenId) const
{
	return FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("MiladyCache"), FString::Printf(TEXT("%d.png"), TokenId));
}

FString UHomeWorldNFTSubsystem::ResolveIPFSUrl(const FString& Uri) const
{
	FString Gateway = IPFSGateway;
	if (Gateway.IsEmpty())
	{
		Gateway = TEXT("https://ipfs.io/ipfs/");
	}
	if (Uri.StartsWith(TEXT("ipfs://")))
	{
		return Gateway + Uri.RightChop(7);
	}
	if (Uri.StartsWith(TEXT("ipfs/")))
	{
		return Gateway + Uri;
	}
	return Uri;
}
