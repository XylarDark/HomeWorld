// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldTraversalComponent.h"
#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"

#define LOG_MOVE(Format, ...) UE_LOG(LogTemp, Log, TEXT("MOVE: " Format), ##__VA_ARGS__)

namespace
{
	static const FName GSpiritBlinkTags[] = {
		FName(TEXT("SpiritAnchor")),
		FName(TEXT("SpiritBlink")),
		FName(TEXT("Shrine_POI")),
		FName(TEXT("ShrinePortal")),
	};
}

UHomeWorldTraversalComponent::UHomeWorldTraversalComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UHomeWorldTraversalComponent::BeginPlay()
{
	Super::BeginPlay();
	CachedCharacter = Cast<ACharacter>(GetOwner());
	if (CachedCharacter)
	{
		CachedMovement = CachedCharacter->GetCharacterMovement();
	}
	CacheDefaultMovement();
	LastSafeGroundLocation = CachedCharacter ? CachedCharacter->GetActorLocation() : FVector::ZeroVector;
	LOG_MOVE("MV-A traversal ready (one CMC)");
}

void UHomeWorldTraversalComponent::CacheDefaultMovement()
{
	if (!CachedMovement)
	{
		return;
	}
	DefaultGravityScale = CachedMovement->GravityScale;
	DefaultJumpZ = CachedMovement->JumpZVelocity;
	if (BodyWalkSpeed > 0.f)
	{
		CachedMovement->MaxWalkSpeed = BodyWalkSpeed;
	}
	if (JumpZVelocity > 0.f)
	{
		CachedMovement->JumpZVelocity = JumpZVelocity;
	}
}

bool UHomeWorldTraversalComponent::IsTraversalBlocked() const
{
	if (!CachedCharacter)
	{
		return true;
	}
	if (const UHomeWorldFallbackGlideComponent* Glide = CachedCharacter->FindComponentByClass<UHomeWorldFallbackGlideComponent>())
	{
		if (Glide->IsGliding())
		{
			return true;
		}
	}
	return false;
}

void UHomeWorldTraversalComponent::SetSprintHeld(bool bHeld)
{
	bSprintHeld = bHeld;
	UpdateSprintSpeed();
}

void UHomeWorldTraversalComponent::SetMountBoostActive(bool bActive)
{
	if (bMountBoostActive == bActive)
	{
		return;
	}
	bMountBoostActive = bActive;
	UpdateSprintSpeed();
	LOG_MOVE("mount_boost %s (same CMC MaxWalkSpeed)", bActive ? TEXT("on") : TEXT("off"));
}

void UHomeWorldTraversalComponent::ApplyFormMovementTuning(bool bSpiritForm)
{
	bSpiritFormTuning = bSpiritForm;
	if (!CachedMovement)
	{
		return;
	}
	CachedMovement->GravityScale = bSpiritForm ? SpiritGravityScale : DefaultGravityScale;
	UpdateSprintSpeed();
	LOG_MOVE("form_tune spirit=%d gravity=%.2f", bSpiritForm ? 1 : 0, CachedMovement->GravityScale);
}

void UHomeWorldTraversalComponent::UpdateSprintSpeed()
{
	if (!CachedMovement || IsTraversalBlocked())
	{
		return;
	}

	float Target = bSpiritFormTuning ? SpiritWalkSpeed : BodyWalkSpeed;
	if (bMountBoostActive && !bSpiritFormTuning)
	{
		Target = MountBoostWalkSpeed;
	}
	else if (bSprintHeld && !bSpiritFormTuning)
	{
		Target = SprintWalkSpeed;
	}
	CachedMovement->MaxWalkSpeed = Target;
}

void UHomeWorldTraversalComponent::UpdateFallSoftReset(float DeltaTime)
{
	if (!CachedCharacter || !CachedMovement || IsTraversalBlocked())
	{
		return;
	}

	if (CachedMovement->IsMovingOnGround())
	{
		LastSafeGroundLocation = CachedCharacter->GetActorLocation();
		TimeInFall = 0.f;
		return;
	}

	if (CachedMovement->IsFalling())
	{
		TimeInFall += DeltaTime;
		const float Drop = LastSafeGroundLocation.Z - CachedCharacter->GetActorLocation().Z;
		if (TimeInFall >= FallResetSeconds || Drop >= FallResetDropCm)
		{
			const float FallTime = TimeInFall;
			FVector ResetLoc = LastSafeGroundLocation;
			if (UCapsuleComponent* Capsule = CachedCharacter->GetCapsuleComponent())
			{
				ResetLoc.Z += Capsule->GetUnscaledCapsuleHalfHeight();
			}
			CachedCharacter->SetActorLocation(ResetLoc);
			CachedMovement->Velocity = FVector::ZeroVector;
			CachedMovement->SetMovementMode(MOVE_Walking);
			TimeInFall = 0.f;
			LOG_MOVE("soft_reset fall (time=%.1fs drop=%.0f cm)", FallTime, Drop);
		}
	}
}

void UHomeWorldTraversalComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	UpdateSprintSpeed();
	UpdateFallSoftReset(DeltaTime);
}

bool UHomeWorldTraversalComponent::ResolveMantleTarget(FVector& OutStandLocation, bool& bOutVault) const
{
	bOutVault = false;
	if (!CachedCharacter || !CachedMovement)
	{
		return false;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	const UCapsuleComponent* Capsule = CachedCharacter->GetCapsuleComponent();
	const float HalfHeight = Capsule ? Capsule->GetUnscaledCapsuleHalfHeight() : 88.f;
	const float Radius = Capsule ? Capsule->GetUnscaledCapsuleRadius() : 42.f;
	const FVector Feet = CachedCharacter->GetActorLocation();
	const FVector Forward = CachedCharacter->GetActorForwardVector().GetSafeNormal2D();
	const FVector TraceStart = Feet + FVector(0.f, 0.f, HalfHeight * 0.35f);

	FCollisionQueryParams Params(NAME_None, false, CachedCharacter);

	FHitResult WallHit;
	const FVector WallEnd = TraceStart + Forward * MantleForwardTraceCm;
	if (!World->LineTraceSingleByChannel(WallHit, TraceStart, WallEnd, ECC_Visibility, Params))
	{
		return false;
	}

	const float ObstacleTopZ = WallHit.ImpactPoint.Z;
	const float RiseNeeded = ObstacleTopZ - Feet.Z;
	if (RiseNeeded <= 10.f || RiseNeeded > MantleMaxRiseCm)
	{
		return false;
	}

	bOutVault = RiseNeeded <= VaultMaxRiseCm;

	const FVector LedgeProbeStart = WallHit.ImpactPoint + Forward * (Radius + 20.f) + FVector(0.f, 0.f, MantleMaxRiseCm + 40.f);
	const FVector LedgeProbeEnd = LedgeProbeStart - FVector(0.f, 0.f, MantleMaxRiseCm + 120.f);
	FHitResult LedgeHit;
	if (!World->LineTraceSingleByChannel(LedgeHit, LedgeProbeStart, LedgeProbeEnd, ECC_Visibility, Params))
	{
		return false;
	}

	OutStandLocation = LedgeHit.ImpactPoint + FVector(0.f, 0.f, HalfHeight + 2.f);
	return true;
}

bool UHomeWorldTraversalComponent::TryMantleOrVault()
{
	if (IsTraversalBlocked() || bSpiritFormTuning)
	{
		return false;
	}

	FVector StandLocation;
	bool bVault = false;
	if (!ResolveMantleTarget(StandLocation, bVault))
	{
		return false;
	}

	if (!CachedCharacter || !CachedMovement)
	{
		return false;
	}

	CachedMovement->StopMovementImmediately();
	CachedCharacter->SetActorLocation(StandLocation);
	CachedMovement->SetMovementMode(MOVE_Walking);
	LastSafeGroundLocation = StandLocation;

	if (bVault)
	{
		LOG_MOVE("VAULT");
	}
	else
	{
		LOG_MOVE("MANTLE");
	}
	return true;
}

AActor* UHomeWorldTraversalComponent::FindSpiritBlinkTarget() const
{
	UWorld* World = GetWorld();
	if (!World || !CachedCharacter)
	{
		return nullptr;
	}

	const FVector Origin = CachedCharacter->GetActorLocation();
	const FVector Forward = CachedCharacter->GetActorForwardVector().GetSafeNormal2D();

	AActor* Best = nullptr;
	float BestScore = -1.f;

	for (const FName& Tag : GSpiritBlinkTags)
	{
		TArray<AActor*> Tagged;
		UGameplayStatics::GetAllActorsWithTag(World, Tag, Tagged);
		for (AActor* Candidate : Tagged)
		{
			if (!Candidate)
			{
				continue;
			}
			const FVector To = Candidate->GetActorLocation() - Origin;
			const float Dist = To.Size2D();
			if (Dist < KINDA_SMALL_NUMBER || Dist > BlinkMaxRangeCm)
			{
				continue;
			}
			const float Dot = FVector::DotProduct(Forward, To.GetSafeNormal2D());
			if (Dot < -0.15f)
			{
				continue;
			}
			const float Score = Dot / Dist;
			if (Score > BestScore)
			{
				BestScore = Score;
				Best = Candidate;
			}
		}
	}

#if WITH_EDITOR
	if (!Best)
	{
		static const FName EditorLabels[] = {
			FName(TEXT("GP_SpiritAnchor")),
			FName(TEXT("GP_Shrine_Portal")),
		};
		for (const FName& Label : EditorLabels)
		{
			for (TActorIterator<AActor> It(World); It; ++It)
			{
				AActor* Actor = *It;
				if (Actor && Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
				{
					const float Dist = FVector::Dist2D(Origin, Actor->GetActorLocation());
					if (Dist <= BlinkMaxRangeCm)
					{
						return Actor;
					}
				}
			}
		}
	}
#endif

	return Best;
}

bool UHomeWorldTraversalComponent::TrySpiritBlink()
{
	if (!bSpiritFormTuning || IsTraversalBlocked())
	{
		LOG_MOVE("SPIRIT_BLINK skipped — need spirit form");
		return false;
	}

	UWorld* World = GetWorld();
	if (!World || !CachedCharacter || !CachedMovement)
	{
		return false;
	}

	const float Now = World->GetTimeSeconds();
	if (Now - LastBlinkWorldTime < BlinkCooldownSeconds)
	{
		LOG_MOVE("SPIRIT_BLINK cooldown");
		return false;
	}

	AActor* Target = FindSpiritBlinkTarget();
	if (!Target)
	{
		LOG_MOVE("SPIRIT_BLINK hook — no SpiritAnchor/Shrine tag in range (place GP_SpiritAnchor)");
		return false;
	}

	const UCapsuleComponent* Capsule = CachedCharacter->GetCapsuleComponent();
	const float HalfHeight = Capsule ? Capsule->GetUnscaledCapsuleHalfHeight() : 88.f;
	FVector Dest = Target->GetActorLocation();
	Dest.Z += HalfHeight;

	CachedMovement->StopMovementImmediately();
	CachedCharacter->SetActorLocation(Dest);
	CachedMovement->SetMovementMode(MOVE_Falling);
	LastBlinkWorldTime = Now;
	LastSafeGroundLocation = Dest;
	LOG_MOVE("SPIRIT_BLINK -> %s", *Target->GetName());
	return true;
}
