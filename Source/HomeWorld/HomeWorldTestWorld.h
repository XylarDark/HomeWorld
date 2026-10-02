// Copyright HomeWorld. All Rights Reserved.

#pragma once

#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * The fixture every T0 beat law stands on: a throwaway world, its time-of-day subsystem,
 * and a character in it.
 *
 * WHY IT IS SHARED RATHER THAN COPIED
 *
 * The fixture has one dangerous property. A world that outlives its test is not a slow
 * leak, it is a fault that surfaces in some LATER test, in a file that has nothing to do
 * with the one that forgot to tear down. That failure mode is only diagnosable if there is
 * exactly one place where teardown can be forgotten, so there is exactly one place where
 * teardown is written. This header was extracted from HomeWorldCampNightTests.cpp and
 * HomeWorldDayGateTests.cpp, which had grown byte-equivalent copies of it.
 *
 * WHY THIS IS A GAME WORLD AND NOT PIE
 *
 * Every gate the beat verbs use is a subsystem query, a component lookup or a line trace.
 * A `UWorld::CreateWorld(EWorldType::Game, ...)` world registers components and services
 * line traces, which is all of them. PIE additionally supplies a default pawn, a player
 * controller and a HUD, and buys nothing here. HomeWorldDayGateTests used to describe its
 * positive halves as "PIE work" and decline to assert them; that turned out to be the
 * reason six beats had no positive evidence at all, since the PIE prove run cannot execute
 * (see HomeWorldBeatNodeGateTests.cpp for the whole argument).
 */
namespace HomeWorldTestWorld
{
	/** A world + TimeOfDay, torn down together. Leaked worlds poison later tests. */
	struct FScopedWorld
	{
		UWorld* World = nullptr;
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = nullptr;

		explicit FScopedWorld(const TCHAR* /*What*/)
		{
			World = UWorld::CreateWorld(EWorldType::Game, false);
			if (World)
			{
				TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
			}
		}

		~FScopedWorld()
		{
			if (World)
			{
				World->DestroyWorld(false);
				World = nullptr;
				TimeOfDay = nullptr;
			}
		}

		/** True when both the world and its subsystem exist. Reports which, if not. */
		bool Ok(FAutomationTestBase* Test) const
		{
			if (!Test->TestNotNull(TEXT("test world"), World))
			{
				return false;
			}
			return Test->TestNotNull(TEXT("time of day subsystem"), TimeOfDay);
		}
	};

	/**
	 * A character at the origin, in whatever form the world's phase allows.
	 *
	 * The pawn is spawned with NO controller, which is load-bearing for the interact
	 * traces and worth stating once here rather than at each use site:
	 * `APawn::GetControlRotation()` returns `FRotator::ZeroRotator` when there is no
	 * controller, and a zero rotator points down +X. So an actor placed on +X is the
	 * thing the character is looking at. Tests that rely on this should place their
	 * target on +X inside InteractTraceLengthCm and then assert the beat actually fired,
	 * so a mis-aimed trace fails loudly instead of reading as a content gap.
	 */
	static AHomeWorldCharacter* SpawnCharacter(UWorld* World)
	{
		if (!World || !GEngine)
		{
			return nullptr;
		}
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		return World->SpawnActor<AHomeWorldCharacter>(Params);
	}
}

#endif // WITH_DEV_AUTOMATION_TESTS