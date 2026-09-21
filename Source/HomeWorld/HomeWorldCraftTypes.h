// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldCraftTypes.generated.h"

/** Named hearth recipes — Docs/canon/SCHEMA.md + GATHER_CRAFT_BIBLE (GC-B). */
UENUM(BlueprintType)
enum class EHomeWorldCraftRecipeId : uint8
{
	Campfire UMETA(DisplayName = "RECIPE_CAMPFIRE"),
	Tent UMETA(DisplayName = "RECIPE_TENT"),
	Torch UMETA(DisplayName = "RECIPE_TORCH"),
	TameBait UMETA(DisplayName = "RECIPE_TAME_BAIT"),
	HealSalve UMETA(DisplayName = "RECIPE_HEAL_SALVE"),
	FishGear UMETA(DisplayName = "RECIPE_FISH_GEAR"),
};

/** Hub bootstrap (no campfire yet) vs placed campfire vs post-unlock kitchen bind target. */
UENUM(BlueprintType)
enum class EHomeWorldCraftStationKind : uint8
{
	HubBootstrap UMETA(DisplayName = "Hub craft point"),
	Campfire UMETA(DisplayName = "Campfire"),
	Kitchen UMETA(DisplayName = "Cottage kitchen"),
	TentPlaceable UMETA(DisplayName = "Tent stub"),
};

namespace HomeWorldCraft
{
	HOMEWORLD_API FName RecipeIdToName(EHomeWorldCraftRecipeId Recipe);
	HOMEWORLD_API EHomeWorldCraftRecipeId RecipeNameToId(FName Name);
	HOMEWORLD_API const TCHAR* GetCraftLogLabel(EHomeWorldCraftRecipeId Recipe);
}
