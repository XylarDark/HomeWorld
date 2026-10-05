// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "GameFramework/CharacterMovementComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldCloudWisp.h"
#include "HomeWorldGlideMovementComponent.h"
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

	// The descent is a glider, not a fall. Assert the real movement mode and class
	// rather than AirControl, which was the old free-fall stand-in.
	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}
	TestTrue(TEXT("launch enters the glide custom movement mode"), Glide->IsGliding());
	TestEqual(TEXT("custom movement mode is the glide mode"),
		Glide->CustomMovementMode, static_cast<uint8>(CMOVE_HW_Glide));
	// MOVEMENT_BIBLE: one CMC. The glide subclass must REPLACE the default, not join it.
	int32 MovementComponentCount = 0;
	for (const UActorComponent* Component : Character->GetComponents())
	{
		if (Component && Component->IsA<UCharacterMovementComponent>())
		{
			++MovementComponentCount;
		}
	}
	TestEqual(TEXT("still exactly one movement component"), MovementComponentCount, 1);

	// Developer decision 2026-10-05: uniform 5 m/s forward and sink across the descent.
	TestEqual(TEXT("glide forward speed is 5 m/s"), Glide->GlideForwardSpeed, 500.0f);
	TestEqual(TEXT("glide sink rate is 5 m/s"), Glide->GlideSinkRate, 500.0f);

	// A glide cannot hold altitude: no input grants vertical authority.
	const FVector Target = Glide->ComputeGlideTargetVelocity();
	TestEqual(TEXT("target descends at the sink rate"), Target.Z, -static_cast<double>(Glide->GlideSinkRate), 0.01);
	const double HorizontalMagnitude = FMath::Sqrt(Target.X * Target.X + Target.Y * Target.Y);
	TestTrue(TEXT("target keeps forward drive"), HorizontalMagnitude > 1.0);

	AHomeWorldCloudWisp* Wisp = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	if (!TestNotNull(TEXT("cloud wisp"), Wisp))
	{
		return false;
	}
	TestTrue(TEXT("wisp collected during active descent"), Character->CollectCloudWisp(Wisp));
	TestEqual(TEXT("wisp remains in carried route state"), Character->GetCarriedCloudWisps(), 1);

	return true;
}

/**
 * The glide-to-walk handoff.
 *
 * The test world created by FScopedWorld is not physics-ticked, so this does NOT
 * simulate a drop. It covers the deterministic contract instead: the descent
 * hands control back through the engine's landing path, and the character clears
 * its descent state. Whether the glide actually reaches the ground from 75 m and
 * touches down on a real floor surface is a PIE question, not an automation one.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentLandingHandsBackControlTest,
	"HomeWorld.Transit.CloudDescent.LandingReturnsWalkControl",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentLandingHandsBackControlTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent landing"));
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
	if (!TestNotNull(TEXT("glider start marker"),
		Scope.World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, MarkerParams)))
	{
		return false;
	}

	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}

	if (!TestTrue(TEXT("day/body launch starts active descent"), Character->TryStartCloudDescent()))
	{
		return false;
	}
	TestTrue(TEXT("descent is gliding before landing"), Character->IsCloudDescentActive());
	TestTrue(TEXT("glide mode is active before landing"), Glide->IsGliding());

	// A glide must not leave horizontal authority behind in the CMC's falling state:
	// StopGlide is the escape hatch and must return to normal falling physics.
	Glide->StopGlide();
	TestFalse(TEXT("stopping the glide leaves glide mode"), Glide->IsGliding());
	TestEqual(TEXT("stopping the glide returns normal falling physics"),
		Glide->MovementMode, MOVE_Falling);

	// Landed() is the engine-side landing callback the glide CMC reaches via
	// ProcessLanded. Assert the character releases its descent state.
	Character->Landed(FHitResult());
	TestFalse(TEXT("landing clears the descent flag"), Character->IsCloudDescentActive());
	TestFalse(TEXT("landing leaves no active glide mode"), Glide->IsGliding());

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
