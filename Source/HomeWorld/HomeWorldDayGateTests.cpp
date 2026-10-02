// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * Behaviour tests for the day-gated T0 beats: #7 rune, #2 kettle, #3 plant, #4 backpack,
 * #6 field gather.
 *
 * WHAT THIS FILE IS, AND WHAT IT DELIBERATELY IS NOT
 *
 * Each of these five beats has a two-sided law in T0_MECHANIC_INVENTORIES_V1. The positive
 * side - "with the prop placed and the right resource in hand, the beat completes" - needs
 * a placed actor in a world and a real interact trace. That is PIE work, and it is what the
 * Lead's prove run covers. Asserting it here would need a fixture world with placed props,
 * which is a much larger harness than the laws are worth.
 *
 * The negative side needs nothing: each gate REFUSES under a wrong phase or the wrong form,
 * and the refusal is the law. That is what this file pins. If a later pass "simplifies" one
 * of these guards - drops the day check because it seems redundant, or lets the spirit form
 * use a day prop - nothing else in the tree would notice.
 *
 * Per the Anti rows, each beat also names a substitute that must NOT count. Those are marked
 * in the individual tests.
 *
 * Per "Week 1 - Agentic Engineering": BDD over unit TDD. These assert what a designer would
 * check by hand after an agent change, in the project's own vocabulary.
 */

namespace HomeWorldDayGateTest
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

		bool Ok(class FAutomationTestBase* Test) const
		{
			return Test->TestNotNull(TEXT("test world"), World)
				&& Test->TestNotNull(TEXT("time of day subsystem"), TimeOfDay);
		}
	};

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

/**
 * The shared day-gate law, checked on all five beats at once.
 *
 * Every one of these props is a DAY prop. Using one at Dusk or Night, or while in spirit
 * form, must be refused. Testing them as one table rather than five near-identical tests is
 * deliberate: the repetition across five call sites is exactly the thing a refactor would
 * break in one place and not the others, and a table cannot silently lose a row.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDayGatesRefuseAtDuskAndNightTest,
	"HomeWorld.T0.DayGates.RefuseAtDuskAndNight",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDayGatesRefuseAtDuskAndNightTest::RunTest(const FString& Parameters)
{
	HomeWorldDayGateTest::FScopedWorld Scope(TEXT("day-gates"));
	if (!Scope.Ok(this))
	{
		AddError(TEXT("cannot reach the day gates without a world"));
		return false;
	}

	// The five gated actions, named so a failure points at the beat, not at a table row.
	const TCHAR* BeatNames[] = {
		TEXT("#7 NODE_RUNE"), TEXT("#2 NODE_KETTLE"), TEXT("#3 NODE_PLANT_SLOT"),
		TEXT("#4 NODE_BACKPACK"), TEXT("#6 NODE_FIELD_GATHER") };

	// Body form throughout - this test is about the phase gate, and DayVerbsOffAtNight plus
	// BothGatesGrantSpirit in HomeWorldFormGateTests already cover the form half.
	for (int32 Pass = 0; Pass < 2; ++Pass)
	{
		const EHomeWorldTimeOfDayPhase Phase =
			Pass == 0 ? EHomeWorldTimeOfDayPhase::Dusk : EHomeWorldTimeOfDayPhase::Night;
		const TCHAR* PhaseName = Pass == 0 ? TEXT("Dusk") : TEXT("Night");

		Scope.TimeOfDay->SetPhase(Phase);
		AHomeWorldCharacter* Character = HomeWorldDayGateTest::SpawnCharacter(Scope.World);
		if (!TestNotNull(FString::Printf(TEXT("character at %s"), PhaseName), Character))
		{
			return false;
		}

		Character->SyncFormWithTimeOfDay();
		TestFalse(FString::Printf(TEXT("%s: body form at %s, no gates granted"), PhaseName, PhaseName),
			Character->GetIsSpiritForm());

		TestFalse(FString::Printf(TEXT("%s refused at %s"), BeatNames[0], PhaseName),
			Character->TryUnlockNodeRune());
		TestFalse(FString::Printf(TEXT("%s refused at %s"), BeatNames[1], PhaseName),
			Character->TryBrewNodeKettleTea());
		TestFalse(FString::Printf(TEXT("%s refused at %s"), BeatNames[2], PhaseName),
			Character->TryPlantNodePlantSlotHerb());
		TestFalse(FString::Printf(TEXT("%s refused at %s"), BeatNames[3], PhaseName),
			Character->TryOpenInventoryGated());
		TestFalse(FString::Printf(TEXT("%s refused at %s"), BeatNames[4], PhaseName),
			Character->TryCollectNodeFieldGather());

		// A refused action must leave no latch behind. A gate that returns false but still
		// sets its flag would pass every assertion above and then behave as unlocked.
		TestFalse(FString::Printf(TEXT("%s: no rune latch from a refused unlock at %s"),
			BeatNames[0], PhaseName), Character->IsRuneGateUnlocked());
		TestFalse(FString::Printf(TEXT("%s: no backpack latch from a refused open at %s"),
			BeatNames[3], PhaseName), Character->IsBackpackEquipped());
		TestFalse(FString::Printf(TEXT("%s: no gather latch from a refused collect at %s"),
			BeatNames[4], PhaseName), Character->IsFieldGatherCollected());
		TestFalse(FString::Printf(TEXT("%s: no tea gate from a refused brew at %s"),
			BeatNames[1], PhaseName), Character->IsTeaSprintGateActive());
	}

	return true;
}

/**
 * #4 MUST: inventory is gated by the backpack, not merely available.
 *
 * "Open inventory without equip != T0 pass" is the Anti row. With no equipped backpack the
 * inventory must refuse. Equipping is a world interact, so the positive half is PIE work -
 * but the negative half is the law that was previously unenforced, because inventory-lite
 * already existed and worked.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FInventoryGatedByBackpackTest,
	"HomeWorld.T0.M4.InventoryGatedByBackpack",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FInventoryGatedByBackpackTest::RunTest(const FString& Parameters)
{
	HomeWorldDayGateTest::FScopedWorld Scope(TEXT("M4 backpack"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldDayGateTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	// Day and body, so the phase and form gates are both satisfied. The ONLY thing left to
	// stop the inventory is the backpack - which is the point of the beat.
	TestFalse(TEXT("day body verbs allowed"), !Character->AreDayBodyAbilitiesAllowed());
	TestFalse(TEXT("no backpack equipped at session start"), Character->IsBackpackEquipped());
	TestFalse(TEXT("M4: inventory refuses with no backpack equipped"),
		Character->TryOpenInventoryGated());

	return true;
}

/**
 * #2 MUST: the sprint buff is gated by tea, not merely available.
 *
 * Anti row: "ungated MV sprint alone != pass". The inventories call out that movement sprint
 * already exists and works, so the beat is only real if tea is what grants the extra window.
 * IsTeaSprintGateActive must be false with no tea brewed.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FTeaGateOffWithoutBrewTest,
	"HomeWorld.T0.M2.TeaGateOffWithoutBrew",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FTeaGateOffWithoutBrewTest::RunTest(const FString& Parameters)
{
	HomeWorldDayGateTest::FScopedWorld Scope(TEXT("M2 kettle"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldDayGateTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	// Day, body, no herb brewed. The gate must be off. Movement sprint itself is untouched
	// and still exists - which is exactly why the Anti row exists. The gate is the public
	// read; the window it reads is protected, and IsTeaSprintGateActive is the contract.
	TestFalse(TEXT("M2: no tea sprint gate before brewing"), Character->IsTeaSprintGateActive());
	TestFalse(TEXT("M2: still no tea gate on a second read - the gate is not self-arming"),
		Character->IsTeaSprintGateActive());

	return true;
}

/**
 * #3 -> #12 MUST: plant and nurture are separate marks, and neither implies the other.
 *
 * "Nurture succeeds on planted slot; day/body nurture != pass" and "N2 stored-only != this
 * beat". The dependency is one-directional and a test that only checked the happy chain would
 * not notice nurture being granted on an unplanted slot - which is the #12 Anti row.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPlantAndNurtureAreDistinctMarksTest,
	"HomeWorld.T0.M3.PlantAndNurtureAreDistinctMarks",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPlantAndNurtureAreDistinctMarksTest::RunTest(const FString& Parameters)
{
	HomeWorldDayGateTest::FScopedWorld Scope(TEXT("M3/M12 plant"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	// Day and body. This world has no placed N1 crop, which is exactly the state the
	// inventories describe as the gap: the slot is not marked.
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldDayGateTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("#3: NODE_PLANT_SLOT is not day-planted with no crop placed"),
		Character->IsNodePlantSlotDayPlanted());
	TestFalse(TEXT("#12: NODE_PLANT_SLOT is not spirit-nurtured with no crop placed"),
		Character->IsNodePlantSlotSpiritNurtured());

	// A refusal must not invent the downstream mark. Nurture is a different verb from plant,
	// and conflating them is what the Anti row forbids.
	Character->TryNurtureNodePlantSlot();
	TestFalse(TEXT("#12: a refused nurture does not mark the slot as nurtured"),
		Character->IsNodePlantSlotSpiritNurtured());
	TestFalse(TEXT("#3: nurturing does not imply the slot was day-planted"),
		Character->IsNodePlantSlotDayPlanted());

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
