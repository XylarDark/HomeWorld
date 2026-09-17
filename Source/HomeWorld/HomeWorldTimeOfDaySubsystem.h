// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.generated.h"

/** Day/night phase for game logic. Stub; drive from DaySequence in Week 2+. */
UENUM(BlueprintType)
enum class EHomeWorldTimeOfDayPhase : uint8
{
	Day,
	Dusk,
	Night,
	Dawn
};

/** Broadcast when phase transitions to Night (optional night encounter hook). Not yet invoked; poll GetIsNight() for now. */
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnNightStarted);

/**
 * World subsystem for day/night. Game code queries phase/time through this API; implement with DaySequence in Week 2+.
 * Stub only; returns default phase and time.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldTimeOfDaySubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	/** Current phase (Day/Night/etc). Stub: returns Day. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Get Current Phase"))
	virtual EHomeWorldTimeOfDayPhase GetCurrentPhase() const;

	/** Normalized time in [0,1] over the full cycle. Stub: returns 0.25 (day). */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Get Normalized Time"))
	virtual float GetNormalizedTime() const;

	/** True when current phase is Night. Use for State Tree IsNight / Defend branch. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Get Is Night"))
	virtual bool GetIsNight() const;

	/** True when Defend-at-home phase is active (Phase 2 / Night). Same as GetIsNight(); use for Act 2 Defend stub and State Tree. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Get Is Defend Phase Active"))
	virtual bool GetIsDefendPhaseActive() const;

	/** Set current phase (Day=0, Dusk=1, Night=2, Dawn=3). Stub: sets hw.TimeOfDay.Phase for testing. Callable from C++/Blueprint. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Set Phase"))
	virtual void SetPhase(EHomeWorldTimeOfDayPhase Phase);

	/** Advance time-of-day to Dawn (e.g. after astral death). Calls SetPhase(Dawn). See docs/tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Advance To Dawn"))
	virtual void AdvanceToDawn();

	/**
	 * Push NightMix scalar to MPC_HomeWorld_Time when the asset exists (WAVE E slice look).
	 * Masters read NightMix per Docs/02_MATERIAL_SHEET.md; created by place_vs_mvp_markers.py.
	 * No-op if MPC missing (Content may be local-only on Windows host).
	 */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Apply Night Mix For Phase"))
	virtual void ApplyNightMixForPhase(EHomeWorldTimeOfDayPhase Phase);

	/** Set NightMix on MPC_HomeWorld_Time directly (0=day, 1=full night overlay). Logs result. */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Set Night Mix Scalar"))
	virtual void SetNightMixScalar(float NightMix);

	/**
	 * Seconds until dawn when current phase is Night (stub countdown).
	 * When phase is set to Night, a fixed-duration countdown starts (see hw.TimeOfDay.NightDurationSeconds, default 120).
	 * Returns -1 when not night. Used by HUD for "time until dawn" display. See docs/tasks (T4 night countdown).
	 */
	UFUNCTION(BlueprintCallable, Category = "TimeOfDay", meta = (DisplayName = "Get Seconds Until Dawn"))
	virtual float GetSecondsUntilDawn() const;

	/** Optional night encounter: broadcast when phase transitions to Night. Currently not invoked; poll GetIsNight() for spawn logic. See docs/tasks/NIGHT_ENCOUNTER.md. */
	UPROPERTY(BlueprintAssignable, Category = "TimeOfDay")
	FOnNightStarted OnNightStarted;

private:
	/** World time at which night phase ends (set when SetPhase(Night) is called). Stub countdown for HUD. */
	float NightPhaseEndTime = 0.f;
};
