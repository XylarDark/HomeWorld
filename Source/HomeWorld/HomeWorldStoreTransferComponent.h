// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldStoreTransferComponent.generated.h"

class AHomeWorldCharacter;
class UHomeWorldInventorySubsystem;

/**
 * PL-C PA-07 — homestead Stored prop transfer (GATHERABLES_WORLD_STORED.md).
 * Day/body Interact: deposit 1 matching RES_* from inventory → StoredCount++,
 * or withdraw 1 Stored → inventory when deposit not possible.
 * Logs STORE: lines. No new masters.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldStoreTransferComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldStoreTransferComponent();

	UFUNCTION(BlueprintCallable, Category = "Store")
	FName GetResourceId() const { return ResourceId; }

	UFUNCTION(BlueprintCallable, Category = "Store")
	int32 GetStoredCount() const { return StoredCount; }

	UFUNCTION(BlueprintCallable, Category = "Store")
	void ConfigureResource(FName InResourceId);

	/** GC-B: craft spend decrements stored without withdrawing to inventory first. */
	void SetStoredCountForCraft(int32 NewCount);

	/** Deposit or withdraw one unit. Returns true on success. */
	UFUNCTION(BlueprintCallable, Category = "Store")
	bool TryTransfer(AHomeWorldCharacter* Character);

protected:
	/** Canonical RES_* for this Stored prop. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Store")
	FName ResourceId = HomeWorldInventory::RES_WOOD;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Store")
	int32 StoredCount = 0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Store", meta = (ClampMin = "1"))
	int32 MaxStored = 99;

private:
	UHomeWorldInventorySubsystem* GetInventory(AHomeWorldCharacter* Character) const;
	bool TryDeposit(UHomeWorldInventorySubsystem* Inv);
	bool TryWithdraw(UHomeWorldInventorySubsystem* Inv);
};
