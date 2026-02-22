// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "HomeWorldAttributeSet.h"
#include "InputActionValue.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"

AHomeWorldCharacter::AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
	AbilitySystemComponent->SetIsReplicated(true);

	AttributeSet = CreateDefaultSubobject<UHomeWorldAttributeSet>(TEXT("AttributeSet"));

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->bUsePawnControlRotation = true;
	CameraBoom->TargetArmLength = 400.0f;
	CameraBoom->bDoCollisionTest = true;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom);
}

UAbilitySystemComponent* AHomeWorldCharacter::GetAbilitySystemComponent() const
{
	return AbilitySystemComponent;
}

void AHomeWorldCharacter::PossessedBy(AController* NewController)
{
	Super::PossessedBy(NewController);
	if (AbilitySystemComponent)
	{
		AbilitySystemComponent->InitAbilityActorInfo(this, this);
	}
}

void AHomeWorldCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(PlayerInputComponent);
	if (!EnhancedInput || !DefaultMappingContext || !MoveAction || !LookAction)
	{
		return;
	}

	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (ULocalPlayer* LP = PC->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Subsystem = LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
			}
		}
	}

	EnhancedInput->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::Move);
	EnhancedInput->BindAction(LookAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::Look);
}

void AHomeWorldCharacter::Move(const FInputActionValue& Value)
{
	const FVector2D Axis = Value.Get<FVector2D>();
	const FVector Forward = GetActorForwardVector();
	const FVector Right = GetActorRightVector();
	FVector Direction = Forward * Axis.Y + Right * Axis.X;
	Direction.Z = 0.0f;
	if (!Direction.IsNearlyZero())
	{
		Direction.Normalize();
		AddMovementInput(Direction, 1.0f);
	}
}

void AHomeWorldCharacter::Look(const FInputActionValue& Value)
{
	const FVector2D Axis = Value.Get<FVector2D>();
	AddControllerYawInput(Axis.X * LookSensitivity);
	AddControllerPitchInput(Axis.Y * LookSensitivity);
}
