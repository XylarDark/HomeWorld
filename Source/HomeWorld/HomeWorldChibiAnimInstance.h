// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldAnimInstance.h"
#include "HomeWorldChibiAnimInstance.generated.h"

/**
 * AnimInstance for chibi Milady characters. Extends UHomeWorldAnimInstance with
 * bounce phase and scale for kawaii/bouncy motion. Drive from Speed or use in
 * Control Rig / additive layer for vertical bounce on walk.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldChibiAnimInstance : public UHomeWorldAnimInstance
{
	GENERATED_BODY()

public:
	/** Phase 0..1 for bounce cycle (e.g. from time or Speed). Use in AnimGraph for vertical offset. */
	UPROPERTY(BlueprintReadOnly, Category = "Chibi")
	float BouncePhase = 0.0f;

	/** Scale of bounce (0 = no bounce). Typical 0.1–0.3 for subtle kawaii. */
	UPROPERTY(BlueprintReadOnly, Category = "Chibi")
	float BounceScale = 0.15f;

	/** Vertical offset to apply (BounceScale * sin(BouncePhase * 2*PI)). Optional: compute in Blueprint. */
	UPROPERTY(BlueprintReadOnly, Category = "Chibi")
	float BounceOffset = 0.0f;

protected:
	virtual void NativeUpdateAnimation(float DeltaSeconds) override;
};
