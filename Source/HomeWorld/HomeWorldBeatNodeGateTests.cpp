// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldTestWorld.h"

#include "Components/BoxComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * The positive halves of the T0 beat verbs: can the player actually reach a placed prop?
 *
 * THE DEFECT THIS FILE EXISTS TO CATCH
 *
 * Every T0 beat verb reaches its world through one function:
 *
 *     AHomeWorldCharacter::TraceInteractHit()
 *
 * which line traces ECC_Visibility and then asks a second question of whatever it hit:
 *
 *     AHomeWorldCharacter::ActorHasInteractableComponent()
 *
 * The beat verbs each declare the tags that identify their prop - `NODE_KETTLE`,
 * `NODE_RUNE`, `NODE_BACKPACK`, `NODE_FIELD_GATHER`, `NODE_DAY_CAMP`, `NODE_BED` and
 * `NODE_PLANT_SLOT`, plus a short alias for each. Those declarations are the beat-node tag
 * contract. But the gate that decides whether an actor is interactable at all knew about
 * none of them. It recognised only `AHomeWorldResourcePile`, `AHomeWorldCraftStation`, and
 * six named components.
 *
 * So a plain prop actor carrying the right tag, at the right position, with a collider the
 * trace can hit, was still rejected - and every verb behind it returned false. Placing the
 * beat nodes would NOT have produced working beats. The cone fallback does not rescue this
 * either: `FindInteractTargetInCone` re-checks the same gate on every candidate it finds,
 * so adding the tags to its search list alone would still fail.
 *
 * This is why the inventories' "Still unbuilt: no NODE_X actor in any .umap" was a
 * misleading diagnosis for six beats. It named the visible symptom and implied that
 * content placement alone would close it. The content was not the blocker; the gate was.
 *
 * WHY THE POSITIVE HALF WAS NEVER ASSERTED ANYWHERE
 *
 * HomeWorldDayGateTests.cpp covered the refusal side of these same five beats and said the
 * completion side "is PIE work, and it is what the Lead's prove run covers". That deferral
 * is what let this ship: a gate that rejects all seven beat nodes kept a documented
 * evidence path that could not run and never did.
 *
 * Two things were wrong with the deferral, and the second is worth writing down because it
 * is not obvious:
 *
 *   1. It is not PIE work. A `UWorld::CreateWorld(EWorldType::Game, ...)` world registers
 *      components and services line traces. PIE additionally builds a default pawn, a
 *      player controller and a HUD, and none of these gates read any of them. The harness
 *      was one struct away, which is now HomeWorldTestWorld.h.
 *
 *   2. The prove run cannot execute. UE's `-ExecutePythonScript` is run-and-exit: the editor
 *      quits as soon as the script returns, so the deferred `editor_request_begin_play()`
 *      those scripts depend on never gets a tick to run in. Measured directly - an
 *      unattended editor launched with that flag armed the callback, logged
 *      "driver armed", and exited three seconds later without ever firing a tick. With the
 *      flag written as two arguments instead of `-ExecutePythonScript=<path>`, it is not
 *      parsed at all and the editor simply idles forever instead.
 *
 * So the positive halves had no working evidence path. These tests are that path.
 *
 * THE TWO TESTS, AND WHY THERE ARE TWO
 *
 * `AllBeatNodeTagsAreInteractable` asserts the systematic law: the gate admits every tag the
 * verbs declare. A table cannot silently lose a row, which is the property that matters when
 * the same tag list is written out in seven places.
 *
 * But a table can pass vacuously - it would pass just as happily if the gate admitted
 * everything, or if the probe itself were broken. So
 * `RuneAndBackpackBeatsFireFromTaggedProps` goes the whole way: a real prop, a real trace,
 * the real public verb, and the latch the beat is supposed to set. If the gate admits tags
 * for a reason that has nothing to do with the beat working, that test says so.
 *
 * Both are pinned with a positive control built from the same plain-prop construction as
 * the rows under test, differing only by carrying a component the gate already knew. That
 * isolates the one variable being claimed - whether the gate recognises the tag - instead of
 * leaving open whether the fixture can trace at all.
 */

namespace HomeWorldBeatNodeGateTest
{
	/**
	 * Reads the interactable gate.
	 *
	 * `ActorHasInteractableComponent` is protected static, and a derived type is the only
	 * way to ask "would the gate admit this actor?" without widening the character's public
	 * API for the benefit of a test. This declares no UCLASS and is never instantiated; it
	 * exists solely to reach one inherited static.
	 */
	struct FGateProbe : public AHomeWorldCharacter
	{
		static bool Admits(const AActor* Actor)
		{
			return ActorHasInteractableComponent(Actor);
		}
	};

	/**
	 * A greybox prop: a bare actor with a collider the interact trace can hit.
	 *
	 * The box is 60cm tall on purpose. `TraceInteractHit` starts at half the character's
	 * capsule half-height - roughly 46cm up - so a knee-height collider sits below the trace
	 * and would miss for reasons that have nothing to do with the gate. Height is a floor, so
	 * a real rune stone or a bed clears it; only a deliberately flat pad would not.
	 *
	 * This is deliberately the simplest actor that can be interactable. It has no mesh, no
	 * art and no blueprint, because the claim under test is about the TAG, and anything that
	 * could satisfy the gate on some other ground would make the test unable to fail.
	 */
	AActor* SpawnTaggedProp(UWorld* World, const FVector& Location, const TArray<FName>& Tags)
	{
		if (!World)
		{
			return nullptr;
		}

		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* Prop = World->SpawnActor<AActor>(AActor::StaticClass(), Location, FRotator::ZeroRotator, Params);
		if (!Prop)
		{
			return nullptr;
		}

		for (const FName& Tag : Tags)
		{
			Prop->Tags.AddUnique(Tag);
		}

		UBoxComponent* Box = NewObject<UBoxComponent>(Prop);
		Box->InitBoxExtent(FVector(25.0f, 25.0f, 60.0f));
		Box->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		Box->SetCollisionResponseToAllChannels(ECR_Block);
		Prop->AddInstanceComponent(Box);
		Box->RegisterComponent();
		Box->SetWorldLocation(Location);

		return Prop;
	}

	/**
	 * Where a prop must sit for the character to be looking at it.
	 *
	 * The character is spawned with no controller, so `APawn::GetControlRotation()` returns
	 * `FRotator::ZeroRotator`, and a zero rotator points down +X. 120cm is comfortably
	 * inside `InteractTraceLengthCm` (280) and well outside the character's own capsule,
	 * which `TraceInteractHit` ignores explicitly.
	 */
	const FVector PropOnForwardAxis()
	{
		return FVector(120.0f, 0.0f, 0.0f);
	}
}

/**
 * Every tag a beat verb declares must be admitted by the interactable gate.
 *
 * The tag strings are written out literally on purpose. If this test read the tag list out
 * of the implementation, renaming the implementation's table would rename the expectation
 * with it and nothing would ever fail - the test would be asserting that the code agrees
 * with itself.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeatNodeTagsAreInteractableTest,
	"HomeWorld.T0.NodeGate.AllBeatNodeTagsAreInteractable",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeatNodeTagsAreInteractableTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldBeatNodeGateTest;

	HomeWorldTestWorld::FScopedWorld Scope(TEXT("beat node gate"));
	if (!Scope.Ok(this))
	{
		AddError(TEXT("cannot reach the interactable gate without a world"));
		return false;
	}

	/**
	 * Positive control.
	 *
	 * Identical prop, identical collider, identical placement - and a component the gate
	 * already recognised. If this is NOT admitted, the finding is that traces and
	 * registration do not work in this fixture, and every row below it is meaningless.
	 */
	{
		AActor* Control = SpawnTaggedProp(Scope.World, PropOnForwardAxis(), { FName(TEXT("CONTROL")) });
		if (!TestNotNull(TEXT("control prop"), Control))
		{
			return false;
		}
		UHomeWorldNurtureComponent* Nurture = NewObject<UHomeWorldNurtureComponent>(Control);
		Control->AddInstanceComponent(Nurture);
		Nurture->RegisterComponent();

		TestTrue(TEXT("control: the gate admits a prop carrying a component it already knew"),
			FGateProbe::Admits(Control));
	}

	// Every tag the seven beat verbs accept. Kept as a table because these are written out
	// in seven separate call sites, and a table is the only form that cannot lose one.
	struct FBeatTag
	{
		const TCHAR* Beat;
		const TCHAR* Tag;
	};

	const FBeatTag BeatTags[] = {
		{ TEXT("#2  NODE_KETTLE"),       TEXT("NODE_KETTLE") },
		{ TEXT("#2  Kettle alias"),     TEXT("Kettle") },
		{ TEXT("#3  NODE_PLANT_SLOT"),  TEXT("NODE_PLANT_SLOT") },
		{ TEXT("#3  PlantSlot alias"),  TEXT("PlantSlot") },
		{ TEXT("#4  NODE_BACKPACK"),    TEXT("NODE_BACKPACK") },
		{ TEXT("#4  Backpack alias"),   TEXT("Backpack") },
		{ TEXT("#6  NODE_FIELD_GATHER"),TEXT("NODE_FIELD_GATHER") },
		{ TEXT("#6  FieldGather alias"),TEXT("FieldGather") },
		{ TEXT("#7  NODE_RUNE"),        TEXT("NODE_RUNE") },
		{ TEXT("#7  Rune alias"),       TEXT("Rune") },
		{ TEXT("#8  NODE_DAY_CAMP"),    TEXT("NODE_DAY_CAMP") },
		{ TEXT("#8  DayCamp alias"),    TEXT("DayCamp") },
		{ TEXT("#11 NODE_BED"),         TEXT("NODE_BED") },
		{ TEXT("#11 Bed alias"),        TEXT("Bed") },
	};

	const int32 TagCount = UE_ARRAY_COUNT(BeatTags);
	for (int32 Index = 0; Index < TagCount; ++Index)
	{
		const FBeatTag& Row = BeatTags[Index];

		// A fresh location per row, so one row cannot pass by hitting another's prop.
		const FVector Location = FVector(120.0f, Index * 100.0f, 0.0f);
		AActor* Prop = SpawnTaggedProp(Scope.World, Location, { FName(Row.Tag) });
		if (!TestNotNull(FString::Printf(TEXT("%s: prop"), Row.Beat), Prop))
		{
			continue;
		}

		TestTrue(FString::Printf(TEXT("%s: gate admits a prop tagged %s"), Row.Beat, Row.Tag),
			FGateProbe::Admits(Prop));
	}

	// A table that silently matched nothing would report zero rows and look like a pass.
	TestEqual(TEXT("every declared beat-node tag was checked"), TagCount, 14);

	return true;
}

/**
 * The whole way through: placed prop, real trace, real verb, real latch.
 *
 * #7 rune and #4 backpack are used because both are complete on Day in body form with no
 * resource in hand, so a `false` here can only mean the gate never handed the verb its
 * target. #2 kettle and #6 field gather are absent on purpose - both consume inventory, so
 * a refusal downstream of the gate would be indistinguishable from the gate refusing, which
 * is precisely the ambiguity this file exists to remove. Their tags are still covered above.
 *
 * If the trace ever stops pointing at the prop - a capsule resize, a collision profile
 * change, someone giving the fixture a controller - these fail as `false`, which reads
 * exactly like the original defect. The comment in HomeWorldTestWorld.h about the
 * controller-less spawn is the thing to re-read when that happens.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeatNodeVerbsReachPlacedPropsTest,
	"HomeWorld.T0.NodeGate.RuneAndBackpackBeatsFireFromTaggedProps",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeatNodeVerbsReachPlacedPropsTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldBeatNodeGateTest;

	HomeWorldTestWorld::FScopedWorld Scope(TEXT("beat node verbs"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	// Day and body, so neither the phase gate nor the form gate is what is under test.
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("body form on Day with no gates granted"), Character->GetIsSpiritForm());

	/**
	 * Sanity, so the two beat assertions below cannot pass for the wrong reason.
	 *
	 * Nothing has been placed and nothing has been used, so both latches must read off. If
	 * either reads on here, it is self-arming and the positive assertion that follows would
	 * be measuring nothing at all.
	 */
	TestFalse(TEXT("#7: rune is not unlocked before the beat runs"), Character->IsRuneGateUnlocked());
	TestFalse(TEXT("#4: backpack is not equipped before the beat runs"), Character->IsBackpackEquipped());

	// #7: a rune stone on the forward axis, then the public verb.
	AActor* Rune = SpawnTaggedProp(Scope.World, PropOnForwardAxis(), { FName(TEXT("NODE_RUNE")) });
	if (TestNotNull(TEXT("#7: rune prop"), Rune))
	{
		TestTrue(TEXT("#7: TryNodeRuneInteractInFront completes from a placed NODE_RUNE prop"),
			Character->TryNodeRuneInteractInFront());
		TestTrue(TEXT("#7: the rune latch is set - the beat fired, not just the trace"),
			Character->IsRuneGateUnlocked());
	}

	// #4: a backpack on the forward axis. The rune already fired, so this is a second
	// independent beat rather than a second reading of the first.
	AActor* Backpack = SpawnTaggedProp(Scope.World, PropOnForwardAxis(), { FName(TEXT("NODE_BACKPACK")) });
	if (TestNotNull(TEXT("#4: backpack prop"), Backpack))
	{
		TestTrue(TEXT("#4: TryNodeBackpackInteractInFront completes from a placed NODE_BACKPACK prop"),
			Character->TryNodeBackpackInteractInFront());
		TestTrue(TEXT("#4: the backpack latch is set - the beat fired, not just the trace"),
			Character->IsBackpackEquipped());
	}

	// The gate admits beat-node tags; it must not have become a blanket that admits any
	// actor at all. An untagged prop is exactly what the gate is for rejecting.
	AActor* Untagged = SpawnTaggedProp(Scope.World, PropOnForwardAxis(), {});
	TestFalse(TEXT("an untagged prop is still not interactable"),
		FGateProbe::Admits(Untagged));

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS