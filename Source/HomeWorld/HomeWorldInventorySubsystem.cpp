// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInventorySubsystem.h"

void UHomeWorldInventorySubsystem::AddResource(FName ResourceType, int32 Amount)
{
	if (Amount <= 0) return;
	ResourceCounts.FindOrAdd(ResourceType, 0) += Amount;
}

int32 UHomeWorldInventorySubsystem::GetResource(FName ResourceType) const
{
	const int32* Ptr = ResourceCounts.Find(ResourceType);
	return Ptr ? *Ptr : 0;
}

int32 UHomeWorldInventorySubsystem::GetTotalPhysicalGoods() const
{
	int32 Total = 0;
	for (const auto& Pair : ResourceCounts)
	{
		Total += Pair.Value;
	}
	return Total;
}

bool UHomeWorldInventorySubsystem::SpendResource(FName ResourceType, int32 Amount)
{
	if (Amount <= 0) return true;
	int32* Ptr = ResourceCounts.Find(ResourceType);
	if (!Ptr || *Ptr < Amount) return false;
	*Ptr -= Amount;
	return true;
}
