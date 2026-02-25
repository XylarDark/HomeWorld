// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"
#include "GameplayAbilitySpec.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerState.h"
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
#include "HAL/FileManager.h"
#include "Misc/Paths.h"

// #region agent log
static void DebugLogLine(const FString& Location, const FString& Message, const FString& DataJson, const FString& HypothesisId)
{
	const FString Path = FPaths::ProjectSavedDir() + TEXT("debug-e79282.log");
	const int64 Timestamp = FDateTime::UtcNow().ToUnixTimestamp() * 1000;
	const FString Line = FString::Printf(TEXT("{\"sessionId\":\"e79282\",\"timestamp\":%lld,\"location\":\"%s\",\"message\":\"%s\",\"data\":%s,\"hypothesisId\":\"%s\"}\n"),
		Timestamp, *Location, *Message.Replace(TEXT("\""), TEXT("\\\"")), *DataJson, *HypothesisId);
	if (FArchive* Ar = IFileManager::Get().CreateFileWriter(*Path, 0x08)) // FILEWRITE_Append
	{
		FTCHARToUTF8 Utf8(*Line);
		Ar->Serialize(const_cast<char*>(Utf8.Get()), Utf8.Length());
		Ar->Close();
		delete Ar;
	}
}
// #endregion

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
	// #region agent log
	{
		const FVector Loc = GetActorLocation();
		const FString DataJson = FString::Printf(TEXT("{\"locX\":%.1f,\"locY\":%.1f,\"locZ\":%.1f,\"hasController\":%s,\"hasCameraBoom\":%s,\"hasFollowCamera\":%s}"),
			Loc.X, Loc.Y, Loc.Z,
			GetController() ? TEXT("true") : TEXT("false"),
			CameraBoom ? TEXT("true") : TEXT("false"),
			FollowCamera ? TEXT("true") : TEXT("false"));
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:BeginPlay"), TEXT("Character BeginPlay"), DataJson, TEXT("H2,H4,H5"));
	}
	// #endregion
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

void AHomeWorldCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	// Apply accumulated movement from the four directional keys (W/S/A/D).
	float Forward = FMath::Clamp(MovementForwardAxis, -1.0f, 1.0f);
	float Right = FMath::Clamp(MovementRightAxis, -1.0f, 1.0f);
	if (Forward != 0.f || Right != 0.f)
	{
		const FRotator ControlRot = GetControlRotation();
		FVector ForwardVec = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::X);
		FVector RightVec = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::Y);
		FVector Direction = ForwardVec * Forward + RightVec * Right;
		Direction.Z = 0.f;
		if (!Direction.IsNearlyZero())
		{
			Direction.Normalize();
			AddMovementInput(Direction, 1.0f);
		}
	}
}

void AHomeWorldCharacter::PossessedBy(AController* NewController)
{
	Super::PossessedBy(NewController);
	// #region agent log
	{
		const FString DataJson = FString::Printf(TEXT("{\"hasController\":true,\"controllerName\":\"%s\"}"), NewController ? *NewController->GetName() : TEXT("null"));
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:PossessedBy"), TEXT("Pawn possessed"), DataJson, TEXT("H2"));
	}
	// #endregion
	if (AbilitySystemComponent)
	{
		// Server and owning client: owner = this. Simulated proxy: owner = PlayerState for replication.
		if (IsLocallyControlled() || HasAuthority())
		{
			AbilitySystemComponent->InitAbilityActorInfo(this, this);
		}
		else if (APlayerState* PS = GetPlayerState())
		{
			AbilitySystemComponent->InitAbilityActorInfo(this, PS);
		}
		// Grant default abilities (assigned in Blueprint) so GAS is "in use"; only for authority/local.
		if (IsLocallyControlled() || HasAuthority())
		{
			for (TSubclassOf<UGameplayAbility> AbilityClass : DefaultAbilities)
			{
				if (AbilityClass)
				{
					AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(AbilityClass, 1, INDEX_NONE, this));
				}
			}
		}
	}
}

void AHomeWorldCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	UEnhancedInputComponent* EnhancedInput = Cast<UEnhancedInputComponent>(PlayerInputComponent);
	// #region agent log
	{
		const FString DataJson = FString::Printf(TEXT("{\"hasEnhancedInput\":%s,\"hasDefaultMappingContext\":%s,\"hasMoveAction\":%s,\"hasLookAction\":%s,\"willReturnEarly\":%s}"),
			EnhancedInput ? TEXT("true") : TEXT("false"),
			DefaultMappingContext ? TEXT("true") : TEXT("false"),
			MoveAction ? TEXT("true") : TEXT("false"),
			LookAction ? TEXT("true") : TEXT("false"),
			(!EnhancedInput || !DefaultMappingContext || !MoveAction || !LookAction) ? TEXT("true") : TEXT("false"));
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:SetupPlayerInputComponent"), TEXT("Input setup"), DataJson, TEXT("H3"));
	}
	// #endregion
	// Fallback: load input assets from project if not set (e.g. when Default Pawn Class is C++ instead of BP_HomeWorldCharacter).
	if (!MoveAction)
	{
		MoveAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Move.IA_Move"));
	}
	if (!LookAction)
	{
		LookAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Look.IA_Look"));
	}
	if (!DefaultMappingContext)
	{
		DefaultMappingContext = LoadObject<UInputMappingContext>(nullptr, TEXT("/Game/HomeWorld/Input/IMC_Default.IMC_Default"));
	}
	if (!MoveForwardAction)
	{
		MoveForwardAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_MoveForward.IA_MoveForward"));
	}
	if (!MoveBackAction)
	{
		MoveBackAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_MoveBack.IA_MoveBack"));
	}
	if (!StrafeLeftAction)
	{
		StrafeLeftAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_StrafeLeft.IA_StrafeLeft"));
	}
	if (!StrafeRightAction)
	{
		StrafeRightAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_StrafeRight.IA_StrafeRight"));
	}
	// #region agent log
	{
		const FString DataJson2 = FString::Printf(TEXT("{\"afterFallback_hasMove\":%s,\"afterFallback_hasLook\":%s,\"afterFallback_hasIMC\":%s,\"willStillReturnEarly\":%s}"),
			MoveAction ? TEXT("true") : TEXT("false"),
			LookAction ? TEXT("true") : TEXT("false"),
			DefaultMappingContext ? TEXT("true") : TEXT("false"),
			(!EnhancedInput || !DefaultMappingContext || !MoveAction || !LookAction) ? TEXT("true") : TEXT("false"));
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:SetupPlayerInputComponent:afterFallback"), TEXT("Input after fallback"), DataJson2, TEXT("H3"));
	}
	// #endregion
	if (!EnhancedInput || !DefaultMappingContext || !MoveAction || !LookAction)
	{
		return;
	}

	bool bMappingContextAdded = false;
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (ULocalPlayer* LP = PC->GetLocalPlayer())
		{
			if (UEnhancedInputLocalPlayerSubsystem* Subsystem = LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>())
			{
				Subsystem->AddMappingContext(DefaultMappingContext, 0);
				bMappingContextAdded = true;
			}
		}
	}
	// #region agent log
	{
		APlayerController* PC = Cast<APlayerController>(GetController());
		ULocalPlayer* LP = PC ? PC->GetLocalPlayer() : nullptr;
		UEnhancedInputLocalPlayerSubsystem* Subsystem = LP ? LP->GetSubsystem<UEnhancedInputLocalPlayerSubsystem>() : nullptr;
		const FString DataJson3 = FString::Printf(TEXT("{\"hasPC\":%s,\"hasLP\":%s,\"hasSubsystem\":%s,\"mappingContextAdded\":%s}"),
			PC ? TEXT("true") : TEXT("false"),
			LP ? TEXT("true") : TEXT("false"),
			Subsystem ? TEXT("true") : TEXT("false"),
			bMappingContextAdded ? TEXT("true") : TEXT("false"));
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:SetupPlayerInputComponent:mapping"), TEXT("Mapping context"), DataJson3, TEXT("H3"));
	}
	// #endregion

	// Prefer four directional actions; explicit pressed/released so movement stops on key up.
	if (MoveForwardAction && MoveBackAction && StrafeLeftAction && StrafeRightAction)
	{
		EnhancedInput->BindAction(MoveForwardAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnMoveForwardPressed);
		EnhancedInput->BindAction(MoveForwardAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnMoveForwardReleased);
		EnhancedInput->BindAction(MoveBackAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnMoveBackPressed);
		EnhancedInput->BindAction(MoveBackAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnMoveBackReleased);
		EnhancedInput->BindAction(StrafeLeftAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnStrafeLeftPressed);
		EnhancedInput->BindAction(StrafeLeftAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnStrafeLeftReleased);
		EnhancedInput->BindAction(StrafeRightAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnStrafeRightPressed);
		EnhancedInput->BindAction(StrafeRightAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnStrafeRightReleased);
	}
	else if (MoveAction)
	{
		EnhancedInput->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::Move);
	}

	EnhancedInput->BindAction(LookAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::Look);

	// Ensure game viewport receives input after bindings are set (fixes PIE when keyboard/mouse don't move or look).
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		if (IsLocallyControlled())
		{
			FInputModeGameOnly InputMode;
			PC->SetInputMode(InputMode);
			PC->SetShowMouseCursor(false);
		}
	}
}

void AHomeWorldCharacter::OnMoveForwardPressed(const FInputActionValue& Value)
{
	MovementForwardAxis = FMath::Clamp(MovementForwardAxis + 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnMoveForwardReleased(const FInputActionValue& Value)
{
	MovementForwardAxis = FMath::Clamp(MovementForwardAxis - 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnMoveBackPressed(const FInputActionValue& Value)
{
	MovementForwardAxis = FMath::Clamp(MovementForwardAxis - 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnMoveBackReleased(const FInputActionValue& Value)
{
	MovementForwardAxis = FMath::Clamp(MovementForwardAxis + 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnStrafeLeftPressed(const FInputActionValue& Value)
{
	MovementRightAxis = FMath::Clamp(MovementRightAxis - 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnStrafeLeftReleased(const FInputActionValue& Value)
{
	MovementRightAxis = FMath::Clamp(MovementRightAxis + 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnStrafeRightPressed(const FInputActionValue& Value)
{
	MovementRightAxis = FMath::Clamp(MovementRightAxis + 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::OnStrafeRightReleased(const FInputActionValue& Value)
{
	MovementRightAxis = FMath::Clamp(MovementRightAxis - 1.0f, -1.0f, 1.0f);
}

void AHomeWorldCharacter::Move(const FInputActionValue& Value)
{
	// #region agent log
	static bool bFirstMove = true;
	if (bFirstMove)
	{
		bFirstMove = false;
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:Move"), TEXT("Move action triggered"), TEXT("{}"), TEXT("H3"));
	}
	// #endregion
	const FVector2D Axis = Value.Get<FVector2D>();
	const FRotator ControlRot = GetControlRotation();
	FVector Forward = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::X);
	FVector Right = FRotationMatrix(FRotator(0.0f, ControlRot.Yaw, 0.0f)).GetUnitAxis(EAxis::Y);
	FVector Direction = Forward * Axis.X + Right * Axis.Y;
	Direction.Z = 0.0f;
	if (!Direction.IsNearlyZero())
	{
		Direction.Normalize();
		AddMovementInput(Direction, 1.0f);
	}
}

void AHomeWorldCharacter::Look(const FInputActionValue& Value)
{
	// #region agent log
	static bool bFirstLook = true;
	if (bFirstLook)
	{
		bFirstLook = false;
		DebugLogLine(TEXT("HomeWorldCharacter.cpp:Look"), TEXT("Look action triggered"), TEXT("{}"), TEXT("H3"));
	}
	// #endregion
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
