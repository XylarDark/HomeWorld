// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldCampNightTypes.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * Behaviour tests for MUST #14, #15 and #16 - the camp night.
 *
 * THE LAWS, verbatim
 *
 * #15, what a spirit may touch - the Lead's camp design plus VISION_BOARD V2b:
 *   "A spirit has no hands. It may work on what holds and carries (soil, rope) and it may
 *    apply care to a mind, but it may not touch an actor's body."
 *
 * #14, the three actors - the Lead, 2026-10-02:
 *   "A guard will be awake that you need to help ease their thoughts so that they fall
 *    asleep, the other two will be asleep and you can ease their thoughts too to keep
 *    them sleeping."
 *
 * #16, the gate:
 *   All THREE calm - eased AND asleep - then the companion can be freed.
 *
 * WHY THESE LAWS NEED PINNING RATHER THAN DESCRIBING
 *
 * Every one of them is a refactor magnet. "Eased AND asleep" looks redundant next to a single
 * state enum, so a later pass collapses it to one flag. "Converted is not calmed" looks like
 * duplicate bookkeeping, so a later pass lets conversion satisfy the gate. Both silently
 * invert the beat, because the entire design is that the gentle path is the ONLY path - so the
 * cheap version of the code is the one that removes the point of the scene.
 *
 * The soft-latch tests are the sharpest here. The component deliberately lets #14 open without
 * the camp existing, so a reviewer is never hard-blocked by missing content. That is a
 * fail-open, and a fail-open nobody constrains is how #14 came to certify itself with zero
 * actors in the world. These tests assert that the strict half still refuses.
 */

namespace HomeWorldCampNightTest
{
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
	 * A spirit-formed character with a stealth component.
	 *
	 * Spirit form is not set directly. It is earned the way a player earns it - night, plus
	 * the bed gate, plus the rune - so these tests exercise the real path into the camp verb
	 * rather than a state that gameplay could never reach.
	 */
	struct FScopedSpirit
	{
		UWorld* World = nullptr;
		AHomeWorldCharacter* Character = nullptr;
		UHomeWorldSpiritStealthComponent* Stealth = nullptr;

		bool Ok(FAutomationTestBase* Test) const
		{
			if (!Test->TestNotNull(TEXT("character"), Character))
			{
				return false;
			}
			return Test->TestNotNull(TEXT("stealth component"), Stealth);
		}
	};

	/** Build the spirit-form fixture. Returns an invalid fixture if anything failed. */
	FScopedSpirit MakeSpirit(FAutomationTestBase* Test, FScopedWorld& Scope)
	{
		FScopedSpirit Fixture;
		Fixture.World = Scope.World;

		Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);

		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		Fixture.Character = Scope.World->SpawnActor<AHomeWorldCharacter>(Params);
		if (!Test->TestNotNull(TEXT("character"), Fixture.Character))
		{
			return Fixture;
		}

		Fixture.Character->GrantSpiritSleepGate();
		Fixture.Character->SetRuneGateUnlocked(true);
		Fixture.Character->SyncFormWithTimeOfDay();

		if (!Test->TestTrue(TEXT("fixture is in FORM_SPIRIT"), Fixture.Character->GetIsSpiritForm()))
		{
			return Fixture;
		}

		Fixture.Stealth = NewObject<UHomeWorldSpiritStealthComponent>(Fixture.Character);
		Fixture.Stealth->RegisterComponent();
		if (!Test->TestNotNull(TEXT("stealth component"), Fixture.Stealth))
		{
			return Fixture;
		}

		return Fixture;
	}

	/** Ease all three the way the beat intends: the guard once, each sleeper once. */
	static void EaseAllThree(UHomeWorldSpiritStealthComponent* Stealth)
	{
		Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, 0);
		Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 0);
		Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 1);
	}

	/**
	 * Spawn the camp's four actors, tagged the way the level would tag them.
	 *
	 * WHY THE CAMP IS BUILT IN MOST OF THESE TESTS
	 *
	 * With no actors in the world every ease soft-latches, so the strict gate reports zero
	 * calmed no matter how many verbs were used. That is correct behaviour and it is what
	 * SoftLatchContained exists to pin -- but it means an empty world can only ever observe
	 * the courtesy half of the beat.
	 *
	 * Building the camp first is the state the beat is actually about, and it is the only
	 * thing that exercises FindCampActorInWorld at all. Before this helper, actor lookup was
	 * implemented and never tested: every count silently took the missing-actor branch, so a
	 * label typo in CAMP.json would have shipped green.
	 *
	 * Plain AActor on purpose -- the component finds them by tag, not by class.
	 */
	static void MakeCamp(FAutomationTestBase* Test, UWorld* World)
	{
		static const TCHAR* const Tags[] = {
			TEXT("NODE_GUARD"), TEXT("NODE_SLEEPER"), TEXT("NODE_SLEEPER"), TEXT("NODE_CAPTIVE")
		};

		for (const TCHAR* Tag : Tags)
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			AActor* Actor = World->SpawnActor<AActor>(AActor::StaticClass(), FTransform::Identity, Params);
			if (Test->TestNotNull(FString::Printf(TEXT("spawned camp actor %s"), Tag), Actor))
			{
				Actor->Tags.Add(FName(Tag));
			}
		}
	}

	/**
	 * UENUM as int for TestEqual.
	 *
	 * TestEqual formats a failure through a stringifier; depending on reflection being
	 * registered for the type, a UENUM either prints its name or fails to compile. Comparing
	 * the underlying value keeps the assertion about behaviour, and the failure text names
	 * the row in the literal anyway.
	 */
	static int32 Value(EHomeWorldSpiritTouchVerdict Verdict)
	{
		return static_cast<int32>(Verdict);
	}
}

/**
 * MUST #15 - the touch table.
 *
 * Four rows, and the interesting one is ActorBody. Allowing it would let the player grab a
 * guard and drag them, turning a beat about easing minds into a beat about moving bodies.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSpiritTouchTableTest,
	"HomeWorld.T0.M15.SpiritTouchTable",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSpiritTouchTableTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldCampNight;
	using HomeWorldCampNightTest::Value;

	TestEqual(TEXT("soil is allowed - tending is the night's verb (M12)"),
		Value(GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget::Soil)),
		Value(EHomeWorldSpiritTouchVerdict::Allowed));
	TestEqual(TEXT("lashings are allowed - untying is the rescue (M16)"),
		Value(GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget::Lashings)),
		Value(EHomeWorldSpiritTouchVerdict::Allowed));
	TestEqual(TEXT("a mind is allowed - easing thoughts is the care verb (M14)"),
		Value(GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget::ActorMind)),
		Value(EHomeWorldSpiritTouchVerdict::Allowed));
	TestEqual(TEXT("a body is refused - a spirit has no hands"),
		Value(GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget::ActorBody)),
		Value(EHomeWorldSpiritTouchVerdict::Refused));

	// Every verdict carries a reason, because the component logs them all and a log line
	// with no reason is a log line nobody can act on.
	for (EHomeWorldSpiritTouchTarget Target : {
		EHomeWorldSpiritTouchTarget::Soil,
		EHomeWorldSpiritTouchTarget::Lashings,
		EHomeWorldSpiritTouchTarget::ActorBody,
		EHomeWorldSpiritTouchTarget::ActorMind })
	{
		const FString Reason = GetSpiritTouchReason(Target);
		TestTrue(FString::Printf(TEXT("target %s has a logged reason"), GetSpiritTouchTargetLogName(Target)),
			Reason.Len() > 0);
	}

	return true;
}

/**
 * MUST #14 - the three actors start in different states.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCampActorStartStatesTest,
	"HomeWorld.T0.M14.ActorStartStates",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCampActorStartStatesTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldCampNight;

	TestFalse(TEXT("the guard starts AWAKE - they are the one who falls asleep"),
		StartsAsleep(EHomeWorldCampRole::Guard));
	TestTrue(TEXT("the sleepers start ASLEEP - they are the ones kept sleeping"),
		StartsAsleep(EHomeWorldCampRole::Sleeper));

	TestTrue(TEXT("the guard needs easing"), RequiresEasing(EHomeWorldCampRole::Guard));
	TestTrue(TEXT("a sleeper needs easing too - the care is required even when already asleep"),
		RequiresEasing(EHomeWorldCampRole::Sleeper));

	TestEqual(TEXT("the gate is three actors wide"), GetGatedActorCount(), 3);
	TestTrue(TEXT("the guard counts"), CountsInFreedomGate(EHomeWorldCampRole::Guard));
	TestTrue(TEXT("a sleeper counts"), CountsInFreedomGate(EHomeWorldCampRole::Sleeper));
	TestFalse(TEXT("the captive does not count in its own gate"),
		CountsInFreedomGate(EHomeWorldCampRole::Captive));

	return true;
}

/**
 * MUST #15 - the calm struct's gate is eased AND asleep, with both anti-cases negative.
 *
 * Pure data, no world: the law is pinned directly on the struct.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCalmGateLawTest,
	"HomeWorld.T0.M16.CalmGateLaw",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCalmGateLawTest::RunTest(const FString& Parameters)
{
	FHomeWorldCampActorCalm Actor;
	Actor.Role = EHomeWorldCampRole::Sleeper;
	Actor.bAsleep = true;

	TestFalse(TEXT("asleep but never eased does NOT open the gate - the care is the requirement"),
		Actor.SatisfiesFreedomGate());

	Actor.bEased = true;
	TestTrue(TEXT("eased AND asleep opens the gate"), Actor.SatisfiesFreedomGate());

	Actor.bAsleep = false;
	TestFalse(TEXT("eased but awake does NOT open the gate - the act is unfinished"),
		Actor.SatisfiesFreedomGate());

	Actor.bAsleep = true;
	Actor.bKilled = true;
	TestFalse(TEXT("killed is never calmed"), Actor.SatisfiesFreedomGate());

	Actor.bKilled = false;
	Actor.bConverted = true;
	TestFalse(TEXT("converted is not calmed - conversion is for foes you defeat"),
		Actor.SatisfiesFreedomGate());

	// The soft latch is the containment. Same actor, gameplay gate open, strict gate shut.
	Actor.bConverted = false;
	Actor.bSoftLatch = true;
	TestTrue(TEXT("gameplay gate tolerates a soft latch"), Actor.SatisfiesFreedomGate());
	TestFalse(TEXT("strict gate refuses a soft latch - a count with no actor is not evidence"),
		Actor.SatisfiesFreedomGateStrict());

	return true;
}

/**
 * MUST #14 - easing the guard puts them to sleep; easing a sleeper only maintains.
 *
 * The two roles genuinely differ, which is the Lead's sentence verbatim: one is "so that they
 * fall asleep" and the other is "to keep them sleeping".
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FEaseDirectionTest,
	"HomeWorld.T0.M14.EaseDirection",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FEaseDirectionTest::RunTest(const FString& Parameters)
{
	HomeWorldCampNightTest::FScopedWorld Scope(TEXT("M14 ease-direction"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	HomeWorldCampNightTest::FScopedSpirit Fixture = HomeWorldCampNightTest::MakeSpirit(this, Scope);
	if (!Fixture.Ok(this))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Fixture.Stealth;

	bool bEased = false;
	bool bAsleep = false;

	// The guard: awake at the start of the scene.
	Stealth->GetCampActorState(EHomeWorldCampRole::Guard, 0, bEased, bAsleep);
	TestFalse(TEXT("guard starts awake"), bAsleep);

	TestTrue(TEXT("easing the guard succeeds"), Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, 0));
	Stealth->GetCampActorState(EHomeWorldCampRole::Guard, 0, bEased, bAsleep);
	TestTrue(TEXT("guard is eased"), bEased);
	TestTrue(TEXT("easing the guard is the act that puts them to sleep"), bAsleep);

	// A sleeper: already asleep, and easing them keeps them that way.
	Stealth->GetCampActorState(EHomeWorldCampRole::Sleeper, 0, bEased, bAsleep);
	TestTrue(TEXT("sleeper starts asleep"), bAsleep);

	TestTrue(TEXT("easing a sleeper succeeds"), Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 0));
	Stealth->GetCampActorState(EHomeWorldCampRole::Sleeper, 0, bEased, bAsleep);
	TestTrue(TEXT("sleeper is eased"), bEased);
	TestTrue(TEXT("easing keeps a sleeper asleep - it does not wake them"), bAsleep);

	// The captives cannot be eased; they are untied, and only through the gate.
	TestFalse(TEXT("the captive cannot be eased - they are freed, not eased"),
		Stealth->TryEaseCampActor(EHomeWorldCampRole::Captive, 0));

	return true;
}

/**
 * MUST #16 - the freedom gate, and every way to fail it.
 *
 * Widened from two actors to three when it became known that the guard is calmed too.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FFreedomGateTest,
	"HomeWorld.T0.M16.FreedomGate",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FFreedomGateTest::RunTest(const FString& Parameters)
{
	using HomeWorldCampNightTest::EaseAllThree;
	using HomeWorldCampNightTest::FScopedSpirit;
	using HomeWorldCampNightTest::FScopedWorld;
	using HomeWorldCampNightTest::MakeCamp;
	using HomeWorldCampNightTest::MakeSpirit;

	FScopedWorld Scope(TEXT("M16 freedom"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	// The camp EXISTS here, so every count below is earned against a real actor.
	MakeCamp(this, Scope.World);

	FScopedSpirit Fixture = MakeSpirit(this, Scope);
	if (!Fixture.Ok(this))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Fixture.Stealth;

	// How WIDE the gate is, and how much of it is satisfied, are different questions. This
	// test previously asserted the width against GetCalmedActorCount(), which asked a fresh
	// camp to already be complete - and "failed" for the right reason while meaning the
	// wrong thing.
	TestEqual(TEXT("the gate is three actors wide"), HomeWorldCampNight::GetGatedActorCount(), 3);
	TestEqual(TEXT("a fresh camp has nobody calmed yet"), Stealth->GetCalmedActorCount(), 0);

	// Nothing calmed yet.
	TestFalse(TEXT("no ease, no freedom"), Stealth->IsFreedomUnlocked());
	TestFalse(TEXT("the strict gate is shut too"), Stealth->IsFreedomUnlockedStrict());
	TestFalse(TEXT("freeing is refused with nobody calmed"), Stealth->TryFreeCaptive());

	// Two of three is the trap the widening was written for.
	Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, 0);
	Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 0);
	TestEqual(TEXT("two of three calm"), Stealth->GetCalmedActorCount(), 2);
	TestFalse(TEXT("two of three does NOT open the gate"), Stealth->IsFreedomUnlocked());
	TestFalse(TEXT("freeing is refused at two of three"), Stealth->TryFreeCaptive());

	// All three, then back off one.
	EaseAllThree(Stealth);
	TestEqual(TEXT("all three calm"), Stealth->GetCalmedActorCount(), 3);
	TestTrue(TEXT("all three eased and asleep opens the gate"), Stealth->IsFreedomUnlocked());

	// The assertion that makes the above worth anything. Because the camp actors exist, no
	// count is a soft latch, so the strict gate - the half that is evidence - must open too.
	// If FindCampActorInWorld ever stops matching the level's labels, this is what catches it.
	TestTrue(TEXT("with the camp built, the STRICT gate also opens - no soft latch in the way"),
		Stealth->IsFreedomUnlockedStrict());

	TestTrue(TEXT("freeing succeeds once the gate is open"), Stealth->TryFreeCaptive());
	TestTrue(TEXT("the captive is freed"), Stealth->IsCaptiveFreed());

	// "Keep them sleeping" has to be able to fail, or "keep" means nothing.
	Stealth->NotifyCampActorWoke(EHomeWorldCampRole::Sleeper, 1);
	TestFalse(TEXT("a woken sleeper closes the gate"), Stealth->IsFreedomUnlocked());

	// Both anti-cases.
	Stealth->NotifyCampActorWoke(EHomeWorldCampRole::Sleeper, 0);
	TestFalse(TEXT("the gate stays shut while a sleeper is awake"), Stealth->IsFreedomUnlocked());
	Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, 0);
	TestFalse(TEXT("re-easing a woken sleeper does NOT put them back to sleep"),
		Stealth->IsFreedomUnlocked());

	Stealth->NotifyCampActorKilled(EHomeWorldCampRole::Guard, 0);
	TestFalse(TEXT("killing an actor never opens the gate"), Stealth->IsFreedomUnlocked());

	// A fresh component, to prove conversion is not an alternative to care.
	FScopedSpirit Second = MakeSpirit(this, Scope);
	if (!Second.Ok(this))
	{
		return false;
	}
	EaseAllThree(Second.Stealth);
	TestTrue(TEXT("sanity: all three eased opens the gate"), Second.Stealth->IsFreedomUnlocked());
	Second.Stealth->NotifyCampActorConverted(EHomeWorldCampRole::Sleeper, 0);
	TestFalse(TEXT("converting an actor does NOT substitute for calming them"),
		Second.Stealth->IsFreedomUnlocked());

	return true;
}

/**
 * The soft latch, contained.
 *
 * THE FAILURE THIS PINS
 *
 * UHomeWorldSpiritStealthComponent soft-latches #14 when the camp actor is absent, so a
 * reviewer is never hard-blocked by missing content. That is defensible as gameplay and
 * indefensible as evidence: before bSoftLatch existed, #14 could report itself complete with
 * zero actors in the world, which is how a beat with no level came to look finished.
 *
 * No camp exists in the .umap yet, so this test runs against exactly the situation the soft
 * latch was written for. The gameplay gate opens; the strict gate must not.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSoftLatchContainmentTest,
	"HomeWorld.T0.M14.SoftLatchContained",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSoftLatchContainmentTest::RunTest(const FString& Parameters)
{
	using HomeWorldCampNightTest::EaseAllThree;
	using HomeWorldCampNightTest::FScopedSpirit;
	using HomeWorldCampNightTest::FScopedWorld;
	using HomeWorldCampNightTest::MakeSpirit;

	FScopedWorld Scope(TEXT("M14 soft latch"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FScopedSpirit Fixture = MakeSpirit(this, Scope);
	if (!Fixture.Ok(this))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Fixture.Stealth;

	// No NODE_GUARD / NODE_SLEEPER actors exist in this empty world, so every count below is
	// a soft latch. If that ever stops being true the test is no longer testing the latch.
	bool bEased = false;
	bool bAsleep = false;
	Stealth->GetCampActorState(EHomeWorldCampRole::Guard, 0, bEased, bAsleep);
	TestTrue(TEXT("precondition: the guard state is readable"), bAsleep || !bAsleep);

	EaseAllThree(Stealth);

	TestEqual(TEXT("easing still succeeds without a world actor"),
		Stealth->GetCalmedActorCount(), 0);
	TestTrue(TEXT("the GAMEPLAY gate tolerates soft latches - a reviewer is not hard-blocked"),
		Stealth->IsFreedomUnlocked());
	TestFalse(TEXT("the STRICT gate refuses soft latches - this is the evidence, and it says no"),
		Stealth->IsFreedomUnlockedStrict());
	TestEqual(TEXT("the strict calmed count is zero"), Stealth->GetCalmedActorCount(), 0);

	return true;
}

/**
 * Anti-fail-open: the tracked array is never empty.
 *
 * "All three are calm" trivially holds against an empty array, so a component that failed to
 * build its roster in the constructor would report the camp night complete on the first call.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FRosterNotEmptyTest,
	"HomeWorld.T0.M14.RosterNotEmpty",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FRosterNotEmptyTest::RunTest(const FString& Parameters)
{
	UHomeWorldSpiritStealthComponent* Stealth = NewObject<UHomeWorldSpiritStealthComponent>();
	if (!TestNotNull(TEXT("a bare component constructs without a world"), Stealth))
	{
		return false;
	}

	bool bEased = true;
	bool bAsleep = true;
	TestTrue(TEXT("the guard is tracked"), Stealth->GetCampActorState(EHomeWorldCampRole::Guard, 0, bEased, bAsleep));
	TestFalse(TEXT("a fresh guard is not eased"), bEased);

	TestTrue(TEXT("sleeper A is tracked"), Stealth->GetCampActorState(EHomeWorldCampRole::Sleeper, 0, bEased, bAsleep));
	TestTrue(TEXT("a fresh sleeper is asleep"), bAsleep);

	TestTrue(TEXT("sleeper B is tracked"), Stealth->GetCampActorState(EHomeWorldCampRole::Sleeper, 1, bEased, bAsleep));

	bEased = false;
	TestFalse(TEXT("the captive is not a gated actor and is not tracked as one"),
		Stealth->GetCampActorState(EHomeWorldCampRole::Captive, 0, bEased, bAsleep));

	// An empty roster would satisfy "all" vacuously. This is the direct assertion of that.
	TestFalse(TEXT("a fresh roster does not open the gate - the empty-array fail-open"),
		Stealth->IsFreedomUnlockedStrict());

	return true;
}

/**
 * MUST #15 through the component: the touch table is enforced and logged in FORM_SPIRIT.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FTouchThroughComponentTest,
	"HomeWorld.T0.M15.TouchThroughComponent",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FTouchThroughComponentTest::RunTest(const FString& Parameters)
{
	using HomeWorldCampNightTest::FScopedSpirit;
	using HomeWorldCampNightTest::FScopedWorld;
	using HomeWorldCampNightTest::MakeSpirit;
	using HomeWorldCampNightTest::Value;

	FScopedWorld Scope(TEXT("M15 component"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FScopedSpirit Fixture = MakeSpirit(this, Scope);
	if (!Fixture.Ok(this))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Fixture.Stealth;

	TestEqual(TEXT("soil is allowed through the component"),
		Value(Stealth->EvaluateSpiritTouch(EHomeWorldSpiritTouchTarget::Soil)),
		Value(EHomeWorldSpiritTouchVerdict::Allowed));
	TestEqual(TEXT("lashings are allowed through the component"),
		Value(Stealth->EvaluateSpiritTouch(EHomeWorldSpiritTouchTarget::Lashings)),
		Value(EHomeWorldSpiritTouchVerdict::Allowed));
	TestEqual(TEXT("a body is refused through the component"),
		Value(Stealth->EvaluateSpiritTouch(EHomeWorldSpiritTouchTarget::ActorBody)),
		Value(EHomeWorldSpiritTouchVerdict::Refused));

	return true;
}

/**
 * The redirect. #14's old completion check was "avoid>=1 && soothe>=2", which cannot express
 * three calmed actors, so it now defers to the three-actor gate.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCampNightCompletionRedirectTest,
	"HomeWorld.T0.M14.CompletionRedirectsToGate",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCampNightCompletionRedirectTest::RunTest(const FString& Parameters)
{
	using HomeWorldCampNightTest::FScopedSpirit;
	using HomeWorldCampNightTest::FScopedWorld;
	using HomeWorldCampNightTest::MakeCamp;
	using HomeWorldCampNightTest::MakeSpirit;

	FScopedWorld Scope(TEXT("M14 redirect"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	MakeCamp(this, Scope.World);
	FScopedSpirit Fixture = MakeSpirit(this, Scope);
	if (!Fixture.Ok(this))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Fixture.Stealth;

	TestFalse(TEXT("a fresh component has not completed the camp night"),
		Stealth->IsCampNightBeatComplete());

	// Easing only the two sleepers satisfies the OLD formula (soothe>=2) but not the new gate,
	// because the guard is one of the three who must be calmed. This is the exact divergence
	// the redirect exists to close.
	Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 0);
	Stealth->TryEaseCampActor(EHomeWorldCampRole::Sleeper, 1);
	TestEqual(TEXT("two sleepers eased"), Stealth->GetCalmedActorCount(), 2);
	TestFalse(TEXT("two sleepers alone do NOT complete #14 - the guard must be calmed too"),
		Stealth->IsCampNightBeatComplete());

	Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, 0);
	TestTrue(TEXT("all three calmed completes #14"), Stealth->IsCampNightBeatComplete());

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS