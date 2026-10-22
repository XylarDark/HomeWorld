// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/TargetPoint.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldShrinePortalComponent.h"
#include "HomeWorldShrinePortalTrigger.h"
#include "HomeWorldTestWorld.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSpawnControlPitchTest,
	"HomeWorld.Camera.SpawnPitch",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSpawnControlPitchTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("spawn control pitch"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	// The Player Start is pitched nearly straight up. Restart copies that pitch
	// onto the controller after PossessedBy has already set -12.
	APlayerStart* Start = Scope.World->SpawnActor<APlayerStart>(
		FVector(0.f, 0.f, 100.f), FRotator(89.9f, 25.f, 0.f), Params);
	AHomeWorldGameMode* GameMode = Scope.World->SpawnActor<AHomeWorldGameMode>(
		FVector::ZeroVector, FRotator::ZeroRotator, Params);
	APlayerController* Controller = Scope.World->SpawnActor<APlayerController>(
		FVector::ZeroVector, FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("player start"), Start) || !TestNotNull(TEXT("game mode"), GameMode)
		|| !TestNotNull(TEXT("controller"), Controller))
	{
		return false;
	}

	GameMode->RestartPlayerAtPlayerStart(Controller, Start);
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(Controller->GetPawn());
	if (!TestNotNull(TEXT("spawned character"), Character))
	{
		return false;
	}
	TestEqual(TEXT("spawn pitch is -12"), Controller->GetControlRotation().Pitch, -12.0);
	TestTrue(TEXT("spawn yaw keeps the player start yaw"),
		FMath::IsNearlyEqual(Controller->GetControlRotation().Yaw, 25.f, 0.1f));

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
	if (UCapsuleComponent* Capsule = Character->GetCapsuleComponent())
	{
		Capsule->SetCapsuleHalfHeight(50.f);
	}
	const float HalfHeight = Character->GetCapsuleComponent()
		? Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight()
		: 0.f;
	Controller->SetControlRotation(FRotator(89.9f, 0.f, 0.f));

	TestTrue(TEXT("the portal teleports"), Trigger->PortalComponent->TryPortalTransit(Character));
	TestEqual(TEXT("portal pitch is -12"), Controller->GetControlRotation().Pitch, -12.0);
	TestTrue(TEXT("arrival stands the capsule on the marker"),
		FMath::IsNearlyEqual(Character->GetActorLocation().Z, Destination->GetActorLocation().Z + HalfHeight, 1.f));
	return true;
}

#endif
