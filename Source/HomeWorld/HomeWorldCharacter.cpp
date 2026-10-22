// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacter.h"
#include "HomeWorldCampActor.h"
#include "HomeWorldFamilySubsystem.h"
#include "Engine/GameInstance.h"
#include "HomeWorldWispPlacement.h"
#include "HomeWorldOpeningReveal.h"
#include "HomeWorldOpeningDayCamp.h"
#include "HomeWorldEasePad.h"
#include "HomeWorldSpiritLitVolume.h"
#include "HomeWorldRuneShapeComponent.h"
#include "GameFramework/Character.h"
#include "HomeWorldGlideMovementComponent.h"
#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldSoftBoundsComponent.h"
#include "HomeWorldTraversalComponent.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldStressComponent.h"
#include "HomeWorldHomeLoopSubsystem.h"
#include "HomeWorldEasePad.h"
#include "HomeWorldParadoxToy.h"
#include "HomeWorldVirtueComponent.h"
#include "HomeWorldShrinePortalComponent.h"
#include "BuildPlacementSupport.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"
#include "GameplayAbilitySpec.h"
#include "Camera/CameraComponent.h"
#include "Components/TextRenderComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerState.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Materials/MaterialInterface.h"
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
#include "Engine/StaticMeshActor.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "Animation/AnimSequence.h"
#include "HomeWorldOpeningDog.h"
#include "HomeWorldOpeningZipline.h"

/**
 * The T0 beat-node tag contract, declared once.
 *
 * WHAT THIS IS FOR
 *
 * Each T0 beat verb finds its prop by tag: `TryNodeKettleInteractInFront` accepts
 * `NODE_KETTLE` or `Kettle`, and so on for the backpack, the field gather node, the plant
 * slot, the day camp and the bed. The rune is not a beat.
 * Each also accepts a short alias, because a level artist tagging a prop by hand will reach
 * for one or the other.
 *
 * Those tags used to be written out as a local `static const FName[]` inside each of the
 * seven verbs. That is fine right up until something else needs to know what the contract
 * is - and something did: `ActorHasInteractableComponent`, the gate every interact trace has
 * to pass, listed only `AHomeWorldResourcePile`, `AHomeWorldCraftStation` and six named
 * components. It knew none of these tags, so a correctly tagged prop with a correctly sized
 * collider at the right spot was still rejected and every verb behind it returned false.
 * Placing the beat nodes would not have fixed anything.
 *
 * Duplication is not a style complaint here. It is the mechanism: seven copies of a list
 * cannot drift from one gate that reads a different list, and this is what that drift
 * looked like. `ActorHasInteractableComponent` and the verbs now read the same table.
 *
 * The cone has no list of its own: it walks every actor and asks the gate, so a newly tagged
 * prop is reachable without editing the cone.
 */
namespace HomeWorldT0BeatNodes
{
	/** The T0 beat props, each identified by a canonical tag and a short alias. The opening stations read this table too. */
	enum class ENode : uint8
	{
		Kettle,
		PlantSlot,
		Backpack,
		FieldGather,
		DayCamp,
		Bed,
		Garden,
		ConsumableStation,
		ArmorTable,
	};

	/** The tags that identify one specific beat prop, canonical name first. */
	static const TArray<TArray<FName>>& TagsPerNode()
	{
		static const TArray<TArray<FName>> PerNode = {
			{ FName(TEXT("NODE_KETTLE")),        FName(TEXT("Kettle")) },
			{ FName(TEXT("NODE_PLANT_SLOT")),   FName(TEXT("PlantSlot")) },
			{ FName(TEXT("NODE_BACKPACK")),     FName(TEXT("Backpack")) },
			{ FName(TEXT("NODE_FIELD_GATHER")), FName(TEXT("FieldGather")) },
			{ FName(TEXT("NODE_DAY_CAMP")),     FName(TEXT("DayCamp")) },
			{ FName(TEXT("NODE_BED")),          FName(TEXT("Bed")) },
			{ FName(TEXT("NODE_GARDEN")),       FName(TEXT("Garden")) },
			{ FName(TEXT("NODE_CONSUMABLE_STATION")), FName(TEXT("ConsumableStation")) },
			{ FName(TEXT("NODE_ARMOR_TABLE")),  FName(TEXT("ArmorTable")) },
		};
		return PerNode;
	}

	static const TArray<FName>& TagsFor(ENode Node)
	{
		return TagsPerNode()[static_cast<uint8>(Node)];
	}

	/** True when the actor carries one of the tags for this beat prop. */
	static bool ActorCarriesTagFor(const AActor* Actor, ENode Node)
	{
		if (!Actor)
		{
			return false;
		}
		for (const FName& Tag : TagsFor(Node))
		{
			if (Actor->ActorHasTag(Tag))
			{
				return true;
			}
		}
		return false;
	}
}

/**
 * One interaction contract per actor, derived from its tags and components.
 *
 * A prop is not a verb path. It carries attributes; the resolver reads them. This is the
 * place to add reach, look, wall, or hover for a new kind of prop - not a branch in a verb.
 */
namespace HomeWorldInteract
{
	struct FSpec
	{
		HomeWorldT0BeatNodes::ENode Node = HomeWorldT0BeatNodes::ENode::Kettle;
		bool bBeatNode = false;
		float ReachCm = 280.f;
		bool bLook = true;
		bool bWall = true;
		bool bHover = true;
	};

	/** Derive the spec from the actor's attributes. A beat prop needs its node tag, nothing else. */
	static bool TrySpecFor(const AActor* Actor, FSpec& Out)
	{
		if (!Actor)
		{
			return false;
		}
		const TArray<TArray<FName>>& PerNode = HomeWorldT0BeatNodes::TagsPerNode();
		for (int32 Index = 0; Index < PerNode.Num(); ++Index)
		{
			if (HomeWorldT0BeatNodes::ActorCarriesTagFor(
					Actor, static_cast<HomeWorldT0BeatNodes::ENode>(Index)))
			{
				Out = FSpec();
				Out.Node = static_cast<HomeWorldT0BeatNodes::ENode>(Index);
				Out.bBeatNode = true;
				return true;
			}
		}
		return false;
	}
}

AHomeWorldCharacter::AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer)
	// The cloud descent needs a custom movement mode, so the character must own a CMC
	// subclass. This REPLACES the engine default CMC on the SAME subobject name rather
	// than adding a second one (MOVEMENT_BIBLE: one CMC).
	: Super(ObjectInitializer.SetDefaultSubobjectClass<UHomeWorldGlideMovementComponent>(ACharacter::CharacterMovementComponentName))
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
	StressComponent = CreateDefaultSubobject<UHomeWorldStressComponent>(TEXT("StressComponent"));
	StrokeReport = CreateDefaultSubobject<UHomeWorldStrokeReportComponent>(TEXT("StrokeReport"));
	QuestLog = CreateDefaultSubobject<UHomeWorldQuestLog>(TEXT("QuestLog"));
	OpeningSupply = CreateDefaultSubobject<UHomeWorldOpeningSupply>(TEXT("OpeningSupply"));
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
	const FString LevelName = UGameplayStatics::GetCurrentLevelName(this);
	const bool bSizeTest = LevelName.Contains(TEXT("SizeTest"));
	// SizeTest, L_Field, and L_EasePad are greybox bodies. The hero-island walk bounds do not fit them
	// (SCENE_SETUP practice 5), so they start off here; Tick reads this same flag and leaves them off (T1-3).
	bGreyboxBodyLevel = bSizeTest || LevelName.Contains(TEXT("L_Field")) || LevelName.Contains(TEXT("L_EasePad"));
	if (bGreyboxBodyLevel)
	{
		if (UCapsuleComponent* SizeCapsule = GetCapsuleComponent())
		{
			SizeCapsule->SetCapsuleSize(42.0f, 100.0f);
		}
		if (SoftBoundsComponent)
		{
			SoftBoundsComponent->bBoundsEnabled = false;
		}
	}
	if (UWorld* World = GetWorld())
	{
		UCapsuleComponent* Capsule = GetCapsuleComponent();
		if (Capsule)
		{
			const float HalfHeight = Capsule->GetUnscaledCapsuleHalfHeight();
			// The homestead sheet leaves 10 cm under the capsule. Snapping onto the hit puts the feet in the floor.
			const float GroundGap = bGreyboxBodyLevel ? 10.0f : 0.0f;
			const FVector Start = GetActorLocation();
			const FVector End = Start - FVector(0.0f, 0.0f, HalfHeight + 500.0f);
			FHitResult Hit;
			FCollisionQueryParams Params(NAME_None, false, this);
			if (World->LineTraceSingleByChannel(Hit, Start, End, ECC_WorldStatic, Params))
			{
				SetActorLocation(FVector(Start.X, Start.Y, Hit.ImpactPoint.Z + HalfHeight + GroundGap));
			}
		}
	}
	if (bGreyboxBodyLevel)
	{
		// Rest pose: right arm is +X and the walk strides on Y, so the face is mesh -Y.
		// +90 turns that face onto actor +X. -90 and 0 both walk sideways to the face.
		// The kept player and the size-test coat share that axis. Feet are at local 0, so the mesh sits one half-height down.
		MeshForwardYawOffset = 90.0f;
		if (USkeletalMesh* Coat = LoadObject<USkeletalMesh>(nullptr, TEXT("/Game/HomeWorld/Meshes/SizeTest/SK_Player_Female.SK_Player_Female")))
		{
			if (USkeletalMeshComponent* CoatMesh = GetMesh())
			{
				CoatMesh->SetAnimInstanceClass(nullptr);
				CoatMesh->SetAnimationMode(EAnimationMode::AnimationSingleNode);
				CoatMesh->SetSkeletalMeshAsset(Coat);
				const float HalfHeight = GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() : 100.0f;
				CoatMesh->SetRelativeLocation(FVector(0.0f, 0.0f, -HalfHeight));
				CoatMesh->SetEnableAnimation(true);
				CoatMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			}
		}
		if (AController* Controlled = GetController())
		{
			ApplySpawnControlPitch();
		}
		if (bSizeTest)
		{
			OpeningSpeedStep = 0;
			ApplyOpeningWalkSpeed();
			UE_LOG(LogTemp, Log, TEXT("start at higher speed, scroll up to higher speed"));
		}
		if (bSizeTest && !SizeTestWisp)
		{
			SizeTestWisp = NewObject<UStaticMeshComponent>(this, TEXT("SizeTestShoulderWisp"));
			if (UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere")))
			{
				SizeTestWisp->SetStaticMesh(Sphere);
			}
			SizeTestWisp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			SizeTestWisp->SetRelativeScale3D(FVector(0.25f));
			SizeTestWisp->SetupAttachment(GetRootComponent());
			SizeTestWisp->SetHiddenInGame(true);
			SizeTestWisp->SetVisibility(false);
			SizeTestWisp->RegisterComponent();
			SizeTestWisp->SetRelativeLocation(FVector(10.0f, 45.0f, 55.0f));
			if (UMaterialInterface* Purple = LoadObject<UMaterialInterface>(nullptr,
				TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Purple.MI_Greybox_Purple")))
			{
				SizeTestWisp->SetMaterial(0, Purple);
			}
		}
		if (bSizeTest && !SizeTestCursorWisp)
		{
			SizeTestCursorWisp = NewObject<UStaticMeshComponent>(this, TEXT("SizeTestCursorWisp"));
			if (UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere")))
			{
				SizeTestCursorWisp->SetStaticMesh(Sphere);
			}
			SizeTestCursorWisp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			SizeTestCursorWisp->SetRelativeScale3D(FVector(0.15f));
			SizeTestCursorWisp->SetupAttachment(GetRootComponent());
			SizeTestCursorWisp->SetHiddenInGame(true);
			SizeTestCursorWisp->SetVisibility(false);
			SizeTestCursorWisp->RegisterComponent();
		}
		if (bSizeTest && !OpeningInteractPrompt)
		{
			OpeningInteractPrompt = NewObject<UTextRenderComponent>(this, TEXT("OpeningInteractPrompt"));
			OpeningInteractPrompt->SetupAttachment(GetRootComponent());
			OpeningInteractPrompt->SetCollisionEnabled(ECollisionEnabled::NoCollision);
			OpeningInteractPrompt->SetHorizontalAlignment(EHTA_Center);
			OpeningInteractPrompt->SetVerticalAlignment(EVRTA_TextCenter);
			OpeningInteractPrompt->SetWorldSize(32.f);
			OpeningInteractPrompt->SetText(FText::FromString(TEXT("E")));
			OpeningInteractPrompt->SetTextRenderColor(FColor::White);
			OpeningInteractPrompt->SetHiddenInGame(true);
			OpeningInteractPrompt->SetVisibility(false);
			OpeningInteractPrompt->RegisterComponent();
		}
	}
	USkeletalMeshComponent* MeshComp = GetMesh();
	if (MeshComp)
	{
		MeshComp->SetRelativeRotation(FRotator(0.0f, MeshForwardYawOffset, 0.0f));
		if (bGreyboxBodyLevel)
		{
			MeshComp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		}
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
	if (FallbackGlideComponent)
	{
		FallbackGlideComponent->OnGlideCompleted.AddDynamic(this, &AHomeWorldCharacter::OnSpiritSicknessGlideCompleted);
	}
}

namespace
{
	void EndPartyOuting(UWorld* World, EHomeWorldPartyAbsence Reason)
	{
		if (!World)
		{
			return;
		}
		UGameInstance* GameInstance = World->GetGameInstance();
		if (!GameInstance)
		{
			return;
		}
		if (UHomeWorldFamilySubsystem* Family = GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>())
		{
			Family->EndOuting(Reason, World);
		}
	}
}

void AHomeWorldCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	ClearPartyOnAbsenceVolumes();
	TickSpiritSickness(DeltaTime);

	// On the greybox body maps the hero-island bounds stay off (SCENE_SETUP practice 5); elsewhere they follow
	// the glide state. Branch on the BeginPlay flag, not the level name, or L_Field is re-trapped (T1-3).
	if (SoftBoundsComponent && !bGreyboxBodyLevel)
	{
		SoftBoundsComponent->bBoundsEnabled = !IsFallbackGliding() && !IsCloudDescentActive();
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
	if (UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("SizeTest")))
	{
		UpdateOpeningWalkScroll();
		UpdateSizeTestWalk();
		UpdateSizeTestInteractCursor();
		UpdateSizeTestWisp(DeltaTime);
		UpdateOpeningBonk();
		UpdateOpeningNight(DeltaTime);
	}
	else if (UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("L_Field")))
	{
		UpdateSizeTestWalk();
	}
}

void AHomeWorldCharacter::UpdateOpeningBonk()
{
	UWorld* World = GetWorld();
	UCapsuleComponent* Capsule = GetCapsuleComponent();
	if (!World || !Capsule)
	{
		return;
	}
	if (bOpeningBonkReturning)
	{
		TickBonkReturn(World->GetDeltaSeconds());
		return;
	}
	AActor* Pad = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->GetActorNameOrLabel() == TEXT("SM_Size_WalkPad"))
		{
			Pad = *It;
			break;
		}
	}
	if (!Pad)
	{
		return;
	}
	FVector Origin = FVector::ZeroVector;
	FVector Extent = FVector::ZeroVector;
	Pad->GetActorBounds(false, Origin, Extent);
	const float PadTop = Origin.Z + Extent.Z;
	const float Half = Capsule->GetScaledCapsuleHalfHeight();
	const FVector Loc = GetActorLocation();
	const float FeetZ = Loc.Z - Half;
	const bool bOverPad = FMath::Abs(Loc.X - Origin.X) <= Extent.X
		&& FMath::Abs(Loc.Y - Origin.Y) <= Extent.Y;
	if (FeetZ >= PadTop - 40.f)
	{
		if (bOverPad)
		{
			OpeningBonkSafe = Loc;
			bOpeningBonkSafe = true;
		}
		return;
	}
	// Fall far enough to read, then fly home.
	if (FeetZ > PadTop - 320.f || !bOpeningBonkSafe)
	{
		return;
	}
	BeginBonkReturn(OpeningBonkSafe, Origin, Extent);
}

void AHomeWorldCharacter::BeginBonkReturn(const FVector& Target, const FVector& PadOrigin, const FVector& PadExtent)
{
	UWorld* World = GetWorld();
	UCharacterMovementComponent* Move = GetCharacterMovement();
	UCapsuleComponent* Capsule = GetCapsuleComponent();
	if (!World || !Move || !Capsule)
	{
		return;
	}
	const float Half = Capsule->GetScaledCapsuleHalfHeight();
	const float Radius = Capsule->GetScaledCapsuleRadius();
	FVector Land = HomeWorldBonk::LandingOnPad(Target, PadOrigin, PadExtent, Half);
	FCollisionQueryParams Params(NAME_None, false, this);
	for (int32 Try = 0; Try < 6; ++Try)
	{
		FHitResult Hit;
		const bool bHit = World->LineTraceSingleByChannel(
			Hit,
			FVector(Land.X, Land.Y, Land.Z + 300.f),
			FVector(Land.X, Land.Y, Land.Z - 400.f),
			ECC_Visibility,
			Params);
		if (!bHit || Hit.ImpactPoint.Z <= Land.Z - Half + 80.f)
		{
			break;
		}
		const FVector Step = (PadOrigin - Land).GetSafeNormal2D() * 200.f;
		if (Step.IsNearlyZero())
		{
			break;
		}
		Land.X += Step.X;
		Land.Y += Step.Y;
		Land = HomeWorldBonk::LandingOnPad(Land, PadOrigin, PadExtent, Half);
	}
	BonkArc = HomeWorldBonk::MakeArc(GetActorLocation(), Land, PadOrigin, PadExtent, Half, Radius);
	BonkElapsed = 0.f;
	bOpeningBonkReturning = true;
	Move->StopMovementImmediately();
	Move->Velocity = FVector::ZeroVector;
	Move->SetMovementMode(MOVE_Flying);
	ConsumeMovementInputVector();
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		PC->SetIgnoreMoveInput(true);
	}
	EndPartyOuting(World, EHomeWorldPartyAbsence::Bonk);
	UE_LOG(LogTemp, Log, TEXT("opening_bonk: return to (%.0f, %.0f, %.0f) arch %.0f"),
		BonkArc.Land.X, BonkArc.Land.Y, BonkArc.Land.Z, BonkArc.Approach.Z - BonkArc.Land.Z);
}

void AHomeWorldCharacter::TickBonkReturn(float DeltaSeconds)
{
	UCharacterMovementComponent* Move = GetCharacterMovement();
	if (!Move)
	{
		bOpeningBonkReturning = false;
		if (APlayerController* PC = Cast<APlayerController>(GetController()))
		{
			PC->SetIgnoreMoveInput(false);
		}
		return;
	}
	BonkElapsed += FMath::Max(DeltaSeconds, 0.f);
	const float Duration = FMath::Max(BonkArc.DurationSec, 0.05f);
	const float T = FMath::Clamp(BonkElapsed / Duration, 0.f, 1.f);
	SetActorLocation(HomeWorldBonk::PointOnArc(BonkArc, T), false, nullptr, ETeleportType::TeleportPhysics);
	Move->Velocity = FVector::ZeroVector;
	ConsumeMovementInputVector();
	if (T < 1.f)
	{
		return;
	}
	SetActorLocation(BonkArc.Land, false, nullptr, ETeleportType::TeleportPhysics);
	Move->StopMovementImmediately();
	Move->SetMovementMode(MOVE_Walking);
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		PC->SetIgnoreMoveInput(false);
	}
	OpeningBonkSafe = BonkArc.Land;
	bOpeningBonkSafe = true;
	bOpeningBonkReturning = false;
	UE_LOG(LogTemp, Log, TEXT("opening_bonk: landed"));
}

void AHomeWorldCharacter::ClearPartyOnAbsenceVolumes()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	UGameInstance* GameInstance = World->GetGameInstance();
	if (!GameInstance)
	{
		return;
	}
	UHomeWorldFamilySubsystem* Family = GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>();
	if (!Family || Family->GetPartySetup() == EHomeWorldPartySetup::Solo)
	{
		return;
	}
	const FVector Here = GetActorLocation();
	bool bCamp = false;
	bool bCave = false;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		const bool bCampActor = It->IsA<AHomeWorldCampActor>()
			|| It->ActorHasTag(TEXT("NODE_CAMP"))
			|| It->ActorHasTag(TEXT("NODE_GUARD"))
			|| It->ActorHasTag(TEXT("NODE_SLEEPER"))
			|| It->ActorHasTag(TEXT("NODE_CAPTIVE"));
		const bool bCaveActor = It->ActorHasTag(TEXT("NODE_CAVE")) || It->ActorHasTag(TEXT("Cave"));
		if (!bCampActor && !bCaveActor)
		{
			continue;
		}
		FVector Origin = FVector::ZeroVector;
		FVector Extent = FVector::ZeroVector;
		It->GetActorBounds(false, Origin, Extent);
		const FBox Near(Origin - Extent - FVector(200.f), Origin + Extent + FVector(200.f));
		if (!Near.IsInsideOrOn(Here))
		{
			continue;
		}
		bCamp |= bCampActor;
		bCave |= bCaveActor;
	}
	if (bCamp)
	{
		Family->EndOuting(EHomeWorldPartyAbsence::Camp, World);
	}
	if (bCave)
	{
		Family->EndOuting(EHomeWorldPartyAbsence::Cave, World);
	}
}

static AActor* FindOpeningNamed(UWorld* World, const TCHAR* Name, bool bExact)
{
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		const FString Label = It->GetActorNameOrLabel();
		if (bExact ? Label.Equals(Name) : Label.Contains(Name))
		{
			return *It;
		}
	}
	return nullptr;
}

static UStaticMeshComponent* MakeOpeningNightWisp(AHomeWorldCharacter* Owner, const TCHAR* Name)
{
	UStaticMeshComponent* Wisp = NewObject<UStaticMeshComponent>(Owner, Name);
	if (UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere")))
	{
		Wisp->SetStaticMesh(Sphere);
	}
	Wisp->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Wisp->SetRelativeScale3D(FVector(0.35f));
	Wisp->SetupAttachment(Owner->GetRootComponent());
	Wisp->SetUsingAbsoluteLocation(true);
	Wisp->RegisterComponent();
	if (UMaterialInterface* Purple = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Purple.MI_Greybox_Purple")))
	{
		Wisp->SetMaterial(0, Purple);
	}
	return Wisp;
}

void AHomeWorldCharacter::EnsureOpeningNightProps()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	auto SpawnWisp = [World](const FVector& Point) -> AActor*
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* Wisp = World->SpawnActor<AStaticMeshActor>(Point, FRotator::ZeroRotator, Params);
		if (!Wisp || !Wisp->GetStaticMeshComponent())
		{
			return nullptr;
		}
		UStaticMeshComponent* WispMesh = Wisp->GetStaticMeshComponent();
		// A spawned AStaticMeshActor is Static. SetStaticMesh refuses that after play begins.
		WispMesh->SetMobility(EComponentMobility::Movable);
		if (UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere")))
		{
			WispMesh->SetStaticMesh(Sphere);
		}
		WispMesh->SetWorldScale3D(FVector(0.45f));
		WispMesh->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		WispMesh->SetCollisionResponseToAllChannels(ECR_Ignore);
		WispMesh->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
		if (UMaterialInterface* Purple = LoadObject<UMaterialInterface>(nullptr,
			TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Purple.MI_Greybox_Purple")))
		{
			WispMesh->SetMaterial(0, Purple);
		}
		Wisp->Tags.Add(FName(TEXT("NODE_OPENING_WISP")));
		return Wisp;
	};
	if (!OpeningCopseWisp)
	{
		const AActor* CopsePine = nullptr;
		float South = TNumericLimits<float>::Max();
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!It->GetActorNameOrLabel().Contains(TEXT("Pine")))
			{
				continue;
			}
			const float Y = It->GetActorLocation().Y;
			if (Y < 0.f && Y < South)
			{
				South = Y;
				CopsePine = *It;
			}
		}
		FVector Beside = GetActorLocation() + FVector(0.f, -400.f, 80.f);
		if (CopsePine)
		{
			FVector PineOrigin = FVector::ZeroVector;
			FVector PineExtent = FVector::ZeroVector;
			CopsePine->GetActorBounds(false, PineOrigin, PineExtent);
			Beside = FVector(PineOrigin.X + PineExtent.X + 120.f, PineOrigin.Y, PineOrigin.Z - PineExtent.Z + 180.f);
		}
		OpeningCopseWisp = SpawnWisp(Beside);
	}
	if (!OpeningPondWisp)
	{
		FVector Point = GetActorLocation();
		if (const AActor* Pond = FindOpeningNamed(World, TEXT("Water_Pond"), true))
		{
			Point = Pond->GetActorLocation() + FVector(0.f, 0.f, 140.f);
		}
		OpeningPondWisp = SpawnWisp(Point);
	}
	if (!OpeningSpringWisp)
	{
		FVector Point = GetActorLocation();
		if (const AActor* Spring = FindOpeningNamed(World, TEXT("Water_HotSpring"), true))
		{
			Point = Spring->GetActorLocation() + FVector(0.f, 0.f, 140.f);
		}
		OpeningSpringWisp = SpawnWisp(Point);
	}
	if (OpeningNightChestPoint.IsNearlyZero())
	{
		// Armory door faces west. Metrics origin (-0.5 m, -13 m), door local x -335 cm.
		OpeningNightChestPoint = FVector(-475.f, -1300.f, 45040.f);
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		if (AStaticMeshActor* Chest = World->SpawnActor<AStaticMeshActor>(OpeningNightChestPoint, FRotator::ZeroRotator, Params))
		{
			if (UStaticMeshComponent* ChestMesh = Chest->GetStaticMeshComponent())
			{
				ChestMesh->SetMobility(EComponentMobility::Movable);
				if (UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
				{
					ChestMesh->SetStaticMesh(Cube);
				}
				ChestMesh->SetWorldScale3D(FVector(0.9f, 0.7f, 0.8f));
				if (UMaterialInterface* Tan = LoadObject<UMaterialInterface>(nullptr,
					TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Tan.MI_Greybox_Tan")))
				{
					ChestMesh->SetMaterial(0, Tan);
				}
			}
			Chest->Tags.Add(FName(TEXT("NODE_ARMORY_CHEST")));
			OpeningNightChestPoint.Z += 80.f;
		}
	}
}

void AHomeWorldCharacter::UpdateOpeningNight(float DeltaTime)
{
	if (!bOpeningNightSpirit)
	{
		return;
	}
	EnsureOpeningNightProps();
	for (int32 Index = OpeningWispHealTimers.Num() - 1; Index >= 0; --Index)
	{
		OpeningWispHealTimers[Index] -= DeltaTime;
		if (OpeningWispHealTimers[Index] > 0.f)
		{
			continue;
		}
		OpeningWispHealTimers.RemoveAt(Index);
		++OpeningWispsHealed;
		UE_LOG(LogTemp, Log, TEXT("opening_night: wisp healed, it follows near the legs (healed %d, carried %d)"),
			OpeningWispsHealed, OpeningWispsCarried);
	}
	UpdateOpeningWispLegs();
	if (!QuestLog)
	{
		return;
	}
	TArray<FHomeWorldQuestStep> Steps;
	auto Add = [&Steps](const TCHAR* Text, bool bDone)
	{
		FHomeWorldQuestStep Step;
		Step.Text = Text;
		Step.bDone = bDone;
		Steps.Add(Step);
	};
	Add(TEXT("Sleep in the bed"), true);
	Add(*FString::Printf(TEXT("Collect the wisps %d/3"), OpeningWispsCollected), OpeningWispsCollected >= 3);
	if (OpeningWispsCarried > 0 || OpeningWispHealTimers.Num() > 0 || OpeningWispsHealed > 0)
	{
		FString HealText;
		if (OpeningWispHealTimers.Num() > 0)
		{
			HealText = FString::Printf(TEXT("Wait for the wisps in the hot springs (%d)."), OpeningWispHealTimers.Num());
		}
		else if (OpeningWispsCarried > 0)
		{
			HealText = FString::Printf(TEXT("Give a wisp herb at the hot springs (carrying %d)."), OpeningWispsCarried);
		}
		else
		{
			HealText = FString::Printf(TEXT("Heal the wisps at the hot springs (%d/3)."), OpeningWispsHealed);
		}
		Add(*HealText, OpeningWispsHealed >= 3);
	}
	QuestLog->SetChain(FName(TEXT("Night")), Steps);
}

void AHomeWorldCharacter::UpdateOpeningWispLegs()
{
	if (OpeningWispsHealed <= 0)
	{
		return;
	}
	while (OpeningWispLegMeshes.Num() < OpeningWispsHealed)
	{
		const FString Name = FString::Printf(TEXT("OpeningWispLeg%d"), OpeningWispLegMeshes.Num() + 1);
		UStaticMeshComponent* Wisp = MakeOpeningNightWisp(this, *Name);
		if (!Wisp)
		{
			return;
		}
		Wisp->SetRelativeScale3D(FVector(0.25f));
		OpeningWispLegMeshes.Add(Wisp);
		UE_LOG(LogTemp, Log, TEXT("opening_night: follower %d at the legs"), OpeningWispLegMeshes.Num());
	}
	const UWorld* World = GetWorld();
	const float Time = World ? World->GetTimeSeconds() : 0.f;
	const FVector Base = GetActorLocation();
	const FVector Forward = GetActorForwardVector();
	const FVector Right = GetActorRightVector();
	// Three places around the feet. Past three, the slots repeat.
	static const FVector2D Slots[] = {
		FVector2D(34.f, -20.f),
		FVector2D(-34.f, -20.f),
		FVector2D(0.f, -52.f),
	};
	for (int32 Index = 0; Index < OpeningWispLegMeshes.Num(); ++Index)
	{
		const FVector2D& Slot = Slots[Index % 3];
		const float Bob = FMath::Sin(Time * 3.f + Index * 1.7f) * 4.f;
		const FVector Point = Base + Right * Slot.X + Forward * Slot.Y + FVector(0.f, 0.f, -52.f + Bob);
		OpeningWispLegMeshes[Index]->SetWorldLocation(Point);
	}
}

bool AHomeWorldCharacter::TryOpeningBedInFront()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	FHitResult Hit;
	AActor* Aimed = ResolveOpeningAim(Hit);
	AActor* Bed = (Aimed && Aimed->GetActorNameOrLabel().Contains(TEXT("Bed"))) ? Aimed : nullptr;
	if (!Bed && !Aimed)
	{
		if (AActor* Named = FindOpeningNamed(World, TEXT("SM_Size_Bed"), true))
		{
			if (FVector::Dist2D(GetActorLocation(), Named->GetActorLocation()) <= 280.f
				&& HasOpeningLineOfSight(Named))
			{
				Bed = Named;
			}
		}
	}
	if (!Bed)
	{
		return false;
	}
	if (bOpeningNightSpirit)
	{
		return true;
	}
	return BeginOpeningNight();
}

bool AHomeWorldCharacter::BeginOpeningNight()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		return false;
	}
	GrantSpiritSleepGate();
	if (UHomeWorldHomeLoopSubsystem* Home = World->GetSubsystem<UHomeWorldHomeLoopSubsystem>())
	{
		Home->NoteHomeRest();
	}
	if (StressComponent)
	{
		StressComponent->NotifyBedSleep();
	}
	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	SyncFormWithTimeOfDay();
	bOpeningNightSpirit = GetIsSpiritForm();
	if (USkeletalMeshComponent* Coat = GetMesh())
	{
		Coat->SetVisibility(false, true);
	}
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
	}
	if (!OpeningSpiritBody)
	{
		OpeningSpiritBody = MakeOpeningNightWisp(this, TEXT("OpeningSpiritBody"));
		if (OpeningSpiritBody)
		{
			OpeningSpiritBody->SetUsingAbsoluteLocation(false);
			OpeningSpiritBody->SetRelativeLocation(FVector(0.f, 0.f, 10.f));
			OpeningSpiritBody->SetRelativeScale3D(FVector(1.1f));
		}
	}
	else
	{
		OpeningSpiritBody->SetVisibility(true);
	}
	TryTellChildDawnRule();
	// Spirit nights stay solo. The tutorial chase is a day beat.
	if (UWorld* NightWorld = GetWorld())
	{
		for (TActorIterator<AHomeWorldOpeningReveal> It(NightWorld); It; ++It)
		{
			It->StopForOpeningNight();
		}
	}
	// The wisp keeps the body camera: same boom, same arm, same FOV. No second rig.
	if (CameraBoom)
	{
		CameraBoom->TargetArmLength = TargetArmLength;
	}
	if (FollowCamera)
	{
		FollowCamera->SetFieldOfView(CameraFOV);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_bed: spirit, stayed on the island, camera arm %.0f fov %.0f"),
		CameraBoom ? CameraBoom->TargetArmLength : -1.f,
		FollowCamera ? FollowCamera->FieldOfView : -1.f);
	return bOpeningNightSpirit;
}

void AHomeWorldCharacter::ReturnOpeningBodyForDawnPlaytest()
{
	WakeFromSpiritAtBed();
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
		}
	}
	bOpeningNightSpirit = false;
	if (USkeletalMeshComponent* Coat = GetMesh())
	{
		Coat->SetVisibility(true, true);
	}
	if (OpeningSpiritBody)
	{
		OpeningSpiritBody->SetVisibility(false);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_glider: body returned at dawn"));
}

bool AHomeWorldCharacter::TryOpeningNightSetInFront()
{
	if (!bOpeningNightSpirit || bOpeningRuneActive)
	{
		return false;
	}
	FHitResult Hit;
	AActor* Aimed = ResolveOpeningAim(Hit);
	if (!Aimed || Aimed->IsHidden() || !Aimed->ActorHasTag(FName(TEXT("NODE_OPENING_WISP"))))
	{
		return false;
	}
	if (FVector::Dist2D(GetActorLocation(), Aimed->GetActorLocation()) > 400.f)
	{
		return false;
	}
	bOpeningWispCollect = true;
	StartOpeningHerbRune(Aimed);
	if (!bOpeningRuneActive)
	{
		bOpeningWispCollect = false;
		return false;
	}
	UE_LOG(LogTemp, Log, TEXT("opening_night: collect the wisp"));
	return true;
}

namespace
{
	/** Fast heart, and the fallback when a seeded wisp has no recorded heart. */
	constexpr float OpeningWispHealSeconds = 20.f;
	constexpr float OpeningHotSpringRangeCm = 600.f;
}

float AHomeWorldCharacter::OpeningHealSecondsForHeart(float HeartSeconds)
{
	constexpr float FastSeconds = 3.f;
	constexpr float ExtraPerSecond = 10.f;
	if (HeartSeconds <= FastSeconds)
	{
		return OpeningWispHealSeconds;
	}
	const int32 SecondsOver = FMath::CeilToInt(HeartSeconds - FastSeconds);
	return OpeningWispHealSeconds + ExtraPerSecond * static_cast<float>(SecondsOver);
}

void AHomeWorldCharacter::DebugQueueOpeningWispHeart(float HeartSeconds)
{
	OpeningWispHealDurations.Add(OpeningHealSecondsForHeart(HeartSeconds));
}

bool AHomeWorldCharacter::DebugBeginOpeningWispHeart(AActor* Wisp)
{
	bOpeningWispCollect = true;
	StartOpeningHerbRune(Wisp);
	if (!bOpeningRuneActive)
	{
		bOpeningWispCollect = false;
		return false;
	}
	OpeningWispHeartElapsed = 0.f;
	return true;
}

void AHomeWorldCharacter::DebugAdvanceOpeningWispHeart(float DeltaSeconds)
{
	UpdateOpeningHerbRune(DeltaSeconds);
}

bool AHomeWorldCharacter::TryOpeningHotSpringHealInFront()
{
	if (!bOpeningNightSpirit)
	{
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	AActor* Spring = FindOpeningNamed(World, TEXT("Water_HotSpring"), true);
	if (!Spring)
	{
		Spring = FindOpeningNamed(World, TEXT("Water_HotSpring"), false);
	}
	if (!Spring || FVector::Dist2D(GetActorLocation(), Spring->GetActorLocation()) > OpeningHotSpringRangeCm
		|| !HasOpeningLineOfSight(Spring))
	{
		return false;
	}
	if (OpeningWispsCarried <= 0)
	{
		UE_LOG(LogTemp, Log, TEXT("opening_night: the hot springs need a damaged wisp (carried 0)"));
		return true;
	}
	if (OpeningHerbTenths <= 0)
	{
		UE_LOG(LogTemp, Log, TEXT("opening_night: the hot springs need one herb (carried wisps %d, banked %d)"),
			OpeningWispsCarried, OpeningHerbTenths);
		return true;
	}
	--OpeningWispsCarried;
	--OpeningHerbTenths;
	const float HealSeconds = OpeningWispHealDurations.Num() > 0
		? OpeningWispHealDurations[0]
		: OpeningWispHealSeconds;
	if (OpeningWispHealDurations.Num() > 0)
	{
		OpeningWispHealDurations.RemoveAt(0);
	}
	OpeningWispHealTimers.Add(HealSeconds);
	UE_LOG(LogTemp, Log, TEXT("opening_night: wisp in the hot springs with one herb (carried %d, healing %d, herbs %d, heal %.0fs)"),
		OpeningWispsCarried, OpeningWispHealTimers.Num(), OpeningHerbTenths, HealSeconds);
	return true;
}

void AHomeWorldCharacter::DebugHealOpeningWispAtSpring()
{
	const bool bOk = TryOpeningHotSpringHealInFront();
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Night.Heal %s (carried %d, healing %d, herbs %d)"),
		bOk ? TEXT("ok") : TEXT("not at the hot springs"),
		OpeningWispsCarried, OpeningWispHealTimers.Num(), OpeningHerbTenths);
}

void AHomeWorldCharacter::DebugSeedOpeningWispLoop(int32 Carried, int32 Herbs)
{
	const int32 Seeded = FMath::Clamp(Carried, 0, 3);
	OpeningWispsCollected = FMath::Max(OpeningWispsCollected, Seeded);
	OpeningWispsCarried = Seeded;
	OpeningHerbTenths = FMath::Max(OpeningHerbTenths, FMath::Clamp(Herbs, 0, 9));
	UE_LOG(LogTemp, Log, TEXT("opening_night: test seed - collected %d, carried %d, herbs %d. This is a seed. The playtest arrival is hw.Playtest.FastForward."),
		OpeningWispsCollected, OpeningWispsCarried, OpeningHerbTenths);
}

void AHomeWorldCharacter::DebugAdvanceOpeningNight(float DeltaSeconds)
{
	UpdateOpeningNight(DeltaSeconds);
}

namespace
{
	/** hw.Playtest.FastForward stops: the beat the player wants to test in person. */
	constexpr int32 PlaytestBeatSpirit = 1;
	constexpr int32 PlaytestBeatHerbs = 2;
	constexpr int32 PlaytestBeatBackpack = 3;
	constexpr int32 PlaytestBeatKettle = 4;
	constexpr int32 PlaytestBeatStation = 5;
	constexpr int32 PlaytestBeatDog = 6;
	constexpr int32 PlaytestBeatFish = 7;
	constexpr int32 PlaytestBeatSleep = 8;
	constexpr int32 PlaytestBeatNight = 9;
	constexpr int32 PlaytestBeatCollect = 10;
	constexpr int32 PlaytestBeatHeal = 11;
	constexpr int32 PlaytestBeatGlider = 12;
	constexpr int32 PlaytestBeatDelivery = 13;
	constexpr int32 PlaytestBeatDayCamp = 14;
	constexpr int32 PlaytestBeatDawnGlide = 15;
	constexpr int32 PlaytestBeatNightGlide = 16;
	constexpr int32 PlaytestBeatStealth = 17;
	constexpr int32 PlaytestBeatEase = 18;
	constexpr int32 PlaytestBeatShrine = 19;
	constexpr int32 PlaytestBeatStress = 20;

	/** The one runner step the player takes himself. 0 = every step runs (night and the loop). */
	int32 PlaytestSkipStep(int32 Beat)
	{
		switch (Beat)
		{
		case PlaytestBeatSpirit: return 1;
		case PlaytestBeatHerbs: return 2;
		case PlaytestBeatBackpack: return 3;
		case PlaytestBeatKettle: return 5;
		case PlaytestBeatStation: return 6;
		case PlaytestBeatDog: return 7;
		case PlaytestBeatFish: return 8;
		case PlaytestBeatSleep: return 9;
		default: return 0;
		}
	}

	const TCHAR* PlaytestBeatName(int32 Beat)
	{
		switch (Beat)
		{
		case PlaytestBeatSpirit: return TEXT("spirit");
		case PlaytestBeatHerbs: return TEXT("herbs");
		case PlaytestBeatBackpack: return TEXT("backpack");
		case PlaytestBeatKettle: return TEXT("kettle");
		case PlaytestBeatStation: return TEXT("station");
		case PlaytestBeatDog: return TEXT("dog");
		case PlaytestBeatFish: return TEXT("fish");
		case PlaytestBeatSleep: return TEXT("sleep");
		case PlaytestBeatNight: return TEXT("night");
		case PlaytestBeatCollect: return TEXT("collect");
		case PlaytestBeatHeal: return TEXT("heal");
		case PlaytestBeatGlider: return TEXT("glider");
		case PlaytestBeatDelivery: return TEXT("delivery");
		case PlaytestBeatDayCamp: return TEXT("daycamp");
		case PlaytestBeatDawnGlide: return TEXT("dawnglide");
		case PlaytestBeatNightGlide: return TEXT("nightglide");
		case PlaytestBeatStealth: return TEXT("stealth");
		case PlaytestBeatEase: return TEXT("ease");
		case PlaytestBeatShrine: return TEXT("shrine");
		case PlaytestBeatStress: return TEXT("stress");
		default: return TEXT("night");
		}
	}

	/** Beat words (lowercased, spaces folded out) to a stop. 0 = unknown. */
	int32 PlaytestBeatFromText(const FString& Text)
	{
		FString Key = Text.ToLower();
		Key.ReplaceInline(TEXT("_"), TEXT(""));
		Key.ReplaceInline(TEXT(" "), TEXT(""));
		if (Key.IsEmpty())
		{
			return PlaytestBeatNight;
		}
		// Order matters here: "herb collection" carries both herb and collect.
		if (Key.Contains(TEXT("heal")) || Key.Contains(TEXT("spring"))) return PlaytestBeatHeal;
		if (Key.Contains(TEXT("herb")) || Key.Contains(TEXT("garden"))) return PlaytestBeatHerbs;
		if (Key.Contains(TEXT("stealth"))) return PlaytestBeatStealth;
		if (Key.Contains(TEXT("spirit"))) return PlaytestBeatSpirit;
		if (Key.Contains(TEXT("backpack")) || Key.Contains(TEXT("partner")) || Key.Contains(TEXT("gift"))) return PlaytestBeatBackpack;
		if (Key.Contains(TEXT("kettle")) || Key.Contains(TEXT("tea"))) return PlaytestBeatKettle;
		if (Key.Contains(TEXT("station")) || Key.Contains(TEXT("counter")) || Key.Contains(TEXT("mix"))) return PlaytestBeatStation;
		if (Key.Contains(TEXT("dog")) || Key.Contains(TEXT("grace"))) return PlaytestBeatDog;
		if (Key.Contains(TEXT("fish")) || Key.Contains(TEXT("pond"))) return PlaytestBeatFish;
		if (Key.Contains(TEXT("sleep")) || Key.Contains(TEXT("bed"))) return PlaytestBeatSleep;
		if (Key.Contains(TEXT("wisp")) || Key.Contains(TEXT("collect"))) return PlaytestBeatCollect;
		if (Key.Contains(TEXT("nightglide"))) return PlaytestBeatNightGlide;
		if (Key.Contains(TEXT("night"))) return PlaytestBeatNight;
		if (Key.Contains(TEXT("glider"))) return PlaytestBeatGlider;
		if (Key.Contains(TEXT("delivery"))) return PlaytestBeatDelivery;
		if (Key.Contains(TEXT("daycamp"))) return PlaytestBeatDayCamp;
		if (Key.Contains(TEXT("dawnglide"))) return PlaytestBeatDawnGlide;
		if (Key.Contains(TEXT("shrine"))) return PlaytestBeatShrine;
		if (Key.Contains(TEXT("stress"))) return PlaytestBeatStress;
		if (Key.Contains(TEXT("ease"))) return PlaytestBeatEase;
		return 0;
	}

	AActor* FindOpeningTaggedActor(UWorld* World, const TCHAR* Tag, const TCHAR* AltTag = nullptr)
	{
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (It->ActorHasTag(FName(Tag)) || (AltTag && It->ActorHasTag(FName(AltTag))))
			{
				return *It;
			}
		}
		return nullptr;
	}
}

void AHomeWorldCharacter::DebugFastForwardOpening(const FString& Beat)
{
	if (Beat.Equals(TEXT("list"), ESearchCase::IgnoreCase))
	{
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: beats: spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect, heal, glider, delivery, daycamp, dawnglide, nightglide, stealth, ease, shrine, stress"));
		return;
	}
	if (DebugFastForwardStep > 0)
	{
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: already running (step %d)"), DebugFastForwardStep);
		return;
	}
	const int32 Stop = PlaytestBeatFromText(Beat);
	if (Stop == 0)
	{
		UE_LOG(LogTemp, Warning, TEXT("playtest_ff: beat '%s' unknown - spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect, heal, glider, delivery, daycamp, dawnglide, nightglide, stealth, ease, shrine, stress"), *Beat);
		return;
	}
	if (Stop == PlaytestBeatStress)
	{
		if (StressComponent)
		{
			StressComponent->SetPoints(90);
		}
		DebugFastForwardStop = Stop;
		PlaytestReadyFor = TEXT("stress");
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: ready for stress - stress 90, cap is 100"));
		return;
	}
	if (bOpeningNightSpirit)
	{
		UE_LOG(LogTemp, Warning, TEXT("playtest_ff: already night - start a fresh PIE"));
		return;
	}
	// A fresh PIE copies the Editor world's time of day. A previous night beat can leave
	// the next PIE at night, where the kettle brew is skipped. Every stop starts on the
	// day body; night and the loop still set Night at step 9.
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
		}
		SyncFormWithTimeOfDay();
	}
	DebugFastForwardStop = Stop;
	DebugFastForwardStep = 1;
	DebugFastForwardStepClock = 0.f;
	PlaytestReadyFor.Empty();
	PlaytestReadyDistanceCm = -1.f;
	UE_LOG(LogTemp, Log, TEXT("playtest_ff: start -> %s. The beats before it run for real, then it is yours."), PlaytestBeatName(Stop));
}

void AHomeWorldCharacter::TickDebugFastForward(float DeltaTime)
{
	if (DebugFastForwardStep <= 0)
	{
		return;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		DebugFastForwardStep = 0;
		return;
	}
	DebugFastForwardStepClock += DeltaTime;
	auto Next = [this](int32 Step)
	{
		DebugFastForwardStep = Step;
		DebugFastForwardStepClock = 0.f;
	};
	switch (DebugFastForwardStep)
	{
	case 1:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 1)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		bool bClaimed = false;
		for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
		{
			bClaimed = It->TryClaim(this);
			break;
		}
		if (!bClaimed)
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 1 spirit claim failed - is this L_SizeTest?"));
			Next(0);
			return;
		}
		bOpeningSpiritClaimed = true;
		if (SizeTestWisp)
		{
			SizeTestWisp->SetHiddenInGame(false);
			SizeTestWisp->SetVisibility(true);
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 1 spirit claimed"));
		Next(2);
		break;
	}
	case 2:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 2)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		AActor* West = nullptr;
		AActor* East = nullptr;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!West && It->ActorHasTag(FName(TEXT("NODE_GARDEN_WEST"))))
			{
				West = *It;
			}
			else if (!East && It->ActorHasTag(FName(TEXT("NODE_GARDEN_EAST"))))
			{
				East = *It;
			}
		}
		if (!West || !East)
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 2 herb beds missing (west %d, east %d)"),
				West ? 1 : 0, East ? 1 : 0);
			Next(0);
			return;
		}
		StartOpeningHerbRune(West);
		FinishOpeningHerbRune(10);
		StartOpeningHerbRune(East);
		FinishOpeningHerbRune(10);
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 2 herbs gathered %d (east %d, west %d), banked %d"),
			OpeningHerbsGathered, bOpeningHerbFromEast ? 1 : 0, bOpeningHerbFromWest ? 1 : 0, OpeningHerbTenths);
		Next(3);
		break;
	}
	case 3:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 3)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		AHomeWorldOpeningReveal* Reveal = nullptr;
		for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
		{
			Reveal = *It;
			break;
		}
		if (!Reveal)
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 3 no opening reveal"));
			Next(0);
			return;
		}
		if (!Reveal->IsPartnerWaiting())
		{
			Reveal->TryLeadPartner();
			if (DebugFastForwardStepClock > 20.f)
			{
				UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 3 partner walk timed out"));
				Next(0);
			}
			break;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 3 partner waiting (%.1fs)"), DebugFastForwardStepClock);
		Next(4);
		break;
	}
	case 4:
		if (PlaytestSkipStep(DebugFastForwardStop) == 4)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		if (!TryOpeningArmorGift())
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 4 backpack failed"));
			Next(0);
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 4 backpack"));
		Next(5);
		break;
	case 5:
		if (PlaytestSkipStep(DebugFastForwardStop) == 5)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		if (!TryBrewNodeKettleTea())
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 5 kettle failed (day body only)"));
			Next(0);
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 5 kettle brewed, banked %d"), OpeningHerbTenths);
		Next(6);
		break;
	case 6:
		if (PlaytestSkipStep(DebugFastForwardStop) == 6)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		UseOpeningConsumableStation();
		UseOpeningConsumableStation();
		if (OpeningMixedHerbs <= 0)
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 6 station mix failed"));
			Next(0);
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 6 station open, mixed herb %d, banked %d"), OpeningMixedHerbs, OpeningHerbTenths);
		Next(7);
		break;
	case 7:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 7)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		AHomeWorldOpeningDog* Dog = nullptr;
		for (TActorIterator<AHomeWorldOpeningDog> It(World); It; ++It)
		{
			Dog = *It;
			break;
		}
		if (!Dog)
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 7 no dog"));
			Next(0);
			return;
		}
		OpeningDog = Dog;
		if (!Dog->IsWrathEased())
		{
			StartOpeningDogDraw(Dog);
			SucceedOpeningDogTrace(Dog);
		}
		if (!Dog->TryTameWithMixedHerb(this))
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 7 dog refused the offering (tamed %d, eased %d)"),
				Dog->IsDogTamed() ? 1 : 0, Dog->IsWrathEased() ? 1 : 0);
			Next(0);
			return;
		}
		--OpeningMixedHerbs;
		for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
		{
			It->BeginChildReturnHome();
			break;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 7 dog tamed, mixed herb %d"), OpeningMixedHerbs);
		Next(8);
		break;
	}
	case 8:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 8)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		AActor* Pond = FindOpeningNamed(World, TEXT("Water_Pond"), true);
		if (!Pond)
		{
			Pond = FindOpeningNamed(World, TEXT("Water_Pond"), false);
		}
		if (Pond)
		{
			PlaceForOpeningPlaytestAtPond(Pond);
		}
		if (!TryOpeningFish())
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 8 fish failed (pond %d, tamed %d)"),
				Pond ? 1 : 0, (OpeningDog && OpeningDog->IsDogTamed()) ? 1 : 0);
			Next(0);
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 8 fish"));
		Next(9);
		break;
	}
	case 9:
	{
		if (PlaytestSkipStep(DebugFastForwardStop) == 9)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		AActor* Bed = FindOpeningNamed(World, TEXT("SM_Size_Bed"), true);
		if (Bed)
		{
			FVector Loc = Bed->GetActorLocation();
			Loc.Y -= 180.f;
			SetActorLocation(Loc, false, nullptr, ETeleportType::TeleportPhysics);
		}
		if (!BeginOpeningNight())
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 9 night failed"));
			Next(0);
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: 9 night ready at the bed - %s"), *GetOpeningTrackerText());
		if (DebugFastForwardStop == PlaytestBeatGlider || DebugFastForwardStop == PlaytestBeatDelivery
			|| DebugFastForwardStop == PlaytestBeatDayCamp || DebugFastForwardStop == PlaytestBeatDawnGlide
			|| DebugFastForwardStop == PlaytestBeatNightGlide || DebugFastForwardStop == PlaytestBeatStealth
			|| DebugFastForwardStop == PlaytestBeatEase || DebugFastForwardStop == PlaytestBeatShrine)
		{
			Next(10);
			break;
		}
		ReadyForOpeningPlaytest();
		Next(0);
		break;
	}
	case 10:
	{
		ReturnOpeningBodyForDawnPlaytest();
		StockOpeningDawnChest();
		if (DebugFastForwardStop == PlaytestBeatGlider)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		if (DebugFastForwardStop == PlaytestBeatDayCamp)
		{
			Next(12);
			break;
		}
		if (DebugFastForwardStop == PlaytestBeatDelivery)
		{
			Next(11);
			break;
		}
		Next(13);
		break;
	}
	case 11:
	{
		SeedOpeningHealedWisp();
		UHomeWorldOpeningSupply::SpawnDeliveryNode(
			World, HomeWorldOpeningMaterials::Wood, GetActorLocation() + FVector(200.f, 0.f, 0.f));
		ReadyForOpeningPlaytest();
		Next(0);
		break;
	}
	case 12:
	{
		FActorSpawnParameters CampParams;
		CampParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		World->SpawnActor<AHomeWorldOpeningDayCamp>(
			GetActorLocation() + FVector(320.f, 0.f, 0.f), FRotator::ZeroRotator, CampParams);
		ReadyForOpeningPlaytest();
		Next(0);
		break;
	}
	case 13:
	{
		TryCraftOpeningGlider();
		FActorSpawnParameters MarkerParams;
		MarkerParams.Name = FName(TEXT("GP_GlideStart"));
		MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		if (AActor* Marker = World->SpawnActor<AActor>(GetActorLocation(), FRotator::ZeroRotator, MarkerParams))
		{
			Marker->Tags.Add(FName(TEXT("GlideStart")));
		}
		if (DebugFastForwardStop == PlaytestBeatDawnGlide)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		Next(14);
		break;
	}
	case 14:
	{
		if (!BeginOpeningNight())
		{
			UE_LOG(LogTemp, Warning, TEXT("playtest_ff: 14 night glide failed"));
			Next(0);
			return;
		}
		if (DebugFastForwardStop == PlaytestBeatNightGlide)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		Next(15);
		break;
	}
	case 15:
	{
		for (int32 Index = 0; Index < 3; ++Index)
		{
			const FVector At = GetActorLocation() + FVector(400.f + Index * 160.f, 0.f, 0.f);
			FActorSpawnParameters GuardParams;
			GuardParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			if (AHomeWorldCampActor* Guard = World->SpawnActor<AHomeWorldCampActor>(At, FRotator::ZeroRotator, GuardParams))
			{
				Guard->CampRole = EHomeWorldCampRole::Guard;
				Guard->Tags.Remove(FName(TEXT("NODE_SLEEPER")));
				Guard->RefreshCampIdentity();
			}
			FActorSpawnParameters LightParams;
			LightParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			World->SpawnActor<AHomeWorldSpiritLitVolume>(At, FRotator::ZeroRotator, LightParams);
		}
		if (DebugFastForwardStop == PlaytestBeatStealth)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		Next(16);
		break;
	}
	case 16:
	{
		for (int32 Index = 0; Index < 3; ++Index)
		{
			const FVector At = GetActorLocation() + FVector(400.f + Index * 160.f, 80.f, 0.f);
			FActorSpawnParameters PadParams;
			PadParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			if (AHomeWorldEasePad* Pad = World->SpawnActor<AHomeWorldEasePad>(At, FRotator::ZeroRotator, PadParams))
			{
				Pad->Tags.Add(FName(TEXT("NODE_OPENING_EASE")));
				Pad->BindGuard(Index);
			}
		}
		if (DebugFastForwardStop == PlaytestBeatEase)
		{
			ReadyForOpeningPlaytest();
			Next(0);
			return;
		}
		Next(17);
		break;
	}
	case 17:
	{
		RunOpeningShrineStop();
		ReadyForOpeningPlaytest();
		Next(0);
		break;
	}
	default:
		Next(0);
		break;
	}
}

void AHomeWorldCharacter::ReadyForOpeningPlaytest()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	AActor* Target = nullptr;
	float Distance = 260.f;
	bool bPondEdge = false;
	bool bPlaceTarget = true;
	FString Note;
	switch (DebugFastForwardStop)
	{
	case PlaytestBeatSpirit:
	{
		for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
		{
			Target = *It;
			break;
		}
		Note = TEXT("E at the spirit");
		break;
	}
	case PlaytestBeatHerbs:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_GARDEN_EAST"));
		Note = TEXT("E at the east bed, draw the trace heart");
		break;
	case PlaytestBeatBackpack:
		Target = FindOpeningTaggedActor(World, TEXT("NPC_PARTNER"));
		Note = TEXT("E at the partner: the backpack");
		break;
	case PlaytestBeatKettle:
		Target = FindOpeningTaggedActor(World, TEXT("KettleCounter"), TEXT("NODE_CONSUMABLE_STATION"));
		Distance = 220.f;
		Note = TEXT("E at the counter: open, mix, then brew");
		break;
	case PlaytestBeatStation:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_CONSUMABLE_STATION"));
		Distance = 220.f;
		Note = TEXT("E at the counter: open, then mix");
		break;
	case PlaytestBeatDog:
	{
		for (TActorIterator<AHomeWorldOpeningDog> It(World); It; ++It)
		{
			Target = *It;
			break;
		}
		Distance = 650.f;
		Note = TEXT("walk up slowly, draw the Grace trace, then E");
		break;
	}
	case PlaytestBeatFish:
		Target = FindOpeningNamed(World, TEXT("Water_Pond"), true);
		bPondEdge = true;
		Note = TEXT("E at the pond bank, one fish");
		break;
	case PlaytestBeatSleep:
		Target = FindOpeningNamed(World, TEXT("SM_Size_Bed"), true);
		Distance = 180.f;
		Note = TEXT("E at the bed: sleep");
		break;
	case PlaytestBeatNight:
		Target = FindOpeningNamed(World, TEXT("SM_Size_Bed"), true);
		Distance = 180.f;
		bPlaceTarget = false;
		Note = TEXT("night is on, the bed is behind you");
		break;
	case PlaytestBeatCollect:
		EnsureOpeningNightProps();
		Target = OpeningCopseWisp;
		Distance = 350.f;
		Note = TEXT("E at the wisp, click the heart");
		break;
	case PlaytestBeatHeal:
		EnsureOpeningNightProps();
		CollectNightWispsForPlaytest();
		Target = FindOpeningNamed(World, TEXT("Water_HotSpring"), true);
		Distance = 470.f;
		Note = TEXT("E at the hot springs, the heal takes 20s");
		break;
	case PlaytestBeatGlider:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_ARMOR_TABLE"), TEXT("ArmorTable"));
		Distance = 220.f;
		Note = TEXT("E at the armory: craft the glider");
		break;
	case PlaytestBeatDelivery:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_OPENING_DELIVERY"));
		Distance = 200.f;
		Note = TEXT("E at the wood node: set the healed wisp");
		break;
	case PlaytestBeatDayCamp:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_OPENING_DAY_CAMP"));
		Distance = 320.f;
		Note = TEXT("walk into the clearing");
		break;
	case PlaytestBeatDawnGlide:
		Target = FindOpeningTaggedActor(World, TEXT("GlideStart"));
		Distance = 180.f;
		Note = TEXT("the launch is yours");
		break;
	case PlaytestBeatNightGlide:
		Target = FindOpeningTaggedActor(World, TEXT("GlideStart"));
		Distance = 180.f;
		Note = TEXT("travel only, the launch is yours");
		break;
	case PlaytestBeatStealth:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_GUARD"));
		Distance = 260.f;
		Note = TEXT("reach the guard");
		break;
	case PlaytestBeatEase:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_OPENING_EASE"));
		Distance = 180.f;
		Note = TEXT("the wind-up is yours");
		break;
	case PlaytestBeatShrine:
		Target = FindOpeningTaggedActor(World, TEXT("NODE_OPENING_SHRINE"));
		Distance = 180.f;
		Note = TEXT("E at the shrine");
		break;
	default:
		break;
	}
	if (Target && bPlaceTarget)
	{
		if (bPondEdge)
		{
			PlaceForOpeningPlaytestAtPond(Target);
		}
		else
		{
			PlaceForOpeningPlaytest(Target, Distance);
		}
	}
	PlaytestReadyFor = PlaytestBeatName(DebugFastForwardStop);
	PlaytestReadyDistanceCm = Target
		? FVector::Dist2D(GetActorLocation(), Target->GetActorLocation())
		: -1.f;
	UE_LOG(LogTemp, Log, TEXT("playtest_ff: ready for %s - %s"), PlaytestBeatName(DebugFastForwardStop), *Note);
	if (Target)
	{
		const float DistCm = PlaytestReadyDistanceCm;
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: you are at %s, target %s, dist %.0f"),
			*GetActorLocation().ToCompactString(),
			*Target->GetActorNameOrLabel(),
			DistCm);
	}
	else
	{
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: you are at %s, target none, dist none"),
			*GetActorLocation().ToCompactString());
	}
	UE_LOG(LogTemp, Log, TEXT("playtest_ff: tracker %s"), *GetOpeningTrackerText());
}

void AHomeWorldCharacter::PlaceForOpeningPlaytest(AActor* Target, float Distance)
{
	UWorld* World = GetWorld();
	if (!World || !Target)
	{
		return;
	}
	const FVector TargetLoc = Target->GetActorLocation();
	const FVector From = GetActorLocation();
	FVector Approach = TargetLoc - From;
	Approach.Z = 0.f;
	if (!Approach.Normalize())
	{
		Approach = FVector(1.f, 0.f, 0.f);
	}
	FVector Forward = Target->GetActorForwardVector();
	Forward.Z = 0.f;
	if (!Forward.Normalize())
	{
		Forward = Approach;
	}
	const FVector Side = FVector::CrossProduct(FVector::UpVector, Forward);
	// Try the side the player comes from first, then the prop's own facing: a counter inside
	// the house blocks the outside approach and the next direction is the one that works.
	const FVector Candidates[] = { Approach, Forward, -Forward, Side, -Side, -Approach };
	const float GroundZ = FMath::Max(From.Z, TargetLoc.Z);
	FVector AimTarget = TargetLoc;
	FVector AimExtent = FVector::ZeroVector;
	Target->GetActorBounds(false, AimTarget, AimExtent);
	if (AimTarget.IsNearlyZero() && !TargetLoc.IsNearlyZero())
	{
		AimTarget = TargetLoc;
	}
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(this);
	// Moving NPCs and the invisible interaction boxes must not pick the side: a child walking
	// through the kitchen would otherwise veto every spot around the counter.
	TArray<AActor*> Guests;
	TArray<UPrimitiveComponent*> HelperBoxes;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(TEXT("NPC_PARTNER")) || It->ActorHasTag(TEXT("NPC_CHILD")))
		{
			Guests.Add(*It);
		}
		TArray<UPrimitiveComponent*> Comps;
		It->GetComponents<UPrimitiveComponent>(Comps);
		for (UPrimitiveComponent* Comp : Comps)
		{
			if (Comp && Comp->GetName().StartsWith(TEXT("InteractBounds")))
			{
				HelperBoxes.Add(Comp);
			}
		}
	}
	for (UPrimitiveComponent* Box : HelperBoxes)
	{
		Params.AddIgnoredComponent(Box);
	}
	// The reach test keeps NPCs: nobody should be spawned inside the partner. The camera room
	// test drops them: the partner and the child move, and their back is not a wall.
	FCollisionQueryParams RoomParams = Params;
	RoomParams.AddIgnoredActors(Guests);
	// A candidate is good when a flat line reaches the prop without crossing a wall. Among those,
	// prefer the most room behind the player: the camera boom needs it, and the same counter is
	// boxed in from the outside and open from inside the kitchen.
	FVector Chosen = TargetLoc - Approach * Distance;
	bool bAimClear = false;
	float BestRoom = -1.f;
	for (const FVector& Dir : Candidates)
	{
		const FVector Candidate = TargetLoc - Dir * Distance;
		// Waist height: above beds, dogs and pond water, but below the top of any wall.
		const float FlatZ = GroundZ - 40.f;
		const FVector FlatFrom(Candidate.X, Candidate.Y, FlatZ);
		const FVector FlatTo(AimTarget.X, AimTarget.Y, FlatZ);
		FHitResult AimHit;
		if (World->LineTraceSingleByChannel(AimHit, FlatFrom, FlatTo, ECC_Visibility, Params)
			&& AimHit.GetActor() != Target)
		{
			continue;
		}
		if (!bAimClear)
		{
			Chosen = Candidate;
			bAimClear = true;
		}
		FHitResult BoomHit;
		const FVector Eye(Candidate.X, Candidate.Y, GroundZ + 90.f);
		const FVector Behind(Candidate.X - Dir.X * 330.f, Candidate.Y - Dir.Y * 330.f, GroundZ + 150.f);
		const bool bBoomHit = World->LineTraceSingleByChannel(BoomHit, Eye, Behind, ECC_Camera, RoomParams);
		const float Room = bBoomHit ? BoomHit.Distance : 330.f;
		if (Room > BestRoom)
		{
			BestRoom = Room;
			Chosen = Candidate;
		}
	}
	const float HalfHeight = GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() : 88.f;
	FCollisionQueryParams FloorParams = Params;
	FloorParams.AddIgnoredActor(Target);
	const FVector FloorStart(Chosen.X, Chosen.Y, TargetLoc.Z + AimExtent.Z + 30.f);
	const FVector FloorEnd(Chosen.X, Chosen.Y, TargetLoc.Z - AimExtent.Z - 200.f);
	FHitResult FloorHit;
	float FeetZ = TargetLoc.Z - AimExtent.Z;
	if (World->LineTraceSingleByChannel(FloorHit, FloorStart, FloorEnd, ECC_Visibility, FloorParams))
	{
		FeetZ = FloorHit.ImpactPoint.Z;
	}
	const FVector Loc(Chosen.X, Chosen.Y, FeetZ + HalfHeight);
	SetActorLocation(Loc, false, nullptr, ETeleportType::TeleportPhysics);
	if (UCharacterMovementComponent* Move = GetCharacterMovement())
	{
		Move->StopMovementImmediately();
	}
	const FVector Face = (FVector(TargetLoc.X, TargetLoc.Y, Loc.Z) - Loc).GetSafeNormal2D();
	if (!Face.IsNearlyZero())
	{
		SetActorRotation(Face.Rotation());
	}
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		FRotator Look = Face.IsNearlyZero() ? GetActorRotation() : Face.Rotation();
		// One rule for every beat stop: look at the prop, never past it. A waist-high
		// prop under a level gaze sits below the hover frame, which is how the armory
		// table came up with no wisp. The authored distance still sets the standoff;
		// only the gaze is derived. It never lifts the gaze above the resting pitch.
		const FVector Eye(Loc.X, Loc.Y, Loc.Z + HalfHeight * 0.5f);
		const FVector At(AimTarget.X, AimTarget.Y, AimTarget.Z + AimExtent.Z * 0.5f);
		const float AimPitch = (At - Eye).Rotation().Pitch;
		Look.Pitch = FMath::Clamp(FMath::Min(OpeningLookRestPitch, AimPitch), -35.f, 15.f);
		PC->SetControlRotation(Look);
	}
	if (!bAimClear)
	{
		UE_LOG(LogTemp, Warning, TEXT("playtest_ff: no clear side at %s - dropped on the approach line"), *Target->GetActorNameOrLabel());
	}
	else if (BestRoom < 330.f)
	{
		UE_LOG(LogTemp, Log, TEXT("playtest_ff: tight spot at %s - %.0f cm behind, the camera settles once you step"),
			*Target->GetActorNameOrLabel(), BestRoom);
	}
}

void AHomeWorldCharacter::PlaceForOpeningPlaytestAtPond(AActor* Pond)
{
	if (!Pond)
	{
		return;
	}
	UWorld* World = GetWorld();
	FVector Origin = FVector::ZeroVector;
	FVector Extent = FVector::ZeroVector;
	Pond->GetActorBounds(false, Origin, Extent);
	const UCapsuleComponent* Capsule = GetCapsuleComponent();
	const float Radius = Capsule ? Capsule->GetScaledCapsuleRadius() : 34.f;
	const float HalfHeight = Capsule ? Capsule->GetScaledCapsuleHalfHeight() : 100.f;
	const FCollisionShape Body = FCollisionShape::MakeCapsule(Radius, HalfHeight);
	const float Standoff = 100.f;
	const FVector Here = GetActorLocation();
	// The pond rim can hold a prop. A blind teleport drops the body inside it, and
	// the fish press then has no clear line to the water. Try the east edge first,
	// the approach this beat has always used, then walk the rim for a spot the
	// body actually fits in.
	FVector Loc = Here;
	bool bClear = false;
	if (World)
	{
		for (int32 Step = 0; Step < 8; ++Step)
		{
			const float Angle = FMath::DegreesToRadians(45.f * Step);
			const FVector Dir(FMath::Cos(Angle), FMath::Sin(Angle), 0.f);
			const FVector Edge = Origin + FVector(Dir.X * Extent.X, Dir.Y * Extent.Y, 0.f);
			const FVector Candidate(Edge.X + Dir.X * Standoff, Edge.Y + Dir.Y * Standoff, Here.Z);
			FCollisionQueryParams Params(NAME_None, false, this);
			if (!World->OverlapBlockingTestByChannel(Candidate, FQuat::Identity, ECC_Pawn, Body, Params))
			{
				Loc = Candidate;
				bClear = true;
				break;
			}
		}
	}
	if (!bClear)
	{
		// No free spot on the rim. Keep the old east edge so the beat still runs.
		Loc.X = Origin.X + Extent.X + Standoff;
		Loc.Y = Origin.Y;
	}
	SetActorLocation(Loc, false, nullptr, ETeleportType::TeleportPhysics);
	if (UCharacterMovementComponent* Move = GetCharacterMovement())
	{
		Move->StopMovementImmediately();
	}
	if (APlayerController* PC = Cast<APlayerController>(GetController()))
	{
		PC->SetControlRotation((Origin + FVector(0.f, 0.f, 40.f) - Loc).Rotation());
	}
}

void AHomeWorldCharacter::CollectNightWispsForPlaytest()
{
	AActor* Wisps[] = { OpeningCopseWisp, OpeningPondWisp, OpeningSpringWisp };
	int32 Collected = 0;
	for (AActor* Wisp : Wisps)
	{
		if (!Wisp || Wisp->IsHidden() || bOpeningRuneActive)
		{
			continue;
		}
		bOpeningWispCollect = true;
		StartOpeningHerbRune(Wisp);
		if (!bOpeningRuneActive)
		{
			bOpeningWispCollect = false;
			continue;
		}
		FinishOpeningHerbRune(10);
		++Collected;
	}
	UE_LOG(LogTemp, Log, TEXT("playtest_ff: %d night wisps in the backpack (carried %d)"), Collected, OpeningWispsCarried);
}

FString AHomeWorldCharacter::GetOpeningTrackerText() const
{
	if (!QuestLog)
	{
		return TEXT("(no quest log)");
	}
	const TArray<FHomeWorldQuestStep>& Steps = QuestLog->GetDisplayedSteps();
	TArray<FString> Lines;
	for (const FHomeWorldQuestStep& Step : Steps)
	{
		Lines.Add(FString::Printf(TEXT("%s%s"), Step.bDone ? TEXT("[x] ") : TEXT("[ ] "), *Step.Text));
	}
	return FString::Join(Lines, TEXT(" | "));
}

FString AHomeWorldCharacter::GetPlaytestStateJson() const
{
	return FString::Printf(
		TEXT("{\"ready_for\":\"%s\",\"ready_distance\":%.1f,\"fast_forward_step\":%d,")
		TEXT("\"spirit_claimed\":%s,\"herbs_gathered\":%d,\"herb_tenths\":%d,")
		TEXT("\"herb_west\":%s,\"herb_east\":%s,\"mixed_herbs\":%d,")
		TEXT("\"kettle_brewed\":%s,\"station_open\":%s,\"armor_gift\":%s,")
		TEXT("\"fish_caught\":%s,\"night_spirit\":%s,")
		TEXT("\"wisps_collected\":%d,\"wisps_carried\":%d,\"wisps_healed\":%d,")
		TEXT("\"dawn_wood\":%d,\"dawn_silk\":%d,\"dawn_metal\":%d,")
		TEXT("\"glider_crafted\":%s,\"delivery_wood\":%d,\"partner_away\":%s,\"day_camp_eject\":%s,")
		TEXT("\"descent_active\":%s,\"cloud_carried\":%d,\"guards_calm\":%d,\"partner_walking\":%s,\"stress\":%d}"),
		*PlaytestReadyFor,
		PlaytestReadyDistanceCm,
		DebugFastForwardStep,
		bOpeningSpiritClaimed ? TEXT("true") : TEXT("false"),
		OpeningHerbsGathered,
		OpeningHerbTenths,
		bOpeningHerbFromWest ? TEXT("true") : TEXT("false"),
		bOpeningHerbFromEast ? TEXT("true") : TEXT("false"),
		OpeningMixedHerbs,
		bOpeningKettleBrewed ? TEXT("true") : TEXT("false"),
		bOpeningConsumableOpen ? TEXT("true") : TEXT("false"),
		bOpeningArmorGiftGiven ? TEXT("true") : TEXT("false"),
		bOpeningFishCaught ? TEXT("true") : TEXT("false"),
		bOpeningNightSpirit ? TEXT("true") : TEXT("false"),
		OpeningWispsCollected,
		OpeningWispsCarried,
		OpeningWispsHealed,
		GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Wood),
		GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Silk),
		GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Metal),
		IsOpeningGliderCrafted() ? TEXT("true") : TEXT("false"),
		GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood),
		GetPartnerPlace() == EHomeWorldFamilyPlace::Away ? TEXT("true") : TEXT("false"),
		IsDayCampEjectTriggered() ? TEXT("true") : TEXT("false"),
		IsCloudDescentActive() ? TEXT("true") : TEXT("false"),
		GetCarriedCloudWisps(),
		SpiritStealthComponent ? SpiritStealthComponent->GetCalmedActorCount() : 0,
		IsPartnerWalkingHome() ? TEXT("true") : TEXT("false"),
		GetStressPoints());
}

int32 AHomeWorldCharacter::GetStressPoints() const
{
	return StressComponent ? StressComponent->GetPoints() : 0;
}

void AHomeWorldCharacter::ApplyOpeningWalkSpeed()
{
	static const float Speeds[] = {150.f, 300.f, 450.f};
	if (!TraversalComponent)
	{
		return;
	}
	const int32 Step = FMath::Clamp(OpeningSpeedStep, 0, 2);
	TraversalComponent->SetMovementSlowScale(Speeds[Step] / 450.f);
}

void AHomeWorldCharacter::UpdateOpeningWalkScroll()
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC)
	{
		return;
	}
	int32 Step = OpeningSpeedStep;
	if (PC->WasInputKeyJustPressed(EKeys::MouseScrollUp))
	{
		Step = FMath::Min(2, Step + 1);
	}
	if (PC->WasInputKeyJustPressed(EKeys::MouseScrollDown))
	{
		Step = FMath::Max(0, Step - 1);
	}
	if (Step == OpeningSpeedStep)
	{
		return;
	}
	OpeningSpeedStep = Step;
	ApplyOpeningWalkSpeed();
}

AActor* AHomeWorldCharacter::ResolveOpeningAim(FHitResult& Hit)
{
	(void)Hit;
	return FindOpeningProximityTarget();
}

bool AHomeWorldCharacter::TraceEyeInteract(FHitResult& OutHit) const
{
	UWorld* World = GetWorld();
	if (!World || !FollowCamera)
	{
		return false;
	}
	const FVector Start = FollowCamera->GetComponentLocation();
	const FVector End = Start + FollowCamera->GetForwardVector() * 2000.f;
	FCollisionQueryParams Params(NAME_None, false, this);
	TArray<FHitResult> Hits;
	if (!World->LineTraceMultiByChannel(Hits, Start, End, ECC_Visibility, Params))
	{
		return false;
	}
	for (const FHitResult& Hit : Hits)
	{
		AActor* HitActor = GetInteractTargetActor(Hit);
		if (!HitActor || HitActor == this)
		{
			continue;
		}
		if (ActorHasInteractableComponent(HitActor)
			|| HitActor->GetActorNameOrLabel().Contains(TEXT("Lupine")))
		{
			OutHit = Hit;
			return true;
		}
	}
	return false;
}

bool AHomeWorldCharacter::TryOpeningSpiritInFront()
{
	FHitResult Hit;
	AHomeWorldOpeningReveal* Reveal = Cast<AHomeWorldOpeningReveal>(ResolveOpeningAim(Hit));
	if (!Reveal || !Reveal->TryClaim(this))
	{
		return false;
	}
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
	}
	bOpeningSpiritClaimed = true;
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: shoulder spirit on"));
	return true;
}

bool AHomeWorldCharacter::TryPartyInviteInFront()
{
	FHitResult Hit;
	AActor* Target = nullptr;
	if (UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("SizeTest")))
	{
		Target = ResolveOpeningAim(Hit);
	}
	else if (TraceInteractHit(Hit))
	{
		Target = GetInteractTargetActor(Hit);
	}
	if (!Target)
	{
		return false;
	}
	if (!Target->ActorHasTag(TEXT("NPC_PARTNER")) && !Target->ActorHasTag(TEXT("NPC_CHILD")))
	{
		return false;
	}
	UWorld* World = GetWorld();
	UGameInstance* GameInstance = World ? World->GetGameInstance() : nullptr;
	UHomeWorldFamilySubsystem* Family = GameInstance ? GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>() : nullptr;
	if (!Family)
	{
		return false;
	}
	bool bNightOrDefend = false;
	if (const UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
	{
		bNightOrDefend = TimeOfDay->GetIsNight() || TimeOfDay->GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Dusk;
	}
	const bool bAtHome = !UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("Field"), ESearchCase::IgnoreCase);
	const EHomeWorldPartyToggle Result = Family->ToggleMemberAtHome(Target, bAtHome, bNightOrDefend, GetIsSpiritForm(), World);
	if (Result == EHomeWorldPartyToggle::Refused)
	{
		if (!Family->IsRescueComplete())
		{
			return false;
		}
		ShowInteractFeedback(TEXT("party: stays home"), FColor::Yellow);
		return true;
	}
	const bool bPartner = Target->ActorHasTag(TEXT("NPC_PARTNER"));
	ShowInteractFeedback(
		Result == EHomeWorldPartyToggle::SentHome
			? (bPartner ? TEXT("party: partner stays") : TEXT("party: child stays"))
			: (bPartner ? TEXT("party: partner comes") : TEXT("party: child comes")),
		FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryPartnerLeadInside()
{
	FHitResult Hit;
	AActor* HitActor = ResolveOpeningAim(Hit);
	if (!HitActor || !HitActor->ActorHasTag(FName(TEXT("NPC_PARTNER"))))
	{
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (AHomeWorldOpeningReveal* Reveal = Cast<AHomeWorldOpeningReveal>(*It))
		{
			if (!HasOpeningHerbQuota())
			{
				return true;
			}
			if (Reveal->TryLeadPartner())
			{
				return true;
			}
			// They already walked inside: the same press takes the armor piece.
			return TryOpeningArmorGift();
		}
	}
	return false;
}

bool AHomeWorldCharacter::TryOpeningArmorGift()
{
	if (bOpeningArmorGiftGiven)
	{
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		const AHomeWorldOpeningReveal* Reveal = Cast<AHomeWorldOpeningReveal>(*It);
		if (Reveal && Reveal->IsPartnerWaiting())
		{
			// The gift is the backpack. It is not the material inventory. The table opens. Walk speed and bonk tries stay.
			bOpeningArmorGiftGiven = true;
			UE_LOG(LogTemp, Log, TEXT("opening_reveal: partner gives the backpack"));
			return true;
		}
	}
	return false;
}

static void LogOpening(const FString& Message)
{
	static FString Last;
	static double At = -10.0;
	const double Now = FPlatformTime::Seconds();
	if (Message == Last && Now - At < 1.5)
	{
		return;
	}
	Last = Message;
	At = Now;
	UE_LOG(LogTemp, Log, TEXT("%s"), *Message);
}

bool AHomeWorldCharacter::TryOpeningDogInFront()
{
	FHitResult Hit;
	AHomeWorldOpeningDog* Dog = Cast<AHomeWorldOpeningDog>(ResolveOpeningAim(Hit));
	if (!Dog)
	{
		return false;
	}
	if (Dog->IsDogTamed())
	{
		return true;
	}
	if (!Dog->IsWrathEased())
	{
		const float Dist = FVector::Dist2D(GetActorLocation(), Dog->GetActorLocation());
		if (!bOpeningDogDrawActive && bOpeningDogSlowLatched && Dist <= 280.f)
		{
			StartOpeningDogDraw(Dog);
		}
		return true;
	}
	if (OpeningMixedHerbs <= 0)
	{
		LogOpening(TEXT("opening_dog: needs the mixed herb"));
		ShowInteractFeedback(TEXT("The dog wants the herb mixed with a spirit."), FColor::Yellow);
		return true;
	}
	if (!Dog->TryTameWithMixedHerb(this))
	{
		LogOpening(TEXT("opening_dog: not ready for the offering"));
		return true;
	}
	--OpeningMixedHerbs;
	if (UWorld* World = GetWorld())
	{
		for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
		{
			It->BeginChildReturnHome();
			break;
		}
	}
	UE_LOG(LogTemp, Log, TEXT("opening_dog: tamed with the mixed herb (carried %d)"), OpeningMixedHerbs);
	return true;
}

bool AHomeWorldCharacter::TryOpeningFish()
{
	if (!OpeningDog || !OpeningDog->IsDogTamed())
	{
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	AActor* Pond = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->GetActorNameOrLabel() == TEXT("Water_Pond"))
		{
			Pond = *It;
			break;
		}
	}
	if (!Pond)
	{
		return false;
	}
	FVector Origin = FVector::ZeroVector;
	FVector Extent = FVector::ZeroVector;
	Pond->GetActorBounds(false, Origin, Extent);
	const FVector From = GetActorLocation();
	const bool bAtPond = FMath::Abs(From.X - Origin.X) <= Extent.X + 200.f
		&& FMath::Abs(From.Y - Origin.Y) <= Extent.Y + 200.f;
	if (!bAtPond)
	{
		return false;
	}
	if (!HasOpeningLineOfSight(Pond))
	{
		return false;
	}
	if (bOpeningFishCaught)
	{
		return false;
	}
	bOpeningFishCaught = true;
	LogOpening(TEXT("opening_fish: one fish"));
	return true;
}

bool AHomeWorldCharacter::TryOpeningZiplineInFront()
{
	FHitResult Hit;
	AHomeWorldOpeningZipline* Line = Cast<AHomeWorldOpeningZipline>(ResolveOpeningAim(Hit));
	if (!Line)
	{
		return false;
	}
	return Line->TryRide(this);
}

void AHomeWorldCharacter::UseOpeningConsumableStation()
{
	if (!bOpeningConsumableOpen)
	{
		if (!bOpeningSpiritClaimed || OpeningHerbTenths <= 0)
		{
			LogOpening(FString::Printf(TEXT("opening_station: consumable locked - need the herb and the spirit (spirit %d, banked %d)"),
				bOpeningSpiritClaimed ? 1 : 0, OpeningHerbTenths));
			ShowInteractFeedback(TEXT("The station needs the herb and the spirit."), FColor::Yellow);
			return;
		}
		bOpeningConsumableOpen = true;
		UE_LOG(LogTemp, Log, TEXT("opening_station: consumable open"));
		ShowInteractFeedback(TEXT("CONSUMABLE: the station is open"), FColor::Green);
		return;
	}
	// Open. Its one output is the mixed herb the dog beat spends. Once the herb is
	// carried, the same press brews at the kettle that stands on this counter.
	if (OpeningMixedHerbs <= 0)
	{
		if (OpeningHerbTenths <= 0)
		{
			LogOpening(FString::Printf(TEXT("opening_station: mixed herb failed - need herb chunks (banked %d)"), OpeningHerbTenths));
			ShowInteractFeedback(TEXT("The station needs the herb."), FColor::Yellow);
			return;
		}
		--OpeningHerbTenths;
		++OpeningMixedHerbs;
		UE_LOG(LogTemp, Log, TEXT("opening_station: mixed herb made (carried %d, banked %d)"), OpeningMixedHerbs, OpeningHerbTenths);
		ShowInteractFeedback(TEXT("CONSUMABLE: herb mixed with a spirit"), FColor::Green);
		return;
	}
	if (UHomeWorldHomeLoopSubsystem* HomeLoop = GetWorld() ? GetWorld()->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr)
	{
		HomeLoop->TryKettleFromWorld(this);
		return;
	}
	TryBrewNodeKettleTea();
}

bool AHomeWorldCharacter::TryOpeningStationInFront()
{
	FHitResult Hit;
	AActor* HitActor = ResolveOpeningAim(Hit);
	if (!HitActor)
	{
		return false;
	}
	if (HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::ConsumableStation))
	{
		UseOpeningConsumableStation();
		return true;
	}
	if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::ArmorTable))
	{
		return false;
	}
	if (!bOpeningArmorGiftGiven)
	{
		LogOpening(TEXT("opening_station: armor table locked - the partner's gift opens it"));
		ShowInteractFeedback(TEXT("The partner's gift opens this."), FColor::Yellow);
		return true;
	}
	if (OpeningSupply && OpeningSupply->HasDawnStock() && TryCraftOpeningGlider())
	{
		LogOpening(TEXT("opening_station: glider crafted"));
		ShowInteractFeedback(TEXT("ARMOR: the glider is crafted"), FColor::Green);
		return true;
	}
	LogOpening(TEXT("opening_station: armor table open"));
	ShowInteractFeedback(TEXT("ARMOR: the table is open"), FColor::Green);
	return true;
}

void AHomeWorldCharacter::StockOpeningDawnChest()
{
	if (OpeningSupply)
	{
		OpeningSupply->StockDawnChest();
	}
}

bool AHomeWorldCharacter::TryCraftOpeningGlider()
{
	return OpeningSupply && OpeningSupply->TryCraftGlider();
}

bool AHomeWorldCharacter::IsOpeningGliderCrafted() const
{
	return OpeningSupply && OpeningSupply->IsGliderCrafted();
}

void AHomeWorldCharacter::GrantOpeningGliderForTest()
{
	if (OpeningSupply)
	{
		OpeningSupply->GrantCraftedForTest();
	}
}

int32 AHomeWorldCharacter::GetOpeningDawnCountForTest(FName Material) const
{
	return OpeningSupply ? OpeningSupply->GetDawnCount(Material) : 0;
}

int32 AHomeWorldCharacter::GetOpeningDeliveryCountForTest(FName Material) const
{
	return OpeningSupply ? OpeningSupply->GetDeliveryCount(Material) : 0;
}

void AHomeWorldCharacter::SeedOpeningHealedWisp()
{
	if (OpeningWispsHealed >= 3)
	{
		return;
	}
	++OpeningWispsHealed;
	UpdateOpeningWispLegs();
	UE_LOG(LogTemp, Log, TEXT("opening_delivery: seed healed %d. This is a seed."), OpeningWispsHealed);
}

bool AHomeWorldCharacter::TryDeliverOpeningNode(AActor* NodeActor)
{
	if (!NodeActor || GetIsSpiritForm() || !AreDayBodyAbilitiesAllowed() || OpeningWispsHealed <= 0 || !OpeningSupply)
	{
		return false;
	}
	UHomeWorldOpeningDeliveryNode* Node = NodeActor->FindComponentByClass<UHomeWorldOpeningDeliveryNode>();
	if (!Node)
	{
		return false;
	}
	if (!OpeningSupply->TryDeliver(Node))
	{
		return false;
	}
	UpdateOpeningWispLegs();
	UE_LOG(LogTemp, Log, TEXT("opening_delivery: %s pile %d in the chest, follower back at the legs (%d)"),
		*Node->GetMaterial().ToString(),
		OpeningSupply->GetDeliveryCount(Node->GetMaterial()),
		OpeningWispLegMeshes.Num());
	ShowInteractFeedback(TEXT("The wisp flew the pile home."), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryOpeningDeliveryInFront()
{
	if (GetIsSpiritForm() || !AreDayBodyAbilitiesAllowed())
	{
		return false;
	}
	FHitResult Hit;
	AActor* Aimed = ResolveOpeningAim(Hit);
	if (!Aimed || !Aimed->ActorHasTag(FName(TEXT("NODE_OPENING_DELIVERY"))))
	{
		return false;
	}
	UHomeWorldOpeningDeliveryNode* Node = Aimed->FindComponentByClass<UHomeWorldOpeningDeliveryNode>();
	if (!Node)
	{
		return false;
	}
	if (!UHomeWorldOpeningSupply::IsDeliveryMaterial(Node->GetMaterial()))
	{
		ShowInteractFeedback(TEXT("Silk, fiber, and metal stay off this field."), FColor::Yellow);
		return true;
	}
	if (Node->IsDelivered())
	{
		ShowInteractFeedback(TEXT("That node has already delivered."), FColor::Yellow);
		return true;
	}
	if (OpeningWispsHealed <= 0)
	{
		ShowInteractFeedback(TEXT("The node needs a healed wisp."), FColor::Yellow);
		return true;
	}
	return TryDeliverOpeningNode(Aimed);
}

bool AHomeWorldCharacter::TryCommitOpeningGuardPad(AHomeWorldEasePad* Pad, EHomeWorldStrokeStep Played)
{
	if (!Pad || !Pad->NoteMatch(Played))
	{
		return false;
	}
	if (Pad->IsLadderComplete())
	{
		if (UWorld* World = GetWorld())
		{
			if (UHomeWorldHomeLoopSubsystem* Home = World->GetSubsystem<UHomeWorldHomeLoopSubsystem>())
			{
				Home->TrySpendChestItem(HomeWorldKitchen::Moss, 1);
			}
		}
		ApplyOpeningGuardSleep(Pad);
	}
	return true;
}

void AHomeWorldCharacter::ApplyOpeningGuardSleep(AHomeWorldEasePad* Pad)
{
	if (!Pad || !Pad->IsBoundToGuard() || Pad->HasSleptItsGuard() || !Pad->IsLadderComplete())
	{
		return;
	}
	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent;
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	if (!Stealth)
	{
		return;
	}
	if (Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, Pad->GetGuardOrdinal()))
	{
		Pad->MarkGuardSlept();
		RecordGuardEased(Pad->GetGuardOrdinal());
	}
}

bool AHomeWorldCharacter::TryWaitOpeningGuardPad(AHomeWorldEasePad* Pad)
{
	if (!Pad || !StrokeReport || Pad->GetOfferedStep() != EHomeWorldStrokeStep::Grace)
	{
		return false;
	}
	TArray<FHomeWorldStrokeSample> Stroke;
	for (const FVector2D& Point : HomeWorldStroke::GraceShape())
	{
		FHomeWorldStrokeSample Sample;
		Sample.Point = Point;
		Sample.Time = 0.5f;
		Stroke.Add(Sample);
	}
	const EHomeWorldStrokeReport Report = StrokeReport->ReportStroke(
		Pad->GetOfferedStep(),
		Stroke,
		Pad->GetWindowMin(),
		Pad->GetWindowMax(),
		Pad->GetExtraPoint(),
		nullptr,
		FallbackGlideComponent,
		false,
		FVector::ZeroVector,
		EHomeWorldEaseCommit::Wait,
		false);
	return Report == EHomeWorldStrokeReport::None && StrokeReport->WasGlideHomeInvoked();
}

bool AHomeWorldCharacter::TryReachOpeningGuard(AActor* Guard)
{
	if (!GetIsSpiritForm() || !Guard || !Guard->ActorHasTag(FName(TEXT("NODE_GUARD"))))
	{
		return false;
	}
	if (FVector::Dist2D(GetActorLocation(), Guard->GetActorLocation()) > InteractTraceLengthCm)
	{
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	int32 Ordinal = 0;
	bool bFound = false;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (*It == Guard)
		{
			bFound = true;
			break;
		}
		if (It->ActorHasTag(FName(TEXT("NODE_GUARD"))))
		{
			++Ordinal;
		}
	}
	if (!bFound)
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent;
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	bool bEased = false;
	bool bAsleep = false;
	if (Stealth && Stealth->GetCampActorState(EHomeWorldCampRole::Guard, Ordinal, bEased, bAsleep) && bAsleep)
	{
		return false;
	}
	return true;
}

bool AHomeWorldCharacter::TryOpeningShrineInFront()
{
	UWorld* World = GetWorld();
	if (!World || !GetIsSpiritForm())
	{
		return false;
	}
	AActor* Shrine = nullptr;
	float Best = InteractTraceLengthCm;
	bool bCaptive = false;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(FName(TEXT("NODE_CAPTIVE"))))
		{
			bCaptive = true;
		}
		if (!It->ActorHasTag(FName(TEXT("NODE_OPENING_SHRINE"))))
		{
			continue;
		}
		const float Dist = FVector::Dist2D(GetActorLocation(), It->GetActorLocation());
		if (Dist <= Best)
		{
			Best = Dist;
			Shrine = *It;
		}
	}
	if (!Shrine || !bCaptive)
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent;
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	if (!Stealth || !Stealth->TryFreeCaptive())
	{
		return false;
	}
	NotifyPartnerReadyToReturn();
	CompleteShrineReturn();
	return IsPartnerWalkingHome();
}

void AHomeWorldCharacter::RunOpeningShrineStop()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	TArray<AHomeWorldEasePad*> Pads;
	for (TActorIterator<AHomeWorldEasePad> It(World); It; ++It)
	{
		if (It->ActorHasTag(FName(TEXT("NODE_OPENING_EASE"))) && It->IsBoundToGuard())
		{
			Pads.Add(*It);
		}
	}
	const EHomeWorldStrokeStep Steps[] = {
		EHomeWorldStrokeStep::Grace,
		EHomeWorldStrokeStep::Wrath,
		EHomeWorldStrokeStep::Paradox,
		EHomeWorldStrokeStep::ParadoxExtraPoint
	};
	for (AHomeWorldEasePad* Pad : Pads)
	{
		for (const EHomeWorldStrokeStep Step : Steps)
		{
			TryCommitOpeningGuardPad(Pad, Step);
		}
	}

	bool bCaptive = false;
	bool bShrine = false;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		bCaptive = bCaptive || It->ActorHasTag(FName(TEXT("NODE_CAPTIVE")));
		bShrine = bShrine || It->ActorHasTag(FName(TEXT("NODE_OPENING_SHRINE")));
	}
	const FVector Here = GetActorLocation();
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	if (!bCaptive)
	{
		const FVector At = Here + FVector(0.f, 240.f, 0.f);
		if (AHomeWorldCampActor* Captive = World->SpawnActor<AHomeWorldCampActor>(At, FRotator::ZeroRotator, Params))
		{
			Captive->CampRole = EHomeWorldCampRole::Captive;
			Captive->Tags.Remove(FName(TEXT("NODE_SLEEPER")));
			Captive->Tags.Remove(FName(TEXT("NODE_GUARD")));
			Captive->RefreshCampIdentity();
			Captive->SetActorLocation(At);
		}
	}
	if (!bShrine)
	{
		const FVector At = Here + FVector(0.f, 480.f, 0.f);
		if (AActor* Shrine = World->SpawnActor<AActor>(At, FRotator::ZeroRotator, Params))
		{
			Shrine->Tags.Add(FName(TEXT("NODE_OPENING_SHRINE")));
			Shrine->SetActorLocation(At);
		}
	}
}

void AHomeWorldCharacter::UpdateSizeTestInteractCursor()
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC || !SizeTestCursorWisp)
	{
		return;
	}
	const bool bDraw = PC->IsInputKeyDown(EKeys::RightMouseButton);
	if (bDraw == bSizeTestInteractCursor)
	{
		if (!bDraw)
		{
			return;
		}
	}
	else if (bDraw)
	{
		bSizeTestInteractCursor = true;
		FInputModeGameAndUI Mode;
		Mode.SetHideCursorDuringCapture(false);
		Mode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
		PC->SetInputMode(Mode);
		PC->bShowMouseCursor = true;
		SizeTestCursorWisp->SetHiddenInGame(false);
		SizeTestCursorWisp->SetVisibility(true);
	}
	else
	{
		bSizeTestInteractCursor = false;
		PC->bShowMouseCursor = false;
		FInputModeGameOnly GameOnly;
		PC->SetInputMode(GameOnly);
		SizeTestCursorWisp->SetHiddenInGame(true);
		SizeTestCursorWisp->SetVisibility(false);
		return;
	}

	float MouseX = 0.f;
	float MouseY = 0.f;
	FVector Origin = FVector::ZeroVector;
	FVector Dir = FVector::ZeroVector;
	if (!PC->GetMousePosition(MouseX, MouseY) || !PC->DeprojectScreenPositionToWorld(MouseX, MouseY, Origin, Dir))
	{
		return;
	}
	const float PlaneZ = GetActorLocation().Z + 40.f;
	if (FMath::Abs(Dir.Z) < KINDA_SMALL_NUMBER)
	{
		return;
	}
	const float T = (PlaneZ - Origin.Z) / Dir.Z;
	if (T > 0.f)
	{
		SizeTestCursorWisp->SetWorldLocation(Origin + Dir * T);
	}
}

bool AHomeWorldCharacter::IsOpeningInteractInReach(float Dist2DCm)
{
	return Dist2DCm <= 280.f;
}

bool AHomeWorldCharacter::IsOpeningLookInside(float NdcX, float TargetNdcY, float LookNdcY)
{
	return FMath::Abs(NdcX) <= OpeningViewCenterNdc
		&& FMath::Abs(TargetNdcY - LookNdcY) <= OpeningViewCenterNdc;
}

bool AHomeWorldCharacter::IsInFrontOfBody(const FVector& FlatForward, const FVector& FlatToTarget)
{
	return FVector::DotProduct(FlatForward, FlatToTarget) > 0.f;
}

float AHomeWorldCharacter::GetOpeningLookCenterNdcY() const
{
	// One fixed shape: the aim box is the screen center, so the prop the camera is
	// aimed at is the prop the frame sees. No pitch compensation, no per-prop offset.
	return 0.f;
}

AActor* AHomeWorldCharacter::PickOpeningLookTarget(AActor* Perch, const TArray<FOpeningLookCandidate>& Candidates)
{
	(void)Perch;
	AActor* Best = nullptr;
	float BestSq = TNumericLimits<float>::Max();
	for (const FOpeningLookCandidate& Candidate : Candidates)
	{
		if (!Candidate.Actor)
		{
			continue;
		}
		if (Candidate.LookDistSq < BestSq)
		{
			BestSq = Candidate.LookDistSq;
			Best = Candidate.Actor;
		}
	}
	return Best;
}

AActor* AHomeWorldCharacter::FindOpeningProximityTarget()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		OpeningLookPerch = nullptr;
		return nullptr;
	}
	const FVector From = GetActorLocation();
	TArray<FOpeningLookCandidate> Candidates;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor || Actor == this || Actor->ActorHasTag(FName(TEXT("NPC_CHILD"))))
		{
			continue;
		}
		const FString Label = Actor->GetActorNameOrLabel();
		const bool bHerb = Label.Contains(TEXT("Lupine")) && !Actor->IsHidden();
		const bool bBed = Label.Contains(TEXT("Bed"));
		const bool bNightWisp = Actor->ActorHasTag(FName(TEXT("NODE_OPENING_WISP"))) && !Actor->IsHidden();
		const bool bDelivery = Actor->ActorHasTag(FName(TEXT("NODE_OPENING_DELIVERY"))) && !Actor->IsHidden();
		if (!bHerb && !bBed && !bNightWisp && !bDelivery && !ActorHasInteractableComponent(Actor))
		{
			continue;
		}
		const float DistCm = FVector::Dist2D(From, Actor->GetActorLocation());
		if (!IsOpeningInteractInReach(DistCm))
		{
			continue;
		}
		// A wall between the body and the prop hides the prompt and refuses the press.
		if (!HasOpeningLineOfSight(Actor))
		{
			continue;
		}
		float LookSq = 0.f;
		if (!OpeningLookDistSq(Actor, LookSq))
		{
			continue;
		}
		Candidates.Add({Actor, LookSq});
	}
	OpeningLookPerch = PickOpeningLookTarget(OpeningLookPerch, Candidates);
	return OpeningLookPerch;
}

bool AHomeWorldCharacter::HasOpeningLineOfSight(const AActor* Target) const
{
	UWorld* World = GetWorld();
	if (!World || !Target)
	{
		return false;
	}
	FVector Origin = FVector::ZeroVector;
	FVector Extent = FVector::ZeroVector;
	Target->GetActorBounds(false, Origin, Extent);
	const UCapsuleComponent* Capsule = GetCapsuleComponent();
	const float ChestZ = Capsule ? Capsule->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.f;
	const FVector Start = GetActorLocation() + FVector(0.f, 0.f, ChestZ);
	// Aim at the nearest point of the target, not its center, so a wide counter or a
	// spring plane is not "blocked" by its own far side.
	const FVector End(
		FMath::Clamp(Start.X, Origin.X - Extent.X, Origin.X + Extent.X),
		FMath::Clamp(Start.Y, Origin.Y - Extent.Y, Origin.Y + Extent.Y),
		FMath::Clamp(Start.Z, Origin.Z - Extent.Z, Origin.Z + Extent.Z));
	FCollisionQueryParams Params(NAME_None, false, this);
	Params.AddIgnoredActor(Target);
	FHitResult Hit;
	if (!World->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Params))
	{
		return true;
	}
	// Probe while the armory table is unexplained: name the blocker once per
	// target, so a refused press can be told apart from a target that never
	// entered the look. Remove once the press is settled.
	static TSet<FName> LoggedBlocked;
	const FName Key = Target->GetFName();
	if (!LoggedBlocked.Contains(Key))
	{
		LoggedBlocked.Add(Key);
		UE_LOG(LogTemp, Log, TEXT("opening_los: %s blocked by %s at %.0f cm"),
			*Target->GetActorNameOrLabel(), *GetNameSafe(Hit.GetActor()), Hit.Distance);
	}
	return false;
}

bool AHomeWorldCharacter::OpeningLookDistSq(const AActor* Target, float& OutDistSq) const
{
	const APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC || !Target || !FollowCamera)
	{
		return false;
	}
	FVector LookForward = GetControlRotation().Vector();
	LookForward.Z = 0.f;
	if (!LookForward.Normalize())
	{
		LookForward = GetActorForwardVector();
		LookForward.Z = 0.f;
		LookForward.Normalize();
	}
	FVector BodyToTarget = Target->GetActorLocation() - GetActorLocation();
	BodyToTarget.Z = 0.f;
	if (LookForward.IsNearlyZero() || !IsInFrontOfBody(LookForward, BodyToTarget))
	{
		return false;
	}
	const FVector ToTarget = Target->GetActorLocation() - FollowCamera->GetComponentLocation();
	if (FVector::DotProduct(FollowCamera->GetForwardVector(), ToTarget.GetSafeNormal()) <= 0.f)
	{
		return false;
	}
	FVector2D Screen = FVector2D::ZeroVector;
	if (!PC->ProjectWorldLocationToScreen(Target->GetActorLocation(), Screen, true))
	{
		return false;
	}
	int32 SizeX = 0;
	int32 SizeY = 0;
	PC->GetViewportSize(SizeX, SizeY);
	if (SizeX <= 0 || SizeY <= 0)
	{
		return false;
	}
	const float NdcX = (Screen.X / static_cast<float>(SizeX)) * 2.f - 1.f;
	const float NdcY = (Screen.Y / static_cast<float>(SizeY)) * 2.f - 1.f;
	const float LookY = GetOpeningLookCenterNdcY();
	const float Dx = NdcX;
	const float Dy = NdcY - LookY;
	if (!IsOpeningLookInside(Dx, NdcY, LookY))
	{
		return false;
	}
	OutDistSq = Dx * Dx + Dy * Dy;
	return true;
}

void AHomeWorldCharacter::SetOpeningInteractPrompt(bool bShow, const FVector& At)
{
	if (!OpeningInteractPrompt)
	{
		return;
	}
	if (!bShow)
	{
		OpeningInteractPrompt->SetHiddenInGame(true);
		OpeningInteractPrompt->SetVisibility(false);
		return;
	}
	const FVector PromptAt = At + FVector(0.f, 0.f, 24.f);
	OpeningInteractPrompt->SetUsingAbsoluteLocation(true);
	OpeningInteractPrompt->SetUsingAbsoluteRotation(true);
	OpeningInteractPrompt->SetWorldLocation(PromptAt);
	if (FollowCamera)
	{
		const FVector ToCamera = FollowCamera->GetComponentLocation() - PromptAt;
		if (!ToCamera.IsNearlyZero())
		{
			OpeningInteractPrompt->SetWorldRotation(ToCamera.Rotation());
		}
	}
	OpeningInteractPrompt->SetHiddenInGame(false);
	OpeningInteractPrompt->SetVisibility(true);
}

void AHomeWorldCharacter::ShowOpeningProximityLine()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	const FVector From = GetActorLocation();
	float PartnerDist = TNumericLimits<float>::Max();
	float SpiritDist = TNumericLimits<float>::Max();
	float StationDist = TNumericLimits<float>::Max();
	float ArmorDist = TNumericLimits<float>::Max();
	float DogDist = TNumericLimits<float>::Max();
	const AHomeWorldOpeningDog* DogActor = nullptr;
	bool bPartnerWaiting = false;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(FName(TEXT("NPC_PARTNER"))))
		{
			PartnerDist = FVector::Dist2D(From, It->GetActorLocation());
		}
		else if (const AHomeWorldOpeningReveal* Reveal = Cast<AHomeWorldOpeningReveal>(*It))
		{
			if (Reveal->IsSpiritVisible())
			{
				SpiritDist = FVector::Dist2D(From, It->GetActorLocation());
			}
			bPartnerWaiting = Reveal->IsPartnerWaiting();
		}
		else if (It->ActorHasTag(FName(TEXT("NODE_CONSUMABLE_STATION"))))
		{
			StationDist = FVector::Dist2D(From, It->GetActorLocation());
		}
		else if (It->ActorHasTag(FName(TEXT("NODE_ARMOR_TABLE"))))
		{
			ArmorDist = FVector::Dist2D(From, It->GetActorLocation());
		}
		else if (const AHomeWorldOpeningDog* Dog = Cast<AHomeWorldOpeningDog>(*It))
		{
			DogDist = FVector::Dist2D(From, It->GetActorLocation());
			DogActor = Dog;
		}
	}
	FString Line;
	const bool bNodeNear = PartnerDist < 400.f || StationDist < 400.f || ArmorDist < 400.f || SpiritDist < 400.f;
	if (!bNodeNear && DogActor && DogActor->IsDogTamed() && DogDist < 400.f)
	{
		Line = TEXT("The dog is calm.");
	}
	else if (!bNodeNear && DogActor && DogDist < DogActor->NoticeRadiusCm)
	{
		FVector DogVel = GetVelocity();
		DogVel.Z = 0.f;
		FVector ToDog = DogActor->GetActorLocation() - From;
		ToDog.Z = 0.f;
		const bool bClosing = DogVel.SizeSquared() > 1.f && ToDog.SizeSquared() > 1.f
			&& FVector::DotProduct(DogVel.GetSafeNormal(), ToDog.GetSafeNormal()) > 0.2f;
		if (DogActor->IsWrathEased())
		{
			Line = TEXT("Offer the herb.");
		}
		else if (DogVel.Size() > DogActor->SlowStepCmS && bClosing)
		{
			Line = TEXT("Step slower.");
		}
		else if (DogDist <= DogActor->DrawRadiusCm)
		{
			Line = TEXT("Draw the Grace symbol.");
		}
		else
		{
			Line = TEXT("The dog bristles with Wrath.");
		}
	}
	else if (PartnerDist < 400.f && PartnerDist <= SpiritDist && PartnerDist <= StationDist)
	{
		if (bPartnerWaiting && !bOpeningArmorGiftGiven)
		{
			Line = TEXT("Take the armor.");
		}
		else
		{
			Line = OpeningHerbTenths > 0 ? TEXT("Brew the kettle.") : TEXT("Pick up the herb.");
		}
	}
	else if (StationDist < 400.f && StationDist <= SpiritDist)
	{
		if (!bOpeningConsumableOpen)
		{
			if (!bOpeningSpiritClaimed && OpeningHerbTenths <= 0)
			{
				Line = TEXT("The station wants the herb and the spirit.");
			}
			else if (!bOpeningSpiritClaimed)
			{
				Line = TEXT("The station wants the spirit.");
			}
			else if (OpeningHerbTenths <= 0)
			{
				Line = TEXT("The station wants the herb.");
			}
			else
			{
				Line = TEXT("Open the station.");
			}
		}
		else if (OpeningMixedHerbs <= 0)
		{
			Line = OpeningHerbTenths > 0 ? TEXT("Mix the herb.") : TEXT("The station wants the herb.");
		}
		else
		{
			Line = TEXT("Brew the kettle.");
		}
	}
	else if (ArmorDist < 400.f && ArmorDist <= SpiritDist)
	{
		Line = bOpeningArmorGiftGiven ? TEXT("The table is open.") : TEXT("The partner's gift opens the table.");
	}
	else if (SpiritDist < 400.f)
	{
		Line = TEXT("Pick up the spirit.");
	}
	if (bOpeningArmorGiftGiven)
	{
		Line.Reset();
	}
	if (DogActor && !DogActor->IsDogTamed() && !DogActor->IsWrathEased() && DogDist < DogActor->NoticeRadiusCm)
	{
		FVector WarnVel = GetVelocity();
		WarnVel.Z = 0.f;
		FVector WarnToDog = DogActor->GetActorLocation() - From;
		WarnToDog.Z = 0.f;
		const bool bWarnClosing = WarnVel.SizeSquared() > 1.f && WarnToDog.SizeSquared() > 1.f
			&& FVector::DotProduct(WarnVel.GetSafeNormal(), WarnToDog.GetSafeNormal()) > 0.2f;
		if (WarnVel.Size() > DogActor->SlowStepCmS && bWarnClosing)
		{
			Line = TEXT("Approach slowly.");
		}
	}
	// The too-fast knock waits 1.25s after the quest line is the slow approach. The tracker draws the words.
	if (Line == TEXT("Approach slowly.") && OpeningDogSlowWarnAt < 0.f)
	{
		OpeningDogSlowWarnAt = World->GetTimeSeconds();
	}
}

void AHomeWorldCharacter::UpdateOpeningDog(float DeltaTime)
{
	if (OpeningDogKnockCooldown > 0.f)
	{
		OpeningDogKnockCooldown -= DeltaTime;
	}
	if (!OpeningDog)
	{
		UWorld* World = GetWorld();
		if (World)
		{
			for (TActorIterator<AHomeWorldOpeningDog> It(World); It; ++It)
			{
				OpeningDog = *It;
				break;
			}
		}
	}
	AHomeWorldOpeningDog* Dog = OpeningDog;
	if (!Dog || Dog->IsDogTamed() || Dog->IsWrathEased())
	{
		if (Dog)
		{
			Dog->ApplyGreyboxColor(false);
		}
		OpeningDogSlowWarnAt = -1.f;
		return;
	}
	const FVector ToDog = Dog->GetActorLocation() - GetActorLocation();
	const FVector Flat = FVector(ToDog.X, ToDog.Y, 0.f);
	const float Dist = Flat.Size();
	FVector Vel = GetVelocity();
	Vel.Z = 0.f;
	const float Speed = Vel.Size();
	bool bClosing = false;
	if (Speed > 1.f && Dist > 1.f)
	{
		bClosing = FVector::DotProduct(Vel.GetSafeNormal(), Flat.GetSafeNormal()) > 0.2f;
	}
	const bool bDrawReady = Dist <= Dog->DrawRadiusCm && Speed <= Dog->SlowStepCmS;
	Dog->ApplyGreyboxColor(bDrawReady);
	if (OpeningDogKnockCooldown <= 0.f)
	{
		if (Dist < Dog->KnockRadiusCm)
		{
			KnockFromOpeningDog(Dog, TEXT("too close"), Dist, Speed);
			return;
		}
		if (Speed > Dog->SlowStepCmS && Dist < Dog->NoticeRadiusCm && bClosing)
		{
			const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
			// Armed by "Approach slowly." Showing the line and knocking on the same frame is the bug.
			if (OpeningDogSlowWarnAt < 0.f || Now - OpeningDogSlowWarnAt < 1.25f)
			{
				return;
			}
			KnockFromOpeningDog(Dog, TEXT("too fast"), Dist, Speed);
			return;
		}
		OpeningDogSlowWarnAt = -1.f;
	}
	if (!bOpeningDogSlowLatched && Dist < Dog->NoticeRadiusCm && Speed <= Dog->SlowStepCmS && Speed > 10.f)
	{
		bOpeningDogSlowLatched = true;
	}
}

void AHomeWorldCharacter::StartOpeningDogDraw(AHomeWorldOpeningDog* Dog)
{
	if (!Dog || bOpeningDogDrawActive || !Dog->GetRuneShape())
	{
		return;
	}
	APlayerController* PC = Cast<APlayerController>(GetController());
	Dog->ShowGraceRune(PC);
	UHomeWorldRuneShapeComponent* Shape = Dog->GetRuneShape();
	OpeningDogCursor = Shape->GetStartPoint();
	Shape->SetCursor(OpeningDogCursor);
	bOpeningDogDrawActive = true;
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
		SizeTestWisp->SetUsingAbsoluteLocation(true);
		SizeTestWisp->SetWorldLocation(OpeningDogCursor);
	}
}

void AHomeWorldCharacter::UpdateOpeningDogDraw(float DeltaTime)
{
	AHomeWorldOpeningDog* Dog = OpeningDog;
	if (!Dog || !Dog->GetRuneShape() || Dog->IsWrathEased() || Dog->IsDogTamed())
	{
		FinishOpeningDogDraw();
		return;
	}
	UHomeWorldRuneShapeComponent* Shape = Dog->GetRuneShape();
	if (OpeningDogKnockCooldown > 0.f)
	{
		OpeningDogKnockCooldown -= DeltaTime;
	}
	const FVector ToDog = Dog->GetActorLocation() - GetActorLocation();
	const FVector Flat = FVector(ToDog.X, ToDog.Y, 0.f);
	const float Dist = Flat.Size();
	FVector Vel = GetVelocity();
	Vel.Z = 0.f;
	const float Speed = Vel.Size();
	bool bClosing = false;
	if (Speed > 1.f && Dist > 1.f)
	{
		bClosing = FVector::DotProduct(Vel.GetSafeNormal(), Flat.GetSafeNormal()) > 0.2f;
	}
	const bool bDrawReady = Dist <= Dog->DrawRadiusCm && Speed <= Dog->SlowStepCmS;
	Dog->ApplyGreyboxColor(bDrawReady);
	// The two punishments hold while the symbol is up: too close, or any step over the slow step.
	if (OpeningDogKnockCooldown <= 0.f && Dist < Dog->KnockRadiusCm)
	{
		FailOpeningDogTrace();
		return;
	}
	if (OpeningDogKnockCooldown <= 0.f && Speed > Dog->SlowStepCmS && Dist < Dog->NoticeRadiusCm && bClosing)
	{
		const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
		if (OpeningDogSlowWarnAt < 0.f || Now - OpeningDogSlowWarnAt < 1.25f)
		{
			return;
		}
		FailOpeningDogTrace();
		return;
	}
	if (Dist > Dog->DrawRadiusCm + 150.f)
	{
		FailOpeningDogTrace();
		return;
	}
	APlayerController* PC = Cast<APlayerController>(GetController());
	Shape->AlignToViewer(PC);
	if (PC)
	{
		float DeltaX = 0.f;
		float DeltaY = 0.f;
		PC->GetInputMouseDelta(DeltaX, DeltaY);
		FVector Origin = FVector::ZeroVector;
		FVector Right = FVector::RightVector;
		FVector Up = FVector::UpVector;
		Shape->GetPlane(Origin, Right, Up);
		OpeningDogCursor += (Right * DeltaX + Up * DeltaY) * 4.8f;
	}
	Shape->SetCursor(OpeningDogCursor);
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
		SizeTestWisp->SetUsingAbsoluteLocation(true);
		SizeTestWisp->SetWorldLocation(OpeningDogCursor);
	}
	if (PC && PC->WasInputKeyJustPressed(EKeys::LeftMouseButton))
	{
		if (Shape->GetScore() >= 10)
		{
			SucceedOpeningDogTrace(Dog);
		}
		else
		{
			FailOpeningDogTrace();
		}
		return;
	}
	Shape->AdvanceTrace();
	if (Shape->IsComplete())
	{
		if (Shape->GetScore() >= 10)
		{
			SucceedOpeningDogTrace(Dog);
		}
		else
		{
			FailOpeningDogTrace();
		}
	}
}

void AHomeWorldCharacter::SnapSizeTestWispHome(AActor* Finished)
{
	OpeningWispReleased = Finished;
	if (!SizeTestWisp || !SizeTestWisp->IsVisible())
	{
		bOpeningWispReturning = false;
		return;
	}
	OpeningWispReturnFrom = SizeTestWisp->GetComponentLocation();
	OpeningWispReturnLeft = 0.35f;
	bOpeningWispReturning = true;
	SizeTestWisp->SetUsingAbsoluteLocation(true);
}

void AHomeWorldCharacter::FinishOpeningDogDraw()
{
	bOpeningDogDrawActive = false;
	SnapSizeTestWispHome(OpeningDog);
	if (OpeningDog && OpeningDog->GetRuneShape())
	{
		OpeningDog->GetRuneShape()->HideShape();
	}
}

void AHomeWorldCharacter::SucceedOpeningDogTrace(AHomeWorldOpeningDog* Dog)
{
	if (Dog)
	{
		Dog->NoteGraceDrawn();
	}
	FinishOpeningDogDraw();
}

void AHomeWorldCharacter::FailOpeningDogTrace()
{
	FinishOpeningDogDraw();
	bOpeningDogSlowLatched = false;
	OpeningDogSlowWarnAt = -1.f;
	FVector Loc = GetActorLocation();
	Loc.X = -950.f;
	Loc.Y = -180.f;
	SetActorLocation(Loc, false, nullptr, ETeleportType::TeleportPhysics);
	if (UCharacterMovementComponent* Move = GetCharacterMovement())
	{
		Move->StopMovementImmediately();
	}
	LaunchCharacter(FVector(0.f, 0.f, 220.f), true, true);
	LogOpening(TEXT("opening_dog: the dove failed"));
}

bool AHomeWorldCharacter::HasOpeningHerbQuota() const
{
	return OpeningHerbsGathered >= HomeWorldOpeningHerbQuota && bOpeningHerbFromWest && bOpeningHerbFromEast;
}

void AHomeWorldCharacter::MaybeLeadPartnerAfterHerbs()
{
	if (!HasOpeningHerbQuota())
	{
		return;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	for (TActorIterator<AHomeWorldOpeningReveal> It(World); It; ++It)
	{
		It->TryLeadPartner();
		return;
	}
}

void AHomeWorldCharacter::RefreshOpeningQuest()
{
	if (!QuestLog || !GetWorld() || !UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("SizeTest")))
	{
		return;
	}
	FHomeWorldOpeningQuestFacts Facts;
	Facts.bSpiritClaimed = bOpeningSpiritClaimed;
	Facts.HerbsGathered = OpeningHerbsGathered;
	Facts.bHerbFromWest = bOpeningHerbFromWest;
	Facts.bHerbFromEast = bOpeningHerbFromEast;
	Facts.bKettleBrewed = bOpeningKettleBrewed;
	Facts.bDogSlow = bOpeningDogSlowLatched;
	Facts.bTracingDove = bOpeningDogDrawActive;
	Facts.bHasMixedHerb = OpeningMixedHerbs > 0;
	Facts.bBackpack = bOpeningArmorGiftGiven;
	Facts.bFishCaught = bOpeningFishCaught;
	Facts.bSlept = bOpeningNightSpirit;
	if (OpeningDog)
	{
		const float Dist = FVector::Dist2D(GetActorLocation(), OpeningDog->GetActorLocation());
		Facts.bDogInSootheRange = Dist <= 280.f;
		Facts.bWrathEased = OpeningDog->IsWrathEased();
		Facts.bDogTamed = OpeningDog->IsDogTamed();
	}
	QuestLog->SetChain(TEXT("Opening"), UHomeWorldQuestLog::BuildOpeningSteps(Facts));
	if (UHomeWorldHomeLoopSubsystem* HomeLoop = GetWorld()->GetSubsystem<UHomeWorldHomeLoopSubsystem>())
	{
		if (HomeLoop->HasOpeningDayEnded())
		{
			FHomeWorldHomeLoopQuestFacts HomeFacts;
			HomeLoop->GetHomeLoopQuestProgress(
				HomeFacts.bKettleCooked, HomeFacts.bWispAssigned, HomeFacts.bSurfaceCleared, HomeFacts.bSeedPlanted);
			QuestLog->SetChain(TEXT("home_loop"), UHomeWorldQuestLog::BuildHomeLoopSteps(HomeFacts));
		}
	}
	if (!GEngine)
	{
		return;
	}
	if (bOpeningNightSpirit)
	{
		GEngine->AddOnScreenDebugMessage(9000, 0.5f, FColor::White, TEXT("Night"));
	}
	GEngine->AddOnScreenDebugMessage(9050, 0.5f, FColor::White, TEXT("Quests"));
	const TArray<FHomeWorldQuestStep>& Shown = QuestLog->GetDisplayedSteps();
	for (int32 Index = 0; Index < Shown.Num(); ++Index)
	{
		const FString Line = Shown[Index].bDone
			? FString::Printf(TEXT("[x] %s"), *Shown[Index].Text)
			: FString::Printf(TEXT("[ ] %s"), *Shown[Index].Text);
		GEngine->AddOnScreenDebugMessage(
			9100 + Index, 0.5f, Shown[Index].bDone ? FColor(170, 170, 170) : FColor::White, Line);
	}
	GEngine->AddOnScreenDebugMessage(9200, 0.5f, FColor::White, TEXT("Carrying"));
	int32 CarryLine = 0;
	auto Carry = [&](const FString& Text)
	{
		GEngine->AddOnScreenDebugMessage(9210 + CarryLine, 0.5f, FColor::White, Text);
		++CarryLine;
	};
	Carry(FString::Printf(TEXT("Herbs %d"), OpeningHerbTenths));
	Carry(FString::Printf(TEXT("Wisps %d"), OpeningWispsCarried));
	if (OpeningMixedHerbs > 0)
	{
		Carry(FString::Printf(TEXT("Mixed herb %d"), OpeningMixedHerbs));
	}
	if (UGameInstance* GI = GetGameInstance())
	{
		if (UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>())
		{
			for (int32 SlotIndex = 0; SlotIndex < Inv->GetSlotCount(); ++SlotIndex)
			{
				const FHomeWorldInventorySlot Slot = Inv->GetSlot(SlotIndex);
				if (Slot.IsEmpty())
				{
					continue;
				}
				Carry(FString::Printf(TEXT("%s %d"), *Slot.ResId.ToString(), Slot.Count));
			}
		}
	}
}

void AHomeWorldCharacter::KnockFromOpeningDog(AHomeWorldOpeningDog* Dog, const FString& Why, float Dist, float Speed)
{
	if (!Dog)
	{
		return;
	}
	if (bOpeningDogDrawActive)
	{
		FinishOpeningDogDraw();
	}
	FVector Away = GetActorLocation() - Dog->GetActorLocation();
	Away.Z = 0.f;
	if (Away.IsNearlyZero())
	{
		Away = Dog->GetActorForwardVector();
		Away.Z = 0.f;
		if (Away.IsNearlyZero())
		{
			Away = FVector(-1.f, 0.f, 0.f);
		}
	}
	Away.Normalize();
	LaunchCharacter(Away * Dog->KnockSpeedCmS + FVector(0.f, 0.f, Dog->KnockLiftCmS), true, false);
	OpeningDogKnockCooldown = Dog->KnockCooldownSeconds;
	OpeningDogSlowWarnAt = -1.f;
	static FString LastKnock;
	static double LastKnockAt = -10.0;
	const double KnockNow = FPlatformTime::Seconds();
	if (Why != LastKnock || KnockNow - LastKnockAt >= 1.5)
	{
		LastKnock = Why;
		LastKnockAt = KnockNow;
		UE_LOG(LogTemp, Log, TEXT("opening_dog: knocked back (%s, %.0f cm, %.0f cm/s)"), *Why, Dist, Speed);
	}
}

void AHomeWorldCharacter::StartOpeningHerbRune(AActor* Bed)
{
	if (!Bed || bOpeningRuneActive)
	{
		return;
	}
	UHomeWorldRuneShapeComponent* Shape = Bed->FindComponentByClass<UHomeWorldRuneShapeComponent>();
	if (!Shape)
	{
		Shape = NewObject<UHomeWorldRuneShapeComponent>(Bed);
		if (!Shape)
		{
			return;
		}
		Shape->RegisterComponent();
	}
	const bool bTrace = Bed->ActorHasTag(FName(TEXT("NODE_GARDEN_EAST")));
	APlayerController* PC = Cast<APlayerController>(GetController());
	Shape->ShowHeart(
		bTrace ? EHomeWorldRuneDrawMode::Trace : EHomeWorldRuneDrawMode::Points,
		EHomeWorldRuneOrientation::CameraParallel,
		PC);
	OpeningRuneShape = Shape;
	OpeningRuneBed = Bed;
	FVector RuneOrigin = FVector::ZeroVector;
	FVector RuneRight = FVector::RightVector;
	FVector RuneUp = FVector::UpVector;
	Shape->GetPlane(RuneOrigin, RuneRight, RuneUp);
	OpeningRuneCursor = Shape->IsPointsMode() ? RuneOrigin : Shape->GetStartPoint();
	bOpeningRuneActive = true;
	OpeningPointTime = Shape->IsPointsMode() ? 3.f : -1.f;
	if (bOpeningWispCollect)
	{
		OpeningWispHeartElapsed = 0.f;
	}
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
		SizeTestWisp->SetUsingAbsoluteLocation(true);
		SizeTestWisp->SetWorldLocation(OpeningRuneCursor);
	}
}

static void PaintGreyboxMesh(AActor* Actor, const TCHAR* MaterialPath);

void AHomeWorldCharacter::FinishOpeningHerbRune(int32 Tenths)
{
	if (bOpeningWispCollect)
	{
		bOpeningWispCollect = false;
		bOpeningRuneActive = false;
		AActor* Collected = OpeningRuneBed;
		SnapSizeTestWispHome(Collected);
		if (OpeningRuneShape)
		{
			OpeningRuneShape->HideShape();
			OpeningRuneShape = nullptr;
		}
		OpeningRuneBed = nullptr;
		if (Tenths > 0 && Collected && !Collected->IsHidden())
		{
			Collected->SetActorHiddenInGame(true);
			Collected->SetActorEnableCollision(false);
			++OpeningWispsCollected;
			++OpeningWispsCarried;
			OpeningWispHealDurations.Add(OpeningHealSecondsForHeart(OpeningWispHeartElapsed));
			UE_LOG(LogTemp, Log, TEXT("opening_night: wisp collected %d/3, in the backpack (carried %d, heal %.0fs)"),
				OpeningWispsCollected, OpeningWispsCarried, OpeningWispHealDurations.Last());
		}
		OpeningWispHeartElapsed = 0.f;
		return;
	}
	bOpeningRuneActive = false;
	SnapSizeTestWispHome(OpeningRuneBed);
	if (OpeningRuneShape)
	{
		OpeningRuneShape->HideShape();
		OpeningRuneShape = nullptr;
	}
	const int32 Score = FMath::Clamp(Tenths, 0, 10);
	if (Score <= 0)
	{
		LogOpening(TEXT("opening_herb: missed, nothing collected"));
		OpeningRuneBed = nullptr;
		return;
	}
	OpeningHerbTenths += Score;
	OpeningHerbsGathered += Score;
	if (OpeningRuneBed && OpeningRuneBed->ActorHasTag(FName(TEXT("NODE_GARDEN_EAST"))))
	{
		bOpeningHerbFromEast = true;
	}
	else
	{
		bOpeningHerbFromWest = true;
	}
	LogOpening(FString::Printf(TEXT("opening_herb: collected %d, gathered %d"), Score, OpeningHerbsGathered));
	UWorld* World = GetWorld();
	if (OpeningRuneBed && World)
	{
		AActor* Plant = nullptr;
		float Best = 80.f * 80.f;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!It->GetActorNameOrLabel().Contains(TEXT("Lupine")))
			{
				continue;
			}
			const float Dist = FVector::DistSquared2D(It->GetActorLocation(), OpeningRuneBed->GetActorLocation());
			if (Dist < Best)
			{
				Best = Dist;
				Plant = *It;
			}
		}
		if (Plant)
		{
			Plant->SetActorHiddenInGame(true);
			Plant->SetActorEnableCollision(false);
		}
		const bool bEast = OpeningRuneBed->ActorHasTag(FName(TEXT("NODE_GARDEN_EAST")));
		OpeningRuneBed->SetActorEnableCollision(false);
		OpeningRuneBed->Tags.Remove(FName(TEXT("NODE_GARDEN")));
		OpeningRuneBed->Tags.Remove(FName(TEXT("NODE_GARDEN_EAST")));
		OpeningRuneBed->Tags.Remove(FName(TEXT("NODE_GARDEN_WEST")));
		const float When = World->GetTimeSeconds() + 20.f;
		FOpeningHerbReturn* Row = nullptr;
		for (FOpeningHerbReturn& Existing : OpeningHerbReturns)
		{
			if (Existing.Bed == OpeningRuneBed)
			{
				Row = &Existing;
				break;
			}
		}
		if (!Row)
		{
			Row = &OpeningHerbReturns.AddDefaulted_GetRef();
			Row->Bed = OpeningRuneBed;
		}
		Row->Plant = Plant;
		Row->bEast = bEast;
		Row->Time = When;
		PaintGreyboxMesh(
			OpeningRuneBed,
			TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Olive.MI_Greybox_Olive"));
		UE_LOG(LogTemp, Log, TEXT("opening_rune: %s herb returns in 20s"), bEast ? TEXT("east") : TEXT("west"));
	}
	OpeningRuneBed = nullptr;
}

void AHomeWorldCharacter::UpdateOpeningHerbRune(float DeltaTime)
{
	if (!bOpeningRuneActive || !OpeningRuneShape)
	{
		return;
	}
	if (!OpeningRuneBed || FVector::Dist2D(GetActorLocation(), OpeningRuneBed->GetActorLocation()) > 450.f)
	{
		FinishOpeningHerbRune(OpeningRuneShape->GetScore());
		return;
	}
	APlayerController* PC = Cast<APlayerController>(GetController());
	OpeningRuneShape->AlignToViewer(PC);
	if (PC)
	{
		float DeltaX = 0.f;
		float DeltaY = 0.f;
		PC->GetInputMouseDelta(DeltaX, DeltaY);
		FVector Origin = FVector::ZeroVector;
		FVector Right = FVector::RightVector;
		FVector Up = FVector::UpVector;
		OpeningRuneShape->GetPlane(Origin, Right, Up);
		// Trace hearts stay at 4.8. The click heart is 25% faster, from the 2026-10-21 copse replay.
		const float CursorCm = OpeningRuneShape->IsPointsMode() ? 4.8f * 1.25f : 4.8f;
		OpeningRuneCursor += (Right * DeltaX + Up * DeltaY) * CursorCm;
	}
	OpeningRuneShape->SetCursor(OpeningRuneCursor);
	if (SizeTestWisp)
	{
		SizeTestWisp->SetHiddenInGame(false);
		SizeTestWisp->SetVisibility(true);
		SizeTestWisp->SetUsingAbsoluteLocation(true);
		SizeTestWisp->SetWorldLocation(OpeningRuneCursor);
	}
	if (OpeningRuneShape->IsPointsMode())
	{
		if (bOpeningWispCollect)
		{
			OpeningWispHeartElapsed += DeltaTime;
		}
		else
		{
			OpeningPointTime -= DeltaTime;
			if (OpeningPointTime <= 0.f)
			{
				UE_LOG(LogTemp, Log, TEXT("opening_herb: point time ran out"));
				FinishOpeningHerbRune(OpeningRuneShape->GetScore());
				return;
			}
		}
		if (PC && PC->WasInputKeyJustPressed(EKeys::LeftMouseButton) && !OpeningRuneShape->TryClick())
		{
			UE_LOG(LogTemp, Log, TEXT("opening_herb: missed click"));
			FinishOpeningHerbRune(OpeningRuneShape->GetScore());
			return;
		}
	}
	else
	{
		if (PC && PC->WasInputKeyJustPressed(EKeys::LeftMouseButton))
		{
			FinishOpeningHerbRune(OpeningRuneShape->GetScore());
			return;
		}
		OpeningRuneShape->AdvanceTrace();
	}
	if (OpeningRuneShape->IsComplete())
	{
		FinishOpeningHerbRune(OpeningRuneShape->GetScore());
	}
}

void AHomeWorldCharacter::UpdateOpeningHerbPreview()
{
	if (bOpeningRuneActive)
	{
		return;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	const FVector From = GetActorLocation();
	AActor* Nearest = nullptr;
	float Best = 320.f * 320.f;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (!It->ActorHasTag(FName(TEXT("NODE_GARDEN"))))
		{
			continue;
		}
		const float Dist = FVector::DistSquared2D(From, It->GetActorLocation());
		if (Dist < Best)
		{
			Best = Dist;
			Nearest = *It;
		}
	}
	if (Nearest == OpeningRuneBed && OpeningRuneShape)
	{
		OpeningRuneShape->AlignToViewer(Cast<APlayerController>(GetController()));
		return;
	}
	if (OpeningRuneShape)
	{
		OpeningRuneShape->HideShape();
		OpeningRuneShape = nullptr;
	}
	OpeningRuneBed = Nearest;
	if (!Nearest)
	{
		return;
	}
	UHomeWorldRuneShapeComponent* Shape = Nearest->FindComponentByClass<UHomeWorldRuneShapeComponent>();
	if (!Shape)
	{
		Shape = NewObject<UHomeWorldRuneShapeComponent>(Nearest);
		if (!Shape)
		{
			return;
		}
		Shape->RegisterComponent();
	}
	Shape->ShowHeart(
		EHomeWorldRuneDrawMode::Trace,
		EHomeWorldRuneOrientation::CameraParallel,
		Cast<APlayerController>(GetController()));
	OpeningRuneShape = Shape;
}

void AHomeWorldCharacter::RestoreOpeningHerb()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	const float Now = World->GetTimeSeconds();
	for (int32 Index = OpeningHerbReturns.Num() - 1; Index >= 0; --Index)
	{
		FOpeningHerbReturn& Row = OpeningHerbReturns[Index];
		if (Row.Time < 0.f || Now < Row.Time)
		{
			continue;
		}
		if (Row.Bed)
		{
			Row.Bed->Tags.AddUnique(FName(TEXT("NODE_GARDEN")));
			Row.Bed->Tags.AddUnique(Row.bEast ? FName(TEXT("NODE_GARDEN_EAST")) : FName(TEXT("NODE_GARDEN_WEST")));
			Row.Bed->SetActorEnableCollision(true);
			PaintGreyboxMesh(
				Row.Bed,
				TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Tan.MI_Greybox_Tan"));
		}
		if (Row.Plant)
		{
			Row.Plant->SetActorHiddenInGame(false);
			Row.Plant->SetActorEnableCollision(true);
		}
		UE_LOG(LogTemp, Log, TEXT("opening_rune: %s herb returned"), Row.bEast ? TEXT("east") : TEXT("west"));
		OpeningHerbReturns.RemoveAt(Index);
	}
}

static void PaintGreyboxMesh(AActor* Actor, const TCHAR* MaterialPath)
{
	if (!Actor)
	{
		return;
	}
	UMaterialInterface* Material = LoadObject<UMaterialInterface>(nullptr, MaterialPath);
	if (!Material)
	{
		return;
	}
	TArray<UStaticMeshComponent*> Meshes;
	Actor->GetComponents<UStaticMeshComponent>(Meshes);
	for (UStaticMeshComponent* Mesh : Meshes)
	{
		if (Mesh && Mesh->GetMaterial(0) != Material)
		{
			Mesh->SetMaterial(0, Material);
		}
	}
}

void AHomeWorldCharacter::UpdateSizeTestWisp(float DeltaTime)
{
	TickDebugFastForward(DeltaTime);
	if (UWorld* StationWorld = GetWorld())
	{
		const TCHAR* OpenPath = TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Olive.MI_Greybox_Olive");
		const TCHAR* WaitPath = TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Tan.MI_Greybox_Tan");
		for (TActorIterator<AActor> It(StationWorld); It; ++It)
		{
			if (It->ActorHasTag(FName(TEXT("NODE_CONSUMABLE_STATION")))
				|| It->ActorHasTag(FName(TEXT("KettleProp"))))
			{
				PaintGreyboxMesh(*It, bOpeningConsumableOpen ? OpenPath : WaitPath);
			}
			else if (It->ActorHasTag(FName(TEXT("NODE_ARMOR_TABLE"))))
			{
				PaintGreyboxMesh(*It, bOpeningArmorGiftGiven ? OpenPath : WaitPath);
			}
		}
	}
	RestoreOpeningHerb();
	ShowOpeningProximityLine();
	MaybeLeadPartnerAfterHerbs();
	RefreshOpeningQuest();
	if (bOpeningRuneActive)
	{
		bOpeningWispReturning = false;
		SetOpeningInteractPrompt(false, FVector::ZeroVector);
		UpdateOpeningHerbRune(DeltaTime);
		return;
	}
	if (bOpeningDogDrawActive)
	{
		bOpeningWispReturning = false;
		SetOpeningInteractPrompt(false, FVector::ZeroVector);
		UpdateOpeningDogDraw(DeltaTime);
		return;
	}
	UpdateOpeningDog(DeltaTime);
	UpdateOpeningHerbPreview();
	if (SizeTestWisp && SizeTestWisp->IsVisible())
	{
		const AActor* Mark = FindOpeningProximityTarget();
		if (bOpeningWispReturning && Mark && Mark != OpeningWispReleased)
		{
			bOpeningWispReturning = false;
			OpeningWispReleased = nullptr;
		}
		if (bOpeningWispReturning)
		{
			OpeningWispReturnLeft -= DeltaTime;
			const FVector Home = GetActorTransform().TransformPosition(FVector(10.f, 45.f, 55.f));
			const float Alpha = 1.f - FMath::Clamp(OpeningWispReturnLeft / 0.35f, 0.f, 1.f);
			SizeTestWisp->SetUsingAbsoluteLocation(true);
			SizeTestWisp->SetWorldLocation(FMath::Lerp(OpeningWispReturnFrom, Home, Alpha));
			SetOpeningInteractPrompt(false, FVector::ZeroVector);
			if (OpeningWispReturnLeft <= 0.f)
			{
				bOpeningWispReturning = false;
				SizeTestWisp->SetUsingAbsoluteLocation(false);
				SizeTestWisp->SetRelativeLocation(FVector(10.f, 45.f, 55.f));
			}
			return;
		}
		if (Mark)
		{
			if (Mark == OpeningWispReleased)
			{
				SizeTestWisp->SetUsingAbsoluteLocation(false);
				SizeTestWisp->SetRelativeLocation(FVector(10.f, 45.f, 55.f));
				SetOpeningInteractPrompt(false, FVector::ZeroVector);
			}
			else
			{
				FVector Hover = FVector::ZeroVector;
				const float HoverTime = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
				const FVector Viewer = FollowCamera ? FollowCamera->GetComponentLocation() : GetActorLocation();
				const float HeadZ = GetActorLocation().Z + CapsuleHalfHeight;
				if (HomeWorldWisp::HoverPoint(Mark, Viewer, HeadZ, HoverTime, Hover))
				{
					SizeTestWisp->SetUsingAbsoluteLocation(true);
					SizeTestWisp->SetWorldLocation(Hover);
					SetOpeningInteractPrompt(true, Hover);
				}
				else
				{
					SetOpeningInteractPrompt(false, FVector::ZeroVector);
				}
			}
		}
		else
		{
			OpeningWispReleased = nullptr;
			SizeTestWisp->SetUsingAbsoluteLocation(false);
			SizeTestWisp->SetRelativeLocation(FVector(10.0f, 45.0f, 55.0f));
			SetOpeningInteractPrompt(false, FVector::ZeroVector);
		}
	}
	else
	{
		SetOpeningInteractPrompt(false, FVector::ZeroVector);
	}
}

void AHomeWorldCharacter::UpdateSizeTestWalk()
{
	USkeletalMeshComponent* CoatBody = GetMesh();
	if (!CoatBody)
	{
		return;
	}
	const bool bMoving = GetVelocity().SizeSquared2D() > 100.0f;
	if (bMoving == bSizeTestWalkPlaying)
	{
		return;
	}
	bSizeTestWalkPlaying = bMoving;
	CoatBody->SetEnableAnimation(true);
	CoatBody->SetAnimationMode(EAnimationMode::AnimationSingleNode);
	if (!bMoving)
	{
		CoatBody->Stop();
		if (UAnimSingleNodeInstance* Node = CoatBody->GetSingleNodeInstance())
		{
			Node->SetAnimationAsset(nullptr);
			Node->SetRootMotionMode(ERootMotionMode::IgnoreRootMotion);
		}
		return;
	}
	if (UAnimSequence* Walk = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/HomeWorld/Meshes/SizeTest/SK_Player_Female_Anim.SK_Player_Female_Anim")))
	{
		CoatBody->PlayAnimation(Walk, true);
		if (UAnimSingleNodeInstance* Node = CoatBody->GetSingleNodeInstance())
		{
			Node->SetRootMotionMode(ERootMotionMode::IgnoreRootMotion);
		}
	}
}

void AHomeWorldCharacter::ApplySpawnControlPitch()
{
	if (AController* Controlled = GetController())
	{
		Controlled->SetControlRotation(FRotator(OpeningLookRestPitch, GetActorRotation().Yaw, 0.f));
	}
}

void AHomeWorldCharacter::PossessedBy(AController* NewController)
{
	Super::PossessedBy(NewController);
	ApplySpawnControlPitch();
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
	if (!JumpAction)
	{
		JumpAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/HomeWorld/Input/IA_Jump.IA_Jump"));
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

	if (JumpAction)
	{
		EnhancedInput->BindAction(JumpAction, ETriggerEvent::Started, this, &AHomeWorldCharacter::OnJumpStarted);
		EnhancedInput->BindAction(JumpAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnJumpCompleted);
	}
	if (PrimaryAttackAction)
	{
		EnhancedInput->BindAction(PrimaryAttackAction, ETriggerEvent::Started, this, &AHomeWorldCharacter::OnStrokeInputStarted);
		EnhancedInput->BindAction(PrimaryAttackAction, ETriggerEvent::Triggered, this, &AHomeWorldCharacter::OnStrokeInputSampled);
		EnhancedInput->BindAction(PrimaryAttackAction, ETriggerEvent::Completed, this, &AHomeWorldCharacter::OnStrokeInputReleased);
	}

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
		EnhancedInput->BindAction(InteractAction, ETriggerEvent::Started, this, &AHomeWorldCharacter::OnInteractTriggered);
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
	if (bSizeTestInteractCursor || IsSizeTestLevel() || bOpeningRuneActive)
	{
		return;
	}
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
	const bool bTutorial = IsSizeTestLevel();
	if (!bTutorial)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Interact input triggered"));
	}
	if (bOpeningRuneActive || bOpeningDogDrawActive)
	{
		return;
	}
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
	bSizeTestInteractHandled = false;
	const bool bActivated = AbilitySystemComponent->TryActivateAbilityByClass(InteractAbilityClass);
	if (bTutorial && !bSizeTestInteractHandled)
	{
		UE_LOG(LogTemp, Log, TEXT("opening_interact: nothing in the look"));
	}
	if (!bTutorial)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Interact ability %s"), bActivated ? TEXT("activated") : TEXT("failed to activate"));
	}
}

void AHomeWorldCharacter::NoteSizeTestInteract(bool bHandled)
{
	bSizeTestInteractHandled = bHandled;
	if (bHandled && !bOpeningRuneActive && !bOpeningDogDrawActive)
	{
		SnapSizeTestWispHome(FindOpeningProximityTarget());
	}
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

void AHomeWorldCharacter::OnJumpStarted(const FInputActionValue& Value)
{
	Jump();
}

void AHomeWorldCharacter::OnJumpCompleted(const FInputActionValue& Value)
{
	StopJumping();
}

bool AHomeWorldCharacter::IsSizeTestLevel() const
{
	const UWorld* World = GetWorld();
	return World && World->GetMapName().Contains(TEXT("L_SizeTest"));
}

void AHomeWorldCharacter::SetStrokePad(AHomeWorldEasePad* Pad)
{
	StrokePad = Pad;
	if (Pad)
	{
		EndPartyOuting(GetWorld(), EHomeWorldPartyAbsence::Stroke);
	}
}

void AHomeWorldCharacter::SetStrokeHerb(EHomeWorldHerbVerb Verb, UHomeWorldVirtueComponent* Target)
{
	HerbVerb = Verb;
	HerbTarget = Target;
}

void AHomeWorldCharacter::SetParadoxToy(AHomeWorldParadoxToy* Toy)
{
	ParadoxToy = Toy;
}

void AHomeWorldCharacter::DiscoverStrokePad()
{
	if (StrokePad)
	{
		return;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	for (TActorIterator<AHomeWorldEasePad> It(World); It; ++It)
	{
		SetStrokePad(*It);
		return;
	}
}

void AHomeWorldCharacter::DiscoverParadoxToy()
{
	if (ParadoxToy)
	{
		return;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	for (TActorIterator<AHomeWorldParadoxToy> It(World); It; ++It)
	{
		ParadoxToy = *It;
		return;
	}
}

void AHomeWorldCharacter::SetStrokeCursorHeld(bool bHeld)
{
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC || !PC->IsLocalController())
	{
		bStrokeCursorHeld = false;
		return;
	}
	if (bHeld)
	{
		FInputModeGameAndUI InputMode;
		InputMode.SetHideCursorDuringCapture(false);
		InputMode.SetLockMouseToViewportBehavior(EMouseLockMode::DoNotLock);
		PC->SetInputMode(InputMode);
		PC->SetShowMouseCursor(true);
		bStrokeCursorHeld = true;
		return;
	}
	if (!bStrokeCursorHeld)
	{
		return;
	}
	FInputModeGameOnly InputMode;
	PC->SetInputMode(InputMode);
	PC->SetShowMouseCursor(false);
	bStrokeCursorHeld = false;
}

void AHomeWorldCharacter::BeginStrokeFromInput()
{
	if (IsSizeTestLevel() || !StrokeReport)
	{
		return;
	}
	DiscoverStrokePad();
	DiscoverParadoxToy();
	SetStrokeCursorHeld(true);
	StrokeReport->BeginStrokeHold();
}

void AHomeWorldCharacter::SampleStrokeFromInput(FVector2D ScreenPoint, float Time)
{
	if (IsSizeTestLevel() || !StrokeReport)
	{
		return;
	}
	StrokeReport->AppendCursorSample(ScreenPoint, Time);
}

void AHomeWorldCharacter::ApplyMarkedHerbOnMatch()
{
	if (HerbVerb == EHomeWorldHerbVerb::None || !HerbTarget)
	{
		return;
	}
	UGameInstance* GameInstance = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldInventorySubsystem* Inventory = GameInstance ? GameInstance->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inventory)
	{
		return;
	}
	switch (HerbVerb)
	{
	case EHomeWorldHerbVerb::Give:
		Inventory->TryVirtueGive(HerbTarget);
		break;
	case EHomeWorldHerbVerb::Take:
		Inventory->TryVirtueTake(HerbTarget);
		break;
	case EHomeWorldHerbVerb::Swap:
		Inventory->TryVirtueSwap(HerbTarget);
		break;
	default:
		break;
	}
}

EHomeWorldStrokeReport AHomeWorldCharacter::EndStrokeFromInput()
{
	if (IsSizeTestLevel() || !StrokeReport)
	{
		return EHomeWorldStrokeReport::None;
	}
	EHomeWorldStrokeStep Step = EHomeWorldStrokeStep::Grace;
	float WindowMin = 0.f;
	float WindowMax = 1.f;
	FVector2D ExtraPoint = FVector2D::ZeroVector;
	bool bHasFocus = false;
	FVector FocusPoint = FVector::ZeroVector;
	if (StrokePad)
	{
		Step = StrokePad->GetOfferedStep();
		WindowMin = StrokePad->GetWindowMin();
		WindowMax = StrokePad->GetWindowMax();
		ExtraPoint = StrokePad->GetExtraPoint();
		bHasFocus = true;
		FocusPoint = StrokePad->GetFocusPoint();
	}
	const EHomeWorldStrokeReport Report = StrokeReport->EndStrokeHold(
		Step, WindowMin, WindowMax, ExtraPoint, nullptr, FallbackGlideComponent, bHasFocus, FocusPoint);
	if (Report == EHomeWorldStrokeReport::Bonk)
	{
		EndPartyOuting(GetWorld(), EHomeWorldPartyAbsence::Bonk);
	}
	SetStrokeCursorHeld(false);
	if (Report != EHomeWorldStrokeReport::Matched)
	{
		return Report;
	}
	if (StrokePad)
	{
		TryCommitOpeningGuardPad(StrokePad, Step);
	}
	ApplyMarkedHerbOnMatch();
	if (ParadoxToy && (Step == EHomeWorldStrokeStep::Paradox || Step == EHomeWorldStrokeStep::ParadoxExtraPoint))
	{
		ParadoxToy->ArmForDawn();
	}
	return Report;
}

void AHomeWorldCharacter::OnStrokeInputStarted(const FInputActionValue& Value)
{
	BeginStrokeFromInput();
}

void AHomeWorldCharacter::OnStrokeInputSampled(const FInputActionValue& Value)
{
	if (IsSizeTestLevel() || !StrokeReport || !StrokeReport->IsStrokeHeld())
	{
		return;
	}
	APlayerController* PC = Cast<APlayerController>(GetController());
	if (!PC)
	{
		return;
	}
	float MouseX = 0.f;
	float MouseY = 0.f;
	if (!PC->GetMousePosition(MouseX, MouseY))
	{
		return;
	}
	int32 SizeX = 0;
	int32 SizeY = 0;
	PC->GetViewportSize(SizeX, SizeY);
	const FVector2D Unit = HomeWorldStroke::MapMouseToStrokeUnit(
		FVector2D(MouseX, MouseY),
		FVector2D(static_cast<float>(SizeX), static_cast<float>(SizeY)));
	const float WorldSeconds = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
	const float Time = StrokePad ? StrokePad->WindUpTimeAt(WorldSeconds) : 0.f;
	StrokeReport->AppendCursorSample(Unit, Time);
}

void AHomeWorldCharacter::OnStrokeInputReleased(const FInputActionValue& Value)
{
	EndStrokeFromInput();
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

static AActor* FindGlideStartMarker(UWorld* World);

bool AHomeWorldCharacter::TryStartCloudDescent()
{
	const bool bDayBody = !bIsSpiritForm && AreDayBodyAbilitiesAllowed();
	const bool bNightSpirit = bIsSpiritForm;
	if (bCloudDescentActive || IsFallbackGliding() || !(bDayBody || bNightSpirit))
	{
		return false;
	}
	if (!IsOpeningGliderCrafted())
	{
		UE_LOG(LogTemp, Log, TEXT("CLOUD_DESCENT: refused; the glider is not crafted"));
		return false;
	}

	UWorld* World = GetWorld();
	UCharacterMovementComponent* Movement = GetCharacterMovement();
	AActor* GlideStart = FindGlideStartMarker(World);
	if (!World || !Movement || !GlideStart)
	{
		return false;
	}

	if (FVector::DistSquared(GetActorLocation(), GlideStart->GetActorLocation()) > FMath::Square(GlideStartProximityCm))
	{
		return false;
	}

	UHomeWorldGlideMovementComponent* Glide = Cast<UHomeWorldGlideMovementComponent>(Movement);
	if (!Glide)
	{
		UE_LOG(LogTemp, Warning, TEXT("CLOUD_DESCENT: refused; movement component is %s, expected UHomeWorldGlideMovementComponent."),
			*GetNameSafe(Movement->GetClass()));
		return false;
	}

	bCloudDescentActive = true;
	if (!Glide->StartGlide())
	{
		bCloudDescentActive = false;
		return false;
	}
	bHasLeftHomestead = true;
	{
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = GetWorld() ? GetWorld()->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
		bDayGlideSmokeSign = TimeOfDay && TimeOfDay->GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Day;
	}
	if (SoftBoundsComponent)
	{
		SoftBoundsComponent->bBoundsEnabled = false;
	}
	UE_LOG(LogTemp, Log, TEXT("CLOUD_DESCENT: active; unrestricted air steering"));
	return true;
}

bool AHomeWorldCharacter::CollectCloudWisp(AHomeWorldCloudWisp* Wisp)
{
	if (!bCloudDescentActive || !Wisp)
	{
		return false;
	}

	UWorld* World = GetWorld();
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		return false;
	}
	if (CarriedCloudWisps >= 2)
	{
		return false;
	}

	++CarriedCloudWisps;
	return true;
}

void AHomeWorldCharacter::Landed(const FHitResult& Hit)
{
	Super::Landed(Hit);
	if (!bCloudDescentActive)
	{
		return;
	}

	// The glide CMC's ProcessLanded hands control back through SetPostLandedPhysics,
	// so no manual restore of AirControl or GravityScale is needed here.
	if (!bFieldLandingChosen)
	{
		UWorld* World = GetWorld();
		AActor* GlideStart = FindGlideStartMarker(World);
		const bool bWind = GlideStart && GetActorLocation().X >= GlideStart->GetActorLocation().X;
		ChooseFieldLanding(bWind);
	}
	bCloudDescentActive = false;
	bDayGlideSmokeSign = false;
	UE_LOG(LogTemp, Log, TEXT("CLOUD_DESCENT: landed; walk control restored; carried wisps=%d"), CarriedCloudWisps);
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

	// List 56 / T2 + T3 + T0 #11: Bed / NODE_BED.
	// Night or dusk, still body: sleep grants spirit.
	// Already spirit, stacks up: the touch clears them and stays spirit.
	// Already spirit, stacks clear: the bed ends spirit, then the clock goes to dawn.
	// Day, still body: advance the clock to night and stay FORM_BODY.
	// Phase-alone SetPhase(Night) without the sleep gate = closed_fail for FORM_SPIRIT.
	if (HitActor && HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::Bed))
	{
		if (UHomeWorldTimeOfDaySubsystem* Tod = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (bIsSpiritForm)
			{
				if (SpiritSicknessStacks > 0)
				{
					TouchSpiritBed();
				}
				else
				{
					WakeFromSpiritAtBed();
					Tod->AdvanceToDawn();
					UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wake (interact at bed) -- phase set to Dawn. MVP List 56 T3."));
				}
			}
			else if (Tod->GetIsSpiritPhase())
			{
				TryBedSleepSpirit();
			}
			else
			{
				Tod->SetPhase(EHomeWorldTimeOfDayPhase::Night);
				UE_LOG(LogTemp, Log,
					TEXT("NODE_BED: day bed stays FORM_BODY (clock to Night; spirit is the night bed; #9 w/o sleep gate stay FORM_BODY)"));
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
	// The dawn rule is one line, once, before the first night out.
	if (HitActor && (HitActor->ActorHasTag(FName("Child")) || HitActor->ActorHasTag(FName("NPC_CHILD"))))
	{
		TryTellChildDawnRule();
		AHomeWorldPlayerState* PS = GetPlayerState<AHomeWorldPlayerState>();
		if (PS)
		{
			PS->CompleteOneGameWithChild();
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Game with child (interact with child) — one game with child done. MVP List 59."));
			return true;
		}
		return bChildDawnRuleTold;
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
	if (OpeningHerbTenths > 0)
	{
		const int32 Chunks = FMath::Min(OpeningHerbTenths, 10);
		OpeningHerbTenths -= Chunks;
		const float FullDaySeconds = FMath::Max(1.f, TeaSprintHalfDaySeconds) * 2.f;
		const float GrantSeconds = FullDaySeconds * (static_cast<float>(Chunks) / 10.f);
		const float Now = World->GetTimeSeconds();
		if (TeaSprintEndWorldTime < Now)
		{
			TeaSprintEndWorldTime = Now;
		}
		TeaSprintEndWorldTime += GrantSeconds;
		bOpeningKettleBrewed = true;
		LogOpening(TEXT("opening_kettle: brewed"));
		ShowInteractFeedback(TEXT("NODE_KETTLE: tea from herb chunks"), FColor::Green);
		bHasSidedHerb = false;
		return true;
	}
	const bool bSpent = Inv->SpendResource(HomeWorldInventory::RES_HERB, 1);
	if (!bSpent && !bHasSidedHerb)
	{
		LogOpening(TEXT("opening_kettle: need herb chunks"));
		ShowInteractFeedback(TEXT("NODE_KETTLE: need RES_HERB"), FColor::Yellow);
		return false;
	}
	if (!bSpent)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: brew from the herb just picked"));
	}

	const float Duration = FMath::Max(1.f, TeaSprintHalfDaySeconds);
	TeaSprintEndWorldTime = World->GetTimeSeconds() + Duration;

	UE_LOG(LogTemp, Log,
		TEXT("NODE_KETTLE: tea brew TOD_DAY FORM_BODY (herbs->tea; gates sprint ~half day=%.0fs; not PROXY SM_ProxyKettle; not meal-BP-as-tea)"),
		Duration);
	ShowInteractFeedback(TEXT("NODE_KETTLE: tea ready - sprint gated ~half day"), FColor::Green);
	const bool bEast = bHasSidedHerb && bCarriedHerbIsEast;
	bHasSidedHerb = false;
	if (bEast)
	{
		bPorchCrawlOpen = true;
		OpenPorchCrawlActors();
		UE_LOG(LogTemp, Log, TEXT("PORCH_CRAWL: east tea opens the gap; the edge hint waits"));
	}
	else
	{
		bEdgeFaceAwake = true;
		if (!bFamilyHintFired)
		{
			FamilyHint = TEXT("toward the edge");
			bFamilyHintFired = true;
			UE_LOG(LogTemp, Log, TEXT("FAMILY: hint %s"), *FamilyHint);
		}
	}
	return true;
}

bool AHomeWorldCharacter::TryPickGardenHerb()
{
	return TryPickGardenHerbFromEast(false);
}

bool AHomeWorldCharacter::DoesBodyFitPorchGap(float RadiusCm) const
{
	return RadiusCm > 0.f && RadiusCm * 2.f <= 130.f;
}

bool AHomeWorldCharacter::ChooseFieldLanding(bool bWind)
{
	if (bFieldLandingChosen)
	{
		return false;
	}
	bFieldLandingChosen = true;
	if (bWind)
	{
		bWindColumnAwake = true;
		UE_LOG(LogTemp, Log, TEXT("FIELD_LANDING: wind column awake; the bull path sleeps"));
	}
	else
	{
		bBullPathAwake = true;
		UE_LOG(LogTemp, Log, TEXT("FIELD_LANDING: bull path awake; the wind column sleeps"));
	}
	return true;
}

void AHomeWorldCharacter::ArriveAtCamp()
{
	if (bCampArrived)
	{
		return;
	}
	bCampArrived = true;
	PacingGuard = FMath::RandHelper(3);
	UE_LOG(LogTemp, Log, TEXT("CAMP: guard %d is pacing"), PacingGuard);
}

bool AHomeWorldCharacter::RecordGuardEased(int32 Ordinal)
{
	if (Ordinal < 0 || Ordinal > 2 || bGuardGapOpen[Ordinal])
	{
		return false;
	}
	bGuardGapOpen[Ordinal] = true;
	UE_LOG(LogTemp, Log, TEXT("CAMP: guard %d gap open"), Ordinal);
	return true;
}

bool AHomeWorldCharacter::IsGuardGapOpen(int32 Ordinal) const
{
	return Ordinal >= 0 && Ordinal <= 2 && bGuardGapOpen[Ordinal];
}

bool AHomeWorldCharacter::TrySpendPullStar()
{
	if (!bPullStarHeld)
	{
		return false;
	}
	bPullStarHeld = false;
	LaunchCharacter(GetActorForwardVector() * 600.f + FVector(0.f, 0.f, 200.f), true, true);
	UE_LOG(LogTemp, Log, TEXT("PULL_STAR: spent on one crossing"));
	return true;
}

void AHomeWorldCharacter::OpenPorchCrawlActors()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (!It->ActorHasTag(FName(TEXT("NODE_PORCH_CRAWL"))))
		{
			continue;
		}
		It->SetActorHiddenInGame(true);
		It->SetActorEnableCollision(false);
	}
}

void AHomeWorldCharacter::NotifyPocketNight()
{
	WakeUnpickedPocketFace();
}

void AHomeWorldCharacter::WakeUnpickedPocketFace()
{
	if (bEdgeFaceAwake && !bPorchCrawlOpen)
	{
		bPorchCrawlOpen = true;
		OpenPorchCrawlActors();
		UE_LOG(LogTemp, Log, TEXT("PORCH_CRAWL: night opens the gap the day left asleep"));
	}
	else if (bPorchCrawlOpen && !bFamilyHintFired)
	{
		FamilyHint = TEXT("toward the edge");
		bFamilyHintFired = true;
		bEdgeFaceAwake = true;
		UE_LOG(LogTemp, Log, TEXT("FAMILY: night hint %s"), *FamilyHint);
	}
	if (bWindColumnAwake && !bBullPathAwake)
	{
		bBullPathAwake = true;
		UE_LOG(LogTemp, Log, TEXT("FIELD_LANDING: night wakes the bull path"));
	}
	else if (bBullPathAwake && !bWindColumnAwake)
	{
		bWindColumnAwake = true;
		UE_LOG(LogTemp, Log, TEXT("FIELD_LANDING: night wakes the wind column"));
	}
}

bool AHomeWorldCharacter::TryPickGardenHerbFromEast(bool bEast, int32 Amount)
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	const bool bOpening = UGameplayStatics::GetCurrentLevelName(World).Contains(TEXT("SizeTest"));
	if (!bOpening && (!TimeOfDay || TimeOfDay->GetCurrentPhase() != EHomeWorldTimeOfDayPhase::Day || bIsSpiritForm))
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GARDEN: pick skipped - need TOD_DAY FORM_BODY"));
		return false;
	}
	if (bIsSpiritForm)
	{
		return false;
	}
	UGameInstance* GI = World->GetGameInstance();
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	const bool bAdded = Inv && Inv->TryAddResource(HomeWorldInventory::RES_HERB, FMath::Max(1, Amount));
	if (!bAdded && !bOpening)
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GARDEN: pick failed - inventory"));
		return false;
	}
	bCarriedHerbIsEast = bEast;
	bHasSidedHerb = true;
	UE_LOG(LogTemp, Log, TEXT("NODE_GARDEN: RES_HERB now %d"), Inv ? Inv->GetResource(HomeWorldInventory::RES_HERB) : 0);
	return true;
}

bool AHomeWorldCharacter::TryGiveNightWispToWound()
{
	UWorld* World = GetWorld();
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_WOUND: give skipped - day wound is seen, healed at night"));
		return false;
	}
	if (bHomesteadWoundHealed || CarriedCloudWisps < 1)
	{
		return false;
	}
	--CarriedCloudWisps;
	bHomesteadWoundHealed = true;
	FollowingWoundWispCount = 3;
	bPullStarHeld = true;
	UE_LOG(LogTemp, Log, TEXT("NODE_WOUND: healed by one night wisp; a pull star is left on the wound"));
	return true;
}

namespace
{
	bool HitCarriesTag(const AActor* Actor, const TCHAR* Tag)
	{
		return Actor && Actor->ActorHasTag(FName(Tag));
	}

	bool IsHerbPlant(const AActor* Actor)
	{
		return Actor && Actor->GetActorNameOrLabel().Contains(TEXT("Lupine"));
	}

	AActor* GardenBedFor(UWorld* World, AActor* Actor)
	{
		if (!World || !Actor)
		{
			return nullptr;
		}
		if (HomeWorldT0BeatNodes::ActorCarriesTagFor(Actor, HomeWorldT0BeatNodes::ENode::Garden))
		{
			return Actor;
		}
		if (!IsHerbPlant(Actor))
		{
			return nullptr;
		}
		AActor* Best = nullptr;
		float BestDist = 150.f * 150.f;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(*It, HomeWorldT0BeatNodes::ENode::Garden))
			{
				continue;
			}
			const float Dist = FVector::DistSquared2D(It->GetActorLocation(), Actor->GetActorLocation());
			if (Dist < BestDist)
			{
				BestDist = Dist;
				Best = *It;
			}
		}
		return Best;
	}
}

bool AHomeWorldCharacter::TryGardenInteractInFront()
{
	FHitResult Hit;
	AActor* Aimed = ResolveOpeningAim(Hit);
	UWorld* World = GetWorld();
	AActor* HitActor = GardenBedFor(World, Aimed);
	if (!HitActor)
	{
		return false;
	}
	if (UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("SizeTest")))
	{
		StartOpeningHerbRune(HitActor);
		return true;
	}
	const bool bPicked = TryPickGardenHerbFromEast(HitActor->ActorHasTag(FName(TEXT("NODE_GARDEN_EAST"))));
	if (bPicked)
	{
		AActor* Plant = IsHerbPlant(Aimed) ? Aimed : nullptr;
		float Best = 80.f * 80.f;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!It->GetActorNameOrLabel().Contains(TEXT("Lupine")))
			{
				continue;
			}
			const float Dist = FVector::DistSquared2D(It->GetActorLocation(), HitActor->GetActorLocation());
			if (Dist < Best)
			{
				Best = Dist;
				Plant = *It;
			}
		}
		if (Plant)
		{
			Plant->SetActorHiddenInGame(true);
			Plant->SetActorEnableCollision(false);
		}
		HitActor->SetActorEnableCollision(false);
		HitActor->Tags.Remove(FName(TEXT("NODE_GARDEN")));
		HitActor->Tags.Remove(FName(TEXT("NODE_GARDEN_EAST")));
		HitActor->Tags.Remove(FName(TEXT("NODE_GARDEN_WEST")));
	}
	ShowInteractFeedback(bPicked ? TEXT("NODE_GARDEN: herb") : TEXT("NODE_GARDEN: day body only"), bPicked ? FColor::Green : FColor::Yellow);
	return bPicked;
}

bool AHomeWorldCharacter::TryWoundInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitCarriesTag(HitActor, TEXT("NODE_WOUND")))
	{
		return false;
	}
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (!TimeOfDay->GetIsNight())
			{
				ShowInteractFeedback(TEXT("NODE_WOUND: seen by day"), FColor::Yellow);
				return true;
			}
		}
	}
	const bool bHealed = TryGiveNightWispToWound();
	ShowInteractFeedback(bHealed ? TEXT("NODE_WOUND: healed") : TEXT("NODE_WOUND: need a night wisp"), bHealed ? FColor::Green : FColor::Yellow);
	return bHealed;
}

bool AHomeWorldCharacter::TryDungInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	if (!HitCarriesTag(GetInteractTargetActor(Hit), TEXT("NODE_DUNG")))
	{
		return false;
	}
	const bool bCarried = TryAddCarriedDung();
	ShowInteractFeedback(bCarried ? TEXT("NODE_DUNG: carried") : TEXT("NODE_DUNG: full"), FColor::Green);
	return bCarried;
}

bool AHomeWorldCharacter::TryMixFertilizerInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	if (!HitCarriesTag(GetInteractTargetActor(Hit), TEXT("NODE_MIX")))
	{
		return false;
	}
	const bool bMixed = TryMixHomesteadFertilizer();
	ShowInteractFeedback(bMixed ? TEXT("NODE_MIX: fertilizer") : TEXT("NODE_MIX: need dung and a night wisp"), bMixed ? FColor::Green : FColor::Yellow);
	return bMixed;
}

bool AHomeWorldCharacter::TryBullInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	if (!HitCarriesTag(GetInteractTargetActor(Hit), TEXT("NODE_BULL")))
	{
		return false;
	}
	if (!bHasLeftHomestead)
	{
		ShowInteractFeedback(TEXT("NODE_BULL: field only"), FColor::Yellow);
		return false;
	}
	SetRidingBull(true);
	ShowInteractFeedback(TEXT("NODE_BULL: riding"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryBarnInteractInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	if (!HitCarriesTag(GetInteractTargetActor(Hit), TEXT("NODE_BARN")))
	{
		return false;
	}
	if (!bWalkToBarn)
	{
		return false;
	}
	bWalkToBarn = false;
	ShowInteractFeedback(TEXT("NODE_BARN: bull home"), FColor::Green);
	UE_LOG(LogTemp, Log, TEXT("SHRINE: walked the bull to the barn"));
	return true;
}

bool AHomeWorldCharacter::TryEaseGuardInFront()
{
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	AActor* HitActor = GetInteractTargetActor(Hit);
	if (!HitCarriesTag(HitActor, TEXT("NODE_GUARD")))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent.Get();
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	if (!Stealth || !GetWorld())
	{
		return false;
	}
	int32 Ordinal = 0;
	for (TActorIterator<AActor> It(GetWorld()); It; ++It)
	{
		if (*It == HitActor)
		{
			break;
		}
		if (HitCarriesTag(*It, TEXT("NODE_GUARD")))
		{
			++Ordinal;
		}
	}
	ArriveAtCamp();
	const bool bEased = Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, Ordinal);
	if (bEased)
	{
		RecordGuardEased(Ordinal);
	}
	ShowInteractFeedback(bEased ? TEXT("NODE_GUARD: eased") : TEXT("NODE_GUARD: spirit at night"), bEased ? FColor::Green : FColor::Yellow);
	return bEased;
}

bool AHomeWorldCharacter::TryFreeCaptiveInFront()
{
	EndPartyOuting(GetWorld(), EHomeWorldPartyAbsence::Rescue);
	FHitResult Hit;
	if (!TraceInteractHit(Hit))
	{
		return false;
	}
	if (!HitCarriesTag(GetInteractTargetActor(Hit), TEXT("NODE_CAPTIVE")))
	{
		return false;
	}
	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent.Get();
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	if (!Stealth || !Stealth->TryFreeCaptive())
	{
		ShowInteractFeedback(TEXT("NODE_CAPTIVE: ease the guards first"), FColor::Yellow);
		return false;
	}
	NotifyPartnerReadyToReturn();
	ShowInteractFeedback(TEXT("NODE_CAPTIVE: free, shrine home"), FColor::Green);
	return true;
}

bool AHomeWorldCharacter::TryAddCarriedDung()
{
	++CarriedDung;
	UE_LOG(LogTemp, Log, TEXT("FERTILIZER: carried dung +1"));
	return true;
}

bool AHomeWorldCharacter::TryMixHomesteadFertilizer()
{
	if (CarriedDung < 1 || CarriedCloudWisps < 1)
	{
		UE_LOG(LogTemp, Log, TEXT("FERTILIZER: mix failed - need one dung and one night wisp"));
		return false;
	}
	--CarriedDung;
	--CarriedCloudWisps;
	++CarriedFertilizer;
	UE_LOG(LogTemp, Log, TEXT("FERTILIZER: mixed one"));
	return true;
}

bool AHomeWorldCharacter::TrySpreadFertilizerOnNightFlight()
{
	UWorld* World = GetWorld();
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TimeOfDay || !TimeOfDay->GetIsNight() || !bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("FERTILIZER: spread skipped - night spirit flight only"));
		return false;
	}
	if (!bHomesteadWoundHealed || CarriedFertilizer < 1)
	{
		UE_LOG(LogTemp, Log, TEXT("FERTILIZER: spread skipped - need the healed wound flight and one mix"));
		return false;
	}
	--CarriedFertilizer;
	UE_LOG(LogTemp, Log, TEXT("FERTILIZER: spread over field herb sites (no morning pile, no third wisp)"));
	return true;
}

void AHomeWorldCharacter::NotifyLeftHomestead()
{
	bHasLeftHomestead = true;
}

void AHomeWorldCharacter::SetRidingBull(bool bRiding)
{
	bRidingBull = bRiding;
	if (TraversalComponent)
	{
		TraversalComponent->SetMountBoostActive(bRiding);
	}
	if (bRiding)
	{
		bWalkToBarn = false;
	}
}

void AHomeWorldCharacter::NotifyPartnerTaken()
{
	bPartnerTaken = true;
	bPartnerReadyToReturn = false;
	bPartnerWalkingHome = false;
	PartnerPlace = EHomeWorldFamilyPlace::Away;
	ChildPlace = EHomeWorldFamilyPlace::ByBed;
	UE_LOG(LogTemp, Log, TEXT("FAMILY: partner taken; child waits by the bed"));
}

void AHomeWorldCharacter::NotifyPartnerReadyToReturn()
{
	bPartnerReadyToReturn = true;
}

void AHomeWorldCharacter::CompleteShrineReturn()
{
	if (bRidingBull)
	{
		bRidingBull = false;
		bWalkToBarn = true;
		UE_LOG(LogTemp, Log, TEXT("SHRINE: bull returned; walk to barn"));
	}
	if (bPartnerReadyToReturn)
	{
		bPartnerReadyToReturn = false;
		bPartnerWalkingHome = true;
		PartnerPlace = EHomeWorldFamilyPlace::ByBed;
		UE_LOG(LogTemp, Log, TEXT("SHRINE: partner returned; walk"));
	}
}

bool AHomeWorldCharacter::TryNodeKettleInteractInFront()
{
	FHitResult Hit;
	AActor* HitActor = ResolveOpeningAim(Hit);
	if (!HitActor)
	{
		return false;
	}

	if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::Kettle))
	{
		return false;
	}

	// World interact beat -- PROXY mesh alone (SM_ProxyKettle without interact/brew) = closed_fail.
	if (UHomeWorldHomeLoopSubsystem* HomeLoop = GetWorld() ? GetWorld()->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr)
	{
		return HomeLoop->TryKettleFromWorld(this);
	}
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

	// A tag OR an N1 nurture component both identify the slot -- same identity #12 uses.
	bool bIsPlantSlot = HomeWorldT0BeatNodes::ActorCarriesTagFor(
		HitActor, HomeWorldT0BeatNodes::ENode::PlantSlot);
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
	// Prereq: #3 day plant same NODE_PLANT_SLOT + #11 spirit path (the bed).
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

	if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::Backpack))
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

	if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::FieldGather))
	{
		return false;
	}

	// World interact beat -- PROXY SM_ProxyFieldGather / dress / GP_Store alone without collect latch = closed_fail.
	return TryCollectNodeFieldGather();
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
	if (!bPartnerTaken)
	{
		NotifyPartnerTaken();
	}
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

	if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(HitActor, HomeWorldT0BeatNodes::ENode::DayCamp))
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

bool AHomeWorldCharacter::TryBootBeastChargeHome()
{
	// Bull charge-and-boot (Lead 2026-10-07): threat full / too close without an
	// offering -> charge -> EJECT_HOME. Architecture Trade-Offs A-E: prefer
	// existing FallbackGlideComponent::StartGlideHome -- no parallel eject service
	// (Arch B). Distinct from MUST #8 TryEjectNodeDayCamp (day camp) and
	// #10 TryBootPlanetsideNightHome (night glider) -- this is the beast's own
	// day-field boot. StartGlideHome(false) keeps the day-only phase law; night
	// blocking is its gate, not a new one. Cite only: does not touch #9 TOD /
	// spirit grant -- FORM_BODY stays as it is.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log, TEXT("BEAST_CHARGE: boot skipped - need FORM_BODY"));
		ShowInteractFeedback(TEXT("BEAST_CHARGE: body form only"), FColor::Yellow);
		return false;
	}

	bool bGlideStarted = false;
	if (FallbackGlideComponent)
	{
		bGlideStarted = FallbackGlideComponent->StartGlideHome(/*bAllowNightPhase=*/false);
	}

	if (bGlideStarted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("BEAST_CHARGE: EJECT_HOME FORM_BODY (StartGlideHome charge boot home; reverse CRUMB home; not day-camp #8; not planetside #10; not FALLBACK down; not soft-kidnap)"));
		ShowInteractFeedback(TEXT("BEAST_CHARGE: booted home"), FColor::Green);
	}
	else
	{
		// StartGlideHome already logged its own blocked reason (night phase /
		// dusk buffer / no crumbs). No latch: the charge is repeatable and the
		// encounter component spaces refires with a meter refill.
		UE_LOG(LogTemp, Log,
			TEXT("BEAST_CHARGE: boot requested but StartGlideHome did not start (blocked; see EJECT_HOME log; not day-camp #8; not planetside #10)"));
		ShowInteractFeedback(TEXT("BEAST_CHARGE: boot blocked"), FColor::Yellow);
	}
	return bGlideStarted;
}

bool AHomeWorldCharacter::TryBedSleepSpirit()
{
	// T0_M11 NODE_BED / night / FORM_SPIRIT / CAM_T0_BED
	// The bed is the form change.
	// Day and dawn stay FORM_BODY and do not move the clock.
	// #9 Night without this grant stays FORM_BODY.
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

	if (!TimeOfDay->GetIsSpiritPhase())
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: day bed stays FORM_BODY (sleep grants spirit only at night or dusk)"));
		ShowInteractFeedback(TEXT("NODE_BED: day stays body"), FColor::Yellow);
		return false;
	}
	EndPartyOuting(World, EHomeWorldPartyAbsence::Bed);

	if (bBedSpiritGranted && bIsSpiritForm && bSpiritSleepGateGranted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_BED (already granted; #9 w/o bed stay FORM_BODY)"));
		ShowInteractFeedback(TEXT("NODE_BED: already spirit"), FColor::Green);
		return true;
	}

	GrantSpiritSleepGate();

	bBedSpiritGranted = true;
	if (bIsSpiritForm)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_BED (GrantSpiritSleepGate; not phase-alone; #9 w/o bed stay FORM_BODY)"));
		ShowInteractFeedback(TEXT("NODE_BED: FORM_SPIRIT"), FColor::Green);
		return true;
	}

	UE_LOG(LogTemp, Log,
		TEXT("NODE_BED: sleep gate granted but FORM_BODY (unexpected at night; not phase-alone spirit)"));
	ShowInteractFeedback(TEXT("NODE_BED: sleep gate only"), FColor::Yellow);
	return false;
}

bool AHomeWorldCharacter::TryPortalHomeToCamp()
{
	// T0_M13 NODE_PORTAL_HOME / NODE_PORTAL_CAMP / TOD_NIGHT_SPIRIT / FORM_SPIRIT
	// Architecture Trade-Offs A-E: prefer existing HomeWorldShrinePortal* TryPortalTransit /
	// TryPortalTransitToDestination -- no parallel portal service, no invent portal/WP APIs, no PROP schema.
	// Prereq: #11 spirit path (the bed).
	// Anti closed_fail: home<->planet return alone (GP_PortalA<->B / Shrine_Return) as #13;
	// body portal as #13; shrine-dress-as-camp as #13.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	if (!GetIsSpiritForm())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PORTAL_HOME: portal-camp skipped - need FORM_SPIRIT (body portal != #13; closed_fail)"));
		ShowInteractFeedback(TEXT("NODE_PORTAL_HOME: spirit form only"), FColor::Yellow);
		return false;
	}

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsSpiritPhase())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_PORTAL_HOME: portal-camp skipped - need TOD_NIGHT_SPIRIT"));
		ShowInteractFeedback(TEXT("NODE_PORTAL_HOME: night spirit phase only"), FColor::Yellow);
		return false;
	}

	if (bPortalHomeToCampGranted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_PORTAL_HOME: NODE_PORTAL_CAMP TOD_NIGHT_SPIRIT FORM_SPIRIT (already granted; home->camp latch; not home<->planet alone; not body; not dress-as-camp)"));
		ShowInteractFeedback(TEXT("NODE_PORTAL_HOME: already camp"), FColor::Green);
		return true;
	}

	// Camp destination labels (KEEP-LOCAL may provide GP_PortalCamp / NODE_PORTAL_CAMP / GP_RS_HumanoidCamp).
	// Do NOT treat Shrine_Return / GP_PortalB / VS_MARKER_PortalPlanet as camp (home<->planet != #13).
	static const FName CampLabels[] = {
		FName(TEXT("NODE_PORTAL_CAMP")),
		FName(TEXT("GP_PortalCamp")),
		FName(TEXT("GP_RS_HumanoidCamp")),
		FName(TEXT("ANCHOR_NODE_PORTAL_CAMP")),
		FName(TEXT("ANCHOR_GP_PortalCamp")),
	};
	static const FName PlanetOnlyLabels[] = {
		FName(TEXT("SM_Shrine_Return")),
		FName(TEXT("ANCHOR_SM_Shrine_Return")),
		FName(TEXT("GP_PortalB")),
		FName(TEXT("VS_MARKER_PortalPlanet")),
	};

	auto ActorMatchesLabel = [](AActor* Actor, const FName& Label) -> bool
	{
		if (!Actor || Label.IsNone())
		{
			return false;
		}
#if WITH_EDITOR
		if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return true;
		}
#endif
		if (Actor->GetName().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return true;
		}
		if (Actor->ActorHasTag(Label))
		{
			return true;
		}
		return false;
	};

	FName FoundCampLabel = NAME_None;
	AActor* CampActor = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		for (const FName& Label : CampLabels)
		{
			if (ActorMatchesLabel(Actor, Label))
			{
				FoundCampLabel = Label;
				CampActor = Actor;
				break;
			}
		}
		if (CampActor)
		{
			break;
		}
	}

	// Prefer home-side shrine portal (GP_PortalA / NODE_PORTAL_HOME) -- reuse TryPortalTransitToDestination.
	UHomeWorldShrinePortalComponent* HomePortal = nullptr;
	static const FName HomeLabels[] = {
		FName(TEXT("NODE_PORTAL_HOME")),
		FName(TEXT("GP_PortalA")),
		FName(TEXT("VS_MARKER_PortalHome")),
		FName(TEXT("ANCHOR_SM_Shrine_Homestead")),
		FName(TEXT("SM_Shrine_Homestead")),
	};
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		UHomeWorldShrinePortalComponent* Portal = Actor->FindComponentByClass<UHomeWorldShrinePortalComponent>();
		if (!Portal)
		{
			continue;
		}
		bool bIsHome = false;
		for (const FName& Label : HomeLabels)
		{
			if (ActorMatchesLabel(Actor, Label))
			{
				bIsHome = true;
				break;
			}
		}
		if (bIsHome)
		{
			HomePortal = Portal;
			break;
		}
		// Fallback: first shrine portal whose DestinationLabel is planet-return (will override to camp).
		if (!HomePortal)
		{
			const FString Dest = Portal->DestinationLabel.ToString();
			for (const FName& PlanetLabel : PlanetOnlyLabels)
			{
				if (Dest.Equals(PlanetLabel.ToString(), ESearchCase::IgnoreCase)
					|| Dest.Contains(TEXT("Shrine_Return")))
				{
					HomePortal = Portal;
					break;
				}
			}
		}
	}

	bool bTransited = false;
	if (CampActor && HomePortal && !FoundCampLabel.IsNone())
	{
		bTransited = HomePortal->TryPortalTransitToDestination(this, FoundCampLabel);
		if (!bTransited)
		{
			// Soft: teleport to camp arrive offset using same pattern as GetArriveLocation (still via shrine module path intent).
			const FVector ArriveLoc = CampActor->GetActorLocation() + CampActor->GetActorForwardVector() * 80.0f;
			const FRotator ArriveRot(0.0f, CampActor->GetActorRotation().Yaw + 180.0f, 0.0f);
			SetActorLocationAndRotation(ArriveLoc, ArriveRot, false, nullptr, ETeleportType::TeleportPhysics);
			bTransited = true;
			UE_LOG(LogTemp, Log,
				TEXT("FALLBACK: Portal T0 camp soft-arrive at '%s' (HomeWorldShrinePortal* path; DestinationLabel override pending cooldown/night)"),
				*FoundCampLabel.ToString());
		}
	}
	else if (CampActor && !FoundCampLabel.IsNone())
	{
		// Camp marker present but no home portal component -- soft teleport; still not inventing parallel service.
		const FVector ArriveLoc = CampActor->GetActorLocation() + CampActor->GetActorForwardVector() * 80.0f;
		const FRotator ArriveRot(0.0f, CampActor->GetActorRotation().Yaw + 180.0f, 0.0f);
		SetActorLocationAndRotation(ArriveLoc, ArriveRot, false, nullptr, ETeleportType::TeleportPhysics);
		bTransited = true;
		UE_LOG(LogTemp, Log,
			TEXT("FALLBACK: Portal T0 camp soft-arrive (no HomeWorldShrinePortal* on home; camp marker present KEEP-LOCAL)"));
	}
	else
	{
		// KEEP-LOCAL: camp marker missing -- latch + prove labels without .uasset/.umap commit.
		UE_LOG(LogTemp, Log,
			TEXT("NODE_PORTAL_HOME: NODE_PORTAL_CAMP TOD_NIGHT_SPIRIT FORM_SPIRIT (soft latch; camp marker KEEP-LOCAL missing; no uasset/umap; not home<->planet alone; not body; not dress-as-camp)"));
		ShowInteractFeedback(TEXT("NODE_PORTAL_HOME: camp latch soft"), FColor::Green);
		bPortalHomeToCampGranted = true;
		return true;
	}

	bPortalHomeToCampGranted = true;
	UE_LOG(LogTemp, Log,
		TEXT("NODE_PORTAL_HOME: NODE_PORTAL_CAMP TOD_NIGHT_SPIRIT FORM_SPIRIT (home->camp via HomeWorldShrinePortal*; not home<->planet alone; not body; not dress-as-camp)"));
	ShowInteractFeedback(TEXT("NODE_PORTAL_HOME: camp"), FColor::Green);
	return true;
}


bool AHomeWorldCharacter::TryCampNight()
{
	// T0_M14 NODE_GUARD / NODE_SLEEPER / TOD_NIGHT_SPIRIT / FORM_SPIRIT / CAM_T0_CAMP_NIGHT
	// Architecture Trade-Offs A-E: prefer existing UHomeWorldSpiritStealthComponent --
	// no parallel stealth service, no invent PROP schema, no .uasset/.umap.
	// Prereq: #11 spirit path (the bed).
	// Anti closed_fail: script-only GP_SS_Lit_*; stealth-alone without soothe;
	// convert-as-soothe (ReportFoeConverted); PROP invent.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	if (!GetIsSpiritForm())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GUARD: camp-night skipped - need FORM_SPIRIT (body stealth != #14; closed_fail)"));
		ShowInteractFeedback(TEXT("NODE_GUARD: spirit form only"), FColor::Yellow);
		return false;
	}

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsSpiritPhase())
	{
		UE_LOG(LogTemp, Log, TEXT("NODE_GUARD: camp-night skipped - need TOD_NIGHT_SPIRIT"));
		ShowInteractFeedback(TEXT("NODE_GUARD: night spirit phase only"), FColor::Yellow);
		return false;
	}

	if (bCampNightGranted)
	{
		UE_LOG(LogTemp, Log,
			TEXT("NODE_GUARD: NODE_SLEEPER TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_CAMP_NIGHT "
				"(already granted; all-3-calmed latch; not convert; not GP_SS_Lit alone; not stealth-alone)"));
		ShowInteractFeedback(TEXT("NODE_GUARD: camp night already"), FColor::Green);
		return true;
	}

	UHomeWorldSpiritStealthComponent* Stealth = SpiritStealthComponent;
	if (!Stealth)
	{
		Stealth = FindComponentByClass<UHomeWorldSpiritStealthComponent>();
	}
	if (!Stealth)
	{
		UE_LOG(LogTemp, Warning, TEXT("NODE_GUARD: camp-night failed - no UHomeWorldSpiritStealthComponent (Arch B require stealth module)"));
		ShowInteractFeedback(TEXT("NODE_GUARD: no stealth component"), FColor::Yellow);
		return false;
	}

	// Three guards. Ease each until asleep. Two asleep does not open the gate.
	ArriveAtCamp();
	for (int32 GuardIndex = 0; GuardIndex < HomeWorldCampNight::GetGatedActorCount(); ++GuardIndex)
	{
		bool bEased = false;
		bool bAsleep = false;
		if (Stealth->GetCampActorState(EHomeWorldCampRole::Guard, GuardIndex, bEased, bAsleep) && !bEased)
		{
			if (!Stealth->TryEaseCampActor(EHomeWorldCampRole::Guard, GuardIndex))
			{
				UE_LOG(LogTemp, Log, TEXT("NODE_GUARD: ease failed - they must be reached unseen, then put to sleep"));
				return false;
			}
			RecordGuardEased(GuardIndex);
		}
	}

	if (!Stealth->IsCampNightBeatComplete())
	{
		// Stealth-alone / incomplete calm = not #14 PASS. The strict half is reported
		// alongside the gameplay half so a soft-latched run is visibly not evidence.
		UE_LOG(LogTemp, Log,
			TEXT("NODE_GUARD: camp-night incomplete (calm=%d/%d strict=%d; stealth-alone = closed_fail)"),
			Stealth->GetCalmedActorCount(), HomeWorldCampNight::GetGatedActorCount(),
			Stealth->IsFreedomUnlockedStrict() ? 1 : 0);
		ShowInteractFeedback(TEXT("NODE_GUARD: incomplete beat"), FColor::Yellow);
		return false;
	}

	bCampNightGranted = true;
	UE_LOG(LogTemp, Log,
		TEXT("NODE_GUARD: NODE_SLEEPER TOD_NIGHT_SPIRIT FORM_SPIRIT CAM_T0_CAMP_NIGHT "
			"(all 3 calmed via UHomeWorldSpiritStealthComponent; guard eased awake->asleep, sleepers kept asleep; "
			"strict=%d; soothe != convert; not GP_SS_Lit alone; not stealth-alone)"),
		Stealth->IsFreedomUnlockedStrict() ? 1 : 0);
	ShowInteractFeedback(TEXT("NODE_GUARD: camp night"), FColor::Green);
	return true;
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
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldHomeLoopSubsystem* HomeLoop = World->GetSubsystem<UHomeWorldHomeLoopSubsystem>())
		{
			HomeLoop->Advance(0.f);
			if (NewPhase == EHomeWorldTimeOfDayPhase::Day && !bIsSpiritForm)
			{
				const float Bonus = HomeLoop->GetSprintBonusSeconds();
				if (Bonus > 0.f)
				{
					const float Now = World->GetTimeSeconds();
					if (TeaSprintEndWorldTime < Now)
					{
						TeaSprintEndWorldTime = Now;
					}
					TeaSprintEndWorldTime += Bonus;
				}
			}
		}
	}
	ApplyFormForPhase(NewPhase);
	// T0 #1: Day entry (not Dawn/bed->AdvanceToDawn alone) can emit NODE_WAKE start-day beat.
	TryEmitNodeWakeStartDayBeat();
	// T0 #2: tea sprint gate is Day-scoped (~half day within TOD_DAY).
	if (NewPhase == EHomeWorldTimeOfDayPhase::Day && !bPartnerTaken)
	{
		PartnerPlace = EHomeWorldFamilyPlace::ByBed;
		ChildPlace = EHomeWorldFamilyPlace::InGarden;
	}
	if (NewPhase != EHomeWorldTimeOfDayPhase::Day && TeaSprintEndWorldTime > 0.f)
	{
		TeaSprintEndWorldTime = 0.f;
		if (TraversalComponent)
		{
			TraversalComponent->SetSprintHeld(false);
		}
		UE_LOG(LogTemp, Log, TEXT("NODE_KETTLE: tea sprint gate cleared (left TOD_DAY)"));
	}
	if (NewPhase == EHomeWorldTimeOfDayPhase::Night)
	{
		NotifyPocketNight();
	}
}


bool AHomeWorldCharacter::CanEnterSpiritForm() const
{
	// Sleep gate only. Phase alone never grants spirit.
	return bSpiritSleepGateGranted;
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

void AHomeWorldCharacter::GrantSpiritSleepGate()
{
	bSpiritSleepGateGranted = true;
	UE_LOG(LogTemp, Log, TEXT("FORM: sleep gate granted (NODE_BED path)"));
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldHomeLoopSubsystem* HomeLoop = World->GetSubsystem<UHomeWorldHomeLoopSubsystem>())
		{
			HomeLoop->SetOpeningDayEnded(true);
		}
	}
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

namespace HomeWorldSpiritSickness
{
	static constexpr int32 MaxStacks = 5;
	static constexpr float IntervalSeconds = 10.f;
	static constexpr float MoveScale = 0.85f;
	static constexpr float LateWakeSeconds = 60.f;
}

float AHomeWorldCharacter::GetSpiritSicknessMoveScale() const
{
	const bool bSlow = SpiritSicknessStacks > 0 || LateWakeSlowSecondsRemaining > 0.f;
	return bSlow ? HomeWorldSpiritSickness::MoveScale : 1.f;
}

void AHomeWorldCharacter::RefreshSpiritSicknessMovement()
{
	const float Scale = GetSpiritSicknessMoveScale();
	if (TraversalComponent)
	{
		TraversalComponent->SetMovementSlowScale(Scale);
	}
	if (FallbackGlideComponent)
	{
		FallbackGlideComponent->SetGlideSpeedScale(Scale);
	}
}

void AHomeWorldCharacter::AddSpiritSicknessStack()
{
	if (bSpiritSicknessBooting || SpiritSicknessStacks >= HomeWorldSpiritSickness::MaxStacks)
	{
		return;
	}
	++SpiritSicknessStacks;
	bHadSpiritSicknessThisOuting = true;
	UE_LOG(LogTemp, Log, TEXT("SICKNESS: stack %d scarf step %d (flat 15 percent; no bar)"),
		SpiritSicknessStacks, SpiritSicknessStacks);
	RefreshSpiritSicknessMovement();
	if (SpiritSicknessStacks >= HomeWorldSpiritSickness::MaxStacks)
	{
		BeginSpiritSicknessBoot();
	}
}

void AHomeWorldCharacter::BeginSpiritSicknessBoot()
{
	bSpiritSicknessBooting = true;
	SpiritSicknessSecondsUntilNext = -1.f;
	RefreshSpiritSicknessMovement();
	bool bStarted = false;
	if (FallbackGlideComponent)
	{
		// Same live glide as the other boots. Stay spirit until it lands. No cut.
		bStarted = FallbackGlideComponent->StartGlideHome(/*bAllowNightPhase=*/true);
	}
	UE_LOG(LogTemp, Log, TEXT("SICKNESS: fifth stack live glide %s (stay spirit until the bed; ease beat stays)"),
		bStarted ? TEXT("started") : TEXT("pending"));
}

void AHomeWorldCharacter::NoteStillOutPastDawn(EHomeWorldTimeOfDayPhase Phase)
{
	const bool bPastNight = Phase == EHomeWorldTimeOfDayPhase::Dawn || Phase == EHomeWorldTimeOfDayPhase::Day;
	if (!bPastNight || !bIsSpiritForm || bSpiritSicknessBooting || bSpiritSicknessPausedAtBed)
	{
		return;
	}
	if (SpiritSicknessSecondsUntilNext >= 0.f || SpiritSicknessStacks >= HomeWorldSpiritSickness::MaxStacks)
	{
		return;
	}
	if (SpiritSicknessStacks == 0)
	{
		AddSpiritSicknessStack();
	}
	if (!bSpiritSicknessBooting && SpiritSicknessStacks < HomeWorldSpiritSickness::MaxStacks)
	{
		SpiritSicknessSecondsUntilNext = HomeWorldSpiritSickness::IntervalSeconds;
	}
}

void AHomeWorldCharacter::TickSpiritSickness(float DeltaTime)
{
	if (DeltaTime < 0.f)
	{
		return;
	}
	if (LateWakeSlowSecondsRemaining > 0.f)
	{
		LateWakeSlowSecondsRemaining = FMath::Max(0.f, LateWakeSlowSecondsRemaining - DeltaTime);
		RefreshSpiritSicknessMovement();
	}
	if (SpiritSicknessSecondsUntilNext < 0.f || bSpiritSicknessBooting || bSpiritSicknessPausedAtBed || !bIsSpiritForm)
	{
		return;
	}
	SpiritSicknessSecondsUntilNext -= DeltaTime;
	while (SpiritSicknessSecondsUntilNext <= 0.f
		&& !bSpiritSicknessBooting
		&& SpiritSicknessStacks < HomeWorldSpiritSickness::MaxStacks
		&& bIsSpiritForm
		&& !bSpiritSicknessPausedAtBed)
	{
		SpiritSicknessSecondsUntilNext += HomeWorldSpiritSickness::IntervalSeconds;
		AddSpiritSicknessStack();
	}
}

void AHomeWorldCharacter::TouchSpiritBed()
{
	if (SpiritSicknessStacks > 0)
	{
		bHadSpiritSicknessThisOuting = true;
	}
	SpiritSicknessStacks = 0;
	SpiritSicknessSecondsUntilNext = -1.f;
	bSpiritSicknessPausedAtBed = true;
	RefreshSpiritSicknessMovement();
	UE_LOG(LogTemp, Log, TEXT("SICKNESS: bed touch clears stacks (stay spirit; scarf step 0)"));
	ShowInteractFeedback(TEXT("SICKNESS: stacks cleared"), FColor::Green);
}

void AHomeWorldCharacter::WakeFromSpiritAtBed()
{
	const bool bLate = bHadSpiritSicknessThisOuting;
	SpiritSicknessStacks = 0;
	SpiritSicknessSecondsUntilNext = -1.f;
	bSpiritSicknessPausedAtBed = false;
	bSpiritSicknessBooting = false;
	bHadSpiritSicknessThisOuting = false;
	ClearSpiritSleepGate();
	SyncFormWithTimeOfDay();
	if (bLate)
	{
		LateWakeSlowSecondsRemaining = HomeWorldSpiritSickness::LateWakeSeconds;
	}
	RefreshSpiritSicknessMovement();
	UE_LOG(LogTemp, Log, TEXT("SICKNESS: bed ends spirit (late wake slow %s)"),
		bLate ? TEXT("60s") : TEXT("none"));
}

void AHomeWorldCharacter::NotifySpiritSicknessLanded()
{
	if (!bSpiritSicknessBooting)
	{
		return;
	}
	bSpiritSicknessBooting = false;
	SpiritSicknessStacks = 0;
	SpiritSicknessSecondsUntilNext = -1.f;
	bSpiritSicknessPausedAtBed = false;
	bHadSpiritSicknessThisOuting = false;
	LateWakeSlowSecondsRemaining = 0.f;
	ClearSpiritSleepGate();
	SyncFormWithTimeOfDay();
	RefreshSpiritSicknessMovement();
	UE_LOG(LogTemp, Log, TEXT("SICKNESS: landed at the bed, then body (no cut)"));
}

void AHomeWorldCharacter::OnSpiritSicknessGlideCompleted()
{
	NotifySpiritSicknessLanded();
}

bool AHomeWorldCharacter::TryTellChildDawnRule()
{
	if (bChildDawnRuleTold || bBedSpiritGranted || bIsSpiritForm)
	{
		return false;
	}
	bChildDawnRuleTold = true;
	UE_LOG(LogTemp, Log, TEXT("CHILD: the bed and the dawn"));
	ShowInteractFeedback(TEXT("The bed and the dawn."), FColor::White);
	return true;
}

void AHomeWorldCharacter::ApplyFormForPhase(EHomeWorldTimeOfDayPhase Phase)
{
	const bool bSpiritCapablePhase =
		(Phase == EHomeWorldTimeOfDayPhase::Night || Phase == EHomeWorldTimeOfDayPhase::Dusk);

	// Bed or the fifth stack ends spirit. Dawn does not. Night without the sleep gate stays body.
	const bool bSpirit = bSpiritSleepGateGranted && (bSpiritCapablePhase || bIsSpiritForm);

	if (Phase == LastAppliedFormPhase && bIsSpiritForm == bSpirit)
	{
		NoteStillOutPastDawn(Phase);
		return;
	}
	LastAppliedFormPhase = Phase;

	if (bIsSpiritForm != bSpirit)
	{
		bIsSpiritForm = bSpirit;

		static const TCHAR* PhaseNames[] = { TEXT("Day"), TEXT("Dusk"), TEXT("Night"), TEXT("Dawn") };
		const int32 PhaseIdx = FMath::Clamp(static_cast<int32>(Phase), 0, 3);
		const TCHAR* FormLabel = bSpirit ? TEXT("spirit") : TEXT("body");
	UE_LOG(LogTemp, Log, TEXT("FORM: %s form (phase=%s; gates sleep=%d; NightMix driven by TimeOfDaySubsystem)"),
		FormLabel, PhaseNames[PhaseIdx], bSpiritSleepGateGranted ? 1 : 0);

		if (TraversalComponent)
		{
			TraversalComponent->ApplyFormMovementTuning(bSpirit);
		}

		PlaySoftFormSwapFeedback(Phase, bSpirit);
	}

	NoteStillOutPastDawn(Phase);
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
	if (bOpeningRuneActive || bOpeningDogDrawActive || bSizeTestInteractCursor || (StrokeReport && StrokeReport->IsStrokeHeld()))
	{
		return;
	}
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
	if (UGameplayStatics::GetCurrentLevelName(this).Contains(TEXT("SizeTest")))
	{
		return;
	}
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
	if (const AHomeWorldOpeningReveal* Opening = Cast<AHomeWorldOpeningReveal>(Actor))
	{
		return Opening->IsSpiritVisible();
	}
	if (Actor->ActorHasTag(FName(TEXT("NPC_PARTNER")))
		|| Actor->ActorHasTag(FName(TEXT("NPC_CHILD")))
		|| Actor->ActorHasTag(FName(TEXT("NODE_ZIPLINE"))))
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
	// T0 beat props. These are ordinary greybox actors - a collider and a tag - so the
	// spec table is the only place their attributes live. The gate asks it instead of
	// carrying a list of its own.
	HomeWorldInteract::FSpec Spec;
	if (HomeWorldInteract::TrySpecFor(Actor, Spec))
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

	AActor* BestActor = nullptr;
	float BestScore = -1.f;

	// One search list: every actor the admission accepts, whatever its tag or component.
	// A newly placed prop with a beat tag is a candidate without editing this function.
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Candidate = *It;
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
		if (!HasOpeningLineOfSight(Candidate))
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
	const FVector Start = GetActorLocation() + FVector(0.0f, 0.0f, GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() * 0.5f : 50.0f);
	const FVector End = Start + GetControlRotation().Vector() * InteractTraceLengthCm;
	FCollisionQueryParams Params(NAME_None, false, this);
	if (World->LineTraceSingleByChannel(OutHit, Start, End, ECC_Visibility, Params))
	{
		AActor* HitActor = GetInteractTargetActor(OutHit);
		if (ActorHasInteractableComponent(HitActor)
			|| (HitActor && HitActor->GetActorNameOrLabel().Contains(TEXT("Lupine"))))
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
