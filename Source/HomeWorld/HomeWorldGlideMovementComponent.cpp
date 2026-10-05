// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGlideMovementComponent.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"

UHomeWorldGlideMovementComponent::UHomeWorldGlideMovementComponent()
{
	// Glide is its own custom mode; the engine has no glide mode to inherit from.
	NavAgentProps.bCanCrouch = false;
}

bool UHomeWorldGlideMovementComponent::IsGliding() const
{
	return MovementMode == MOVE_Custom && CustomMovementMode == CMOVE_HW_Glide;
}

bool UHomeWorldGlideMovementComponent::StartGlide()
{
	if (IsGliding())
	{
		return false;
	}

	SetMovementMode(MOVE_Custom, CMOVE_HW_Glide);

	// Seed velocity along the current facing so the first frame does not read as a stall.
	if (Velocity.IsNearlyZero() && CharacterOwner)
	{
		Velocity = CharacterOwner->GetActorForwardVector() * GlideForwardSpeed;
	}

	UE_LOG(LogTemp, Log, TEXT("CLOUD_DESCENT: glide mode entered; forward=%.0f cm/s sink=%.0f cm/s"),
		GlideForwardSpeed, GlideSinkRate);
	return true;
}

void UHomeWorldGlideMovementComponent::StopGlide()
{
	if (!IsGliding())
	{
		return;
	}

	SetMovementMode(MOVE_Falling);
}

FVector UHomeWorldGlideMovementComponent::ComputeGlideTargetVelocity() const
{
	// Unrestricted steering: the owning actor's yaw picks the heading, nothing clamps it.
	const FVector Heading = CharacterOwner ? CharacterOwner->GetActorForwardVector().GetSafeNormal2D() : FVector::ForwardVector;

	// Trimmed glide: forward drive plus a fixed sink. Altitude is spent, not held,
	// and there is no vertical input authority, so this cannot become free flight.
	return (Heading * GlideForwardSpeed) - (FVector::UpVector * GlideSinkRate);
}

void UHomeWorldGlideMovementComponent::PhysCustom(float DeltaTime, int32 Iterations)
{
	if (!IsGliding() || DeltaTime < MIN_TICK_TIME || !CharacterOwner || !UpdatedComponent)
	{
		return;
	}

	const FVector Target = ComputeGlideTargetVelocity();

	// Converge on the glide target rather than snapping to it, so steering reads as
	// responsive but never teleports.
	// VInterpTo, not VInterpConstantTo: this rate is a time constant (target reached in
	// 1/GlideSteeringResponsiveness seconds). A constant-rate interp would read 8.0 as
	// 8 cm/s and take ~62 s to reach full sink, which stretched a 75 m drop to 43 s.
	Velocity = FMath::VInterpTo(Velocity, Target, DeltaTime, GlideSteeringResponsiveness);

	// Gravity is expressed only through GlideSinkRate; do not accumulate it separately
	// or the two would compound into an accelerating dive.
	FHitResult Hit;
	MoveUpdatedComponent(Velocity, UpdatedComponent->GetComponentQuat(), true, &Hit);

	if (Hit.bBlockingHit)
	{
		HandleImpact(Hit, DeltaTime, Velocity);
		if (Hit.GetComponent() && CharacterOwner->GetCapsuleComponent() &&
			Hit.GetComponent()->GetCollisionObjectType() == ECC_Pawn)
		{
			// Pawn-vs-pawn: push out instead of stopping dead.
			SlideAlongSurface(Velocity, 1.0f - Hit.Time, Hit.Normal, Hit, true);
		}
		else if (IsWalkable(Hit))
		{
			// Touched down. Hand off to the engine so walking resumes and
			// ACharacter::Landed fires exactly as it does for a normal fall.
			ProcessLanded(Hit, DeltaTime, Iterations);
			return;
		}
		else
		{
			// Non-walkable surface: slide along it and keep gliding.
			SlideAlongSurface(Velocity, 1.0f - Hit.Time, Hit.Normal, Hit, true);
		}
	}
}