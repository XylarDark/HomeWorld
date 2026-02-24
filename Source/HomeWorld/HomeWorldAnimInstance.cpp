// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldAnimInstance.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

void UHomeWorldAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
	Super::NativeUpdateAnimation(DeltaSeconds);

	APawn* Pawn = TryGetPawnOwner();
	if (!Pawn)
	{
		return;
	}

	const FVector Velocity = Pawn->GetVelocity();
	Speed = Velocity.Size2D();
	bIsMoving = Speed > 5.0f;

	if (const ACharacter* Character = Cast<ACharacter>(Pawn))
	{
		if (const UCharacterMovementComponent* Movement = Character->GetCharacterMovement())
		{
			bIsInAir = Movement->IsFalling();
		}
	}
}
