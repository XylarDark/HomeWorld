// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Math/RotationMatrix.h"
#include "HomeWorldAttributeSet.h"
#include "InputActionValue.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/World.h"
#include "Engine/HitResult.h"
#include "CollisionQueryParams.h"
#include "Components/CapsuleComponent.h"

AHomeWorldCharacter::AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
	AbilitySystemComponent->SetIsReplicated(true);

	AttributeSet = CreateDefaultSubobject<UHomeWorldAttributeSet>(TEXT("AttributeSet"));

	// Character orients to movement direction (not camera yaw) so third-person feels natural when moving with WASD.
	bUseControllerRotationYaw = false;
	if (UCharacterMovementComponent* Movement = GetCharacterMovement())
	{
		Movement->bOrientRotationToMovement = true;
		Movement->RotationRate = FRotator(0.0f, RotationRateYaw, 0.0f);
	}
	// Human-sized capsule and Pawn collision so the character stands on the ground correctly (Task: Character touching the ground).
	if (UCapsuleComponent* Capsule = GetCapsuleComponent())
	{
		Capsule->SetCapsuleSize(CapsuleRadius, CapsuleHalfHeight);
		Capsule->SetCollisionProfileName(FName("Pawn"));
	}

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->bUsePawnControlRotation = true;
	CameraBoom->TargetArmLength = TargetArmLength;
	CameraBoom->bDoCollisionTest = true;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom);
	FollowCamera->SetFieldOfView(CameraFOV);
}

UAbilitySystemComponent* AHomeWorldCharacter::GetAbilitySystemComponent() const
{
	return AbilitySystemComponent;
}

void AHomeWorldCharacter::BeginPlay()
{
	Super::BeginPlay();
	// Apply Blueprint/class defaults for rotation rate (constructor only sees base default).
	if (UCharacterMovementComponent* Movement = GetCharacterMovement())
	{
		Movement->RotationRate = FRotator(0.0f, RotationRateYaw, 0.0f);
	}
	// Place character on ground if we hit something below (avoids floating when Player Start is slightly high).
	if (UWorld* World = GetWorld())
	{
		UCapsuleComponent* Capsule = GetCapsuleComponent();
		if (Capsule)
		{
			const float HalfHeight = Capsule->GetUnscaledCapsuleHalfHeight();
			const FVector Start = GetActorLocation();
			const FVector End = Start - FVector(0.0f, 0.0f, HalfHeight + 500.0f);
			FHitResult Hit;
			FCollisionQueryParams Params(NAME_None, false, this);
			if (World->LineTraceSingleByChannel(Hit, Start, End, ECC_WorldStatic, Params))
			{
				SetActorLocation(FVector(Start.X, Start.Y, Hit.ImpactPoint.Z + HalfHeight));
			}
		}
	}
	USkeletalMeshComponent* MeshComp = GetMesh();
	if (MeshComp)
	{
		MeshComp->SetRelativeRotation(FRotator(0.0f, MeshForwardYawOffset, 0.0f));
	}
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
	// Camera-relative movement: W = move toward where the camera looks, so the character feels responsive to the camera.
	const FRotator ControlRot = GetControlRotation();
	FVector Forward = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::X);
	FVector Right = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::Y);
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
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC)
	{
		return;
	}
	FRotator R = PC->GetControlRotation();
	R.Yaw += Axis.X * LookSensitivity;
	// Clamp pitch so the camera doesn't flip over the top or go below the horizon; keeps third-person feel consistent.
	R.Pitch = FMath::Clamp(R.Pitch + Axis.Y * LookSensitivity, MinPitch, MaxPitch);
	R.Roll = 0.0f;
	PC->SetControlRotation(R);
}
