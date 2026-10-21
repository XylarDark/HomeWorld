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

bool UHomeWorldHomeLoopSubsystem::CanRunStation(EHomeWorldHomeStation Station) const
{
	if (!bWindowOpen || !bBodyForm)
	{
		return false;
	}
	if (bOpeningDayEnded)
	{
		return true;
	}
	return Station == EHomeWorldHomeStation::Sink || Station == EHomeWorldHomeStation::Pot;
}

void UHomeWorldHomeLoopSubsystem::OpenWindow()
{
	bWindowOpen = true;
	WindowRemaining = 90.f;
}

void UHomeWorldHomeLoopSubsystem::SyncPhase()
{
	UWorld* World = GetWorld();
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TimeOfDay)
	{
		return;
	}
	const EHomeWorldTimeOfDayPhase Phase = TimeOfDay->GetCurrentPhase();
	if (!bPhaseInitialized)
	{
		bPhaseInitialized = true;
		LastPhase = Phase;
		if (Phase == EHomeWorldTimeOfDayPhase::Dawn || Phase == EHomeWorldTimeOfDayPhase::Dusk)
		{
			OpenWindow();
		}
		return;
	}
	if (Phase == LastPhase)
	{
		return;
	}
	LastPhase = Phase;
	const bool bHomeTime = Phase == EHomeWorldTimeOfDayPhase::Dawn || Phase == EHomeWorldTimeOfDayPhase::Dusk;
	if (bHomeTime && !bWindowOpen)
	{
		OpenWindow();
	}
	else if (!bHomeTime && bWindowOpen)
	{
		CloseWindow();
	}
}

void UHomeWorldHomeLoopSubsystem::EnsureWorks(const FHomeWorldRecipe& Recipe)
{
	if (Works.Num() != Recipe.Ingredients.Num())
	{
		Works.SetNum(Recipe.Ingredients.Num());
	}
}

bool UHomeWorldHomeLoopSubsystem::BeginPrep(FName RecipeId, int32 IngredientIndex)
{
	if (!bWindowOpen || !bBodyForm)
	{
		return false;
	}
	FHomeWorldRecipe Recipe;
	if (!GetRecipe(RecipeId, Recipe) || !Recipe.Ingredients.IsValidIndex(IngredientIndex))
	{
		return false;
	}
	if (!CanRunStation(Recipe.Ingredients[IngredientIndex].PrepStation))
	{
		return false;
	}
	if (!ActiveRecipeId.IsNone() && ActiveRecipeId != RecipeId)
	{
		return false;
	}
	EnsureWorks(Recipe);
	FIngredientWork& Work = Works[IngredientIndex];
	if (Work.bPrepStarted)
	{
		return false;
	}
	Work.bPrepStarted = true;
	Work.PrepRemaining = Recipe.Ingredients[IngredientIndex].PrepSeconds;
	Work.CookDuration = Recipe.Ingredients[IngredientIndex].CookSeconds;
	Work.ChestItemId = Recipe.Ingredients[IngredientIndex].ChestItemId;
	ActiveRecipeId = RecipeId;
	return true;
}

bool UHomeWorldHomeLoopSubsystem::TryKettleFromWorld(AHomeWorldCharacter* Character)
{
	if (!bOpeningDayEnded)
	{
		return TryOpeningKettleBrew(Character);
	}
	if (Character)
	{
		SetBodyForm(!Character->GetIsSpiritForm());
	}
	return BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0);
}

bool UHomeWorldHomeLoopSubsystem::DiscardPrepped(int32 IngredientIndex)
{
	if (!CanRunStation(EHomeWorldHomeStation::Garbage) || !Works.IsValidIndex(IngredientIndex))
	{
		return false;
	}
	FIngredientWork& Work = Works[IngredientIndex];
	if (!Work.bPrepped || Work.bCooking || Work.bCooked)
	{
		return false;
	}
	LastServe = FHomeWorldServeResult();
	LastServe.bDiscarded = true;
	LastServe.RecipeId = ActiveRecipeId;
	LastServe.SpentItemIds.Add(Work.ChestItemId);
	Work = FIngredientWork();
	if (GetActiveWorkCount() == 0)
	{
		ActiveRecipeId = NAME_None;
		Works.Reset();
	}
	return true;
}

int32 UHomeWorldHomeLoopSubsystem::GetActiveWorkCount() const
{
	int32 Count = 0;
	for (const FIngredientWork& Work : Works)
	{
		if (Work.bPrepStarted && !Work.bCooked)
		{
			++Count;
		}
	}
	return Count;
}

float UHomeWorldHomeLoopSubsystem::GetPrepRemaining(int32 IngredientIndex) const
{
	if (!Works.IsValidIndex(IngredientIndex) || !Works[IngredientIndex].bPrepStarted || Works[IngredientIndex].bPrepped)
	{
		return 0.f;
	}
	return Works[IngredientIndex].PrepRemaining;
}

bool UHomeWorldHomeLoopSubsystem::IsIngredientPrepped(int32 IngredientIndex) const
{
	return Works.IsValidIndex(IngredientIndex) && Works[IngredientIndex].bPrepped;
}

bool UHomeWorldHomeLoopSubsystem::IsIngredientCooking(int32 IngredientIndex) const
{
	return Works.IsValidIndex(IngredientIndex) && Works[IngredientIndex].bCooking;
}

bool UHomeWorldHomeLoopSubsystem::AllIngredientsCooked() const
{
	FHomeWorldRecipe Recipe;
	if (ActiveRecipeId.IsNone() || !GetRecipe(ActiveRecipeId, Recipe) || Works.Num() != Recipe.Ingredients.Num())
	{
		return false;
	}
	for (const FIngredientWork& Work : Works)
	{
		if (!Work.bCooked)
		{
			return false;
		}
	}
	return true;
}

float UHomeWorldHomeLoopSubsystem::SyncFactorFromFinishes() const
{
	if (Works.Num() == 0)
	{
		return 0.5f;
	}
	float MinFinish = Works[0].CookFinishedAt;
	float MaxFinish = MinFinish;
	for (const FIngredientWork& Work : Works)
	{
		MinFinish = FMath::Min(MinFinish, Work.CookFinishedAt);
		MaxFinish = FMath::Max(MaxFinish, Work.CookFinishedAt);
	}
	return (MaxFinish - MinFinish) <= 1.5f ? 1.f : 0.5f;
}

void UHomeWorldHomeLoopSubsystem::ServeActive(float SyncFactor, bool bKeepUnfinishedPrep)
{
	LastServe = FHomeWorldServeResult();
	LastServe.bServed = true;
	LastServe.SyncFactor = SyncFactor;
	LastServe.RecipeId = ActiveRecipeId;

	TArray<FIngredientWork> Kept;
	for (const FIngredientWork& Work : Works)
	{
		const bool bInVessel = Work.bCooking || Work.bCooked;
		if (bInVessel)
		{
			LastServe.SpentItemIds.Add(Work.ChestItemId);
			continue;
		}
		if (bKeepUnfinishedPrep && Work.bPrepStarted && !Work.bPrepped)
		{
			Kept.Add(Work);
		}
	}
	Works = MoveTemp(Kept);
	if (Works.Num() == 0)
	{
		ActiveRecipeId = NAME_None;
	}
}

void UHomeWorldHomeLoopSubsystem::CloseWindow()
{
	bWindowOpen = false;
	WindowRemaining = 0.f;
	bool bStillCooking = false;
	for (const FIngredientWork& Work : Works)
	{
		if (Work.bCooking && !Work.bCooked)
		{
			bStillCooking = true;
			break;
		}
	}
	if (bStillCooking)
	{
		ServeActive(0.5f, true);
	}
}

void UHomeWorldHomeLoopSubsystem::ApplyStep(float Step)
{
	for (FIngredientWork& Work : Works)
	{
		float TimeLeft = Step;
		if (Work.bPrepStarted && !Work.bPrepped)
		{
			const float PrepUse = FMath::Min(TimeLeft, Work.PrepRemaining);
			Work.PrepRemaining -= PrepUse;
			TimeLeft -= PrepUse;
			if (Work.PrepRemaining <= 0.f)
			{
				Work.PrepRemaining = 0.f;
				Work.bPrepped = true;
			}
		}
		if (TimeLeft <= 0.f)
		{
			continue;
		}
		if (Work.bPrepped && !Work.bCooking && !Work.bCooked)
		{
			Work.bCooking = true;
			Work.CookRemaining = Work.CookDuration;
		}
		if (Work.bCooking && !Work.bCooked)
		{
			Work.CookRemaining -= TimeLeft;
			if (Work.CookRemaining <= 0.f)
			{
				Work.CookRemaining = 0.f;
				Work.bCooked = true;
				Work.bCooking = false;
				Work.CookFinishedAt = HomeClockSeconds + Step;
			}
		}
	}
	if (AllIngredientsCooked())
	{
		ServeActive(SyncFactorFromFinishes(), false);
	}
}

void UHomeWorldHomeLoopSubsystem::Advance(float Seconds)
{
	SyncPhase();
	float Left = FMath::Max(0.f, Seconds);
	while (Left > KINDA_SMALL_NUMBER && bWindowOpen)
	{
		const float Step = FMath::Min(Left, WindowRemaining);
		if (Step <= KINDA_SMALL_NUMBER)
		{
			CloseWindow();
			break;
		}
		ApplyStep(Step);
		WindowRemaining -= Step;
		HomeClockSeconds += Step;
		Left -= Step;
		if (WindowRemaining <= KINDA_SMALL_NUMBER)
		{
			CloseWindow();
		}
	}
}
