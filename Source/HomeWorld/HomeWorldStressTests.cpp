// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "GameFramework/PlayerController.h"
#include "HomeWorldEasePad.h"
#include "HomeWorldHomeLoopSubsystem.h"
#include "HomeWorldMossTuft.h"
#include "HomeWorldStressComponent.h"
#include "HomeWorldTestWorld.h"
#include "HomeWorldVirtueComponent.h"

namespace
{
	UHomeWorldStressComponent* StressOf(AHomeWorldCharacter* Character)
	{
		return Character ? Character->FindComponentByClass<UHomeWorldStressComponent>() : nullptr;
	}

	/** The chest starts with a placeholder seed of moss; these tests count from an empty chest. */
	void DrainMoss(UHomeWorldHomeLoopSubsystem* Home)
	{
		while (Home && Home->TrySpendChestItem(HomeWorldKitchen::Moss, 1))
		{
		}
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressHitTest, "HomeWorld.Stress.Hit",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressHitTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress hit"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldStressComponent* Stress = StressOf(Character);
	if (!TestNotNull(TEXT("stress"), Stress))
	{
		return false;
	}
	TestEqual(TEXT("a player starts at 0"), Stress->GetPoints(), 0);
	Stress->NotifyHit();
	TestEqual(TEXT("a hit adds 10"), Stress->GetPoints(), 10);
	for (int32 Index = 0; Index < 20; ++Index)
	{
		Stress->NotifyHit();
	}
	TestEqual(TEXT("stress caps at 100"), Stress->GetPoints(), 100);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressBonkTest, "HomeWorld.Stress.Bonk",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressBonkTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress bonk"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldStressComponent* Stress = StressOf(Character);
	if (!TestNotNull(TEXT("stress"), Stress))
	{
		return false;
	}
	Stress->NotifyBonk();
	TestEqual(TEXT("a bonk adds 5"), Stress->GetPoints(), 5);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressMissedTendTest, "HomeWorld.Stress.MissedTend",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressMissedTendTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress missed tend"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	APlayerController* Controller = Scope.World ? Scope.World->SpawnActor<APlayerController>() : nullptr;
	UHomeWorldHomeLoopSubsystem* Home = Scope.World ? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("player"), Character) || !TestNotNull(TEXT("controller"), Controller) || !TestNotNull(TEXT("home"), Home))
	{
		return false;
	}
	Controller->Possess(Character);
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Home->Advance(0.f);
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	Home->Advance(0.f);
	TestEqual(TEXT("a day with no home tend adds 20"), Character->GetStressPoints(), 20);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressGraceMealTest, "HomeWorld.Stress.GraceMeal",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressGraceMealTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress grace meal"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldStressComponent* Stress = StressOf(Character);
	UHomeWorldHomeLoopSubsystem* Home = Scope.World ? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("stress"), Stress) || !TestNotNull(TEXT("home"), Home))
	{
		return false;
	}
	Stress->SetPoints(40);
	DrainMoss(Home);
	TestTrue(TEXT("the chest holds one moss"), Home->TryAddChestItem(HomeWorldKitchen::Moss, 1));
	TestTrue(TEXT("the meal is served"), Home->ServeGraceMossMeal(Character));
	TestEqual(TEXT("a Grace-moss meal subtracts 30"), Stress->GetPoints(), 10);
	TestEqual(TEXT("the moss is spent"), Home->GetChestCount(HomeWorldKitchen::Moss), 0);
	TestFalse(TEXT("an empty chest does not serve"), Home->ServeGraceMossMeal(Character));
	TestEqual(TEXT("a missed meal does not change stress"), Stress->GetPoints(), 10);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressBedSleepTest, "HomeWorld.Stress.BedSleep",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressBedSleepTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress bed"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldStressComponent* Stress = StressOf(Character);
	if (!TestNotNull(TEXT("stress"), Stress))
	{
		return false;
	}
	Stress->SetPoints(25);
	FActorSpawnParameters Params;
	Params.Name = TEXT("SM_Size_Bed");
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AActor* Bed = Scope.World->SpawnActor<AActor>(FVector(80.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("bed"), Bed))
	{
		return false;
	}
	TestTrue(TEXT("bed sleep starts"), Character->TryOpeningBedInFront());
	TestEqual(TEXT("bed sleep subtracts 10"), Stress->GetPoints(), 15);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressCapSwapTest, "HomeWorld.Stress.CapSwap",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressCapSwapTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress cap swap"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldStressComponent* Stress = StressOf(Character);
	if (!TestNotNull(TEXT("stress"), Stress) || !TestNotNull(TEXT("player"), Character))
	{
		return false;
	}
	UHomeWorldVirtueComponent* Virtue = NewObject<UHomeWorldVirtueComponent>(Character);
	Virtue->RegisterComponent();
	TestTrue(TEXT("Grace is on the player"), Virtue->TryGivePole(EHomeWorldVirtuePole::Grace));
	Stress->SetPoints(90);
	const int32 Stat = Stress->GetUntouchedStat();
	TestFalse(TEXT("under the cap, Swap does not flip"), Stress->TryCapSwap(Virtue));
	TestTrue(TEXT("Grace remains"), Virtue->HasPole(EHomeWorldVirtuePole::Grace));
	Stress->NotifyHit();
	TestEqual(TEXT("the tenth hit reaches the cap"), Stress->GetPoints(), 100);
	TestTrue(TEXT("Swap at the cap flips Grace to Wrath"), Stress->TryCapSwap(Virtue));
	TestTrue(TEXT("Wrath is the sin"), Virtue->HasPole(EHomeWorldVirtuePole::Wrath));
	TestFalse(TEXT("Grace is gone"), Virtue->HasPole(EHomeWorldVirtuePole::Grace));
	TestEqual(TEXT("stress resets to 50"), Stress->GetPoints(), 50);
	TestTrue(TEXT("the rune shows"), Stress->IsRuneVisible());
	TestTrue(TEXT("the interaction changes"), Stress->GetInteractionName() == FName(TEXT("Wrath")));
	TestEqual(TEXT("Swap does not lower a stat"), Stress->GetUntouchedStat(), Stat);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressMossGatherTest, "HomeWorld.Stress.MossGather",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressMossGatherTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress moss"));
	UHomeWorldHomeLoopSubsystem* Home = Scope.Ok(this) ? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home"), Home))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldMossTuft* Tree = Scope.World->SpawnActor<AHomeWorldMossTuft>(FVector(100.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	AHomeWorldMossTuft* Rock = Scope.World->SpawnActor<AHomeWorldMossTuft>(FVector(200.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	AHomeWorldMossTuft* Wrath = Scope.World->SpawnActor<AHomeWorldMossTuft>(FVector(300.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("tree tuft"), Tree) || !TestNotNull(TEXT("rock tuft"), Rock) || !TestNotNull(TEXT("wrath tuft"), Wrath))
	{
		return false;
	}
	Tree->SetSource(TEXT("tree"));
	Rock->SetSource(TEXT("rock"));
	Wrath->SetSource(TEXT("tree"));
	DrainMoss(Home);
	TestTrue(TEXT("a Grace wisp gathers a tree"), Home->TryGatherGraceMoss(Tree, EHomeWorldVirtuePole::Grace));
	TestTrue(TEXT("a Grace wisp gathers a rock"), Home->TryGatherGraceMoss(Rock, EHomeWorldVirtuePole::Grace));
	TestFalse(TEXT("a gathered tuft is spent"), Home->TryGatherGraceMoss(Tree, EHomeWorldVirtuePole::Grace));
	TestFalse(TEXT("Wrath does not gather"), Home->TryGatherGraceMoss(Wrath, EHomeWorldVirtuePole::Wrath));
	TestEqual(TEXT("the kitchen chest holds two moss"), Home->GetChestCount(HomeWorldKitchen::Moss), 2);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressPadSpendTest, "HomeWorld.Stress.PadSpend",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressPadSpendTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress pad moss"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	UHomeWorldHomeLoopSubsystem* Home = Scope.World ? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("player"), Character) || !TestNotNull(TEXT("home"), Home))
	{
		return false;
	}
	DrainMoss(Home);
	Home->TryAddChestItem(HomeWorldKitchen::Moss, 1);
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(FVector(400.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("pad"), Pad))
	{
		return false;
	}
	const EHomeWorldStrokeStep Steps[] = {
		EHomeWorldStrokeStep::Grace,
		EHomeWorldStrokeStep::Wrath,
		EHomeWorldStrokeStep::Paradox,
		EHomeWorldStrokeStep::ParadoxExtraPoint
	};
	for (const EHomeWorldStrokeStep Step : Steps)
	{
		TestTrue(TEXT("a ladder step matches"), Character->TryCommitOpeningGuardPad(Pad, Step));
	}
	TestEqual(TEXT("a finished ladder spends one moss"), Home->GetChestCount(HomeWorldKitchen::Moss), 0);
	TestFalse(TEXT("an empty chest does not go negative"), Home->TrySpendChestItem(HomeWorldKitchen::Moss, 1));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FStressFastForwardTest, "HomeWorld.Stress.FastForward",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStressFastForwardTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stress fast forward"));
	AHomeWorldCharacter* Character = Scope.Ok(this) ? HomeWorldTestWorld::SpawnCharacter(Scope.World) : nullptr;
	if (!TestNotNull(TEXT("player"), Character))
	{
		return false;
	}
	Character->DebugFastForwardOpening(TEXT("stress"));
	TestEqual(TEXT("the stop is stress 90"), Character->GetStressPoints(), 90);
	TestTrue(TEXT("the snapshot says stress 90"), Character->GetPlaytestStateJson().Contains(TEXT("\"stress\":90")));
	return true;
}

#endif
