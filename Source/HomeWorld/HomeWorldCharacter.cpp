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
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/DateTime.h"

// #region agent log
static void DebugLog(const char* HypothesisId, const char* Location, const char* Message, const FString& DataJson)
{
	FString Path = FPaths::ProjectDir() + TEXT("debug-cb22d5.log");
	FString Existing;
	FFileHelper::LoadFileToString(Existing, *Path);
	int64 Ts = (int64)FDateTime::UtcNow().ToUnixTimestamp() * 1000;
	Existing += FString::Printf(TEXT("{\"sessionId\":\"cb22d5\",\"hypothesisId\":\"%s\",\"location\":\"%s\",\"message\":\"%s\",\"data\":%s,\"timestamp\":%lld}\n"),
		*FString(HypothesisId), *FString(Location), *FString(Message), *DataJson, Ts);
	FFileHelper::SaveStringToFile(Existing, *Path);
}
// #endregion

AHomeWorldCharacter::AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
	AbilitySystemComponent->SetIsReplicated(true);

	AttributeSet = CreateDefaultSubobject<UHomeWorldAttributeSet>(TEXT("AttributeSet"));

	// Third-person camera: character orients to movement, not to camera
	bUseControllerRotationYaw = false;
	if (UCharacterMovementComponent* Movement = GetCharacterMovement())
	{
		Movement->bOrientRotationToMovement = true;
		Movement->RotationRate = FRotator(0.0f, RotationRateYaw, 0.0f);
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
	// #region agent log
	USkeletalMeshComponent* MeshComp = GetMesh();
	DebugLog("H5", "HomeWorldCharacter.cpp:BeginPlay", "BeginPlay", FString::Printf(TEXT("{\"hasMesh\":%d,\"meshOffsetYaw\":%.1f}"), MeshComp ? 1 : 0, MeshForwardYawOffset));
	// #endregion
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
	// #region agent log
	DebugLog("H1", "HomeWorldCharacter.cpp:SetupPlayerInputComponent", "Input setup entry", FString::Printf(TEXT("{\"hasEnhanced\":%d,\"hasCtx\":%d,\"hasMove\":%d,\"hasLook\":%d}"),
		EnhancedInput ? 1 : 0, DefaultMappingContext ? 1 : 0, MoveAction ? 1 : 0, LookAction ? 1 : 0));
	// #endregion
	if (!EnhancedInput || !DefaultMappingContext || !MoveAction || !LookAction)
	{
		// #region agent log
		DebugLog("H1", "HomeWorldCharacter.cpp:SetupPlayerInputComponent", "Input setup early return", TEXT("{\"earlyReturn\":1}"));
		// #endregion
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
	// #region agent log
	DebugLog("H1", "HomeWorldCharacter.cpp:SetupPlayerInputComponent", "Input bindings applied", TEXT("{\"bound\":1}"));
	// #endregion
}

void AHomeWorldCharacter::Move(const FInputActionValue& Value)
{
	const FVector2D Axis = Value.Get<FVector2D>();
	// Camera-relative movement: W = move toward where the camera looks
	const FRotator ControlRot = GetControlRotation();
	FVector Forward = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::X);
	FVector Right = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::Y);
	FVector Direction = Forward * Axis.Y + Right * Axis.X;
	Direction.Z = 0.0f;
	// #region agent log
	static bool moveLogged = false;
	if (!moveLogged) { moveLogged = true; DebugLog("H2", "HomeWorldCharacter.cpp:Move", "Move called", FString::Printf(TEXT("{\"axisX\":%.2f,\"axisY\":%.2f,\"dirNonZero\":%d}"), Axis.X, Axis.Y, !Direction.IsNearlyZero() ? 1 : 0)); }
	// #endregion
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
	// #region agent log
	static bool lookEntryLogged = false;
	if (!lookEntryLogged) { lookEntryLogged = true; DebugLog("H3", "HomeWorldCharacter.cpp:Look", "Look entry", FString::Printf(TEXT("{\"hasPC\":%d}"), PC ? 1 : 0)); }
	// #endregion
	if (!PC)
	{
		return;
	}
	FRotator R = PC->GetControlRotation();
	R.Yaw += Axis.X * LookSensitivity;
	R.Pitch = FMath::Clamp(R.Pitch + Axis.Y * LookSensitivity, MinPitch, MaxPitch);
	R.Roll = 0.0f;
	// #region agent log
	static bool lookAppliedLogged = false;
	if (!lookAppliedLogged) { lookAppliedLogged = true; DebugLog("H3", "HomeWorldCharacter.cpp:Look", "Look applied", FString::Printf(TEXT("{\"pitchClamped\":%.1f,\"minPitch\":%.1f,\"maxPitch\":%.1f}"), R.Pitch, MinPitch, MaxPitch)); }
	// #endregion
	PC->SetControlRotation(R);
}
