// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/StaticMeshActor.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTestWorld.h"

/**
 * The 2026-10-21 heal lock, confirmed at the desk as 2A.
 * 3.0 seconds is 20. 3.1 and 4.0 are 30. 4.1 is 40.
 * The collect heart may run past 3 seconds. The hot-spring deposit uses that length.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningHealTimeTest,
	"HomeWorld.Opening.HealTime",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningHealTimeTest::RunTest(const FString& Parameters)
{
	TestEqual(TEXT("3.0 seconds is 20"), AHomeWorldCharacter::OpeningHealSecondsForHeart(3.0f), 20.f);
	TestEqual(TEXT("under 3 seconds is 20"), AHomeWorldCharacter::OpeningHealSecondsForHeart(1.0f), 20.f);
	TestEqual(TEXT("3.1 seconds is 30"), AHomeWorldCharacter::OpeningHealSecondsForHeart(3.1f), 30.f);
	TestEqual(TEXT("4.0 seconds is 30"), AHomeWorldCharacter::OpeningHealSecondsForHeart(4.0f), 30.f);
	TestEqual(TEXT("4.1 seconds is 40"), AHomeWorldCharacter::OpeningHealSecondsForHeart(4.1f), 40.f);

	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening heal time"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SetActorLocation(FVector::ZeroVector);
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	Params.Name = FName(TEXT("SM_Size_Bed"));
	AActor* Bed = Scope.World->SpawnActor<AStaticMeshActor>(FVector(150.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	Params.Name = FName(TEXT("Water_HotSpring"));
	AActor* Spring = Scope.World->SpawnActor<AStaticMeshActor>(FVector(0.f, 300.f, 0.f), FRotator::ZeroRotator, Params);
	Params.Name = FName(TEXT("OpeningWispHeart"));
	AActor* Wisp = Scope.World->SpawnActor<AStaticMeshActor>(FVector(80.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("character"), Character) || !TestNotNull(TEXT("bed"), Bed)
		|| !TestNotNull(TEXT("spring"), Spring) || !TestNotNull(TEXT("wisp"), Wisp))
	{
		return false;
	}
#if WITH_EDITOR
	Bed->SetActorLabel(TEXT("SM_Size_Bed"));
	Spring->SetActorLabel(TEXT("Water_HotSpring"));
#endif

	if (!TestTrue(TEXT("the collect heart starts"), Character->DebugBeginOpeningWispHeart(Wisp)))
	{
		return false;
	}
	Character->DebugAdvanceOpeningWispHeart(4.1f);
	TestTrue(TEXT("the collect heart is still open after 4.1 seconds"), Character->IsOpeningWispHeartActiveForTest());

	if (!TestTrue(TEXT("sleep starts the night"), Character->TryOpeningBedInFront()))
	{
		return false;
	}
	Character->DebugSeedOpeningWispLoop(2, 2);
	Character->DebugQueueOpeningWispHeart(3.0f);
	Character->DebugQueueOpeningWispHeart(4.1f);
	TestTrue(TEXT("the first deposit starts"), Character->TryOpeningHotSpringHealInFront());
	TestTrue(TEXT("the second deposit starts"), Character->TryOpeningHotSpringHealInFront());
	TestEqual(TEXT("a 3.0 heart heals for 20 seconds"), Character->GetOpeningWispHealTimerForTest(0), 20.f);
	TestEqual(TEXT("a 4.1 heart heals for 40 seconds"), Character->GetOpeningWispHealTimerForTest(1), 40.f);
	return true;
}

#endif
