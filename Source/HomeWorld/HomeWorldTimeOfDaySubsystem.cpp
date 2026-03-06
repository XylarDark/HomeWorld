// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldTimeOfDaySubsystem.h"
#include "HAL/IConsoleManager.h"
#include "Engine/World.h"

namespace
{
	// Override phase for testing (e.g. Defend branch). 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = use default.
	static TAutoConsoleVariable<int32> CVarTimeOfDayPhase(
		TEXT("hw.TimeOfDay.Phase"), 0,
		TEXT("Override time-of-day phase for testing: 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = default (Day)."));

	// Fixed duration of night phase in seconds for "time until dawn" stub countdown (T4 HUD). Default 120.
	static TAutoConsoleVariable<float> CVarNightDurationSeconds(
		TEXT("hw.TimeOfDay.NightDurationSeconds"), 120.f,
		TEXT("Night phase duration in seconds for stub countdown (Dawn in Ns). Used when phase is set to Night."));
}

EHomeWorldTimeOfDayPhase UHomeWorldTimeOfDaySubsystem::GetCurrentPhase() const
{
	const int32 Override = CVarTimeOfDayPhase.GetValueOnGameThread();
	if (Override >= 0 && Override <= 3)
	{
		return static_cast<EHomeWorldTimeOfDayPhase>(Override);
	}
	// Stub: drive from DaySequence in Week 2+.
	return EHomeWorldTimeOfDayPhase::Day;
}

float UHomeWorldTimeOfDaySubsystem::GetNormalizedTime() const
{
	// Stub: 0.25 = day; implement with DaySequence.
	return 0.25f;
}

bool UHomeWorldTimeOfDaySubsystem::GetIsNight() const
{
	return GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Night;
}

bool UHomeWorldTimeOfDaySubsystem::GetIsDefendPhaseActive() const
{
	return GetIsNight();
}

void UHomeWorldTimeOfDaySubsystem::SetPhase(EHomeWorldTimeOfDayPhase Phase)
{
	IConsoleVariable* CVar = IConsoleManager::Get().FindConsoleVariable(TEXT("hw.TimeOfDay.Phase"));
	if (CVar)
	{
		CVar->Set(static_cast<int32>(Phase));
	}
	// Start stub countdown when entering night so GetSecondsUntilDawn() and HUD "Dawn in Ns" work (T4).
	if (Phase == EHomeWorldTimeOfDayPhase::Night && GetWorld())
	{
		const float Duration = CVarNightDurationSeconds.GetValueOnGameThread();
		NightPhaseEndTime = GetWorld()->GetTimeSeconds() + Duration;
	}
}

void UHomeWorldTimeOfDaySubsystem::AdvanceToDawn()
{
	// Do not restore Health here — restoration is via day activities only (DAY_RESTORATION_LOOP.md, VISION).
	SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
}

float UHomeWorldTimeOfDaySubsystem::GetSecondsUntilDawn() const
{
	if (!GetIsNight() || !GetWorld()) return -1.f;
	const float Now = GetWorld()->GetTimeSeconds();
	// NightPhaseEndTime is set when SetPhase(Night) is called; if phase was set via console (CVar), use default duration from now.
	if (NightPhaseEndTime <= 0.f)
	{
		const float Duration = CVarNightDurationSeconds.GetValueOnGameThread();
		return Duration; // fixed stub: "Dawn in 120s" when phase set via hw.TimeOfDay.Phase 2
	}
	const float Remaining = NightPhaseEndTime - Now;
	return FMath::Max(0.f, Remaining);
}
