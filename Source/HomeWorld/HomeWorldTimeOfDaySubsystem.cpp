// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldTimeOfDaySubsystem.h"
#include "HAL/IConsoleManager.h"

namespace
{
	// Override phase for testing (e.g. Defend branch). 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = use default.
	static TAutoConsoleVariable<int32> CVarTimeOfDayPhase(
		TEXT("hw.TimeOfDay.Phase"), 0,
		TEXT("Override time-of-day phase for testing: 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = default (Day)."));
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
