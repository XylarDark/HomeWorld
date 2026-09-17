// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInventoryTypes.h"

namespace HomeWorldInventory
{
	static const TArray<FName> AllResourceIds = {
		RES_WOOD, RES_FIBER, RES_STONE, RES_BERRY, RES_HERB, RES_SEED
	};

	FName NormalizeResourceId(FName Raw)
	{
		if (Raw.IsNone())
		{
			return NAME_None;
		}
		const FString S = Raw.ToString();
		if (S.StartsWith(TEXT("RES_")))
		{
			return Raw;
		}
		if (S.Equals(TEXT("Wood"), ESearchCase::IgnoreCase))
		{
			return RES_WOOD;
		}
		if (S.Equals(TEXT("Ore"), ESearchCase::IgnoreCase) || S.Equals(TEXT("Stone"), ESearchCase::IgnoreCase))
		{
			return RES_STONE;
		}
		if (S.Equals(TEXT("Flowers"), ESearchCase::IgnoreCase) || S.Equals(TEXT("Flower"), ESearchCase::IgnoreCase)
			|| S.Equals(TEXT("Herb"), ESearchCase::IgnoreCase))
		{
			return RES_HERB;
		}
		if (S.Equals(TEXT("Fiber"), ESearchCase::IgnoreCase))
		{
			return RES_FIBER;
		}
		if (S.Equals(TEXT("Berry"), ESearchCase::IgnoreCase) || S.Equals(TEXT("Food"), ESearchCase::IgnoreCase))
		{
			return RES_BERRY;
		}
		if (S.Equals(TEXT("Seed"), ESearchCase::IgnoreCase))
		{
			return RES_SEED;
		}
		return Raw;
	}

	bool IsValidResourceId(FName NormalizedId)
	{
		return AllResourceIds.Contains(NormalizedId);
	}

	const TArray<FName>& GetAllResourceIds()
	{
		return AllResourceIds;
	}
}
