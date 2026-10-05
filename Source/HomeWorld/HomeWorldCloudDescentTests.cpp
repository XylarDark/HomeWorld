// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "GameFramework/CharacterMovementComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldCloudWisp.h"
#include "HomeWorldTestWorld.h"
#include "HomeWorldTimeOfDaySubsystem.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentSteeringAndWispTest,
	"HomeWorld.Transit.CloudDescent.UnrestrictedSteeringAndWispCarry",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentSteeringAndWispTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	FActorSpawnParameters MarkerParams;
	MarkerParams.Name = FName(TEXT("GP_GlideStart"));
	MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AActor* Marker = Scope.World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, MarkerParams);
	if (!TestNotNull(TEXT("glider start marker"), Marker))
	{
		return false;
	}

	TestTrue(TEXT("day/body launch starts active descent"), Character->TryStartCloudDescent());
	TestTrue(TEXT("descent is active"), Character->IsCloudDescentActive());
	TestEqual(TEXT("air control is full so steering has no corridor authority limit"),
		Character->GetCharacterMovement()->AirControl, 1.0f);
	TestTrue(TEXT("launch uses falling movement"), Character->GetCharacterMovement()->MovementMode == MOVE_Falling);

	AHomeWorldCloudWisp* Wisp = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	if (!TestNotNull(TEXT("cloud wisp"), Wisp))
	{
		return false;
	}
	TestTrue(TEXT("wisp collected during active descent"), Character->CollectCloudWisp(Wisp));
	TestEqual(TEXT("wisp remains in carried route state"), Character->GetCarriedCloudWisps(), 1);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
