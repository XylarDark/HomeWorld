// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldVirtueSpawnTable.h"

UHomeWorldVirtueSpawnTable::UHomeWorldVirtueSpawnTable()
{
	CharacterChances = HomeWorldVirtue::PlaceholderChances();
	CollectibleChances = HomeWorldVirtue::PlaceholderChances();
}

bool UHomeWorldVirtueSpawnTable::AreChancesNonIncreasing() const
{
	return HomeWorldVirtue::ChancesAreNonIncreasing(CharacterChances)
		&& HomeWorldVirtue::ChancesAreNonIncreasing(CollectibleChances);
}
