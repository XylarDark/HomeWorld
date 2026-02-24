// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldTimeOfDaySubsystem.h"

EHomeWorldTimeOfDayPhase UHomeWorldTimeOfDaySubsystem::GetCurrentPhase() const
{
	// Stub: drive from DaySequence in Week 2+.
	return EHomeWorldTimeOfDayPhase::Day;
}

float UHomeWorldTimeOfDaySubsystem::GetNormalizedTime() const
{
	// Stub: 0.25 = day; implement with DaySequence.
	return 0.25f;
}
