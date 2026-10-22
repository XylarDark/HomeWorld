// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/TargetPoint.h"
#include "GameFramework/PlayerController.h"
#include "HomeWorldShrinePortalComponent.h"
#include "HomeWorldShrinePortalTrigger.h"
#include "HomeWorldTestWorld.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSpawnControlPitchTest,
	"HomeWorld.Camera.SpawnPitch",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSpawnControlPitchTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("spawn control pitch"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	APlayerController* Controller = Scope.World->SpawnActor<APlayerController>();
	if (!TestNotNull(TEXT("character"), Character) || !TestNotNull(TEXT("controller"), Controller))
	{
		return false;
	}
	Controller->Possess(Character);
	TestEqual(TEXT("spawn pitch is -12"), Controller->GetControlRotation().Pitch, -12.0);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	ATargetPoint* Destination = Scope.World->SpawnActor<ATargetPoint>(
		FVector(800.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	AHomeWorldShrinePortalTrigger* Trigger = Scope.World->SpawnActor<AHomeWorldShrinePortalTrigger>(
		FVector::ZeroVector, FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("destination"), Destination) || !TestNotNull(TEXT("portal"), Trigger)
		|| !TestNotNull(TEXT("portal component"), Trigger->PortalComponent.Get()))
	{
		return false;
	}
#if WITH_EDITOR
	Destination->SetActorLabel(TEXT("ANCHOR_PitchReturn"));
#endif
	Trigger->PortalComponent->DestinationLabel = FName(TEXT("ANCHOR_PitchReturn"));
	Trigger->PortalComponent->bRequireNight = false;
	Character->NotifyLeftHomestead();
	Controller->SetControlRotation(FRotator(89.9f, 0.f, 0.f));

	TestTrue(TEXT("the portal teleports"), Trigger->PortalComponent->TryPortalTransit(Character));
	TestEqual(TEXT("portal pitch is -12"), Controller->GetControlRotation().Pitch, -12.0);
	return true;
}

#endif
