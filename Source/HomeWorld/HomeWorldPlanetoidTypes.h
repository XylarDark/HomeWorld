// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldPlanetoidTypes.generated.h"

/** Planetoid biome type. Per PLANETOID_BIOMES.md: four biomes with distinct harvestables, monster types, and dungeon types. */
UENUM(BlueprintType)
enum class EBiomeType : uint8
{
	Desert,
	Forest,
	Marsh,
	Canyon,
	Max UMETA(Hidden)
};

/** Planetoid zone alignment: what the player does there (fight, harvest, empower). Per PLANETOID_BIOMES.md §3. */
UENUM(BlueprintType)
enum class EPlanetoidAlignment : uint8
{
	/** Fight: combat, conversion; strip sin, convert foes. */
	Corrupted,
	/** Harvest: gather resources; no combat focus. */
	Neutral,
	/** Empower: buffs, spirits, restoration. */
	Positive,
	Max UMETA(Hidden)
};
