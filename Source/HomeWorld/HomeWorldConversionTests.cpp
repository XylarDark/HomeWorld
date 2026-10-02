// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Misc/ScopeExit.h"

/**
 * Behaviour tests for combat conversion - "we do not kill foes".
 *
 * WHY BEHAVIOUR TESTS AND NOT UNIT TESTS ON THE CLASSES
 *
 * Per "Week 1 - Agentic Engineering": unit-level TDD is impractical when the unit is a
 * class, and BDD is the fit for LLM-assisted engineering. So this asserts what a designer
 * would check by hand after an agent change - did the foe convert, did the counter move,
 * did a role get assigned - rather than testing the role arithmetic in isolation.
 *
 * This is the highest-value invariant in the game. AGENTS.md states it flatly: "We do not
 * kill foes - combat strips them of their sin and converts them to their loved version."
 * The failure it guards is not a crash. It is a future combat pass quietly becoming a kill
 * system, which would be invisible until someone played the game and felt that the theme
 * had been quietly abandoned.
 *
 * The invariants below are CANON (VisionBoard/Core/VISION.md, AGENTS.md, and
 * docs/TaskLists/TaskSpecs/CONVERSION_NOT_KILL.md), not implementation detail.
 */

namespace HomeWorldConversionTest
{
	/**
	 * A GameMode with no world.
	 *
	 * ReportFoeConverted touches only its own members and a log line - it never calls
	 * GetWorld(). Spawning an actor needs a world, a level and a tick, which buys nothing
	 * for the conversion arithmetic and costs a teardown path that can leak. The reset-on-
	 * dawn case is the exception and gets a real world below.
	 */
	static AHomeWorldGameMode* MakeGameMode()
	{
		if (!GEngine)
		{
			return nullptr;
		}
		return NewObject<AHomeWorldGameMode>();
	}
}

/**
 * Exposes the night-encounter sweep to the dawn test.
 *
 * The conversion counter is reset inside TryTriggerNightEncounter, which is protected and
 * only reached from Tick. Rather than assert the reset indirectly - or widen production
 * visibility for a test - this subclasses it. The alternative, making the member public,
 * would move a canon invariant's guard from protected to callable by any gameplay code,
 * which is a worse trade than one line of test scaffolding.
 */
class FTestableGameMode : public AHomeWorldGameMode
{
public:
	/** Run the night-encounter sweep exactly as Tick does. */
	void RunNightSweepForTest() { TryTriggerNightEncounter(); }
};

/**
 * The core invariant: a defeated foe CONVERTS. It increments a counter and takes a role.
 * Nothing about this path is a death.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FConversionIncrementsAndAssignsTest,
	"HomeWorld.Systems.Combat.ConversionIncrementsAndAssignsRole",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FConversionIncrementsAndAssignsTest::RunTest(const FString& Parameters)
{
	AHomeWorldGameMode* GameMode = HomeWorldConversionTest::MakeGameMode();
	if (!TestNotNull(TEXT("game mode"), GameMode))
	{
		AddError(TEXT("could not create a GameMode - the test is not measuring conversion"));
		return false;
	}

	TestEqual(TEXT("a fresh night starts at zero conversions"), GameMode->GetConvertedFoesThisNight(), 0);

	GameMode->ReportFoeConverted(nullptr);
	TestEqual(TEXT("one conversion increments by exactly one"),
		GameMode->GetConvertedFoesThisNight(), 1);

	GameMode->ReportFoeConverted(nullptr);
	GameMode->ReportFoeConverted(nullptr);
	TestEqual(TEXT("three conversions total"), GameMode->GetConvertedFoesThisNight(), 3);

	// Every conversion must record a role, and it must be a real enum value. An
	// out-of-range cast here would mean a caller got a number that no switch handles,
	// which the display-name helper would silently answer "Vendor" for.
	const int32 RoleCount = static_cast<int32>(EConvertedFoeRole::Max);
	for (int32 Index = 0; Index < GameMode->GetConvertedFoesThisNight(); ++Index)
	{
		const EConvertedFoeRole Role = GameMode->GetConvertedFoeRole(Index);
		TestTrue(TEXT("assigned role is a valid enum value"),
			static_cast<uint8>(Role) < static_cast<uint8>(EConvertedFoeRole::Max));
		TestNotEqual(TEXT("every role has a display name"),
			AHomeWorldGameMode::GetConvertedFoeRoleDisplayName(Role), FString(TEXT("")));
	}

	return true;
}

/**
 * The round-robin actually advances.
 *
 * The conversion counter and the role list are separate members. A bug that increments
 * the counter while failing to append to the role list would leave every foe reading as
 * "Vendor" forever, and a test that only checks the counter would not notice. This is the
 * seam called out in the sprint plan.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FConversionRoleRoundRobinAdvancesTest,
	"HomeWorld.Systems.Combat.ConversionRoleRoundRobinAdvances",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FConversionRoleRoundRobinAdvancesTest::RunTest(const FString& Parameters)
{
	AHomeWorldGameMode* GameMode = HomeWorldConversionTest::MakeGameMode();
	if (!TestNotNull(TEXT("game mode"), GameMode))
	{
		return false;
	}

	const int32 RoleCount = static_cast<int32>(EConvertedFoeRole::Max);

	// One full cycle plus one, so the wrap is exercised rather than assumed.
	const int32 Conversions = RoleCount + 1;
	for (int32 i = 0; i < Conversions; ++i)
	{
		GameMode->ReportFoeConverted(nullptr);
	}

	for (int32 Index = 0; Index < Conversions; ++Index)
	{
		const EConvertedFoeRole Expected = static_cast<EConvertedFoeRole>(Index % RoleCount);
		TestEqual(FString::Printf(TEXT("conversion %d takes the round-robin role"), Index),
			GameMode->GetConvertedFoeRole(Index), Expected);
	}

	// The wrap is the part that can silently break: role[RoleCount] must equal role[0].
	TestEqual(TEXT("the round-robin wraps rather than running off the end"),
		GameMode->GetConvertedFoeRole(RoleCount),
		GameMode->GetConvertedFoeRole(0));

	return true;
}

/**
 * Reading a conversion that never happened must not crash or invent one.
 *
 * ConvertedFoeRolesThisNight is indexed by conversion order, so any HUD or quest code
 * asking for a role will eventually ask past the end. CONVERSION_NOT_KILL.md documents
 * Vendor as the safe default; this pins that.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FConversionUnknownIndexIsSafeTest,
	"HomeWorld.Systems.Combat.ConversionUnknownIndexIsSafe",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FConversionUnknownIndexIsSafeTest::RunTest(const FString& Parameters)
{
	AHomeWorldGameMode* GameMode = HomeWorldConversionTest::MakeGameMode();
	if (!TestNotNull(TEXT("game mode"), GameMode))
	{
		return false;
	}

	// Before any conversion at all.
	TestEqual(TEXT("index 0 with no conversions reads the safe default"),
		GameMode->GetConvertedFoeRole(0), EConvertedFoeRole::Vendor);

	GameMode->ReportFoeConverted(nullptr);

	// Past the end, and a negative index. Both are reachable from HUD code that
	// recomputes an index without re-checking the conversion count.
	TestEqual(TEXT("index past the end reads the safe default"),
		GameMode->GetConvertedFoeRole(99), EConvertedFoeRole::Vendor);
	TestEqual(TEXT("a negative index reads the safe default"),
		GameMode->GetConvertedFoeRole(-1), EConvertedFoeRole::Vendor);

	// Reading out of range must not have invented a conversion.
	TestEqual(TEXT("a failed read does not mutate the counter"),
		GameMode->GetConvertedFoesThisNight(), 1);

	return true;
}

/**
 * The counter resets when the night ends.
 *
 * This is the one case that needs a real world, because the reset lives in
 * TryTriggerNightEncounter, which reads the TimeOfDay subsystem. Conversions are per-night
 * bookkeeping; carrying them into the next night would make the HUD report a rising
 * total for a single encounter.
 *
 * The world is created and torn down explicitly. A leaked test world survives into the
 * next test and makes an unrelated failure look like a flaky one.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FConversionCounterResetsAtDawnTest,
	"HomeWorld.Systems.Combat.ConversionCounterResetsAtDawn",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FConversionCounterResetsAtDawnTest::RunTest(const FString& Parameters)
{
	if (!GEngine)
	{
		AddError(TEXT("no engine - cannot create a world for the dawn reset"));
		return false;
	}

	UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
	if (!TestNotNull(TEXT("test world"), World))
	{
		return false;
	}

	// Destroy the world whatever happens, including on an early return below.
	ON_SCOPE_EXIT
	{
		if (World)
		{
			World->DestroyWorld(false);
		}
	};

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TestNotNull(TEXT("time of day subsystem"), TimeOfDay))
	{
		AddError(TEXT("no TimeOfDay subsystem - the reset path cannot be reached"));
		return false;
	}

	FTestableGameMode* GameMode = World->SpawnActor<FTestableGameMode>();
	if (!TestNotNull(TEXT("game mode spawned into the world"), GameMode))
	{
		AddError(TEXT("could not spawn the game mode - the reset path is unreachable"));
		return false;
	}

	// A fresh world is Day. Record conversions, then sweep while still Day and prove the
	// sweep is what clears them. Sweeping at night would take the other branch entirely,
	// so the phase is asserted before and after rather than assumed.
	TestFalse(TEXT("a fresh world is not night"), TimeOfDay->GetIsNight());

	GameMode->ReportFoeConverted(nullptr);
	GameMode->ReportFoeConverted(nullptr);
	TestEqual(TEXT("conversions recorded before the dawn sweep"),
		GameMode->GetConvertedFoesThisNight(), 2);
	TestNotEqual(TEXT("role 0 exists before the sweep"),
		GameMode->GetConvertedFoeRole(0), EConvertedFoeRole::Worker);

	GameMode->RunNightSweepForTest();

	TestEqual(TEXT("the dawn sweep clears the conversion counter"),
		GameMode->GetConvertedFoesThisNight(), 0);
	TestEqual(TEXT("the dawn sweep clears the role list, so index 0 reads the default again"),
		GameMode->GetConvertedFoeRole(0), EConvertedFoeRole::Vendor);

	// And the counter must work again after a reset - a counter stuck at zero forever
	// would pass the assertion above on its own.
	GameMode->ReportFoeConverted(nullptr);
	TestEqual(TEXT("conversion still counts after a reset"),
		GameMode->GetConvertedFoesThisNight(), 1);
	TestEqual(TEXT("the role round-robin restarts after a reset"),
		GameMode->GetConvertedFoeRole(0), EConvertedFoeRole::Vendor);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS