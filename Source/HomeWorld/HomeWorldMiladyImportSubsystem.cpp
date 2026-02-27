// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMiladyImportSubsystem.h"
#include "HomeWorldWalletSubsystem.h"
#include "HomeWorldNFTSubsystem.h"

namespace
{
	const int32 MILADY_IMPORT_TOTAL_STEPS = 5;
}

void UHomeWorldMiladyImportSubsystem::ImportMiladyByTokenId(int32 TokenId)
{
	// Requires Web3 plugin to call tokenURI(tokenId) and pass URL to ImportMiladyFromMetadataURL. Until then, broadcast failure.
	(void)TokenId;
	OnImportComplete.Broadcast(false);
}

void UHomeWorldMiladyImportSubsystem::ImportMiladyFromMetadataURL(const FString& MetadataURL, int32 TokenId)
{
	UWorld* World = GetWorld();
	if (!World)
	{
		OnImportComplete.Broadcast(false);
		return;
	}
	UGameInstance* GI = World->GetGameInstance();
	if (!GI)
	{
		OnImportComplete.Broadcast(false);
		return;
	}
	UHomeWorldNFTSubsystem* NFT = GI->GetSubsystem<UHomeWorldNFTSubsystem>();
	if (!NFT)
	{
		OnImportComplete.Broadcast(false);
		return;
	}
	PendingTokenId = TokenId;
	NFT->LoadMiladyConfig();
	OnImportProgress.Broadcast(TEXT("Fetch metadata"), 1, MILADY_IMPORT_TOTAL_STEPS);
	NFT->OnMetadataReceived.AddDynamic(this, &UHomeWorldMiladyImportSubsystem::OnNFTMetadataReceived);
	NFT->FetchMetadataFromURL(MetadataURL, TokenId);
}

void UHomeWorldMiladyImportSubsystem::OnNFTMetadataReceived(bool bSuccess, FMiladyTokenMetadata Meta)
{
	UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldNFTSubsystem* NFT = GI ? GI->GetSubsystem<UHomeWorldNFTSubsystem>() : nullptr;
	if (NFT)
	{
		NFT->OnMetadataReceived.RemoveAll(this);
	}
	if (!bSuccess || !NFT)
	{
		OnImportComplete.Broadcast(false);
		return;
	}
	LastImportedMetadata = Meta;
	OnImportProgress.Broadcast(TEXT("Download PNG"), 2, MILADY_IMPORT_TOTAL_STEPS);
	NFT->OnPNGDownloaded.AddDynamic(this, &UHomeWorldMiladyImportSubsystem::OnNFTPNGDownloaded);
	NFT->DownloadMiladyPNG(Meta.ImageURI, PendingTokenId);
}

void UHomeWorldMiladyImportSubsystem::OnNFTPNGDownloaded(bool bSuccess, FString LocalPath)
{
	UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldNFTSubsystem* NFT = GI ? GI->GetSubsystem<UHomeWorldNFTSubsystem>() : nullptr;
	if (NFT)
	{
		NFT->OnPNGDownloaded.RemoveAll(this);
	}
	if (!bSuccess)
	{
		OnImportComplete.Broadcast(false);
		return;
	}
	LastDownloadedPNGPath = LocalPath;
	OnImportProgress.Broadcast(TEXT("Meshy 2D->3D (stub)"), 3, MILADY_IMPORT_TOTAL_STEPS);
	OnImportProgress.Broadcast(TEXT("VRM4U import (stub)"), 4, MILADY_IMPORT_TOTAL_STEPS);
	OnImportProgress.Broadcast(TEXT("Done"), MILADY_IMPORT_TOTAL_STEPS, MILADY_IMPORT_TOTAL_STEPS);
	OnImportComplete.Broadcast(true);
}
