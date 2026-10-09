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
 * The implementation is:
 *
 *     bool bSpirit = bSpiritCapablePhase && CanEnterSpiritForm();
 *     bool CanEnterSpiritForm() const { return bSpiritSleepGateGranted; }
 *
 * Phase alone can never grant spirit. The bed is the form change. That is the T0 law, expressed in one line - and it is
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
 * The bed at night grants spirit.
 *
 * This is the positive half of #9. A build where spirit was impossible would satisfy
 * "night without the sleep gate stays body" while shipping no night.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBedAtNightGrantsSpiritTest,
	"HomeWorld.T0.M11.BedAtNightGrantsSpirit",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBedAtNightGrantsSpiritTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M11 night bed"));
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

	TestTrue(TEXT("night bed grants spirit"), Character->TryBedSleepSpirit());
	TestTrue(TEXT("sleep gate is on"), Character->IsSpiritSleepGateGranted());
	TestTrue(TEXT("can enter spirit from the bed alone"), Character->CanEnterSpiritForm());
	TestTrue(TEXT("M11: night bed is FORM_SPIRIT"), Character->GetIsSpiritForm());

	return true;
}

/**
 * The day bed stays body. Sleep does not grant spirit and does not move the clock.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDayBedStaysBodyTest,
	"HomeWorld.T0.M11.DayBedStaysBody",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDayBedStaysBodyTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M11 day bed"));
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
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("day bed refuses the spirit grant"), Character->TryBedSleepSpirit());
	TestEqual(TEXT("day bed does not move the clock"), Scope.TimeOfDay->GetCurrentPhase(),
		EHomeWorldTimeOfDayPhase::Day);
	TestFalse(TEXT("M11: day bed stays FORM_BODY"), Character->GetIsSpiritForm());
	TestFalse(TEXT("day bed does not leave the sleep gate on"), Character->IsSpiritSleepGateGranted());

	return true;
}

/**
 * Dawn does not end spirit. Still out, the first sickness stack starts.
 * Vision board, 2026-10-08. Replaces the 2026-10-02 law that dawn cleared the sleep gate.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDawnKeepsSpiritAndStartsSicknessTest,
	"HomeWorld.T0.M9.DawnKeepsSpiritAndStartsSickness",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDawnKeepsSpiritAndStartsSicknessTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("M9 dawn-keeps-spirit"));
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
	Character->SyncFormWithTimeOfDay();
	TestTrue(TEXT("spirit at night with the bed"), Character->GetIsSpiritForm());
	TestEqual(TEXT("night has no sickness stack yet"), Character->GetSpiritSicknessStacks(), 0);
	TestTrue(TEXT("night move scale is full"),
		FMath::IsNearlyEqual(Character->GetSpiritSicknessMoveScale(), 1.f));

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	Character->SyncFormWithTimeOfDay();

	TestTrue(TEXT("Dawn keeps FORM_SPIRIT"), Character->GetIsSpiritForm());
	TestTrue(TEXT("Dawn keeps the sleep gate"), Character->IsSpiritSleepGateGranted());
	TestEqual(TEXT("Dawn out of bed starts one stack"), Character->GetSpiritSicknessStacks(), 1);
	TestEqual(TEXT("scarf takes one colder step"), Character->GetSpiritSicknessScarfStep(), 1);
	TestTrue(TEXT("one stack slows movement 15 percent"),
		FMath::IsNearlyEqual(Character->GetSpiritSicknessMoveScale(), 0.85f));

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Character->SyncFormWithTimeOfDay();
	TestTrue(TEXT("Day still out stays FORM_SPIRIT"), Character->GetIsSpiritForm());
	TestEqual(TEXT("Day does not add a second immediate stack"), Character->GetSpiritSicknessStacks(), 1);

	return true;
}

/**
 * Touch clears stacks and stays spirit. Wake ends spirit and, if the outing was late, slows for one minute.
 * Forty seconds later the fifth stack starts the live glide and does not cut to body.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSpiritSicknessBedAndFifthStackTest,
	"HomeWorld.T0.Sickness.BedTouchWakeAndFifthStack",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSpiritSicknessBedAndFifthStackTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("sickness bed and fifth"));
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

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	Character->SyncFormWithTimeOfDay();
	TestEqual(TEXT("first stack at dawn"), Character->GetSpiritSicknessStacks(), 1);

	Character->TouchSpiritBed();
	TestEqual(TEXT("touch clears stacks"), Character->GetSpiritSicknessStacks(), 0);
	TestEqual(TEXT("touch clears the scarf"), Character->GetSpiritSicknessScarfStep(), 0);
	TestTrue(TEXT("touch stays spirit"), Character->GetIsSpiritForm());
	TestTrue(TEXT("touch restores move scale before the wake"),
		FMath::IsNearlyEqual(Character->GetSpiritSicknessMoveScale(), 1.f));
	Character->TickSpiritSickness(10.f);
	TestEqual(TEXT("paused at the bed, no new stack"), Character->GetSpiritSicknessStacks(), 0);

	Character->WakeFromSpiritAtBed();
	TestFalse(TEXT("the bed ends spirit"), Character->GetIsSpiritForm());
	TestFalse(TEXT("the bed clears the sleep gate"), Character->IsSpiritSleepGateGranted());
	TestTrue(TEXT("a late wake slows movement"),
		FMath::IsNearlyEqual(Character->GetSpiritSicknessMoveScale(), 0.85f));
	Character->TickSpiritSickness(60.f);
	TestTrue(TEXT("the late-wake minute ends"),
		FMath::IsNearlyEqual(Character->GetSpiritSicknessMoveScale(), 1.f));

	AHomeWorldCharacter* StillOut = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("still out"), StillOut))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	StillOut->GrantSpiritSleepGate();
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	StillOut->SyncFormWithTimeOfDay();
	StillOut->TickSpiritSickness(40.f);
	TestEqual(TEXT("fifth stack at forty seconds"), StillOut->GetSpiritSicknessStacks(), 5);
	TestEqual(TEXT("scarf is five steps colder"), StillOut->GetSpiritSicknessScarfStep(), 5);
	TestTrue(TEXT("fifth stack stays spirit until the landing"), StillOut->GetIsSpiritForm());
	TestTrue(TEXT("fifth stack arms the live glide"), StillOut->IsSpiritSicknessBootPending());

	StillOut->NotifySpiritSicknessLanded();
	TestFalse(TEXT("landing is body"), StillOut->GetIsSpiritForm());
	TestFalse(TEXT("landing clears the sleep gate"), StillOut->IsSpiritSleepGateGranted());
	TestEqual(TEXT("landing clears stacks"), StillOut->GetSpiritSicknessStacks(), 0);
	TestFalse(TEXT("landing is not still booting"), StillOut->IsSpiritSicknessBootPending());
	TestTrue(TEXT("the boot is not the late-wake minute"),
		FMath::IsNearlyEqual(StillOut->GetSpiritSicknessMoveScale(), 1.f));

	return true;
}

/** The child says the dawn rule once, and only before the first night out. */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FChildDawnRuleOnceTest,
	"HomeWorld.T0.Sickness.ChildSaysDawnRuleOnce",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FChildDawnRuleOnceTest::RunTest(const FString& Parameters)
{
	HomeWorldFormTest::FScopedWorld Scope(TEXT("child dawn rule"));
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

	TestTrue(TEXT("the child says it once"), Character->TryTellChildDawnRule());
	TestFalse(TEXT("the child does not repeat it"), Character->TryTellChildDawnRule());

	AHomeWorldCharacter* AlreadyOut = HomeWorldFormTest::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("already out"), AlreadyOut))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AlreadyOut->GrantSpiritSleepGate();
	TestFalse(TEXT("no lesson after the first night out"), AlreadyOut->TryTellChildDawnRule());

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
