// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "MiladyTypes.h"
#include "HomeWorldNFTSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMiladyMetadataReceived, bool, bSuccess, FMiladyTokenMetadata, Metadata);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnMiladyPNGDownloaded, bool, bSuccess, FString, LocalPath);

/**
 * Game instance subsystem for Milady NFT (Remilia Collective) and metadata.
 * - Verify ownership via balanceOf (requires Web3 plugin; stub until then).
 * - Resolve tokenURI → metadata JSON (HTTP); parse image URL for PNG fetch.
 * Config: DefaultGame.ini [Milady] RemiliaContractAddress, EthereumRPCURL, IPFSGateway.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldNFTSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Broadcast when FetchMetadataFromURL completes. */
	UPROPERTY(BlueprintAssignable, Category = "Milady|NFT")
	FOnMiladyMetadataReceived OnMetadataReceived;

	/** Broadcast when DownloadMiladyPNG completes. */
	UPROPERTY(BlueprintAssignable, Category = "Milady|NFT")
	FOnMiladyPNGDownloaded OnPNGDownloaded;

	/** Verify that the given wallet owns at least one Milady. Requires Web3 plugin eth_call balanceOf; stub returns false until integrated. */
	UFUNCTION(BlueprintCallable, Category = "Milady|NFT", meta = (DisplayName = "Verify Milady Ownership"))
	bool VerifyMiladyOwnership(const FString& WalletAddress);

	/** Fetch metadata from a tokenURI result (e.g. https://ipfs.io/ipfs/... or ipfs://...). Resolves IPFS to gateway, HTTP GET, parses image field. Broadcasts OnMetadataReceived when done. */
	UFUNCTION(BlueprintCallable, Category = "Milady|NFT", meta = (DisplayName = "Fetch Metadata From URL"))
	void FetchMetadataFromURL(const FString& MetadataURL, int32 TokenId);

	/** Download PNG from ImageURI (IPFS gateway or HTTPS) and save to Saved/MiladyCache/TokenId.png. Broadcasts OnPNGDownloaded when done. */
	UFUNCTION(BlueprintCallable, Category = "Milady|NFT", meta = (DisplayName = "Download Milady PNG"))
	void DownloadMiladyPNG(const FString& ImageURI, int32 TokenId);

	/** Get path where downloaded PNG is saved (Saved/MiladyCache/TokenId.png). */
	UFUNCTION(BlueprintPure, Category = "Milady|NFT", meta = (DisplayName = "Get Cached PNG Path"))
	FString GetCachedPNGPath(int32 TokenId) const;

	/** Remilia Collective contract address (mainnet). Read from config [Milady] RemiliaContractAddress. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady|Config")
	FString RemiliaContractAddress;

	/** Ethereum RPC URL for eth_call. Read from config [Milady] EthereumRPCURL. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady|Config")
	FString EthereumRPCURL;

	/** IPFS gateway base (e.g. https://ipfs.io/ipfs/). Read from config [Milady] IPFSGateway. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady|Config")
	FString IPFSGateway;

	/** Load config from DefaultGame.ini [Milady]. Call once at startup or when needed. */
	UFUNCTION(BlueprintCallable, Category = "Milady|Config", meta = (DisplayName = "Load Milady Config"))
	void LoadMiladyConfig();

protected:
	void OnMetadataResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess);
	void OnPNGResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSuccess);
	FString ResolveIPFSUrl(const FString& Uri) const;

	int32 PendingMetadataTokenId = 0;
	int32 PendingPNGTokenId = 0;
};
