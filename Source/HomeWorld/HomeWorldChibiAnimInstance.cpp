// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldChibiAnimInstance.h"

void UHomeWorldChibiAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);

	// Simple bounce phase: advance with time when moving, else idle at 0.
	if (Speed > 5.0f)
	{
		BouncePhase += DeltaSeconds * 4.0f; // ~4 cycles per second when walking
		if (BouncePhase >= 1.0f)
		{
			BouncePhase -= 1.0f;
		}
	}
	else
	{
		BouncePhase = 0.0f;
	}
	// Vertical bounce: sin wave
	constexpr float TwoPi = 6.28318530718f;
	BounceOffset = BounceScale * FMath::Sin(BouncePhase * TwoPi);
}
