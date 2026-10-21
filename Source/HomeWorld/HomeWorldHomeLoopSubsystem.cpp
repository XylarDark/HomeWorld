// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldHomeLoopSubsystem.h"

#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"

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
	OutRecipe = FHomeWorldRecipe();
	OutRecipe.Id = RecipeId;
	OutRecipe.Vessel = EHomeWorldHomeVessel::Pot;
	OutRecipe.BuffId = EHomeWorldHomeBuff::Stamina;

	if (RecipeId == FName(TEXT("RECIPE_KETTLE")))
	{
		FHomeWorldRecipeIngredient Herb;
		Herb.ChestItemId = FName(TEXT("ITEM_HERB"));
		Herb.PrepStation = EHomeWorldHomeStation::Sink;
		Herb.PrepSeconds = 4.f;
		Herb.CookSeconds = 10.f;
		OutRecipe.Ingredients.Add(Herb);
		return true;
	}

	if (RecipeId == FName(TEXT("RECIPE_GREENS_HERB")))
	{
		FHomeWorldRecipeIngredient Herb;
		Herb.ChestItemId = FName(TEXT("ITEM_HERB"));
		Herb.PrepStation = EHomeWorldHomeStation::Sink;
		Herb.PrepSeconds = 4.f;
		Herb.CookSeconds = 10.f;
		OutRecipe.Ingredients.Add(Herb);

		FHomeWorldRecipeIngredient Greens;
		Greens.ChestItemId = FName(TEXT("ITEM_GREENS"));
		Greens.PrepStation = EHomeWorldHomeStation::Board;
		Greens.PrepSeconds = 6.f;
		Greens.CookSeconds = 10.f;
		OutRecipe.Ingredients.Add(Greens);
		return true;
	}

	return false;
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
		if (int32* Count = Chest.Find(Work.ChestItemId))
		{
			if (*Count > 0)
			{
				--(*Count);
			}
		}
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
	ArmFromServe(SyncFactor);
}

void UHomeWorldHomeLoopSubsystem::ArmFromServe(float SyncFactor)
{
	if (!bOpeningDayEnded)
	{
		return;
	}
	if (LastPhase != EHomeWorldTimeOfDayPhase::Dawn && LastPhase != EHomeWorldTimeOfDayPhase::Dusk)
	{
		return;
	}
	FHomeWorldRecipe Recipe;
	if (!GetRecipe(LastServe.RecipeId, Recipe))
	{
		return;
	}
	ArmedBuff.bOccupied = true;
	ArmedBuff.bLive = false;
	ArmedBuff.BuffId = Recipe.BuffId;
	ArmedBuff.SyncFactor = SyncFactor;
	ArmedBuff.CleanFactor = GetCleanFactor();
	ArmedBuff.CoveredDayId = UpcomingDayId;
}

float UHomeWorldHomeLoopSubsystem::GetCleanFactor() const
{
	if (DustSurfaces.Num() == 0)
	{
		return 1.f;
	}
	int32 Sum = 0;
	for (const FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		Sum += Surface.Dust;
	}
	const float Cap = static_cast<float>(DustSurfaces.Num() * 3);
	const float Filthy = Cap > 0.f ? static_cast<float>(Sum) / Cap : 0.f;
	return 1.f - 0.5f * Filthy;
}

float UHomeWorldHomeLoopSubsystem::GetSprintBonusSeconds() const
{
	if (!ArmedBuff.bLive || ArmedBuff.BuffId != EHomeWorldHomeBuff::Stamina)
	{
		return 0.f;
	}
	return 60.f * ArmedBuff.SyncFactor * ArmedBuff.CleanFactor;
}

void UHomeWorldHomeLoopSubsystem::EnterDay()
{
	ActiveDayId = UpcomingDayId;
	++UpcomingDayId;
	ArmedBuff.bLive = ArmedBuff.bOccupied && ArmedBuff.CoveredDayId == ActiveDayId;
	if (ArmedBuff.bLive && ArmedBuff.BuffId != EHomeWorldHomeBuff::Stamina)
	{
		UE_LOG(LogTemp, Log, TEXT("home_loop: buff logs only"));
	}
}

void UHomeWorldHomeLoopSubsystem::LeaveDay()
{
	if (ArmedBuff.bOccupied && ArmedBuff.CoveredDayId == ActiveDayId)
	{
		ArmedBuff = FHomeWorldArmedBuff();
	}
	ArmedBuff.bLive = false;
	ActiveDayId = 0;
}

void UHomeWorldHomeLoopSubsystem::ApplyPhase(EHomeWorldTimeOfDayPhase Phase, bool bFirst)
{
	const bool bWasDay = !bFirst && LastPhase == EHomeWorldTimeOfDayPhase::Day;
	const bool bIsDay = Phase == EHomeWorldTimeOfDayPhase::Day;
	const bool bHome = Phase == EHomeWorldTimeOfDayPhase::Dawn || Phase == EHomeWorldTimeOfDayPhase::Dusk;

	if (!bFirst && !bHome && bWindowOpen)
	{
		CloseWindow();
	}
	if (bWasDay && !bIsDay)
	{
		LeaveDay();
	}
	if (bIsDay && (bFirst || LastPhase != EHomeWorldTimeOfDayPhase::Day))
	{
		EnterDay();
	}
	if (bHome && !bWindowOpen)
	{
		OpenWindow();
	}
	if (Phase == EHomeWorldTimeOfDayPhase::Dawn && (bFirst || LastPhase != EHomeWorldTimeOfDayPhase::Dawn))
	{
		AddDawnDust();
	}
	LastPhase = Phase;
	bPhaseInitialized = true;
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
		ApplyPhase(Phase, true);
		return;
	}
	if (Phase == LastPhase)
	{
		return;
	}
	ApplyPhase(Phase, false);
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
	RunCleaningWisps();
	GrowPlots();
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
	TickClean(Step);
}

void UHomeWorldHomeLoopSubsystem::Advance(float Seconds)
{
	SyncPhase();
	RunAssignedStations();
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

bool UHomeWorldHomeLoopSubsystem::TryAssignWispToStation(FName WispId, EHomeWorldHomeStation Station)
{
	if (WispId.IsNone())
	{
		return false;
	}
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.WispId == WispId)
		{
			return false;
		}
	}
	FHomeWorldWispAssignment Assignment;
	Assignment.WispId = WispId;
	Assignment.Target = EHomeWorldWispTarget::Station;
	Assignment.Station = Station;
	WispAssignments.Add(Assignment);
	return true;
}

const FHomeWorldWispAssignment* UHomeWorldHomeLoopSubsystem::FindWisp(FName WispId) const
{
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.WispId == WispId)
		{
			return &Assignment;
		}
	}
	return nullptr;
}

void UHomeWorldHomeLoopSubsystem::RunAssignedStations()
{
	if (!bWindowOpen)
	{
		return;
	}
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.Target != EHomeWorldWispTarget::Station)
		{
			continue;
		}
		FHomeWorldRecipe Recipe;
		const FName RecipeId = ActiveRecipeId.IsNone() ? FName(TEXT("RECIPE_KETTLE")) : ActiveRecipeId;
		if (!GetRecipe(RecipeId, Recipe))
		{
			continue;
		}
		for (int32 Index = 0; Index < Recipe.Ingredients.Num(); ++Index)
		{
			if (Recipe.Ingredients[Index].PrepStation != Assignment.Station)
			{
				continue;
			}
			const bool bStarted = Works.IsValidIndex(Index) && Works[Index].bPrepStarted;
			if (!bStarted)
			{
				BeginPrep(RecipeId, Index);
			}
		}
	}
}

bool UHomeWorldHomeLoopSubsystem::TryAssignWispToSurface(FName WispId, FName SurfaceId)
{
	if (WispId.IsNone() || SurfaceId.IsNone() || FindSurface(SurfaceId) == nullptr)
	{
		return false;
	}
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.WispId == WispId)
		{
			return false;
		}
	}
	FHomeWorldWispAssignment Assignment;
	Assignment.WispId = WispId;
	Assignment.Target = EHomeWorldWispTarget::Surface;
	Assignment.SurfaceId = SurfaceId;
	WispAssignments.Add(Assignment);
	return true;
}

bool UHomeWorldHomeLoopSubsystem::RegisterDustProp(FName SurfaceId)
{
	if (SurfaceId.IsNone() || SurfaceId == FName(TEXT("Floor")) || FindSurface(SurfaceId) != nullptr)
	{
		return false;
	}
	int32 Props = 0;
	for (const FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		if (Surface.SurfaceId != FName(TEXT("Floor")))
		{
			++Props;
		}
	}
	if (Props >= 6)
	{
		return false;
	}
	FHomeWorldDustSurface Surface;
	Surface.SurfaceId = SurfaceId;
	DustSurfaces.Add(Surface);
	return true;
}

FHomeWorldDustSurface* UHomeWorldHomeLoopSubsystem::FindSurface(FName SurfaceId)
{
	for (FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		if (Surface.SurfaceId == SurfaceId)
		{
			return &Surface;
		}
	}
	return nullptr;
}

const FHomeWorldDustSurface* UHomeWorldHomeLoopSubsystem::FindSurface(FName SurfaceId) const
{
	for (const FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		if (Surface.SurfaceId == SurfaceId)
		{
			return &Surface;
		}
	}
	return nullptr;
}

void UHomeWorldHomeLoopSubsystem::SetSurfaceDust(FName SurfaceId, int32 Dust)
{
	if (FHomeWorldDustSurface* Surface = FindSurface(SurfaceId))
	{
		Surface->Dust = FMath::Clamp(Dust, 0, 3);
	}
	DustTotal = 0;
	for (const FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		DustTotal += Surface.Dust;
	}
}

void UHomeWorldHomeLoopSubsystem::ClearSurface(FName SurfaceId)
{
	SetSurfaceDust(SurfaceId, 0);
}

void UHomeWorldHomeLoopSubsystem::AddDawnDust()
{
	if (FindSurface(FName(TEXT("Floor"))) == nullptr)
	{
		FHomeWorldDustSurface Floor;
		Floor.SurfaceId = FName(TEXT("Floor"));
		DustSurfaces.Add(Floor);
	}
	for (FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		Surface.Dust = FMath::Min(3, Surface.Dust + 1);
	}
	DustTotal = 0;
	for (const FHomeWorldDustSurface& Surface : DustSurfaces)
	{
		DustTotal += Surface.Dust;
	}
}

int32 UHomeWorldHomeLoopSubsystem::GetSurfaceDust(FName SurfaceId) const
{
	const FHomeWorldDustSurface* Surface = FindSurface(SurfaceId);
	return Surface ? Surface->Dust : 0;
}

bool UHomeWorldHomeLoopSubsystem::BeginClean(FName SurfaceId)
{
	if (!bWindowOpen || !bBodyForm || FindSurface(SurfaceId) == nullptr || CleanRemaining > 0.f)
	{
		return false;
	}
	CleanSurfaceId = SurfaceId;
	CleanRemaining = 3.f;
	return true;
}

void UHomeWorldHomeLoopSubsystem::TickClean(float Step)
{
	if (CleanRemaining <= 0.f)
	{
		return;
	}
	CleanRemaining -= Step;
	if (CleanRemaining <= 0.f)
	{
		CleanRemaining = 0.f;
		ClearSurface(CleanSurfaceId);
		CleanSurfaceId = NAME_None;
	}
}

void UHomeWorldHomeLoopSubsystem::RunCleaningWisps()
{
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.Target == EHomeWorldWispTarget::Surface)
		{
		ClearSurface(Assignment.SurfaceId);
		return;
		}
	}
}

bool UHomeWorldHomeLoopSubsystem::PlantSeed(int32 PlotIndex, UHomeWorldInventorySubsystem* Inventory, FName CropItemId)
{
	if (!bWindowOpen || !bBodyForm || !Inventory || PlotIndex < 0 || PlotIndex >= 4 || CropItemId.IsNone())
	{
		return false;
	}
	if (!Inventory->SpendResource(HomeWorldInventory::RES_SEED, 1))
	{
		return false;
	}
	if (Plots.Num() <= PlotIndex)
	{
		Plots.SetNum(PlotIndex + 1);
	}
	FHomeWorldPlot& Plot = Plots[PlotIndex];
	if (Plot.bPlanted)
	{
		Inventory->TryAddResource(HomeWorldInventory::RES_SEED, 1);
		return false;
	}
	Plot = FHomeWorldPlot();
	Plot.Index = PlotIndex;
	Plot.bPlanted = true;
	Plot.CropItemId = CropItemId;
	return true;
}

bool UHomeWorldHomeLoopSubsystem::TryAssignWispToPlot(FName WispId, int32 PlotIndex)
{
	if (WispId.IsNone() || !Plots.IsValidIndex(PlotIndex) || !Plots[PlotIndex].bPlanted)
	{
		return false;
	}
	for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
	{
		if (Assignment.WispId == WispId)
		{
			return false;
		}
	}
	FHomeWorldWispAssignment Assignment;
	Assignment.WispId = WispId;
	Assignment.Target = EHomeWorldWispTarget::Plot;
	Assignment.PlotIndex = PlotIndex;
	WispAssignments.Add(Assignment);
	return true;
}

bool UHomeWorldHomeLoopSubsystem::ClearWisp(FName WispId)
{
	const int32 Removed = WispAssignments.RemoveAll([&WispId](const FHomeWorldWispAssignment& Assignment)
	{
		return Assignment.WispId == WispId;
	});
	return Removed > 0;
}

void UHomeWorldHomeLoopSubsystem::GrowPlots()
{
	for (FHomeWorldPlot& Plot : Plots)
	{
		if (!Plot.bPlanted || Plot.bReady)
		{
			continue;
		}
		bool bTended = false;
		for (const FHomeWorldWispAssignment& Assignment : WispAssignments)
		{
			if (Assignment.Target == EHomeWorldWispTarget::Plot && Assignment.PlotIndex == Plot.Index)
			{
				bTended = true;
				break;
			}
		}
		if (!bTended)
		{
			continue;
		}
		++Plot.WindowsGrown;
		if (Plot.WindowsGrown >= 2)
		{
			Plot.bReady = true;
		}
	}
}

bool UHomeWorldHomeLoopSubsystem::HarvestPlot(int32 PlotIndex)
{
	FHomeWorldPlot* Plot = FindPlot(PlotIndex);
	if (!Plot || !Plot->bReady)
	{
		return false;
	}
	int32& Count = Chest.FindOrAdd(Plot->CropItemId);
	++Count;
	*Plot = FHomeWorldPlot();
	Plot->Index = PlotIndex;
	return true;
}

int32 UHomeWorldHomeLoopSubsystem::GetChestCount(FName ItemId) const
{
	const int32* Count = Chest.Find(ItemId);
	return Count ? *Count : 0;
}

int32 UHomeWorldHomeLoopSubsystem::GetPlotWindows(int32 PlotIndex) const
{
	return Plots.IsValidIndex(PlotIndex) ? Plots[PlotIndex].WindowsGrown : 0;
}

bool UHomeWorldHomeLoopSubsystem::IsPlotReady(int32 PlotIndex) const
{
	return Plots.IsValidIndex(PlotIndex) && Plots[PlotIndex].bReady;
}

FHomeWorldPlot* UHomeWorldHomeLoopSubsystem::FindPlot(int32 PlotIndex)
{
	return Plots.IsValidIndex(PlotIndex) ? &Plots[PlotIndex] : nullptr;
}
