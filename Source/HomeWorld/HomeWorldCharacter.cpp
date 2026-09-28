// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldSoftBoundsComponent.h"
#include "HomeWorldTraversalComponent.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldShrinePortalComponent.h"
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
#include "HomeWorldGameMode.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldResourcePile.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldCraftSubsystem.h"
#include "HomeWorldCraftStation.h"
#include "HomeWorldMinigameInteractComponent.h"
#include "HomeWorldBossSealComponent.h"
#include "HomeWorldCombatDreamTypes.h"
#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldStoreTransferComponent.h"
#include "HomeWorldSpiritHealComponent.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "InputActionValue.h"
#include "InputAction.h"
#include "InputMappingContext.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "Engine/World.h"
#include "Engine/HitResult.h"
#include "Engine/ActorInstanceHandle.h"
#include "CollisionQueryParams.h"
#include "Components/CapsuleComponent.h"
#include "Components/PrimitiveComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "Components/PointLightComponent.h"
#include "Particles/ParticleSystem.h"
#include "Sound/SoundBase.h"
#include "TimerManager.h"
#include "EngineUtils.h"

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

	FallbackGlideComponent = CreateDefaultSubobject<UHomeWorldFallbackGlideComponent>(TEXT("FallbackGlideComponent"));
	SoftBoundsComponent = CreateDefaultSubobject<UHomeWorldSoftBoundsComponent>(TEXT("SoftBoundsComponent"));
	TraversalComponent = CreateDefaultSubobject<UHomeWorldTraversalComponent>(TEXT("TraversalComponent"));
	SpiritStealthComponent = CreateDefaultSubobject<UHomeWorldSpiritStealthComponent>(TEXT("SpiritStealthComponent"));
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

	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			TimeOfDay->OnPhaseChanged.AddDynamic(this, &AHomeWorldCharacter::OnTimeOfDayPhaseChanged);
			SyncFormWithTimeOfDay();
			// T0 #1 NODE_WAKE: homestead start-day beat via existing TOD + spawn hooks (not PlayerStart alone).
			TryEmitNodeWakeStartDayBeat();
			// T0_DEFAULT_SKYBOX_DAY: Engine stock day sky via existing TOD (not kettle / other T0).
			TimeOfDay->EnsureDefaultBrightDaySky(true);
		}
	}
	if (TraversalComponent)
	{
		TraversalComponent->ApplyFormMovementTuning(GetIsSpiritForm());
	}
}

void AHomeWorldCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	if (SoftBoundsComponent)
	{
		SoftBoundsComponent->bBoundsEnabled = !IsFallbackGliding();
	}

	if (IsFallbackGliding())
	{
		return;
	}

	UpdateInteractRangeHint(DeltaTime);

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
			// T1: Lethal astral damage → RequestAstralDeath. When Health goes to 0 at night, advance to dawn + respawn.
			AbilitySystemComponent->GetGameplayAttributeValueChangeDelegate(UHomeWorldAttributeSet::GetHealthAttribute()).AddUObject(this, &AHomeWorldCharacter::OnHealthChanged);
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
	if (!AstralDeathAction)
	{
		AstralDeathAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_AstralDeath.IA_AstralDeath"));
	}
	if (!SpiritShieldAction)
	{
		SpiritShieldAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_SpiritShield.IA_SpiritShield"));
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
	if (DodgeAction)
	{
		EnhancedInput->BindAction(DodgeAction, ETriggerEvent::Started, this, &AHomeWorldCharacter::OnSprintStarted);
		EnhancedInput->BindAction(DodgeAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnSprintCompleted);
		if (DodgeAbilityClass)
		{
			EnhancedInput->BindAction(DodgeAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnDodgeTriggered);
		}
	}
	if (InteractAction && InteractAbilityClass)
	{
		EnhancedInput->BindAction(InteractAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnInteractTriggered);
	}
	if (PlaceAction && PlaceAbilityClass)
	{
		EnhancedInput->BindAction(PlaceAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnPlaceTriggered);
	}
	if (AstralDeathAction)
	{
		EnhancedInput->BindAction(AstralDeathAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnAstralDeathTriggered);
	}
	if (SpiritShieldAction && SpiritShieldAbilityClass)
	{
		EnhancedInput->BindAction(SpiritShieldAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnSpiritShieldTriggered);
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

void AHomeWorldCharacter::OnAstralDeathTriggered(const FInputActionValue& Value)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: AstralDeath input triggered (dawn + respawn)"));
	RequestAstralDeath();
}

void AHomeWorldCharacter::OnSprintStarted(const FInputActionValue& Value)
{
	if (!AreDayBodyAbilitiesAllowed())
	{
		UE_LOG(LogTemp, Log, TEXT("FORM: day verb rejected - sprint (TOD_NIGHT_HOME body night)"));
		return;
	}
	// T0 #2: tea gates sprint. Ungated day-verb sprint alone = closed_fail for MUST #2.
	if (!IsTeaSprintGateActive())
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_KETTLE: sprint rejected - need tea (ungated sprint alone = closed_fail for MUST #2; not meal-BP-as-tea)"));
		return;
	}
	if (TraversalComponent)
	{
		TraversalComponent->SetSprintHeld(true);
	}
	UE_LOG(LogTemp, Log,
		TEXT("NODE_KETTLE: tea-gated sprint TOD_DAY FORM_BODY (half-day gate active; not ungated MV alone)"));
}

void AHomeWorldCharacter::OnSprintCompleted(const FInputActionValue& Value)
{
	if (TraversalComponent)
	{
		TraversalComponent->SetSprintHeld(false);
	}
}

void AHomeWorldCharacter::Jump()
{
	if (TraversalComponent && TraversalComponent->TryMantleOrVault())
	{
		return;
	}
	Super::Jump();
}

bool AHomeWorldCharacter::TryMantleOrVault()
{
	if (!AreDayBodyAbilitiesAllowed())
	{
		UE_LOG(LogTemp, Log, TEXT("FORM: day verb rejected — mantle (TOD_NIGHT_HOME body night)"));
		return false;
	}
	return TraversalComponent ? TraversalComponent->TryMantleOrVault() : false;
}

bool AHomeWorldCharacter::TrySpiritBlink()
{
	return TraversalComponent ? TraversalComponent->TrySpiritBlink() : false;
}

void AHomeWorldCharacter::OnSpiritShieldTriggered(const FInputActionValue& Value)
{
	if (GetIsSpiritForm() && TrySpiritBlink())
	{
		return;
	}
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield input triggered"));
	if (!AbilitySystemComponent)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield skipped - no AbilitySystemComponent"));
		return;
	}
	if (!SpiritShieldAbilityClass)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield skipped - SpiritShieldAbilityClass not set on Blueprint"));
		return;
	}
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(SpiritShieldAbilityClass);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
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

FName AHomeWorldCharacter::GetSpiritIdForDeath()
{
	return FName(*FString::Printf(TEXT("%s_%u"), *GetName(), GetUniqueID()));
}

void AHomeWorldCharacter::OnHealthChanged(const FOnAttributeChangeData& Data)
{
	if (Data.NewValue > 0.f) return;
	// Only player character: astral death is "player's astral form defeated at night".
	if (!Cast<APlayerController>(GetController())) return;
	UWorld* World = GetWorld();
	if (!World) return;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsNight()) return;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Lethal astral damage (Health 0 at night) -> RequestAstralDeath"));
	RequestAstralDeath();
}

void AHomeWorldCharacter::RequestAstralDeath()
{
	AHomeWorldGameMode::RequestAstralDeath(this);
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

bool AHomeWorldCharacter::ConsumeMealRestore(EMealType MealType)
{
	UWorld* World = GetWorld();
	if (!World) return false;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (TimeOfDay && TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: ConsumeMealRestore only available by day (current phase is night)."));
		return false;
	}
	UHomeWorldAttributeSet* AttrSet = Cast<UHomeWorldAttributeSet>(AttributeSet);
	if (!AttrSet)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: ConsumeMealRestore failed - no AttributeSet."));
		return false;
	}
	const float Current = AttrSet->GetHealth();
	const float Max = AttrSet->GetMaxHealth();
	const float RestoreAmount = 25.f;
	const float NewHealth = FMath::Min(Current + RestoreAmount, Max);
	AttrSet->SetHealth(NewHealth);

	APlayerController* PC = Cast<APlayerController>(GetController());
	AHomeWorldPlayerState* PS = PC ? Cast<AHomeWorldPlayerState>(PC->PlayerState) : nullptr;
	if (PS)
	{
		PS->SetDayRestorationBuff(true);
		PS->IncrementMealsConsumedToday();
		PS->SetLastMealTriggered(MealType);
		PS->AddLovePoints(1);  // T1: meal contributes to love (HUD "Love: N" and night bonuses).
		// T2 caretaker stub: if Family-tagged actors exist in level, count as "meal with family".
		static const FName FamilyTag(TEXT("Family"));
		TArray<AActor*> FamilyActors;
		UGameplayStatics::GetAllActorsWithTag(World, FamilyTag, FamilyActors);
		if (FamilyActors.Num() > 0)
		{
			PS->IncrementMealsWithFamilyToday();
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: ConsumeMealRestore — meal with family (Family actors=%d); meals with family today=%d (caretaker stub)."), FamilyActors.Num(), PS->GetMealsWithFamilyToday());
		}
	}
	const TCHAR* MealName = MealType == EMealType::Breakfast ? TEXT("Breakfast") : (MealType == EMealType::Lunch ? TEXT("Lunch") : TEXT("Dinner"));
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: ConsumeMealRestore %s — Health %.0f -> %.0f, day buff set, meals today=%d (visible at night / HUD)."), MealName, Current, NewHealth, PS ? PS->GetMealsConsumedToday() : 0);
	return true;
}

bool AHomeWorldCharacter::IsFallbackGliding() const
{
	return FallbackGlideComponent && FallbackGlideComponent->IsGliding();
}

void AHomeWorldCharacter::CancelFallbackGlide()
{
	if (FallbackGlideComponent)
	{
		FallbackGlideComponent->CancelGlide();
	}
}

static AActor* FindGlideStartMarker(UWorld* World)
{
	if (!World)
	{
		return nullptr;
	}
	static const FName GlideStartNames[] = {
		FName(TEXT("GP_GlideStart")),
		FName(TEXT("CRUMB_Depart_Lookout")),
		FName(TEXT("VS_MARKER_LeaveIsland_FALLBACK")),
	};
	for (const FName& Label : GlideStartNames)
	{
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			AActor* Actor = *It;
			if (!Actor)
			{
				continue;
			}
#if WITH_EDITOR
			if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
			{
				return Actor;
			}
#endif
			if (Actor->GetName().Equals(Label.ToString(), ESearchCase::CaseSensitive))
			{
				return Actor;
			}
		}
	}
	TArray<AActor*> Tagged;
	UGameplayStatics::GetAllActorsWithTag(World, FName(TEXT("GlideStart")), Tagged);
	return Tagged.Num() > 0 ? Tagged[0] : nullptr;
}

bool AHomeWorldCharacter::TryStartFallbackGlide()
{
	if (!FallbackGlideComponent || FallbackGlideComponent->IsGliding())
	{
		return false;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	AActor* GlideStart = FindGlideStartMarker(World);
	if (!GlideStart)
	{
		UE_LOG(LogTemp, Log, TEXT("FALLBACK: TryStartFallbackGlide — no GP_GlideStart / CRUMB_Depart_Lookout in level"));
		return false;
	}

	const float DistSq = FVector::DistSquared(GetActorLocation(), GlideStart->GetActorLocation());
	if (DistSq > FMath::Square(GlideStartProximityCm))
	{
		UE_LOG(LogTemp, Log, TEXT("FALLBACK: TryStartFallbackGlide — too far from glide start (%.0f cm max)"), GlideStartProximityCm);
		return false;
	}

	const bool bStarted = FallbackGlideComponent->StartGlide();
	UE_LOG(LogTemp, Log, TEXT("FALLBACK: TryStartFallbackGlide %s near %s"), bStarted ? TEXT("started") : TEXT("failed"), *GlideStart->GetName());
	return bStarted;
}

bool AHomeWorldCharacter::TryShrinePortalInteract()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	const FVector Start = GetActorLocation() + FVector(0.0f, 0.0f, GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.0f);
	const FVector Forward = GetControlRotation().Vector();
	const float TraceLength = 320.0f;
	const FVector End = Start + Forward * TraceLength;
	FHitResult Hit;
	FCollisionQueryParams Params(NAME_None, false, this);
	if (!World->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		return false;
	}

	AActor* HitActor = Hit.GetActor();
	if (!HitActor)
	{
		return false;
	}

	UHomeWorldShrinePortalComponent* Portal = HitActor->FindComponentByClass<UHomeWorldShrinePortalComponent>();
	if (!Portal && HitActor->GetAttachParentActor())
	{
		Portal = HitActor->GetAttachParentActor()->FindComponentByClass<UHomeWorldShrinePortalComponent>();
	}
	if (!Portal)
	{
		static const FName PortalTags[] = { FName(TEXT("ShrinePortal")), FName(TEXT("Portal_POI")) };
		for (const FName& Tag : PortalTags)
		{
			if (HitActor->ActorHasTag(Tag))
			{
				Portal = HitActor->FindComponentByClass<UHomeWorldShrinePortalComponent>();
				break;
			}
		}
	}

	if (Portal)
	{
		return Portal->TryPortalTransit(this);
	}
	return false;
}

bool AHomeWorldCharacter::TryTameBeastInFront()
{
	if (GetIsSpiritForm())
	{
		ShowInteractFeedback(TEXT("TAME: day/body form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldBeastTameComponent* Tame = HitActor->FindComponentByClass<UHomeWorldBeastTameComponent>())
	{
		if (Tame->GetTameState() == EHomeWorldBeastTameState::Tamed)
		{
			const bool bPromoted = Tame->TryPromoteToHelper(this);
			ShowInteractFeedback(
				bPromoted ? TEXT("TAME: promoted to helper") : TEXT("TAME: helper promote failed"),
				bPromoted ? FColor::Green : FColor::Yellow);
			return bPromoted;
		}
		const bool bOffered = Tame->TryOfferFood(this);
		ShowInteractFeedback(
			bOffered ? TEXT("TAME: food offered — stay calm") : TEXT("TAME: need RES_BERRY or RES_HERB"),
			bOffered ? FColor::Green : FColor::Yellow);
		return bOffered;
	}
	return false;
}

bool AHomeWorldCharacter::TryHealSpiritInFront()
{
	if (!GetIsSpiritForm())
	{
		ShowInteractFeedback(TEXT("HEAL: night/spirit form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldSpiritHealComponent* Heal = HitActor->FindComponentByClass<UHomeWorldSpiritHealComponent>())
	{
		const bool bHealed = Heal->TryHeal(this);
		if (bHealed && SpiritStealthComponent)
		{
			SpiritStealthComponent->NotifyInteractWhileLit();
		}
		ShowInteractFeedback(
			bHealed ? TEXT("HEAL: spirit healed") : TEXT("HEAL: need RES_HERB/RES_SEED or already healed"),
			bHealed ? FColor::Green : FColor::Yellow);
		return bHealed;
	}
	return false;
}

bool AHomeWorldCharacter::TryNurtureInFront()
{
	// Existing homestead nurture path (V7). T0 #12 N1 NODE_PLANT_SLOT gated inside TryNurture
	// (same-slot day plant #3 + FORM_SPIRIT / TOD_NIGHT_SPIRIT). No parallel nurture service.
	if (!GetIsSpiritForm())
	{
		ShowInteractFeedback(TEXT("NURTURE: night/spirit form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldNurtureComponent* Nurture = HitActor->FindComponentByClass<UHomeWorldNurtureComponent>())
	{
		const bool bResult = Nurture->TryNurture(this);
		FString Feedback = bResult ? TEXT("NURTURE: success - M_Nurtured on") : TEXT("NURTURE: need required RES in inventory");
		if (!bResult && Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop && !Nurture->GetIsDayPlantedGivenHerb())
		{
			Feedback = TEXT("NODE_PLANT_SLOT: need day plant first (#3)");
		}
		else if (bResult && Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
		{
			Feedback = TEXT("NODE_PLANT_SLOT: spirit nurture");
		}
		ShowInteractFeedback(Feedback, bResult ? FColor::Green : FColor::Yellow);
		return bResult;
	}
	return false;
}


bool AHomeWorldCharacter::TryMinigameInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldMinigameInteractComponent* Minigame = HitActor->FindComponentByClass<UHomeWorldMinigameInteractComponent>())
	{
		const bool bOk = Minigame->TryMinigameInteract(this);
		if (bOk && SpiritStealthComponent)
		{
			SpiritStealthComponent->NotifyInteractWhileLit();
		}
		if (bOk && HomeWorldCombatDream::IsPolishFirstMinigame(Minigame->GetMinigameKind()))
		{
			ShowInteractFeedback(TEXT("MINIGAME:POSSESS — spirit anchors the dream (stub)"), FColor::Cyan);
		}
		return bOk;
	}
	return false;
}

bool AHomeWorldCharacter::TryBossSealInFront()
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	AHomeWorldPlayerState* PS = PC ? PC->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
	if (!PS || (!PS->GetDayBossActive() && !PS->GetNightBossActive()))
	{
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldBossSealComponent* Seal = HitActor->FindComponentByClass<UHomeWorldBossSealComponent>())
	{
		const bool bOk = Seal->TrySealStub(this);
		if (bOk)
		{
			ShowInteractFeedback(TEXT("BOSS:SEAL — banish stub (no kill)"), FColor::Green);
		}
		return bOk;
	}
	return false;
}

bool AHomeWorldCharacter::TryCraftInFront()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (GetIsSpiritForm() || (TimeOfDay && TimeOfDay->GetIsNight()))
	{
		UE_LOG(LogTemp, Log, TEXT("CRAFT: blocked — night or spirit form"));
		ShowInteractFeedback(TEXT("CRAFT: day/body form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	AHomeWorldCraftStation* Station = Cast<AHomeWorldCraftStation>(HitActor);
	if (!Station)
	{
		return false;
	}

	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldCraftSubsystem* Craft = GI ? GI->GetSubsystem<UHomeWorldCraftSubsystem>() : nullptr;
	if (!Craft)
	{
		UE_LOG(LogTemp, Warning, TEXT("CRAFT: fail — CraftSubsystem missing"));
		return false;
	}

	const bool bBeforeUnlock = Craft->IsCottageUnlocked();
	const bool bOk = Craft->TryInteractAtStation(this, Station);
	if (bOk)
	{
		if (Craft->IsCottageUnlocked() && !bBeforeUnlock)
		{
			ShowInteractFeedback(TEXT("PROGRESS:COTTAGE_UNLOCK"), FColor::Cyan);
		}
		else
		{
			ShowInteractFeedback(TEXT("CRAFT: ok — see Output Log"), FColor::Green);
		}
	}
	else
	{
		ShowInteractFeedback(TEXT("CRAFT: need resources or wrong step"), FColor::Yellow);
	}
	return bOk;
}

bool AHomeWorldCharacter::TryStoreTransferInFront()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (GetIsSpiritForm() || (TimeOfDay && TimeOfDay->GetIsNight()))
	{
		UE_LOG(LogTemp, Log, TEXT("STORE: blocked — night or spirit form"));
		ShowInteractFeedback(TEXT("STORE: day/body form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (UHomeWorldStoreTransferComponent* Store = HitActor->FindComponentByClass<UHomeWorldStoreTransferComponent>())
	{
		const bool bResult = Store->TryTransfer(this);
		ShowInteractFeedback(
			bResult ? TEXT("STORE: transfer ok") : TEXT("STORE: nothing to deposit/withdraw"),
			bResult ? FColor::Green : FColor::Yellow);
		return bResult;
	}
	return false;
}

bool AHomeWorldCharacter::TryHarvestInFront()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	// SYS V3: gather day/body only.
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (GetIsSpiritForm() || (TimeOfDay && TimeOfDay->GetIsNight()))
	{
		UE_LOG(LogTemp, Log, TEXT("GATHER: blocked — night or spirit form"));
		ShowInteractFeedback(TEXT("GATHER: day/body form only"), FColor::Yellow);
		return false;
	}

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
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
		if (Pile->TryHarvest(Inv))
		{
			UE_LOG(LogTemp, Log, TEXT("GATHER: harvest ok (total Physical: %d)"), Inv->GetTotalPhysicalGoods());
			ShowInteractFeedback(
				FString::Printf(TEXT("GATHER: +1 resource (total %d)"), Inv->GetTotalPhysicalGoods()),
				FColor::Green);
			return true;
		}
		ShowInteractFeedback(TEXT("GATHER: pile empty or blocked"), FColor::Yellow);
		return false;
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
				Inv->TryAddResource(HomeWorldInventory::RES_WOOD, 3);
				const int32 PhysicalTotal = Inv->GetTotalPhysicalGoods();
				UE_LOG(LogTemp, Log, TEXT("GATHER: treasure RES_WOOD +3 (total Physical: %d)"), PhysicalTotal);
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

	// List 57 T2: Breakfast (tag Breakfast) — in-world meal trigger. Interact (E) triggers ConsumeMealRestore(Breakfast).
	if (HitActor && HitActor->ActorHasTag(FName("Breakfast")))
	{
		const bool bOk = ConsumeMealRestore(EMealType::Breakfast);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Breakfast (interact) — %s. MVP List 57 T2."), bOk ? TEXT("consumed") : TEXT("skipped (e.g. night)"));
		return bOk;
	}

	// List 57 T3: Lunch (tag Lunch) — in-world meal trigger. Interact (E) or overlap triggers lunch.
	if (HitActor && HitActor->ActorHasTag(FName("Lunch")))
	{
		const bool bOk = ConsumeMealRestore(EMealType::Lunch);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Lunch (interact) — %s. MVP List 57 T3."), bOk ? TEXT("consumed") : TEXT("skipped (e.g. night)"));
		return bOk;
	}

	// List 57 T4: Dinner (tag Dinner) — in-world meal trigger. Interact (E) or overlap triggers dinner.
	if (HitActor && HitActor->ActorHasTag(FName("Dinner")))
	{
		const bool bOk = ConsumeMealRestore(EMealType::Dinner);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Dinner (interact) — %s. MVP List 57 T4."), bOk ? TEXT("consumed") : TEXT("skipped (e.g. night)"));
		return bOk;
	}

	// List 56 / T2 + T3 + T0 #11: Bed / NODE_BED -- go to bed (day) or wake (night).
	// Go-to-bed grants sleep gate (GrantSpiritSleepGate); spirit only if rune unlocked (#7).
	// Phase-alone SetPhase(Night) without this path = closed_fail for FORM_SPIRIT. Soft-kidnap != bed.
	if (HitActor && (HitActor->ActorHasTag(FName("Bed")) || HitActor->ActorHasTag(FName("NODE_BED"))))
	{
		if (UHomeWorldTimeOfDaySubsystem* Tod = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (Tod->GetIsNight())
			{
				Tod->AdvanceToDawn();
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wake (interact at bed) -- phase set to Dawn. MVP List 56 T3."));
			}
			else
			{
				// T0 #11: bed path grants sleep gate then form via CanEnterSpiritForm (not phase alone).
				if (bRuneGateUnlocked)
				{
					TryBedSleepSpirit();
				}
				else
				{
					Tod->SetPhase(EHomeWorldTimeOfDayPhase::Night);
					GrantSpiritSleepGate();
					UE_LOG(LogTemp, Log,
						TEXT("NODE_BED: sleep gate Night FORM_BODY (need NODE_RUNE for FORM_SPIRIT TOD_NIGHT_SPIRIT CAM_T0_BED; not phase-alone spirit; #9 w/o bed stay FORM_BODY)"));
				}
			}
			return true;
		}
	}

	// List 58 T3: Partner (tag Partner) — in-world love task. Interact (E) completes one love task (AddLovePoints + LoveTasksCompletedToday).
	if (HitActor && HitActor->ActorHasTag(FName("Partner")))
	{
		AHomeWorldPlayerState* PS = GetPlayerState<AHomeWorldPlayerState>();
		if (PS)
		{
			PS->CompleteOneLoveTask();
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Love task (interact with partner) — one love task done. MVP List 58 T3."));
			return true;
		}
	}

	// List 59 T1/T3: Child (tag Child) — in-world game-with-child. Interact (E) completes one game with child (AddLovePoints + GamesWithChildToday).
	if (HitActor && HitActor->ActorHasTag(FName("Child")))
	{
		AHomeWorldPlayerState* PS = GetPlayerState<AHomeWorldPlayerState>();
		if (PS)
		{
			PS->CompleteOneGameWithChild();
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Game with child (interact with child) — one game with child done. MVP List 59."));
			return true;
		}
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

void AHomeWorldCharacter::TryEmitNodeWakeStartDayBeat()
{
	// T0_M1 NODE_WAKE / TOD_DAY / FORM_BODY / CAM_T0_WAKE
	// Architecture Trade-Offs A-E: prefer existing GP_PlayerStart / PlayerStart_VS_MVP /
	// UHomeWorldTimeOfDaySubsystem hooks -- no parallel wake service, no new schema, no invent wake/WP APIs.
	// Anti closed_fail: PlayerStart alone != NODE_WAKE; PROXY SM_ProxyWakeMarker != world wake;
	// bed->Dawn alone (AdvanceToDawn) != start-day beat.
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		return;
	}

	const EHomeWorldTimeOfDayPhase Phase = TimeOfDay->GetCurrentPhase();
	if (Phase != EHomeWorldTimeOfDayPhase::Day)
	{
		// Leaving Day (or sitting on Dawn/Dusk/Night) clears the once-per-Day latch.
		bNodeWakeEmittedForCurrentDay = false;
		return;
	}

	// Wake prove requires FORM_BODY at Day.
	if (bIsSpiritForm)
	{
		return;
	}

	if (bNodeWakeEmittedForCurrentDay)
	{
		return;
	}
	bNodeWakeEmittedForCurrentDay = true;

	UE_LOG(LogTemp, Log,
		TEXT("NODE_WAKE: start-day beat TOD_DAY FORM_BODY CAM_T0_WAKE (homestead; not PlayerStart alone; not PROXY SM_ProxyWakeMarker; not bed->Dawn alone)"));
}

bool AHomeWorldCharacter::IsTeaSprintGateActive() const
{
	UWorld* World = GetWorld();
	if (!World || TeaSprintEndWorldTime <= 0.f)
	{
		return false;
	}
	if (bIsSpiritForm)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		return false;
	}
	return World->GetTimeSeconds() < TeaSprintEndWorldTime;
}

bool AHomeWorldCharacter::TryBrewNodeKettleTea()
{
	// T0_M2 NODE_KETTLE / TOD_DAY / FORM_BODY
	// Architecture Trade-Offs A-E: prefer existing inventory RES_HERB + Traversal day-verb sprint
	// -- no parallel tea service, no new schema, no invent kettle/tea/WP APIs.
	// Anti closed_fail: PROXY SM_ProxyKettle alone != world kettle; meal-BP != tea;
	// ungated sprint alone != tea-gated sprint.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: brew skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_KETTLE: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: brew skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_KETTLE: body form only"), FColor::Yellow);
		return false;
	}

	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_KETTLE: brew failed - no InventorySubsystem"));
		return false;
	}
	if (!Inv->SpendResource(HomeWorldInventory::RES_HERB, 1))
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: brew failed - need RES_HERB (herbs->tea)"));
		ShowInteractFeedback(TEXT("NODE_KETTLE: need RES_HERB"), FColor::Yellow);
		return false;
	}

	const float Duration = FMath::Max(1.f, TeaSprintHalfDaySeconds);
	TeaSprintEndWorldTime = World->GetTimeSeconds() + Duration;

	UE_LOG(LogTemp, Log,
		TEXT("NODE_KETTLE: tea brew TOD_DAY FORM_BODY (herbs->tea; gates sprint ~half day=%.0fs; not PROXY SM_ProxyKettle; not meal-BP-as-tea)"),
		Duration);
	ShowInteractFeedback(TEXT("NODE_KETTLE: tea ready - sprint gated ~half day"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryNodeKettleInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName KettleTags[] = {
		FName(TEXT("NODE_KETTLE")),
		FName(TEXT("Kettle")),
	};
	bool bIsKettle = false;
	for (const FName& Tag : KettleTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsKettle = true;
			break;
		}
	}
	if (!bIsKettle)
	{
		return false;
	}

	// World interact beat -- PROXY mesh alone (SM_ProxyKettle without interact/brew) = closed_fail.
	return TryBrewNodeKettleTea();
}

bool AHomeWorldCharacter::IsNodePlantSlotDayPlanted() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (UHomeWorldNurtureComponent* Nurture = It->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop && Nurture->GetIsDayPlantedGivenHerb())
			{
				return true;
			}
		}
	}
	return false;
}

bool AHomeWorldCharacter::TryPlantNodePlantSlotHerb()
{
	// T0_M3 NODE_PLANT_SLOT / TOD_DAY / FORM_BODY
	// Architecture Trade-Offs A-E: prefer existing HomeWorldNurtureTarget / N1 planter / inventory RES_HERB
	// -- no parallel plant service, no new schema, no invent plant/WP APIs.
	// Anti closed_fail: GP_N1_Crop nurture-only != day plant-given-herb; PROXY SM_ProxyPlantSlot alone != world plant;
	// TryNurtureInFront / spirit nurture != plant beat. #12 nurture DEFER (same slot identity only).
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PLANT_SLOT: plant skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PLANT_SLOT: plant skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: body form only"), FColor::Yellow);
		return false;
	}

	UHomeWorldNurtureComponent* Slot = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (UHomeWorldNurtureComponent* Nurture = It->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
			{
				Slot = Nurture;
				break;
			}
		}
	}
	if (!Slot)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_PLANT_SLOT: plant failed - no N1_Crop HomeWorldNurtureTarget slot in world"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: no plant slot"), FColor::Yellow);
		return false;
	}

	if (Slot->GetIsDayPlantedGivenHerb())
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_PLANT_SLOT: day plant given herb TOD_DAY FORM_BODY (already planted; same slot for #12; not TryNurture; not PROXY SM_ProxyPlantSlot)"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: already planted"), FColor::Green);
		return true;
	}

	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_PLANT_SLOT: plant failed - no InventorySubsystem"));
		return false;
	}
	if (!Inv->SpendResource(HomeWorldInventory::RES_HERB, 1))
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PLANT_SLOT: plant failed - need RES_HERB (given herb)"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: need RES_HERB"), FColor::Yellow);
		return false;
	}

	Slot->MarkDayPlantedGivenHerb();
	UE_LOG(LogTemp, Log,
		TEXT("NODE_PLANT_SLOT: day plant given herb TOD_DAY FORM_BODY (not GP_N1 nurture-only; not PROXY SM_ProxyPlantSlot; not TryNurture; #12 DEFER)"));
	ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: day plant given herb"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryNodePlantSlotInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName PlantTags[] = {
		FName(TEXT("NODE_PLANT_SLOT")),
		FName(TEXT("PlantSlot")),
	};
	bool bIsPlantSlot = false;
	for (const FName& Tag : PlantTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsPlantSlot = true;
			break;
		}
	}
	// Prefer N1 nurture target as the world plant slot (same identity #12 uses) -- not PROXY mesh alone.
	if (UHomeWorldNurtureComponent* Nurture = HitActor->FindComponentByClass<UHomeWorldNurtureComponent>())
	{
		if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
		{
			bIsPlantSlot = true;
		}
	}
	if (!bIsPlantSlot)
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyPlantSlot alone without plant/spend = closed_fail.
	// Do NOT call TryNurtureInFront here (spirit nurture = #12, not day plant).
	return TryPlantNodePlantSlotHerb();
}

bool AHomeWorldCharacter::IsNodePlantSlotSpiritNurtured() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (UHomeWorldNurtureComponent* Nurture = It->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop
				&& Nurture->GetIsDayPlantedGivenHerb()
				&& Nurture->GetIsNurtured())
			{
				return true;
			}
		}
	}
	return false;
}

bool AHomeWorldCharacter::TryNurtureNodePlantSlot()
{
	// T0_M12 NODE_PLANT_SLOT / TOD_NIGHT_SPIRIT / FORM_SPIRIT
	// Architecture Trade-Offs A-E: prefer existing TryNurture / HomeWorldNurtureComponent / N1 slot
	// -- no parallel nurture service, no new schema, no invent nurture/WP APIs.
	// Prereq: #3 day plant same NODE_PLANT_SLOT + #11 spirit path (rune+bed).
	// Anti closed_fail: different-slot N2; body-form nurture as #12; day-plant-alone as spirit nurture.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	if (!GetIsSpiritForm())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PLANT_SLOT: nurture skipped - need FORM_SPIRIT"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: spirit form only"), FColor::Yellow);
		return false;
	}

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsSpiritPhase())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PLANT_SLOT: nurture skipped - need TOD_NIGHT_SPIRIT"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: night spirit phase only"), FColor::Yellow);
		return false;
	}

	UHomeWorldNurtureComponent* Slot = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (UHomeWorldNurtureComponent* Nurture = It->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
			{
				Slot = Nurture;
				break;
			}
		}
	}
	if (!Slot)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_PLANT_SLOT: nurture failed - no N1_Crop HomeWorldNurtureTarget slot in world"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: no plant slot"), FColor::Yellow);
		return false;
	}

	if (!Slot->GetIsDayPlantedGivenHerb())
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_PLANT_SLOT: nurture failed - need day plant given herb first (#3 same-slot prereq; unplanted != spirit nurture; not different-slot N2)"));
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: need day plant first"), FColor::Yellow);
		return false;
	}

	// N1 only -- never score N2_Stored as #12 same-slot prove.
	const bool bOk = Slot->TryNurture(this);
	if (bOk)
	{
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: spirit nurture"), FColor::Green);
	}
	else
	{
		ShowInteractFeedback(TEXT("NODE_PLANT_SLOT: nurture need RES_SEED"), FColor::Yellow);
	}
	return bOk;
}

bool AHomeWorldCharacter::TryEquipNodeBackpack()
{
	// T0_M4 NODE_BACKPACK / TOD_DAY / FORM_BODY
	// Architecture Trade-Offs A-E: prefer existing UHomeWorldInventorySubsystem
	// -- no parallel inventory service, no new schema, no invent backpack/WP APIs.
	// Anti closed_fail: ungated inventory-lite alone != equip->inventory;
	// PROXY SM_ProxyBackpack alone != world equip.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_BACKPACK: equip skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_BACKPACK: equip skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: body form only"), FColor::Yellow);
		return false;
	}

	if (bBackpackEquipped)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BACKPACK: equip TOD_DAY FORM_BODY (already equipped; inventory gated; not inventory-lite alone; not PROXY SM_ProxyBackpack)"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: already equipped"), FColor::Green);
		return true;
	}

	bBackpackEquipped = true;
	UE_LOG(LogTemp, Log,
		TEXT("NODE_BACKPACK: equip TOD_DAY FORM_BODY (gates inventory open/use; not inventory-lite alone; not PROXY SM_ProxyBackpack)"));
	ShowInteractFeedback(TEXT("NODE_BACKPACK: equipped - inventory gated"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryNodeBackpackInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName BackpackTags[] = {
		FName(TEXT("NODE_BACKPACK")),
		FName(TEXT("Backpack")),
	};
	bool bIsBackpack = false;
	for (const FName& Tag : BackpackTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsBackpack = true;
			break;
		}
	}
	if (!bIsBackpack)
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyBackpack alone without equip latch = closed_fail.
	return TryEquipNodeBackpack();
}

bool AHomeWorldCharacter::TryOpenInventoryGated()
{
	// Inventory open/use requires NODE_BACKPACK equip latch (existing UHomeWorldInventorySubsystem).
	// Ungated inventory-lite alone = closed_fail for MUST #4.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_BACKPACK: inventory rejected - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_BACKPACK: inventory rejected - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: body form only"), FColor::Yellow);
		return false;
	}
	if (!bBackpackEquipped)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BACKPACK: inventory rejected - need equip (ungated inventory-lite = closed_fail; not PROXY SM_ProxyBackpack)"));
		ShowInteractFeedback(TEXT("NODE_BACKPACK: need equip first"), FColor::Yellow);
		return false;
	}

	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_BACKPACK: inventory failed - no InventorySubsystem"));
		return false;
	}

	UE_LOG(LogTemp, Log,
		TEXT("NODE_BACKPACK: inventory gated open TOD_DAY FORM_BODY (slots=%d total=%d; not inventory-lite alone; not PROXY SM_ProxyBackpack)"),
		Inv->GetSlotCount(), Inv->GetTotalPhysicalGoods());
	for (int32 Si = 0; Si < Inv->GetSlotCount(); ++Si)
	{
		const FHomeWorldInventorySlot Slot = Inv->GetSlot(Si);
		if (Slot.IsEmpty())
		{
			UE_LOG(LogTemp, Log, TEXT("INVENTORY: slot[%d]=empty"), Si);
		}
		else
		{
			UE_LOG(LogTemp, Log, TEXT("INVENTORY: slot[%d]=%s x%d"), Si, *Slot.ResId.ToString(), Slot.Count);
		}
	}
	ShowInteractFeedback(TEXT("NODE_BACKPACK: inventory open (gated)"), FColor::Green);
	return true;
}


bool AHomeWorldCharacter::TryCollectNodeFieldGather()
{
	// T0_M6 NODE_FIELD_GATHER / TOD_DAY / FORM_BODY / CAM_T0_FIELD
	// Architecture Trade-Offs A-E: prefer existing inventory RES_HERB / RES_SEED
	// -- no parallel gather service, no new schema, no invent gather/WP APIs.
	// Anti closed_fail: dress-only != beat; GP_Store alone != NODE_FIELD_GATHER;
	// PROXY SM_ProxyFieldGather alone != world beat; NODE_PLANT_SLOT (#3) != field gather;
	// ungated hw.Gather.Flowers alone != this named beat. Glide (#5) cite only.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_FIELD_GATHER: collect skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_FIELD_GATHER: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_FIELD_GATHER: collect skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_FIELD_GATHER: body form only"), FColor::Yellow);
		return false;
	}

	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_FIELD_GATHER: collect failed - no InventorySubsystem"));
		return false;
	}

	if (bFieldGatherCollected)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_FIELD_GATHER: field collect TOD_DAY FORM_BODY CAM_T0_FIELD (already collected; RES_HERB/RES_SEED via inventory; not dress/GP_Store/PROXY SM_ProxyFieldGather; not NODE_PLANT_SLOT; not ungated Gather.Flowers)"));
		ShowInteractFeedback(TEXT("NODE_FIELD_GATHER: already collected"), FColor::Green);
		return true;
	}

	const bool bHerb = Inv->TryAddResource(HomeWorldInventory::RES_HERB, 1);
	const bool bSeed = Inv->TryAddResource(HomeWorldInventory::RES_SEED, 1);
	if (!bHerb && !bSeed)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_FIELD_GATHER: collect failed - inventory full (need RES_HERB/RES_SEED path)"));
		ShowInteractFeedback(TEXT("NODE_FIELD_GATHER: inventory full"), FColor::Yellow);
		return false;
	}

	bFieldGatherCollected = true;
	UE_LOG(LogTemp, Log,
		TEXT("NODE_FIELD_GATHER: field collect TOD_DAY FORM_BODY CAM_T0_FIELD (RES_HERB+%d RES_SEED+%d; not dress/GP_Store alone; not PROXY SM_ProxyFieldGather; not NODE_PLANT_SLOT; not ungated Gather.Flowers; glide #5 cite only)"),
		bHerb ? 1 : 0, bSeed ? 1 : 0);
	ShowInteractFeedback(TEXT("NODE_FIELD_GATHER: field collect herb/seed"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryNodeFieldGatherInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName FieldGatherTags[] = {
		FName(TEXT("NODE_FIELD_GATHER")),
		FName(TEXT("FieldGather")),
	};
	bool bIsFieldGather = false;
	for (const FName& Tag : FieldGatherTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsFieldGather = true;
			break;
		}
	}
	if (!bIsFieldGather)
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyFieldGather / dress / GP_Store alone without collect latch = closed_fail.
	return TryCollectNodeFieldGather();
}

bool AHomeWorldCharacter::TryUnlockNodeRune()
{
	// T0_M7 NODE_RUNE / TOD_DAY / FORM_BODY
	// Architecture Trade-Offs A-E: prefer existing SetRuneGateUnlocked / bRuneGateUnlocked /
	// CanEnterSpiritForm -- no parallel form service, no invent WP/form APIs (Arch B).
	// Anti closed_fail: PROXY SM_ProxyRune alone != world unlock; spirit on phase alone != beat;
	// bed->spirit without unlock = closed_fail (#11 HOLD until unlock). #11 / #9 DEFER.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_RUNE: unlock skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_RUNE: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_RUNE: unlock skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_RUNE: body form only"), FColor::Yellow);
		return false;
	}

	if (bRuneGateUnlocked)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_RUNE: unlock TOD_DAY FORM_BODY (already unlocked; SetRuneGateUnlocked latch; not PROXY SM_ProxyRune; not spirit on phase alone; bed->spirit without unlock = closed_fail)"));
		ShowInteractFeedback(TEXT("NODE_RUNE: already unlocked"), FColor::Green);
		return true;
	}

	SetRuneGateUnlocked(true);
	UE_LOG(LogTemp, Log,
		TEXT("NODE_RUNE: unlock TOD_DAY FORM_BODY (SetRuneGateUnlocked; not PROXY SM_ProxyRune alone; not spirit on phase alone; bed->spirit without unlock = closed_fail; #11 HOLD until unlock)"));
	ShowInteractFeedback(TEXT("NODE_RUNE: unlocked"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryNodeRuneInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName RuneTags[] = {
		FName(TEXT("NODE_RUNE")),
		FName(TEXT("Rune")),
	};
	bool bIsRune = false;
	for (const FName& Tag : RuneTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsRune = true;
			break;
		}
	}
	if (!bIsRune)
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyRune alone without unlock latch = closed_fail.
	return TryUnlockNodeRune();
}

bool AHomeWorldCharacter::TryEjectNodeDayCamp()
{
	// T0_M8 NODE_DAY_CAMP / EJECT_HOME / TOD_DAY / FORM_BODY / CAM_T0_CAMP_DAY
	// Architecture Trade-Offs A-E: prefer existing FallbackGlideComponent::StartGlideHome
	// (reverse CRUMB toward home) -- no parallel eject service (Arch B).
	// Anti closed_fail: script-only GP_RS_HumanoidCamp* != world camp; PROXY SM_ProxyDayCamp != beat;
	// island->planet FALLBACK StartGlide alone != EJECT_HOME; convert stub != eject.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_DAY_CAMP: eject skipped - need TOD_DAY"));
		ShowInteractFeedback(TEXT("NODE_DAY_CAMP: day only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_DAY_CAMP: eject skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_DAY_CAMP: body form only"), FColor::Yellow);
		return false;
	}

	if (bDayCampEjectTriggered)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_DAY_CAMP: EJECT_HOME TOD_DAY FORM_BODY CAM_T0_CAMP_DAY (already ejected; StartGlideHome reverse CRUMB; not FALLBACK down; not PROXY SM_ProxyDayCamp; not GP_RS_HumanoidCamp* script-only; not convert stub)"));
		ShowInteractFeedback(TEXT("NODE_DAY_CAMP: already ejected"), FColor::Green);
		return true;
	}

	bool bGlideStarted = false;
	if (FallbackGlideComponent)
	{
		bGlideStarted = FallbackGlideComponent->StartGlideHome();
	}

	bDayCampEjectTriggered = true;
	if (bGlideStarted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_DAY_CAMP: EJECT_HOME TOD_DAY FORM_BODY CAM_T0_CAMP_DAY (StartGlideHome launch→glider→home; reverse CRUMB; not FALLBACK island→planet alone; not PROXY SM_ProxyDayCamp; not GP_RS_HumanoidCamp* script-only; not convert stub)"));
		ShowInteractFeedback(TEXT("NODE_DAY_CAMP: EJECT_HOME glide"), FColor::Green);
	}
	else
	{
		// Soft path: latch + prove labels still fire when crumbs absent (console prove without map bake).
		// Prefer glide when present; do not invent parallel eject service.
		UE_LOG(LogTemp, Log,
			TEXT("NODE_DAY_CAMP: EJECT_HOME TOD_DAY FORM_BODY CAM_T0_CAMP_DAY (eject latch; StartGlideHome pending crumbs/soft; not FALLBACK island→planet alone; not PROXY SM_ProxyDayCamp; not GP_RS_HumanoidCamp* script-only; not convert stub)"));
		ShowInteractFeedback(TEXT("NODE_DAY_CAMP: EJECT_HOME latch"), FColor::Green);
	}
	return true;
}

bool AHomeWorldCharacter::TryNodeDayCampInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitActor)
	{
		return false;
	}

	static const FName DayCampTags[] = {
		FName(TEXT("NODE_DAY_CAMP")),
		FName(TEXT("DayCamp")),
	};
	bool bIsDayCamp = false;
	for (const FName& Tag : DayCampTags)
	{
		if (HitActor->ActorHasTag(Tag))
		{
			bIsDayCamp = true;
			break;
		}
	}
	if (!bIsDayCamp)
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyDayCamp alone without eject latch = closed_fail.
	return TryEjectNodeDayCamp();
}

bool AHomeWorldCharacter::TryBootPlanetsideNightHome()
{
	// T0_M10 EJECT_HOME / TOD_NIGHT_HOME / FORM_BODY / NODE_GLIDER
	// Architecture Trade-Offs A-E: prefer existing FallbackGlideComponent::StartGlideHome
	// (reverse CRUMB planet->home, bAllowNightPhase) -- no parallel eject service (Arch B).
	// Distinct from MUST #8 TryEjectNodeDayCamp / hw.DayCamp.Eject (day-camp cartoon).
	// Anti closed_fail: FALLBACK-down TryStartFallbackGlide/StartGlide != boot;
	// soft-kidnap != boot; scoring #8 day-camp as #10 = closed_fail.
	// Cite #9 TOD_NIGHT_HOME law (w/o bed stay FORM_BODY) -- do not re-Act #9 / do not grant spirit.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GLIDER: planetside boot skipped - need TOD_NIGHT_HOME (Night)"));
		ShowInteractFeedback(TEXT("NODE_GLIDER: night only"), FColor::Yellow);
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GLIDER: planetside boot skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("NODE_GLIDER: body form only"), FColor::Yellow);
		return false;
	}

	if (bPlanetsideNightBootTriggered)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_GLIDER: EJECT_HOME TOD_NIGHT_HOME FORM_BODY (already booted; StartGlideHome reverse planet->home; not day-camp #8; not FALLBACK down; not soft-kidnap)"));
		ShowInteractFeedback(TEXT("NODE_GLIDER: already booted"), FColor::Green);
		return true;
	}

	bool bGlideStarted = false;
	if (FallbackGlideComponent)
	{
		// Night allow: #10 planetside night context (not #8 day-only default).
		bGlideStarted = FallbackGlideComponent->StartGlideHome(/*bAllowNightPhase=*/true);
	}

	bPlanetsideNightBootTriggered = true;
	if (bGlideStarted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_GLIDER: EJECT_HOME TOD_NIGHT_HOME FORM_BODY (StartGlideHome planetside night boot home; reverse CRUMB planet->home; not day-camp #8 TryEjectNodeDayCamp; not FALLBACK island->planet; not soft-kidnap)"));
		ShowInteractFeedback(TEXT("NODE_GLIDER: EJECT_HOME boot"), FColor::Green);
	}
	else
	{
		// Soft path: latch + prove labels still fire when crumbs absent (console prove without map bake).
		// Prefer glide when present; do not invent parallel eject service.
		UE_LOG(LogTemp, Log,
			TEXT("NODE_GLIDER: EJECT_HOME TOD_NIGHT_HOME FORM_BODY (boot latch; StartGlideHome pending crumbs/soft; not day-camp #8; not FALLBACK island->planet; not soft-kidnap)"));
		ShowInteractFeedback(TEXT("NODE_GLIDER: EJECT_HOME latch"), FColor::Green);
	}
	return true;
}

bool AHomeWorldCharacter::TryBedSleepSpirit()
{
	// T0_M11 NODE_BED / TOD_NIGHT_SPIRIT / FORM_SPIRIT / CAM_T0_BED / NODE_RUNE
	// Architecture Trade-Offs A-E: prefer existing GrantSpiritSleepGate / CanEnterSpiritForm /
	// ApplyFormForPhase -- no parallel form service, no invent WP/form APIs (Arch B).
	// Anti closed_fail: phase-only spirit; spirit w/o bed+rune; soft-kidnap != bed.
	// #9 Night@home w/o bed stay FORM_BODY -- do not break (cite only).
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_BED: sleep-spirit skipped - TimeOfDay missing"));
		return false;
	}

	if (!bRuneGateUnlocked)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: sleep-spirit skipped - need NODE_RUNE first (hw.Rune.Unlock); bed->spirit without unlock = closed_fail"));
		ShowInteractFeedback(TEXT("NODE_BED: unlock rune first"), FColor::Yellow);
		return false;
	}

	if (bBedSpiritGranted && bIsSpiritForm && bSpiritSleepGateGranted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_BED NODE_RUNE (already granted; GrantSpiritSleepGate latch; not phase-alone; not soft-kidnap; #9 w/o bed stay FORM_BODY)"));
		ShowInteractFeedback(TEXT("NODE_BED: already spirit"), FColor::Green);
		return true;
	}

	// Night then sleep gate -- SyncFormVia GrantSpiritSleepGate applies FORM_SPIRIT when CanEnterSpiritForm.
	if (!TimeOfDay->GetIsNight())
	{
		TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	}
	GrantSpiritSleepGate();

	bBedSpiritGranted = true;
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_BED NODE_RUNE (GrantSpiritSleepGate + CanEnterSpiritForm; not phase-alone; not soft-kidnap; #9 w/o bed stay FORM_BODY)"));
		ShowInteractFeedback(TEXT("NODE_BED: FORM_SPIRIT"), FColor::Green);
		return true;
	}

	UE_LOG(LogTemp, Log,
		TEXT("NODE_BED: sleep gate granted but FORM_BODY (unexpected; need Night + NODE_RUNE; not phase-alone spirit)"));
	ShowInteractFeedback(TEXT("NODE_BED: sleep gate only"), FColor::Yellow);
	return false;
}

void AHomeWorldCharacter::SyncFormWithTimeOfDay()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		return;
	}
	ApplyFormForPhase(TimeOfDay->GetCurrentPhase());
}

void AHomeWorldCharacter::OnTimeOfDayPhaseChanged(EHomeWorldTimeOfDayPhase NewPhase)
{
	ApplyFormForPhase(NewPhase);
	// T0 #1: Day entry (not Dawn/bed->AdvanceToDawn alone) can emit NODE_WAKE start-day beat.
	TryEmitNodeWakeStartDayBeat();
	// T0 #2: tea sprint gate is Day-scoped (~half day within TOD_DAY).
	if (NewPhase != EHomeWorldTimeOfDayPhase::Day && TeaSprintEndWorldTime > 0.f)
	{
		TeaSprintEndWorldTime = 0.f;
		if (TraversalComponent)
		{
			TraversalComponent->SetSprintHeld(false);
		}
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: tea sprint gate cleared (left TOD_DAY)"));
	}
}


bool AHomeWorldCharacter::CanEnterSpiritForm() const
{
	// Named gates only (Architecture B): hide phase auto-spirit. #7 rune + #11 sleep.
	return bSpiritSleepGateGranted && bRuneGateUnlocked;
}

bool AHomeWorldCharacter::AreDayBodyAbilitiesAllowed() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return true;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		return true;
	}
	const EHomeWorldTimeOfDayPhase Phase = TimeOfDay->GetCurrentPhase();
	// Day verbs off at Dusk/Night (T0 TOD_NIGHT_HOME) — Night remains active; form stays body without gates.
	return Phase == EHomeWorldTimeOfDayPhase::Day || Phase == EHomeWorldTimeOfDayPhase::Dawn;
}

void AHomeWorldCharacter::SetRuneGateUnlocked(bool bUnlocked)
{
	if (bRuneGateUnlocked == bUnlocked)
	{
		return;
	}
	bRuneGateUnlocked = bUnlocked;
	UE_LOG(LogTemp, Log, TEXT("FORM: rune gate %s"), bUnlocked ? TEXT("unlocked") : TEXT("locked"));
	SyncFormWithTimeOfDay();
}

void AHomeWorldCharacter::GrantSpiritSleepGate()
{
	bSpiritSleepGateGranted = true;
	UE_LOG(LogTemp, Log, TEXT("FORM: sleep gate granted (NODE_BED path; spirit still needs rune gate)"));
	SyncFormWithTimeOfDay();
}

void AHomeWorldCharacter::ClearSpiritSleepGate()
{
	if (!bSpiritSleepGateGranted)
	{
		return;
	}
	bSpiritSleepGateGranted = false;
	UE_LOG(LogTemp, Log, TEXT("FORM: sleep gate cleared"));
}

void AHomeWorldCharacter::ApplyFormForPhase(EHomeWorldTimeOfDayPhase Phase)
{
	const bool bSpiritCapablePhase =
		(Phase == EHomeWorldTimeOfDayPhase::Night || Phase == EHomeWorldTimeOfDayPhase::Dusk);

	if (!bSpiritCapablePhase)
	{
		ClearSpiritSleepGate();
	}

	// T0 #9 TOD_NIGHT_HOME: Night/Dusk without named gates → FORM_BODY (no auto-spirit).
	const bool bSpirit = bSpiritCapablePhase && CanEnterSpiritForm();

	if (Phase == LastAppliedFormPhase && bIsSpiritForm == bSpirit)
	{
		return;
	}
	LastAppliedFormPhase = Phase;

	if (bIsSpiritForm == bSpirit)
	{
		return;
	}
	bIsSpiritForm = bSpirit;

	static const TCHAR* PhaseNames[] = { TEXT("Day"), TEXT("Dusk"), TEXT("Night"), TEXT("Dawn") };
	const int32 PhaseIdx = FMath::Clamp(static_cast<int32>(Phase), 0, 3);
	const TCHAR* FormLabel = bSpirit ? TEXT("spirit") : TEXT("body");
	UE_LOG(LogTemp, Log, TEXT("FORM: %s form (phase=%s; gates sleep=%d rune=%d; NightMix driven by TimeOfDaySubsystem)"),
		FormLabel, PhaseNames[PhaseIdx], bSpiritSleepGateGranted ? 1 : 0, bRuneGateUnlocked ? 1 : 0);

	if (TraversalComponent)
	{
		TraversalComponent->ApplyFormMovementTuning(bSpirit);
	}

	PlaySoftFormSwapFeedback(Phase, bSpirit);
}

void AHomeWorldCharacter::PlaySoftFormSwapFeedback(EHomeWorldTimeOfDayPhase Phase, bool bSpirit)
{
	static const TCHAR* PhaseNames[] = { TEXT("Day"), TEXT("Dusk"), TEXT("Night"), TEXT("Dawn") };
	const int32 PhaseIdx = FMath::Clamp(static_cast<int32>(Phase), 0, 3);
	const TCHAR* FormLabel = bSpirit ? TEXT("spirit") : TEXT("body");

	UE_LOG(LogTemp, Log, TEXT("NF2: soft_feedback form=%s phase=%s sound=%s particles=%s"),
		FormLabel,
		PhaseNames[PhaseIdx],
		SoftFormSwapSound ? TEXT("yes") : TEXT("none"),
		SoftFormSwapParticles ? TEXT("yes") : TEXT("none"));

	const FVector Loc = GetActorLocation();

	if (SoftFormSwapSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, SoftFormSwapSound, Loc);
	}
	if (SoftFormSwapParticles)
	{
		UGameplayStatics::SpawnEmitterAtLocation(GetWorld(), SoftFormSwapParticles, Loc);
	}

	// Handmade soft glow pulse — warm amber for body, cool moonlight for spirit (art bible).
	UPointLightComponent* Glow = NewObject<UPointLightComponent>(this, TEXT("NF2SoftFormGlow"));
	if (!Glow)
	{
		return;
	}
	Glow->SetupAttachment(GetRootComponent());
	Glow->RegisterComponent();
	Glow->SetMobility(EComponentMobility::Movable);
	Glow->SetIntensity(bSpirit ? 600.f : 900.f);
	Glow->SetAttenuationRadius(350.f);
	Glow->SetCastShadows(false);
	if (bSpirit)
	{
		Glow->SetLightColor(FLinearColor(0.55f, 0.65f, 0.95f));
	}
	else
	{
		Glow->SetLightColor(FLinearColor(1.0f, 0.72f, 0.35f));
	}

	TWeakObjectPtr<UPointLightComponent> WeakGlow(Glow);
	FTimerHandle FadeHandle;
	if (UWorld* World = GetWorld())
	{
		World->GetTimerManager().SetTimer(
			FadeHandle,
			FTimerDelegate::CreateLambda([WeakGlow]()
			{
				if (UPointLightComponent* Light = WeakGlow.Get())
				{
					Light->DestroyComponent();
				}
			}),
			0.55f,
			false);
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

void AHomeWorldCharacter::ShowInteractFeedback(const FString& Message, FColor Color) const
{
	UE_LOG(LogTemp, Log, TEXT("INTERACT: %s"), *Message);
	if (GEngine)
	{
		GEngine->AddOnScreenDebugMessage(-1, 2.5f, Color, Message);
	}
}

bool AHomeWorldCharacter::ActorHasInteractableComponent(const AActor* Actor)
{
	if (!Actor)
	{
		return false;
	}
	if (Cast<AHomeWorldResourcePile>(Actor))
	{
		return true;
	}
	if (Actor->FindComponentByClass<UHomeWorldBeastTameComponent>()
		|| Actor->FindComponentByClass<UHomeWorldSpiritHealComponent>()
		|| Actor->FindComponentByClass<UHomeWorldNurtureComponent>()
		|| Actor->FindComponentByClass<UHomeWorldStoreTransferComponent>()
		|| Actor->FindComponentByClass<UHomeWorldMinigameInteractComponent>()
		|| Actor->FindComponentByClass<UHomeWorldBossSealComponent>())
	{
		return true;
	}
	if (Cast<AHomeWorldCraftStation>(Actor))
	{
		return true;
	}
	return false;
}

bool AHomeWorldCharacter::FindInteractTargetInCone(FHitResult& OutHit) const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	const float HalfHeight = GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.0f;
	const FVector Start = GetActorLocation() + FVector(0.0f, 0.0f, HalfHeight);
	const FVector Forward = GetControlRotation().Vector();

	static const FName InteractTags[] = {
		FName(TEXT("ResourcePile")),
		FName(TEXT("StoreProp")),
		FName(TEXT("SpiritHeal")),
		FName(TEXT("SpiritWound")),
		FName(TEXT("NurtureTarget")),
		FName(TEXT("BeastPad")),
		FName(TEXT("CraftStation")),
		FName(TEXT("MinigameStub")),
		FName(TEXT("BossSealStub")),
	};

	AActor* BestActor = nullptr;
	float BestScore = -1.f;

	for (const FName& Tag : InteractTags)
	{
		TArray<AActor*> TaggedActors;
		UGameplayStatics::GetAllActorsWithTag(World, Tag, TaggedActors);
		for (AActor* Candidate : TaggedActors)
		{
			if (!ActorHasInteractableComponent(Candidate))
			{
				continue;
			}

			const FVector ToTarget = Candidate->GetActorLocation() - Start;
			const float Dist = ToTarget.Size();
			if (Dist < KINDA_SMALL_NUMBER || Dist > InteractTraceLengthCm)
			{
				continue;
			}

			const float Dot = FVector::DotProduct(Forward, ToTarget / Dist);
			if (Dot < 0.35f)
			{
				continue;
			}

			const float Score = Dot / Dist;
			if (Score > BestScore)
			{
				BestScore = Score;
				BestActor = Candidate;
			}
		}
	}

	if (!BestActor)
	{
		return false;
	}

	const FVector ImpactPoint = BestActor->GetActorLocation();
	OutHit.Reset();
	OutHit.bBlockingHit = true;
	OutHit.Location = ImpactPoint;
	OutHit.ImpactPoint = ImpactPoint;
	OutHit.TraceStart = Start;
	OutHit.TraceEnd = ImpactPoint;
	OutHit.Distance = FVector::Dist(Start, ImpactPoint);
	OutHit.ImpactNormal = -Forward.GetSafeNormal();
	OutHit.Normal = OutHit.ImpactNormal;

	UPrimitiveComponent* PrimComp = Cast<UPrimitiveComponent>(BestActor->GetRootComponent());
	if (!PrimComp)
	{
		PrimComp = BestActor->FindComponentByClass<UPrimitiveComponent>();
	}
	OutHit.HitObjectHandle = FActorInstanceHandle(BestActor);
	if (PrimComp)
	{
		OutHit.Component = PrimComp;
	}
	// Resolve handle so GetActor() works for downstream interact (UE 5.7 lazy handle).
	OutHit.GetActor();
	return true;
}

bool AHomeWorldCharacter::TraceInteractHit(FHitResult& OutHit) const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	const float HalfHeight = GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.0f;
	const FVector Start = GetActorLocation() + FVector(0.0f, 0.0f, HalfHeight);
	const FVector End = Start + GetControlRotation().Vector() * InteractTraceLengthCm;
	FCollisionQueryParams Params(NAME_None, false, this);
	if (World->LineTraceSingleByChannel(OutHit, Start, End, ECC_Visibility, Params))
	{
		if (ActorHasInteractableComponent(GetInteractTargetActor(OutHit)))
		{
			return true;
		}
	}
	return FindInteractTargetInCone(OutHit);
}

AActor* AHomeWorldCharacter::GetInteractTargetActor(const FHitResult& Hit) const
{
	if (AActor* Actor = Hit.GetActor())
	{
		return Actor;
	}
	if (UPrimitiveComponent* Comp = Hit.GetComponent())
	{
		return Comp->GetOwner();
	}
	return nullptr;
}

FString AHomeWorldCharacter::BuildInteractRangeHint(AActor* Target) const
{
	if (!Target)
	{
		return FString();
	}
	if (Target->FindComponentByClass<UHomeWorldBeastTameComponent>())
	{
		return TEXT("[E] Tame beast");
	}
	if (Target->FindComponentByClass<UHomeWorldSpiritHealComponent>())
	{
		return TEXT("[E] Heal spirit");
	}
	if (Target->FindComponentByClass<UHomeWorldNurtureComponent>())
	{
		return TEXT("[E] Nurture crop/store");
	}
	if (Target->FindComponentByClass<UHomeWorldStoreTransferComponent>())
	{
		return TEXT("[E] Store transfer");
	}
	if (Cast<AHomeWorldResourcePile>(Target))
	{
		return TEXT("[E] Gather resource");
	}
	return FString();
}

void AHomeWorldCharacter::UpdateInteractRangeHint(float DeltaTime)
{
	if (!IsPlayerControlled())
	{
		return;
	}

	InteractHintAccumulator += DeltaTime;
	if (InteractHintAccumulator < InteractHintRefreshSeconds)
	{
		return;
	}
	InteractHintAccumulator = 0.f;

	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return;
	}

	const FString Hint = BuildInteractRangeHint(GetInteractTargetActor(Hit));
	if (!Hint.IsEmpty())
	{
		ShowInteractFeedback(Hint, FColor::Cyan);
	}
}
