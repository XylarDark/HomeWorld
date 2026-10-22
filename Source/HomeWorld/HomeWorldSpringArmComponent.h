// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SpringArmComponent.h"
#include "HomeWorldSpringArmComponent.generated.h"

/**
 * Spring arm that refuses a zero-length camera hit.
 * A sweep that starts inside a blocker reports the arm origin. The stock blend
 * then parks the camera on the pawn. A hit further along the arm still shortens.
 */
UCLASS()
class HOMEWORLD_API UHomeWorldSpringArmComponent : public USpringArmComponent
{
	GENERATED_BODY()

protected:
	virtual FVector BlendLocations(
		const FVector& DesiredArmLocation,
		const FVector& TraceHitLocation,
		bool bHitSomething,
		float DeltaTime) override;
};
