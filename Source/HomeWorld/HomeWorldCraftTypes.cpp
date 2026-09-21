// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCraftTypes.h"

namespace HomeWorldCraft
{
	FName RecipeIdToName(const EHomeWorldCraftRecipeId Recipe)
	{
		switch (Recipe)
		{
		case EHomeWorldCraftRecipeId::Campfire: return FName(TEXT("RECIPE_CAMPFIRE"));
		case EHomeWorldCraftRecipeId::Tent: return FName(TEXT("RECIPE_TENT"));
		case EHomeWorldCraftRecipeId::Torch: return FName(TEXT("RECIPE_TORCH"));
		case EHomeWorldCraftRecipeId::TameBait: return FName(TEXT("RECIPE_TAME_BAIT"));
		case EHomeWorldCraftRecipeId::HealSalve: return FName(TEXT("RECIPE_HEAL_SALVE"));
		case EHomeWorldCraftRecipeId::FishGear: return FName(TEXT("RECIPE_FISH_GEAR"));
		default: return NAME_None;
		}
	}

	EHomeWorldCraftRecipeId RecipeNameToId(const FName Name)
	{
		if (Name == FName(TEXT("RECIPE_CAMPFIRE"))) { return EHomeWorldCraftRecipeId::Campfire; }
		if (Name == FName(TEXT("RECIPE_TENT"))) { return EHomeWorldCraftRecipeId::Tent; }
		if (Name == FName(TEXT("RECIPE_TORCH"))) { return EHomeWorldCraftRecipeId::Torch; }
		if (Name == FName(TEXT("RECIPE_TAME_BAIT"))) { return EHomeWorldCraftRecipeId::TameBait; }
		if (Name == FName(TEXT("RECIPE_HEAL_SALVE"))) { return EHomeWorldCraftRecipeId::HealSalve; }
		if (Name == FName(TEXT("RECIPE_FISH_GEAR"))) { return EHomeWorldCraftRecipeId::FishGear; }
		return EHomeWorldCraftRecipeId::Campfire;
	}

	const TCHAR* GetCraftLogLabel(const EHomeWorldCraftRecipeId Recipe)
	{
		switch (Recipe)
		{
		case EHomeWorldCraftRecipeId::Campfire: return TEXT("CAMPFIRE");
		case EHomeWorldCraftRecipeId::Tent: return TEXT("TENT");
		case EHomeWorldCraftRecipeId::Torch: return TEXT("TORCH");
		case EHomeWorldCraftRecipeId::TameBait: return TEXT("TAME_BAIT");
		case EHomeWorldCraftRecipeId::HealSalve: return TEXT("HEAL_SALVE");
		case EHomeWorldCraftRecipeId::FishGear: return TEXT("FISH_GEAR");
		default: return TEXT("UNKNOWN");
		}
	}
}
