// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Misc/ScopeExit.h"

/**
 * Behaviour tests for MUST #9 - TOD_NIGHT_HOME - and the form gates it depends on.
 *
 * THE LAW, verbatim from T0_MECHANIC_INVENTORIES_V1
 *
 *   "On homestead at Night/Dusk WITHOUT successful bed: stay FORM_BODY; no spirit;
 *    day abilities off."
 *   DONE-WHEN: "Night@home w/o bed -> FORM: body (not spirit) + day verbs rejected/off"
 *   Anti:      "Do not 'fix' by disabling Night entirely"
 *
 * #9 is P0. It is also the law that three other bites depend on: #11 requires it, #10 reuses
 * it, and #14 needs spirit reach. A silent regression here does not fail one beat - it makes
 * three behave as though they pass while the player is in the wrong form.
 *
 * WHY THIS IS THE FIRST TEST IN THE TRACK
 *
 * The implementation is already correct:
 *
 *     bool bSpirit = bSpiritCapablePhase && CanEnterSpiritForm();
 *     bool CanEnterSpiritForm() const { return bSpiritSleepGateGranted && bRuneGateUnlocked; }
 *
 * Phase alone can never grant spirit. That is the T0 law, expressed in one line - and it is
 * exactly the kind of line that gets "simplified" by a later pass, at which point the theme
 * quietly changes and nothing fails. So the law is pinned here in the project's own
 * vocabulary: FORM_BODY, FORM_SPIRIT, closed_fail.
 *
 * Per "Week 1 - Agentic Engineering": BDD over unit TDD. These assert the outcomes a
 * designer would check by hand after an agent change, not the boolean arithmetic.
 */

namespace HomeWorldFormTest
{
	/**
	 * A character in a real world, because the form sync reads the TimeOfDay subsystem.
	 *
	 * A NewObject'd character has no world, so CanEnterSpiritForm still works (it reads only
	 * its own members) but ApplyFormForPhase and AreDayBodyAbilitiesAllowed both return their
	 * no-world defaults. Testing those defaults would test a branch no player ever hits.
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

	/** A world plus its time-of-day subsystem, torn down together. */
	struct FScopedWorld
	{
		UWorld* World = nullptr;
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = nullptr;

		explicit FScopedWorld(const TCHAR* What)
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
			if (!Test->TestNotNull(TEXT("test world"), World))
			{
				return false;
			}
			if (!Test->TestNotNull(TEXT("time of day subsystem"), TimeOfDay))
			{
				return false;
			}
			return true;
		}
	};
}

/**
 * THE P0 LAW. Night without the named gates must stay FORM_BODY.
 *
 * This is the assertion the whole T0 form stack exists to make, and the one a later "simplify
 * the phase check" would silently delete.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNightWithoutGatesStaysBodyTest,
	"HomeWorld.T0.M9.NightWithoutGatesStaysBody",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FNightWithoutGatesStaysBodyTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M9 night-without-gates"));
	if (!Scope.Ok(this))
	{
		AddError(TEXT("cannot reach the form path without a world and a TimeOfDay subsystem"));
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	// A fresh character has neither gate. Night is the strongest case: if phase alone could
	// grant spirit, this is where it would show.
	TestFalse(TEXT("no sleep gate before a bed"), Character->IsSpiritSleepGateGranted());
	TestFalse(TEXT("no rune gate before #7 unlock"), Character->IsRuneGateUnlocked());
	TestFalse(TEXT("can-enter-spirit is false with no gates"), Character->CanEnterSpiritForm());

	Character->SyncFormWithTimeOfDay();

	TestEqual(TEXT("the phase really is Night"), Scope.TimeOfDay->GetCurrentPhase(),
		EHomeWorldTimeOfDayPhase::Night);
	TestFalse(TEXT("M9: night without gates stays FORM_BODY"), Character->GetIsSpiritForm());

	// Dusk is the other spirit-capable phase and had the same defect. Same assertion.
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dusk);
	Character->SyncFormWithTimeOfDay();
	TestFalse(TEXT("M9: dusk without gates stays FORM_BODY"), Character->GetIsSpiritForm());

	// The Anti row: night must not be "fixed" by disabling it. Night has to still be night.
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	TestEqual(TEXT("Anti: night is not disabled to satisfy the form law"),
		Scope.TimeOfDay->GetCurrentPhase(), EHomeWorldTimeOfDayPhase::Night);
	TestTrue(TEXT("Anti: night is still night after the round trip"),
		Scope.TimeOfDay->GetIsNight());

	return true;
}

/**
 * Day verbs are off at night, on at day.
 *
 * The DONE-WHEN names both halves: "FORM: body (not spirit) + day verbs rejected/off". Testing
 * only the form half would pass while sprint stays live at midnight, which is its own bug.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDayVerbsOffAtNightTest,
	"HomeWorld.T0.M9.DayVerbsOffAtNight",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDayVerbsOffAtNightTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M9 day-verbs"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	TestTrue(TEXT("day verbs allowed at Day"), Character->AreDayBodyAbilitiesAllowed());
	TestTrue(TEXT("day verbs allowed at Dawn"), [&] {
		Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
		return Character->AreDayBodyAbilitiesAllowed();
	}());

	TestFalse(TEXT("day verbs off at Dusk"), [&] {
		Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dusk);
		return Character->AreDayBodyAbilitiesAllowed();
	}());

	TestFalse(TEXT("day verbs off at Night"), [&] {
		Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		return Character->AreDayBodyAbilitiesAllowed();
	}());

	return true;
}

/**
 * BOTH gates grant spirit at night - and both are required.
 *
 * This is the positive half of #9, and it is the half that proves the negative half means
 * something. A build where spirit was impossible would satisfy "night without gates stays
 * body" perfectly while shipping no game.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBothGatesGrantSpiritTest,
	"HomeWorld.T0.M9.BothGatesGrantSpirit",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBothGatesGrantSpiritTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M9 both-gates"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	// Sleep only - rune still missing. This is the #11 dependency and must NOT grant spirit.
	Character->GrantSpiritSleepGate();
	TestTrue(TEXT("sleep gate granted by the bed path"), Character->IsSpiritSleepGateGranted());
	TestFalse(TEXT("sleep alone is not enough - rune still required"),
		Character->CanEnterSpiritForm());
	Character->SyncFormWithTimeOfDay();
	TestFalse(TEXT("closed_fail guard: sleep without rune must not become FORM_SPIRIT"),
		Character->GetIsSpiritForm());

	// Now the second gate. This is the only route to FORM_SPIRIT.
	Character->SetRuneGateUnlocked(true);
	TestTrue(TEXT("rune gate unlocked by #7"), Character->IsRuneGateUnlocked());
	TestTrue(TEXT("sleep AND rune grants spirit form"), Character->CanEnterSpiritForm());
	Character->SyncFormWithTimeOfDay();
	TestTrue(TEXT("M9 + #7 + #11: both gates at night gives FORM_SPIRIT"),
		Character->GetIsSpiritForm());

	return true;
}

/**
 * Day and dawn clear the sleep gate, so a new day starts in the body.
 *
 * ApplyFormForPhase calls ClearSpiritSleepGate on any non-spirit-capable phase. If that were
 * removed, a player who slept would stay spirit-formed all day - a soft-lock on the wrong
 * half of the transformation, and one that only shows up after a full day/night cycle.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDayClearsSleepGateTest,
	"HomeWorld.T0.M9.DayClearsSleepGate",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDayClearsSleepGateTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M9 day-clears"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	Character->GrantSpiritSleepGate();
	Character->SetRuneGateUnlocked(true);
	Character->SyncFormWithTimeOfDay();
	TestTrue(TEXT("spirit at night with both gates"), Character->GetIsSpiritForm());

	// Dawn. The phase itself is not spirit-capable, so the gate must clear.
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("Dawn returns the player to FORM_BODY"), Character->GetIsSpiritForm());
	TestFalse(TEXT("Dawn clears the sleep gate"), Character->IsSpiritSleepGateGranted());
	TestTrue(TEXT("Dawn leaves the rune latch alone - it is a day unlock, not a bed grant"),
		Character->IsRuneGateUnlocked());

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
