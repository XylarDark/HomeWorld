// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpringArmComponent.h"

FVector UHomeWorldSpringArmComponent::BlendLocations(
	const FVector& DesiredArmLocation,
	const FVector& TraceHitLocation,
	bool bHitSomething,
	float DeltaTime)
{
	(void)DeltaTime;
	if (!bHitSomething)
	{
		return DesiredArmLocation;
	}

	// SweepSingle's start-penetrating block is stored at the arm origin, so the
	// distance is 0 and the camera sits on the pawn. A positive distance is the
	// sphere stopping at a real surface; that shorten stays.
	const FVector ArmOrigin = GetComponentLocation() + TargetOffset;
	if (FVector::DistSquared(ArmOrigin, TraceHitLocation) <= 1.f)
	{
		return DesiredArmLocation;
	}
	return TraceHitLocation;
}
