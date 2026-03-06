// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldInventorySubsystem.generated.h"

/**
 * Game instance subsystem for player resource inventory (Phase 1 resource collection).
 * Used when the player harvests resource piles: harvest interaction calls AddResource;
 * building/placement can call SpendResource. Stub for Day 3 (resource collection loop).
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldInventorySubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Add amount of a resource (e.g. from harvesting a pile). ResourceType matches AHomeWorldResourcePile::ResourceType. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Add Resource"))
	void AddResource(FName ResourceType, int32 Amount);

	/** Current amount of the given resource type (0 if never added). */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Resource"))
	int32 GetResource(FName ResourceType) const;

	/** Total count of all physical goods (sum of all resource amounts). Used for physical vs spiritual goods (T7); log via hw.Goods. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Total Physical Goods"))
	int32 GetTotalPhysicalGoods() const;

	/** Spend amount if player has enough; returns true if spent, false if insufficient. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Spend Resource"))
	bool SpendResource(FName ResourceType, int32 Amount);

private:
	UPROPERTY()
	TMap<FName, int32> ResourceCounts;
};
