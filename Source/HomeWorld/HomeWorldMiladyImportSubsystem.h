// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "MiladyTypes.h"
#include "HomeWorldMiladyImportSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FOnMiladyImportProgress, FString, StepName, int32, StepIndex, int32, TotalSteps);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnMiladyImportComplete, bool, bSuccess);

/**
 * Game instance subsystem that orchestrates the full Milady import flow:
 * Wallet (address) -> Verify ownership -> Fetch metadata -> Download PNG -> Meshy 2D->3D -> VRM4U import -> Retarget -> Spawn.
 * Stub: runs metadata fetch + PNG download via NFT subsystem; Meshy/VRM4U steps require plugins and are placeholders.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldMiladyImportSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Broadcast progress (step name, index, total). */
	UPROPERTY(BlueprintAssignable, Category = "Milady|Import")
	FOnMiladyImportProgress OnImportProgress;

	/** Broadcast when import finishes (success or failure). */
	UPROPERTY(BlueprintAssignable, Category = "Milady|Import")
	FOnMiladyImportComplete OnImportComplete;

	/** Start full import for the given token ID. Requires Web3 plugin to call tokenURI(tokenId) first; until then use ImportMiladyFromMetadataURL with a known metadata URL. */
	UFUNCTION(BlueprintCallable, Category = "Milady|Import", meta = (DisplayName = "Import Milady By Token Id"))
	void ImportMiladyByTokenId(int32 TokenId);

	/** Start import from a known metadata URL (e.g. from tokenURI or test). Fetches metadata, downloads PNG; Meshy/VRM4U steps are stubs until plugins integrated. */
	UFUNCTION(BlueprintCallable, Category = "Milady|Import", meta = (DisplayName = "Import Milady From Metadata URL"))
	void ImportMiladyFromMetadataURL(const FString& MetadataURL, int32 TokenId);

	/** Get last imported token metadata (if any). */
	UPROPERTY(BlueprintReadOnly, Category = "Milady|Import")
	FMiladyTokenMetadata LastImportedMetadata;

	/** Local path to last downloaded PNG (Saved/MiladyCache/TokenId.png). */
	UPROPERTY(BlueprintReadOnly, Category = "Milady|Import")
	FString LastDownloadedPNGPath;

private:
	UFUNCTION()
	void OnNFTMetadataReceived(bool bSuccess, FMiladyTokenMetadata Meta);
	UFUNCTION()
	void OnNFTPNGDownloaded(bool bSuccess, FString LocalPath);

	int32 PendingTokenId = 0;
};
