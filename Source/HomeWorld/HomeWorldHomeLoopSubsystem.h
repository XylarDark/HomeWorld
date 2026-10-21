// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "HomeWorldHomeLoopTypes.h"
#include "HomeWorldTimeOfDaySubsystem.h"

class AHomeWorldCharacter;
class UHomeWorldInventorySubsystem;

#include "HomeWorldHomeLoopSubsystem.generated.h"

/**
 * Cooking, cleaning, and the garden. Docs/42_HOME_LOOP_DESIGN.md.
 * Stations, dust, plots, and the armed buff live here, beside the character's tea gate.
 */
UCLASS()
class HOMEWORLD_API UHomeWorldHomeLoopSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	/** The six stations, in design order. No timers. */
	void GetStationIds(TArray<EHomeWorldHomeStation>& OutIds) const;

	/** Logs `home_loop: station <Id>` and returns that same line. */
	FString LogStation(EHomeWorldHomeStation Station) const;

	/** Bite 1 has no clock. Stays 0 until a later bite starts one. */
	float GetHomeClockSeconds() const { return HomeClockSeconds; }

	/** Recipe row. RECIPE_KETTLE is the first food id. */
	bool GetRecipe(FName RecipeId, FHomeWorldRecipe& OutRecipe) const;

	/**
	 * Opening-day kettle. Calls TryBrewNodeKettleTea and does not write the armed slot.
	 * After the first sleep, a later bite serves through the station timers instead.
	 */
	bool TryOpeningKettleBrew(AHomeWorldCharacter* Character);

	/** True until a post-tutorial serve writes the slot. */
	bool IsArmedBuffSlotEmpty() const { return !ArmedBuff.bOccupied; }
	const FHomeWorldArmedBuff& GetArmedBuff() const { return ArmedBuff; }

	/** Stamina seconds on the covered Day. 0 when the slot is empty or the Day is not active. */
	float GetSprintBonusSeconds() const;

	/** The first sleep that ends the opening day. Brews before that stay on the sprint path. */
	void SetOpeningDayEnded(bool bEnded) { bOpeningDayEnded = bEnded; }
	bool HasOpeningDayEnded() const { return bOpeningDayEnded; }

	/** Spirit form cannot run a station. Tests and the pawn set this before a run. */
	void SetBodyForm(bool bInBodyForm) { bBodyForm = bInBodyForm; }

	/** Dawn or dusk, 90 s. Advance is the test clock. */
	void Advance(float Seconds);
	bool IsHomeWindowOpen() const { return bWindowOpen; }
	float GetWindowRemaining() const { return WindowRemaining; }

	/** True when this station may run: home window, body form, and past the tutorial gate. */
	bool CanRunStation(EHomeWorldHomeStation Station) const;

	/** Start prep for one ingredient. Cook begins on a later Advance, once prep has finished. */
	bool BeginPrep(FName RecipeId, int32 IngredientIndex);

	/**
	 * Before the opening day ends, this is TryOpeningKettleBrew.
	 * After the first sleep, it starts kettle prep instead.
	 */
	bool TryKettleFromWorld(AHomeWorldCharacter* Character);

	bool DiscardPrepped(int32 IngredientIndex);

	int32 GetActiveWorkCount() const;
	float GetPrepRemaining(int32 IngredientIndex) const;
	bool IsIngredientPrepped(int32 IngredientIndex) const;
	bool IsIngredientCooking(int32 IngredientIndex) const;

	const FHomeWorldServeResult& GetLastServe() const { return LastServe; }
	int32 GetDustTotal() const { return DustTotal; }

	/** One wisp, one target. A second target on the same wisp is refused. */
	bool TryAssignWispToStation(FName WispId, EHomeWorldHomeStation Station);
	bool TryAssignWispToSurface(FName WispId, FName SurfaceId);
	const FHomeWorldWispAssignment* FindWisp(FName WispId) const;

	bool RegisterDustProp(FName SurfaceId);
	int32 GetSurfaceDust(FName SurfaceId) const;
	bool BeginClean(FName SurfaceId);

	bool PlantSeed(int32 PlotIndex, UHomeWorldInventorySubsystem* Inventory, FName CropItemId);
	bool TryAssignWispToPlot(FName WispId, int32 PlotIndex);
	bool ClearWisp(FName WispId);
	bool HarvestPlot(int32 PlotIndex);
	int32 GetChestCount(FName ItemId) const;
	int32 GetPlotWindows(int32 PlotIndex) const;
	bool IsPlotReady(int32 PlotIndex) const;

	/** Progress for the home_loop quest chain. Does not write the quest log. */
	void GetHomeLoopQuestProgress(bool& bKettleCooked, bool& bWispAssigned, bool& bSurfaceCleared, bool& bSeedPlanted) const;

private:
	void SyncPhase();
	void ApplyPhase(EHomeWorldTimeOfDayPhase Phase, bool bFirst);
	void EnterDay();
	void LeaveDay();
	void ArmFromServe(float SyncFactor);
	float GetCleanFactor() const;
	void OpenWindow();
	void CloseWindow();
	void ApplyStep(float Step);
	void ServeActive(float SyncFactor, bool bKeepUnfinishedPrep);
	void EnsureWorks(const FHomeWorldRecipe& Recipe);
	bool AllIngredientsCooked() const;
	float SyncFactorFromFinishes() const;

	struct FIngredientWork
	{
		bool bPrepStarted = false;
		bool bPrepped = false;
		bool bCooking = false;
		bool bCooked = false;
		float PrepRemaining = 0.f;
		float CookRemaining = 0.f;
		float CookDuration = 0.f;
		float CookFinishedAt = -1.f;
		FName ChestItemId;
	};

	void RunAssignedStations();
	void AddDawnDust();
	void SetSurfaceDust(FName SurfaceId, int32 Dust);
	void ClearSurface(FName SurfaceId);
	FHomeWorldDustSurface* FindSurface(FName SurfaceId);
	const FHomeWorldDustSurface* FindSurface(FName SurfaceId) const;
	void TickClean(float Step);
	void RunCleaningWisps();
	void GrowPlots();
	FHomeWorldPlot* FindPlot(int32 PlotIndex);

	float HomeClockSeconds = 0.f;
	bool bOpeningDayEnded = false;
	bool bBodyForm = true;
	bool bWindowOpen = false;
	bool bPhaseInitialized = false;
	float WindowRemaining = 0.f;
	int32 DustTotal = 0;
	int32 UpcomingDayId = 1;
	int32 ActiveDayId = 0;
	EHomeWorldTimeOfDayPhase LastPhase = EHomeWorldTimeOfDayPhase::Day;
	FName ActiveRecipeId = NAME_None;
	TArray<FIngredientWork> Works;
	FHomeWorldServeResult LastServe;
	FHomeWorldArmedBuff ArmedBuff;
	TArray<FHomeWorldWispAssignment> WispAssignments;
	TArray<FHomeWorldDustSurface> DustSurfaces;
	FName CleanSurfaceId;
	float CleanRemaining = 0.f;
	bool bClearedASurface = false;
	bool bPlantedASeed = false;
	TArray<FHomeWorldPlot> Plots;
	TMap<FName, int32> Chest;
};
