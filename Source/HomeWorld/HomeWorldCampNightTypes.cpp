// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCampNightTypes.h"

namespace HomeWorldCampNight
{
	int32 GetGatedActorCount()
	{
		// Three guards. Kept as a function rather than a constant so a
		// test can assert the gate's width instead of trusting a number typed in prose.
		return 3;
	}

	bool StartsAsleep(EHomeWorldCampRole Role)
	{
		switch (Role)
		{
		// The guard holds a lit torch and a waking post. This is the actor whose state
		// the player actually changes, and the reason #14 cannot be "avoid and move on".
		case EHomeWorldCampRole::Guard:
			return false;
		// The two sleepers are the "keep them sleeping" pair.
		case EHomeWorldCampRole::Sleeper:
			return true;
		case EHomeWorldCampRole::Captive:
		default:
			return false;
		}
	}

	bool RequiresEasing(EHomeWorldCampRole Role)
	{
		switch (Role)
		{
		// The guard needs easing to fall asleep.
		case EHomeWorldCampRole::Guard:
			return true;
		// The sleepers need easing to STAY asleep. This is the load-bearing one: the
		// gate is satisfied by eased+asleep, so an untouched sleeper that happens to be
		// asleep does not open the door. The care is the requirement, not the outcome.
		case EHomeWorldCampRole::Sleeper:
			return true;
		case EHomeWorldCampRole::Captive:
		default:
			return false;
		}
	}

	bool CountsInFreedomGate(EHomeWorldCampRole Role)
	{
		return Role == EHomeWorldCampRole::Guard || Role == EHomeWorldCampRole::Sleeper;
	}

	const TCHAR* GetRoleLogName(EHomeWorldCampRole Role)
	{
		switch (Role)
		{
		case EHomeWorldCampRole::Guard: return TEXT("GUARD");
		case EHomeWorldCampRole::Sleeper: return TEXT("SLEEPER");
		case EHomeWorldCampRole::Captive: return TEXT("CAPTIVE");
		default: return TEXT("UNKNOWN");
		}
	}

	EHomeWorldSpiritTouchVerdict GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget Target)
	{
		switch (Target)
		{
		// Night tending. Must #12.
		case EHomeWorldSpiritTouchTarget::Soil:
			return EHomeWorldSpiritTouchVerdict::Allowed;
		// Unbinding is the rescue. Must #16.
		case EHomeWorldSpiritTouchTarget::Lashings:
			return EHomeWorldSpiritTouchVerdict::Allowed;
		// The care verb, and the exception that lets #14 and #16 exist at all.
		case EHomeWorldSpiritTouchTarget::ActorMind:
			return EHomeWorldSpiritTouchVerdict::Allowed;
		// A spirit has no hands. If this were Allowed the player could grab a guard and
		// drag them, and the beat becomes about moving bodies instead of easing minds.
		case EHomeWorldSpiritTouchTarget::ActorBody:
		default:
			return EHomeWorldSpiritTouchVerdict::Refused;
		}
	}

	const TCHAR* GetSpiritTouchReason(EHomeWorldSpiritTouchTarget Target)
	{
		switch (Target)
		{
		case EHomeWorldSpiritTouchTarget::Soil:
			return TEXT("allowed: tending soil is the night's verb (M12)");
		case EHomeWorldSpiritTouchTarget::Lashings:
			return TEXT("allowed: untying the lashings is the rescue (M16)");
		case EHomeWorldSpiritTouchTarget::ActorMind:
			return TEXT("allowed: easing thoughts is the care verb (M14)");
		case EHomeWorldSpiritTouchTarget::ActorBody:
			return TEXT("refused: a spirit has no hands; ease their thoughts, do not touch them");
		default:
			return TEXT("refused: unknown target");
		}
	}

	const TCHAR* GetSpiritTouchTargetLogName(EHomeWorldSpiritTouchTarget Target)
	{
		switch (Target)
		{
		case EHomeWorldSpiritTouchTarget::Soil: return TEXT("SOIL");
		case EHomeWorldSpiritTouchTarget::Lashings: return TEXT("LASHINGS");
		case EHomeWorldSpiritTouchTarget::ActorBody: return TEXT("ACTOR_BODY");
		case EHomeWorldSpiritTouchTarget::ActorMind: return TEXT("ACTOR_MIND");
		default: return TEXT("UNKNOWN");
		}
	}
}