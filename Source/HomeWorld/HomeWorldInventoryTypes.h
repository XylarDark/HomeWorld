// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldInventoryTypes.generated.h"

/** Six canonical RES_* IDs per Docs/03_SYSTEMS_MVP §3. */
namespace HomeWorldInventory
{
	inline const FName RES_WOOD = FName(TEXT("RES_WOOD"));
	inline const FName RES_FIBER = FName(TEXT("RES_FIBER"));
	inline const FName RES_STONE = FName(TEXT("RES_STONE"));
	inline const FName RES_BERRY = FName(TEXT("RES_BERRY"));
	inline const FName RES_HERB = FName(TEXT("RES_HERB"));
	inline const FName RES_SEED = FName(TEXT("RES_SEED"));

	inline constexpr int32 SlotCount = 6;
	inline constexpr int32 StackMax = 9;

	/** Map legacy pile/tutorial names to RES_* (evolve stub, do not parallel inventory). */
	FName NormalizeResourceId(FName Raw);

	/** True when Raw (after normalize) is one of the six RES_* IDs. */
	bool IsValidResourceId(FName NormalizedId);

	/** All six RES_* IDs in stable order (slot schema 0–5 when full set carried). */
	const TArray<FName>& GetAllResourceIds();
}

USTRUCT(BlueprintType)
struct FHomeWorldInventorySlot
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Inventory")
	FName ResId = NAME_None;

	UPROPERTY(BlueprintReadOnly, Category = "Inventory")
	int32 Count = 0;

	bool IsEmpty() const { return ResId.IsNone() || Count <= 0; }
};
