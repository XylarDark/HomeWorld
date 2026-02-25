// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "HomeWorldAnimInstance.generated.h"

/**
 * C++ AnimInstance that exposes locomotion data (Speed, IsInAir) for the AnimBP.
 * Set this as the parent class of ABP_HomeWorldCharacter so the AnimGraph can
 * read Speed/IsInAir directly without any EventGraph wiring.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldAnimInstance : public UAnimInstance
{
	GENERATED_BODY()

public:
	/** Horizontal speed (cm/s) of the owning pawn. Use in AnimGraph for Idle/Locomotion blend. */
	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	float Speed = 0.0f;

	/** True when the character is falling/jumping (not on ground). */
	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	bool bIsInAir = false;

	/** True when the character has any movement input (Speed > small threshold). */
	UPROPERTY(BlueprintReadOnly, Category = "Locomotion")
	bool bIsMoving = false;

protected:
	virtual void NativeUpdateAnimation(float DeltaSeconds) override;
};
