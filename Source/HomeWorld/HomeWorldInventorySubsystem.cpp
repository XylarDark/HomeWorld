// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInventorySubsystem.h"

void UHomeWorldInventorySubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	Super::Initialize(Collection);
	EnsureSlotArray();
}

void UHomeWorldInventorySubsystem::EnsureSlotArray()
{
	if (Slots.Num() != HomeWorldInventory::SlotCount)
	{
		Slots.SetNum(HomeWorldInventory::SlotCount);
	}
}

int32 UHomeWorldInventorySubsystem::FindSlotIndexForResource(FName NormalizedId) const
{
	for (int32 i = 0; i < Slots.Num(); ++i)
	{
		if (Slots[i].ResId == NormalizedId && Slots[i].Count > 0)
		{
			return i;
		}
	}
	return INDEX_NONE;
}

int32 UHomeWorldInventorySubsystem::FindEmptySlotIndex() const
{
	for (int32 i = 0; i < Slots.Num(); ++i)
	{
		if (Slots[i].IsEmpty())
		{
			return i;
		}
	}
	return INDEX_NONE;
}

bool UHomeWorldInventorySubsystem::TryAddResource(FName ResourceType, int32 Amount)
{
	if (Amount <= 0)
	{
		return false;
	}

	const FName Normalized = HomeWorldInventory::NormalizeResourceId(ResourceType);
	if (!HomeWorldInventory::IsValidResourceId(Normalized))
	{
		UE_LOG(LogTemp, Warning, TEXT("GATHER: reject unknown resource id '%s'"), *ResourceType.ToString());
		return false;
	}

	EnsureSlotArray();

	int32 SlotIndex = FindSlotIndexForResource(Normalized);
	if (SlotIndex == INDEX_NONE)
	{
		SlotIndex = FindEmptySlotIndex();
		if (SlotIndex == INDEX_NONE)
		{
			UE_LOG(LogTemp, Log, TEXT("GATHER: fail inventory full (no slot for %s)"), *Normalized.ToString());
			return false;
		}
		Slots[SlotIndex].ResId = Normalized;
		Slots[SlotIndex].Count = 0;
	}

	const int32 Space = HomeWorldInventory::StackMax - Slots[SlotIndex].Count;
	if (Space < Amount)
	{
		UE_LOG(LogTemp, Log, TEXT("GATHER: fail stack full for %s (%d/%d)"),
			*Normalized.ToString(), Slots[SlotIndex].Count, HomeWorldInventory::StackMax);
		return false;
	}

	Slots[SlotIndex].Count += Amount;
	UE_LOG(LogTemp, Log, TEXT("GATHER: %s +%d (slot %d now %d/%d)"),
		*Normalized.ToString(), Amount, SlotIndex, Slots[SlotIndex].Count, HomeWorldInventory::StackMax);
	return true;
}

void UHomeWorldInventorySubsystem::AddResource(FName ResourceType, int32 Amount)
{
	TryAddResource(ResourceType, Amount);
}

int32 UHomeWorldInventorySubsystem::GetResource(FName ResourceType) const
{
	const FName Normalized = HomeWorldInventory::NormalizeResourceId(ResourceType);
	const int32 SlotIndex = FindSlotIndexForResource(Normalized);
	return SlotIndex != INDEX_NONE ? Slots[SlotIndex].Count : 0;
}

int32 UHomeWorldInventorySubsystem::GetTotalPhysicalGoods() const
{
	int32 Total = 0;
	for (const FHomeWorldInventorySlot& Slot : Slots)
	{
		Total += Slot.Count;
	}
	return Total;
}

bool UHomeWorldInventorySubsystem::SpendResource(FName ResourceType, int32 Amount)
{
	if (Amount <= 0)
	{
		return true;
	}

	const FName Normalized = HomeWorldInventory::NormalizeResourceId(ResourceType);
	const int32 SlotIndex = FindSlotIndexForResource(Normalized);
	if (SlotIndex == INDEX_NONE || Slots[SlotIndex].Count < Amount)
	{
		return false;
	}

	Slots[SlotIndex].Count -= Amount;
	if (Slots[SlotIndex].Count <= 0)
	{
		Slots[SlotIndex].ResId = NAME_None;
		Slots[SlotIndex].Count = 0;
	}
	return true;
}

bool UHomeWorldInventorySubsystem::HasTameFood(int32 Amount) const
{
	return GetResource(HomeWorldInventory::RES_BERRY) >= Amount
		|| GetResource(HomeWorldInventory::RES_HERB) >= Amount;
}

bool UHomeWorldInventorySubsystem::HasHealResource(int32 Amount) const
{
	return GetResource(HomeWorldInventory::RES_HERB) >= Amount
		|| GetResource(HomeWorldInventory::RES_SEED) >= Amount;
}

FName UHomeWorldInventorySubsystem::SpendHealResource()
{
	if (GetResource(HomeWorldInventory::RES_HERB) >= 1)
	{
		if (SpendResource(HomeWorldInventory::RES_HERB, 1))
		{
			return HomeWorldInventory::RES_HERB;
		}
	}
	if (GetResource(HomeWorldInventory::RES_SEED) >= 1)
	{
		if (SpendResource(HomeWorldInventory::RES_SEED, 1))
		{
			return HomeWorldInventory::RES_SEED;
		}
	}
	return NAME_None;
}

void UHomeWorldInventorySubsystem::CopySlotsTo(TArray<FHomeWorldInventorySlot>& OutSlots) const
{
	OutSlots = Slots;
}

void UHomeWorldInventorySubsystem::RestoreSlotsFrom(const TArray<FHomeWorldInventorySlot>& InSlots)
{
	EnsureSlotArray();
	if (InSlots.Num() == HomeWorldInventory::SlotCount)
	{
		Slots = InSlots;
	}
}

FName UHomeWorldInventorySubsystem::SpendTameFood()
{
	if (GetResource(HomeWorldInventory::RES_BERRY) >= 1)
	{
		if (SpendResource(HomeWorldInventory::RES_BERRY, 1))
		{
			return HomeWorldInventory::RES_BERRY;
		}
	}
	if (GetResource(HomeWorldInventory::RES_HERB) >= 1)
	{
		if (SpendResource(HomeWorldInventory::RES_HERB, 1))
		{
			return HomeWorldInventory::RES_HERB;
		}
	}
	return NAME_None;
}

FHomeWorldInventorySlot UHomeWorldInventorySubsystem::GetSlot(int32 SlotIndex) const
{
	if (SlotIndex >= 0 && SlotIndex < Slots.Num())
	{
		return Slots[SlotIndex];
	}
	return FHomeWorldInventorySlot();
}

void UHomeWorldInventorySubsystem::SetLastBossRewardDisplay(int32 Amount, float DisplayUntilTime)
{
	LastBossRewardAmount = Amount;
	LastBossRewardDisplayUntil = DisplayUntilTime;
}

bool UHomeWorldInventorySubsystem::GetLastBossRewardForHUD(int32& OutAmount, float& OutDisplayUntil) const
{
	OutAmount = LastBossRewardAmount;
	OutDisplayUntil = LastBossRewardDisplayUntil;
	return LastBossRewardAmount > 0 && LastBossRewardDisplayUntil > 0.f;
}
