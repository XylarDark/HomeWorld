// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "BuildPlacementSupport.h"
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
#include "HomeWorldResourcePile.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "InputActionValue.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/World.h"
#include "Engine/HitResult.h"
#include "CollisionQueryParams.h"
#include "Components/CapsuleComponent.h"
#include "Engine/GameInstance.h"

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
	if (!PrimaryAttackAction)
	{
		PrimaryAttackAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_PrimaryAttack.IA_PrimaryAttack"));
	}
	if (!DodgeAction)
	{
		DodgeAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Dodge.IA_Dodge"));
	}
	if (!InteractAction)
	{
		InteractAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Interact.IA_Interact"));
	}
	if (!PlaceAction)
	{
		PlaceAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Place.IA_Place"));
	}
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

	if (PrimaryAttackAction && PrimaryAttackAbilityClass)
	{
		EnhancedInput->BindAction(PrimaryAttackAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnPrimaryAttackTriggered);
	}
	if (DodgeAction && DodgeAbilityClass)
	{
		EnhancedInput->BindAction(DodgeAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnDodgeTriggered);
	}
	if (InteractAction && InteractAbilityClass)
	{
		EnhancedInput->BindAction(InteractAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnInteractTriggered);
	}
	if (PlaceAction && PlaceAbilityClass)
	{
		EnhancedInput->BindAction(PlaceAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnPlaceTriggered);
	}

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

void AHomeWorldCharacter::OnPrimaryAttackTriggered(const FInputActionValue& Value)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: PrimaryAttack input triggered"));
	if (!AbilitySystemComponent)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: PrimaryAttack skipped - no AbilitySystemComponent"));
		return;
	}
	if (!PrimaryAttackAbilityClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: PrimaryAttack skipped - PrimaryAttackAbilityClass not set on Blueprint"));
		return;
	}
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(PrimaryAttackAbilityClass);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: PrimaryAttack ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
}

void AHomeWorldCharacter::OnDodgeTriggered(const FInputActionValue& Value)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Dodge input triggered"));
	if (!AbilitySystemComponent)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Dodge skipped - no AbilitySystemComponent"));
		return;
	}
	if (!DodgeAbilityClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Dodge skipped - DodgeAbilityClass not set on Blueprint"));
		return;
	}
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(DodgeAbilityClass);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Dodge ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
}

void AHomeWorldCharacter::OnInteractTriggered(const FInputActionValue& Value)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Interact input triggered"));
	if (!AbilitySystemComponent)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Interact skipped - no AbilitySystemComponent"));
		return;
	}
	if (!InteractAbilityClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Interact skipped - InteractAbilityClass not set on Blueprint"));
		return;
	}
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(InteractAbilityClass);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Interact ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
}

void AHomeWorldCharacter::OnPlaceTriggered(const FInputActionValue& Value)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Place input triggered"));
	if (!AbilitySystemComponent)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Place skipped - no AbilitySystemComponent"));
		return;
	}
	if (!PlaceAbilityClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Place skipped - PlaceAbilityClass not set on Blueprint"));
		return;
	}
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(PlaceAbilityClass);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Place ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
}

bool AHomeWorldCharacter::TryPlaceAtCursor()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Place failed - no World"));
		return false;
	}
	if (!PlaceActorClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Place failed - PlaceActorClass not set (assign BP_BuildOrder_Wall or placeholder in Blueprint)"));
		return false;
	}
	const float MaxDistance = 10000.0f;
	FHitResult OutHit;
	FTransform OutTransform;
	if (!UBuildPlacementSupport::GetPlacementTransform(World, MaxDistance, OutHit, OutTransform))
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Place failed - no hit (aim at ground or surface)"));
		return false;
	}
	AActor* Spawned = World->SpawnActor<AActor>(PlaceActorClass, OutTransform);
	if (!Spawned)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Place failed - spawn failed at %s"), *OutTransform.GetLocation().ToString());
		return false;
	}
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Place succeeded at %s (spawned %s)"), *OutTransform.GetLocation().ToString(), *GetNameSafe(Spawned));
	return true;
}

FName AHomeWorldCharacter::GetSpiritIdForDeath() const
{
	return FName(*FString::Printf(TEXT("%s_%u"), *GetName(), GetUniqueID()));
}

void AHomeWorldCharacter::ReportDeathAndAddSpirit()
{
	UWorld* World = GetWorld();
	if (!World) return;
	UGameInstance* GI = World->GetGameInstance();
	if (!GI) return;
	UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>();
	if (!Spirits) return;
	FName SpiritId = GetSpiritIdForDeath();
	Spirits->AddSpirit(SpiritId);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Character '%s' reported death and added as spirit: %s"), *GetName(), *SpiritId.ToString());
}

bool AHomeWorldCharacter::TryHarvestInFront()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	const FVector Start = GetActorLocation() + FVector(0.0f, 0.0f, GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.0f);
	const FVector Forward = GetControlRotation().Vector();
	const float TraceLength = 280.0f;
	const FVector End = Start + Forward * TraceLength;
	FHitResult Hit;
	FCollisionQueryParams Params(NAME_None, false, this);
	if (!World->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		return false;
	}
	AHomeWorldResourcePile* Pile = Cast<AHomeWorldResourcePile>(Hit.GetActor());
	if (Pile)
	{
		UGameInstance* GI = World->GetGameInstance();
		if (!GI)
		{
			return false;
		}
		UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
		if (!Inv)
		{
			return false;
		}
		const FName ResourceType = Pile->ResourceType;
		const int32 Amount = Pile->AmountPerHarvest;
		Inv->AddResource(ResourceType, Amount);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Harvest succeeded - %s +%d"), *ResourceType.ToString(), Amount);
		return true;
	}

	// Day 18: Treasure POI (tag Treasure_POI) — grant resources and remove actor
	AActor* HitActor = Hit.GetActor();
	if (HitActor && HitActor->ActorHasTag(FName("Treasure_POI")))
	{
		UGameInstance* GI = World->GetGameInstance();
		if (GI)
		{
			if (UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>())
			{
				Inv->AddResource(FName("Wood"), 25);
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Treasure opened - Wood +25"));
			}
		}
		HitActor->Destroy();
		return true;
	}

	// Day 18: Shrine POI (tag Shrine_POI) — placeholder (future: GAS buff)
	if (HitActor && HitActor->ActorHasTag(FName("Shrine_POI")))
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Shrine activated (placeholder)"));
		return true;
	}

	return false;
}

void AHomeWorldCharacter::Move(const FInputActionValue& Value)
{
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
