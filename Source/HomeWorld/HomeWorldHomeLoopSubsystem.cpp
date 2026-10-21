// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldHomeLoopSubsystem.h"

#include "HomeWorldCharacter.h"

namespace HomeWorldHomeLoop
{
	static const TCHAR* StationName(EHomeWorldHomeStation Station)
	{
		switch (Station)
		{
		case EHomeWorldHomeStation::Sink: return TEXT("Sink");
		case EHomeWorldHomeStation::Board: return TEXT("Board");
		case EHomeWorldHomeStation::Pot: return TEXT("Pot");
		case EHomeWorldHomeStation::Stove: return TEXT("Stove");
		case EHomeWorldHomeStation::Oven: return TEXT("Oven");
		case EHomeWorldHomeStation::Garbage: return TEXT("Garbage");
		default: return TEXT("Unknown");
		}
	}
}

void UHomeWorldHomeLoopSubsystem::GetStationIds(TArray<EHomeWorldHomeStation>& OutIds) const
{
	OutIds.Reset();
	OutIds.Add(EHomeWorldHomeStation::Sink);
	OutIds.Add(EHomeWorldHomeStation::Board);
	OutIds.Add(EHomeWorldHomeStation::Pot);
	OutIds.Add(EHomeWorldHomeStation::Stove);
	OutIds.Add(EHomeWorldHomeStation::Oven);
	OutIds.Add(EHomeWorldHomeStation::Garbage);
}

FString UHomeWorldHomeLoopSubsystem::LogStation(EHomeWorldHomeStation Station) const
{
	const FString Line = FString::Printf(TEXT("home_loop: station %s"), HomeWorldHomeLoop::StationName(Station));
	UE_LOG(LogTemp, Log, TEXT("%s"), *Line);
	return Line;
}

bool UHomeWorldHomeLoopSubsystem::GetRecipe(FName RecipeId, FHomeWorldRecipe& OutRecipe) const
{
	if (RecipeId != FName(TEXT("RECIPE_KETTLE")))
	{
		return false;
	}

	OutRecipe = FHomeWorldRecipe();
	OutRecipe.Id = RecipeId;
	OutRecipe.Vessel = EHomeWorldHomeVessel::Pot;
	OutRecipe.BuffId = EHomeWorldHomeBuff::Stamina;

	FHomeWorldRecipeIngredient Herb;
	Herb.ChestItemId = FName(TEXT("ITEM_HERB"));
	Herb.PrepStation = EHomeWorldHomeStation::Sink;
	Herb.PrepSeconds = 4.f;
	Herb.CookSeconds = 10.f;
	OutRecipe.Ingredients.Add(Herb);
	return true;
}

bool UHomeWorldHomeLoopSubsystem::TryOpeningKettleBrew(AHomeWorldCharacter* Character)
{
	if (!Character)
	{
		return false;
	}
	return Character->TryBrewNodeKettleTea();
}
