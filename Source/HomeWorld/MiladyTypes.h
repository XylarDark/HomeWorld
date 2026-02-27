// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "MiladyTypes.generated.h"

/** Metadata for a Milady NFT token (from tokenURI → JSON). Used for IPFS image URL. */
USTRUCT(BlueprintType)
struct FMiladyTokenMetadata
{
	GENERATED_BODY()

	/** Resolved image URL (IPFS gateway or HTTPS). Use for PNG download. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady")
	FString ImageURI;

	/** Raw token URI from contract (e.g. ipfs://... or https://...). */
	UPROPERTY(BlueprintReadOnly, Category = "Milady")
	FString TokenURI;

	/** Token ID. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady")
	int32 TokenId = 0;

	/** Optional name from metadata JSON. */
	UPROPERTY(BlueprintReadOnly, Category = "Milady")
	FString Name;
};
