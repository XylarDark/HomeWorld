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
};
