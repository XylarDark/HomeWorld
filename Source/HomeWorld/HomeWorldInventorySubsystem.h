// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldInventorySubsystem.generated.h"

/**
 * Game instance subsystem — SYS V3 six-slot inventory-lite (Docs/03_SYSTEMS_MVP §2–3).
 * Exactly six slots; one stack per RES_*; stack max 9. Gather calls TryAddResource; tame/heal spend via SpendResource.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldInventorySubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

	virtual void Initialize(FSubsystemCollectionBase& Collection) override;

public:
	/** Try to add Amount of ResourceType (+1 gather). Returns false when inventory cannot accept (full stack / no empty slot). */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Try Add Resource"))
	bool TryAddResource(FName ResourceType, int32 Amount);

	/** Legacy alias — calls TryAddResource; logs GATHER: fail when inventory full. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Add Resource"))
	void AddResource(FName ResourceType, int32 Amount);

	/** Current count for normalized RES_* (legacy names mapped). */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Resource"))
	int32 GetResource(FName ResourceType) const;

	/** Sum of all six slot counts (physical goods). */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Total Physical Goods"))
	int32 GetTotalPhysicalGoods() const;

	/** Spend Amount if stack has enough; clears slot at 0. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Spend Resource"))
	bool SpendResource(FName ResourceType, int32 Amount);

	/** True if at least Amount of berry or herb is available (V4 tame offer). Prefers berry. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Has Tame Food"))
	bool HasTameFood(int32 Amount = 1) const;

	/** Spend 1× RES_BERRY or RES_HERB for tame offer. Returns spent id or NAME_None. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Spend Tame Food"))
	FName SpendTameFood();

	/** V6 heal — RES_HERB or RES_SEED available. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Has Heal Resource"))
	bool HasHealResource(int32 Amount = 1) const;

	/** Spend 1× RES_HERB (prefer) or RES_SEED for heal. */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Spend Heal Resource"))
	FName SpendHealResource();

	/** V8 — copy slot array for SaveGame. */
	void CopySlotsTo(TArray<FHomeWorldInventorySlot>& OutSlots) const;

	/** V8 — restore slots from SaveGame (replaces current). */
	void RestoreSlotsFrom(const TArray<FHomeWorldInventorySlot>& InSlots);

	/** Read-only slot view (0–5). */
	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Slot"))
	FHomeWorldInventorySlot GetSlot(int32 SlotIndex) const;

	UFUNCTION(BlueprintCallable, Category = "Inventory", meta = (DisplayName = "Get Slot Count"))
	int32 GetSlotCount() const { return HomeWorldInventory::SlotCount; }

	void SetLastBossRewardDisplay(int32 Amount, float DisplayUntilTime);
	bool GetLastBossRewardForHUD(int32& OutAmount, float& OutDisplayUntil) const;

private:
	UPROPERTY()
	TArray<FHomeWorldInventorySlot> Slots;

	int32 LastBossRewardAmount = 0;
	float LastBossRewardDisplayUntil = 0.f;

	void EnsureSlotArray();
	int32 FindSlotIndexForResource(FName NormalizedId) const;
	int32 FindEmptySlotIndex() const;
};
