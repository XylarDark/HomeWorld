// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Components/BoxComponent.h"
#include "Engine/StaticMeshActor.h"
#include "EngineUtils.h"
#include "HomeWorldCampActor.h"
#include "HomeWorldEasePad.h"
#include "HomeWorldHomeLoopSubsystem.h"
#include "HomeWorldSpiritLitVolume.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldTestWorld.h"

namespace
{
	const EHomeWorldStrokeStep PadSteps[] = {
		EHomeWorldStrokeStep::Grace,
		EHomeWorldStrokeStep::Wrath,
		EHomeWorldStrokeStep::Paradox,
		EHomeWorldStrokeStep::ParadoxExtraPoint
	};

	AHomeWorldCharacter* MakeSpirit(FAutomationTestBase* Test, HomeWorldTestWorld::FScopedWorld& Scope)
	{
		Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
		if (!Test->TestNotNull(TEXT("character"), Character))
		{
			return nullptr;
		}
		Character->SetActorLocation(FVector::ZeroVector);
		Character->GrantSpiritSleepGate();
		Character->SyncFormWithTimeOfDay();
		if (!Test->TestTrue(TEXT("the player is spirit"), Character->GetIsSpiritForm()))
		{
			return nullptr;
		}
		return Character;
	}

	AHomeWorldCampActor* SpawnGuard(UWorld* World, const FVector& At)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AHomeWorldCampActor* Guard = World->SpawnActor<AHomeWorldCampActor>(At, FRotator::ZeroRotator, Params);
		if (!Guard)
		{
			return nullptr;
		}
		Guard->CampRole = EHomeWorldCampRole::Guard;
		Guard->Tags.Remove(FName(TEXT("NODE_SLEEPER")));
		Guard->RefreshCampIdentity();
		Guard->SetActorLocation(At);
		return Guard;
	}

	AHomeWorldEasePad* SpawnPad(UWorld* World, const FVector& At, int32 Ordinal)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AHomeWorldEasePad* Pad = World->SpawnActor<AHomeWorldEasePad>(At, FRotator::ZeroRotator, Params);
		if (!Pad)
		{
			return nullptr;
		}
		Pad->Tags.Add(FName(TEXT("NODE_OPENING_EASE")));
		Pad->BindGuard(Ordinal);
		return Pad;
	}

	bool GuardAsleep(AHomeWorldCharacter* Character, int32 Ordinal)
	{
		UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>();
		bool bEased = false;
		bool bAsleep = false;
		return Stealth
			&& Stealth->GetCampActorState(EHomeWorldCampRole::Guard, Ordinal, bEased, bAsleep)
			&& bAsleep;
	}

	AActor* FindTagged(UWorld* World, const TCHAR* Tag)
	{
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (It->ActorHasTag(FName(Tag)))
			{
				return *It;
			}
		}
		return nullptr;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningGuardPadTest,
	"HomeWorld.Opening.GuardPad",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningGuardPadTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening guard pad"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = MakeSpirit(this, Scope);
	if (!Character)
	{
		return false;
	}
	for (int32 Index = 0; Index < 3; ++Index)
	{
		if (!TestNotNull(TEXT("guard"), SpawnGuard(Scope.World, FVector(400.f + Index * 160.f, 0.f, 0.f))))
		{
			return false;
		}
	}
	AHomeWorldEasePad* Pads[3];
	for (int32 Index = 0; Index < 3; ++Index)
	{
		Pads[Index] = SpawnPad(Scope.World, FVector(400.f + Index * 160.f, 80.f, 0.f), Index);
		if (!TestNotNull(TEXT("pad"), Pads[Index]))
		{
			return false;
		}
	}

	for (int32 Step = 0; Step < 3; ++Step)
	{
		TestTrue(TEXT("a ladder step matches"), Character->TryCommitOpeningGuardPad(Pads[0], PadSteps[Step]));
	}
	TestFalse(TEXT("three steps leave the guard awake"), GuardAsleep(Character, 0));
	TestTrue(TEXT("the fourth step matches"), Character->TryCommitOpeningGuardPad(Pads[0], PadSteps[3]));
	TestTrue(TEXT("a finished ladder sleeps that guard"), GuardAsleep(Character, 0));
	TestFalse(TEXT("the other guards stay awake"), GuardAsleep(Character, 1));

	TestFalse(TEXT("a wrong step does not match"), Character->TryCommitOpeningGuardPad(Pads[1], EHomeWorldStrokeStep::Paradox));
	TestEqual(TEXT("a wrong step does not advance the ladder"), Pads[1]->GetCompletedSteps(), 0);
	TestFalse(TEXT("a wrong step does not sleep the guard"), GuardAsleep(Character, 1));

	TestTrue(TEXT("a wait calls the glide home"), Character->TryWaitOpeningGuardPad(Pads[1]));
	TestEqual(TEXT("a wait does not advance the ladder"), Pads[1]->GetCompletedSteps(), 0);
	TestFalse(TEXT("a wait does not sleep the guard"), GuardAsleep(Character, 1));

	AHomeWorldEasePad* Unbound = SpawnPad(Scope.World, FVector(900.f, 0.f, 0.f), INDEX_NONE);
	if (!TestNotNull(TEXT("unbound pad"), Unbound))
	{
		return false;
	}
	Unbound->BindGuard(INDEX_NONE);
	for (const EHomeWorldStrokeStep Step : PadSteps)
	{
		Character->TryCommitOpeningGuardPad(Unbound, Step);
	}
	TestTrue(TEXT("an unbound ladder can finish"), Unbound->IsLadderComplete());
	TestFalse(TEXT("an unbound ladder sleeps nobody"), Unbound->HasSleptItsGuard());
	UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	if (!TestNotNull(TEXT("stealth"), Stealth))
	{
		return false;
	}
	TestEqual(TEXT("one guard is asleep"), Stealth->GetCalmedActorCount(), 1);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningGuardReachTest,
	"HomeWorld.Opening.GuardReach",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningGuardReachTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening guard reach"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	const FVector GuardAt(400.f, 0.f, 0.f);
	AHomeWorldCampActor* Guard = SpawnGuard(Scope.World, GuardAt);
	AHomeWorldCharacter* Body = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldCharacter* Spirit = MakeSpirit(this, Scope);
	if (!TestNotNull(TEXT("guard"), Guard) || !TestNotNull(TEXT("body"), Body) || !Spirit)
	{
		return false;
	}
	TestFalse(TEXT("a body without the bed stays body"), Body->GetIsSpiritForm());

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldSpiritLitVolume* Light = Scope.World->SpawnActor<AHomeWorldSpiritLitVolume>(GuardAt, FRotator::ZeroRotator, Params);
	UBoxComponent* Box = Light ? Light->FindComponentByClass<UBoxComponent>() : nullptr;
	if (!TestNotNull(TEXT("sight box"), Box))
	{
		return false;
	}
	TestTrue(TEXT("the sight box extent is 180 cm"), FMath::IsNearlyEqual(Box->GetUnscaledBoxExtent().X, 180.0));

	Body->SetActorLocation(GuardAt + FVector(100.f, 0.f, 0.f));
	TestFalse(TEXT("a body inside the light box is not a reach"), Body->TryReachOpeningGuard(Guard));

	Spirit->SetActorLocation(GuardAt + FVector(200.f, 0.f, 0.f));
	TestTrue(TEXT("spirit outside the light box and inside 280 cm is a reach"), Spirit->TryReachOpeningGuard(Guard));
	Spirit->SetActorLocation(GuardAt + FVector(280.f, 0.f, 0.f));
	TestTrue(TEXT("280 cm is still a reach"), Spirit->TryReachOpeningGuard(Guard));
	Spirit->SetActorLocation(GuardAt + FVector(281.f, 0.f, 0.f));
	TestFalse(TEXT("past 280 cm is not a reach"), Spirit->TryReachOpeningGuard(Guard));

	AHomeWorldEasePad* Pad = SpawnPad(Scope.World, GuardAt + FVector(0.f, 80.f, 0.f), 0);
	if (!TestNotNull(TEXT("pad"), Pad))
	{
		return false;
	}
	for (const EHomeWorldStrokeStep Step : PadSteps)
	{
		Spirit->TryCommitOpeningGuardPad(Pad, Step);
	}
	Spirit->SetActorLocation(GuardAt + FVector(100.f, 0.f, 0.f));
	TestTrue(TEXT("the guard is asleep"), GuardAsleep(Spirit, 0));
	TestFalse(TEXT("an asleep guard is not a reach"), Spirit->TryReachOpeningGuard(Guard));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningShrineStopTest,
	"HomeWorld.Opening.ShrineStop",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningShrineStopTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening shrine stop"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = MakeSpirit(this, Scope);
	if (!Character)
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	const FVector PartnerAt(2000.f, 0.f, 0.f);
	AStaticMeshActor* Partner = Scope.World->SpawnActor<AStaticMeshActor>(PartnerAt, FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("kettle partner"), Partner))
	{
		return false;
	}
	Partner->Tags.Add(FName(TEXT("NPC_PARTNER")));
	Partner->SetActorLocation(PartnerAt);

	for (int32 Index = 0; Index < 3; ++Index)
	{
		if (!TestNotNull(TEXT("guard"), SpawnGuard(Scope.World, FVector(400.f + Index * 160.f, 0.f, 0.f)))
			|| !TestNotNull(TEXT("pad"), SpawnPad(Scope.World, FVector(400.f + Index * 160.f, 80.f, 0.f), Index)))
		{
			return false;
		}
	}

	Character->RunOpeningShrineStop();
	TestFalse(TEXT("the stop does not press the shrine"), Character->IsPartnerWalkingHome());
	TestNotNull(TEXT("the captive is spawned for this run"), FindTagged(Scope.World, TEXT("NODE_CAPTIVE")));
	AActor* Shrine = FindTagged(Scope.World, TEXT("NODE_OPENING_SHRINE"));
	if (!TestNotNull(TEXT("the shrine is spawned for this run"), Shrine))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	if (!TestNotNull(TEXT("stealth"), Stealth))
	{
		return false;
	}
	TestEqual(TEXT("the three ladders sleep the three guards"), Stealth->GetCalmedActorCount(), 3);

	Character->SetActorLocation(Shrine->GetActorLocation() + FVector(100.f, 0.f, 0.f));
	TestTrue(TEXT("one E frees the captive and walks the partner"), Character->TryOpeningShrineInFront());
	TestTrue(TEXT("the partner is walking home"), Character->IsPartnerWalkingHome());
	TestTrue(TEXT("the kettle partner stays put"), FMath::IsNearlyZero(FVector::Dist(Partner->GetActorLocation(), PartnerAt)));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningShrineMissingTest,
	"HomeWorld.Opening.ShrineMissing",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningShrineMissingTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening shrine missing guard"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = MakeSpirit(this, Scope);
	if (!Character)
	{
		return false;
	}
	for (int32 Index = 0; Index < 2; ++Index)
	{
		if (!TestNotNull(TEXT("guard"), SpawnGuard(Scope.World, FVector(400.f + Index * 160.f, 0.f, 0.f))))
		{
			return false;
		}
	}
	for (int32 Index = 0; Index < 3; ++Index)
	{
		if (!TestNotNull(TEXT("pad"), SpawnPad(Scope.World, FVector(400.f + Index * 160.f, 80.f, 0.f), Index)))
		{
			return false;
		}
	}
	Character->RunOpeningShrineStop();
	AActor* Shrine = FindTagged(Scope.World, TEXT("NODE_OPENING_SHRINE"));
	if (!TestNotNull(TEXT("shrine"), Shrine))
	{
		return false;
	}
	Character->SetActorLocation(Shrine->GetActorLocation() + FVector(100.f, 0.f, 0.f));
	TestFalse(TEXT("a missing guard refuses the shrine"), Character->TryOpeningShrineInFront());
	TestFalse(TEXT("the partner does not walk"), Character->IsPartnerWalkingHome());
	return true;
}

/**
 * Moss is what puts each guard to sleep (UL2 3A). A finished ladder with an empty
 * chest is refused: the guard stays awake and the chest stays at 0. With one moss
 * the same ladder spends it and the guard sleeps.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningGuardPadNeedsMossTest,
	"HomeWorld.Opening.GuardPadNeedsMoss",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningGuardPadNeedsMossTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening guard pad needs moss"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = MakeSpirit(this, Scope);
	UHomeWorldHomeLoopSubsystem* Home = Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>();
	if (!Character || !TestNotNull(TEXT("home"), Home))
	{
		return false;
	}
	TestEqual(TEXT("a new world's kitchen chest starts with 6 moss"), Home->GetChestCount(HomeWorldKitchen::Moss), 6);
	while (Home->TrySpendChestItem(HomeWorldKitchen::Moss, 1))
	{
	}
	TestEqual(TEXT("the chest is empty"), Home->GetChestCount(HomeWorldKitchen::Moss), 0);

	AHomeWorldCampActor* Dry = SpawnGuard(Scope.World, FVector(400.f, 0.f, 0.f));
	AHomeWorldEasePad* DryPad = SpawnPad(Scope.World, FVector(400.f, 80.f, 0.f), 0);
	if (!TestNotNull(TEXT("guard"), Dry) || !TestNotNull(TEXT("pad"), DryPad))
	{
		return false;
	}
	for (int32 Step = 0; Step < 3; ++Step)
	{
		TestTrue(TEXT("a ladder step matches"), Character->TryCommitOpeningGuardPad(DryPad, PadSteps[Step]));
	}
	TestFalse(TEXT("a finished ladder with no moss is refused"), Character->TryCommitOpeningGuardPad(DryPad, PadSteps[3]));
	TestFalse(TEXT("a failed moss spend keeps the guard awake"), GuardAsleep(Character, 0));
	TestEqual(TEXT("a failed moss spend leaves the chest at 0"), Home->GetChestCount(HomeWorldKitchen::Moss), 0);

	TestTrue(TEXT("one moss goes in the chest"), Home->TryAddChestItem(HomeWorldKitchen::Moss, 1));
	AHomeWorldCampActor* Wet = SpawnGuard(Scope.World, FVector(560.f, 0.f, 0.f));
	AHomeWorldEasePad* WetPad = SpawnPad(Scope.World, FVector(560.f, 80.f, 0.f), 1);
	if (!TestNotNull(TEXT("second guard"), Wet) || !TestNotNull(TEXT("second pad"), WetPad))
	{
		return false;
	}
	for (const EHomeWorldStrokeStep Step : PadSteps)
	{
		TestTrue(TEXT("a ladder step matches"), Character->TryCommitOpeningGuardPad(WetPad, Step));
	}
	TestTrue(TEXT("a successful moss spend sleeps the guard"), GuardAsleep(Character, 1));
	TestEqual(TEXT("the spend subtracts one moss"), Home->GetChestCount(HomeWorldKitchen::Moss), 0);
	TestFalse(TEXT("the first guard is still awake"), GuardAsleep(Character, 0));
	return true;
}

#endif
