// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGlideMovementComponent.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"
#include "Misc/ScopeExit.h"

// Same-tick re-entry probe. HomeWorld.Transit.CloudDescent.SameFrameLandingNoReentry reads it
// to prove a landing does not recurse back into PhysCustom.
namespace HomeWorldGlideProbe
{
	int32 GCalls = 0;
	int32 GDepth = 0;
	int32 GMaxDepth = 0;
}

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
	++HomeWorldGlideProbe::GCalls;
	++HomeWorldGlideProbe::GDepth;
	HomeWorldGlideProbe::GMaxDepth = FMath::Max(HomeWorldGlideProbe::GMaxDepth, HomeWorldGlideProbe::GDepth);
	ON_SCOPE_EXIT { --HomeWorldGlideProbe::GDepth; };
	// Same-tick re-entry guard. The landing hand-off below runs StartNewPhysics, which
	// must never come back into the glide on the same stack (PIE STACK_OVERFLOW, 2026-10-22).
	if (HomeWorldGlideProbe::GDepth > 1)
	{
		return;
	}

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
	// Velocity is cm/s; one tick moves Velocity * DeltaTime, not a full second of travel.
	const FVector Delta = Velocity * DeltaTime;
	FHitResult Hit;
	MoveUpdatedComponent(Delta, UpdatedComponent->GetComponentQuat(), true, &Hit);

	if (Hit.bBlockingHit)
	{
		HandleImpact(Hit, DeltaTime, Velocity);
		if (Hit.GetComponent() && CharacterOwner->GetCapsuleComponent() &&
			Hit.GetComponent()->GetCollisionObjectType() == ECC_Pawn)
		{
			// Pawn-vs-pawn: push out instead of stopping dead.
			SlideAlongSurface(Delta, 1.0f - Hit.Time, Hit.Normal, Hit, true);
		}
		else if (IsWalkable(Hit))
		{
			// Touched down. Hand off to the engine so walking resumes and
			// ACharacter::Landed fires exactly as it does for a normal fall.
			// ProcessLanded only switches to walking from MOVE_Falling; from the glide
			// mode it restarted PhysCustom with the whole tick, forever. Leave the glide
			// first and hand over only the time this tick has left.
			const float RemainingTime = DeltaTime * (1.0f - Hit.Time);
			SetMovementMode(MOVE_Falling);
			ProcessLanded(Hit, RemainingTime, Iterations);
			return;
		}
		else
		{
			// Non-walkable surface: slide along it and keep gliding.
			SlideAlongSurface(Delta, 1.0f - Hit.Time, Hit.Normal, Hit, true);
		}
	}
}