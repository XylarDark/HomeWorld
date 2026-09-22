// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"

namespace
{
	const TArray<FName> GFallbackCrumbOrder = {
		FName(TEXT("CRUMB_Depart_Lookout")),
		FName(TEXT("CRUMB_Air_01")),
		FName(TEXT("CRUMB_Islet_01")),
		FName(TEXT("CRUMB_Air_02")),
		FName(TEXT("CRUMB_Islet_02")),
		FName(TEXT("CRUMB_Air_03")),
		FName(TEXT("CRUMB_Islet_03")),
		FName(TEXT("CRUMB_Approach")),
		FName(TEXT("CRUMB_Landing")),
	};

}

#define LOG_FALLBACK(Format, ...) UE_LOG(LogTemp, Log, TEXT("FALLBACK: " Format), ##__VA_ARGS__)

const TArray<FName>& UHomeWorldFallbackGlideComponent::GetLockedCrumbOrder()
{
	return GFallbackCrumbOrder;
}

UHomeWorldFallbackGlideComponent::UHomeWorldFallbackGlideComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
}

void UHomeWorldFallbackGlideComponent::BeginPlay()
{
	Super::BeginPlay();
	CachedCharacter = Cast<ACharacter>(GetOwner());
	if (CachedCharacter)
	{
		CachedMovement = CachedCharacter->GetCharacterMovement();
	}
}

AActor* UHomeWorldFallbackGlideComponent::FindActorByLabel(UWorld* World, FName Label) const
{
	if (!World || Label.IsNone())
	{
		return nullptr;
	}

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
		if (Actor->GetFName() == Label)
		{
			return Actor;
		}
		if (Actor->GetName().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return Actor;
		}
	}
	return nullptr;
}

bool UHomeWorldFallbackGlideComponent::ResolveCrumbPath(UWorld* World, TArray<FVector>& OutLocations)
{
	OutLocations.Reset();
	if (!World)
	{
		return false;
	}

	for (const FName& CrumbName : GFallbackCrumbOrder)
	{
		AActor* CrumbActor = FindActorByLabel(World, CrumbName);
		if (!CrumbActor)
		{
			LOG_FALLBACK(TEXT("ResolveCrumbPath failed — missing actor label '%s'"), *CrumbName.ToString());
			return false;
		}
		OutLocations.Add(CrumbActor->GetActorLocation());
		LOG_FALLBACK(TEXT("Resolved %s @ %s"), *CrumbName.ToString(), *CrumbActor->GetActorLocation().ToString());
	}
	return OutLocations.Num() == GFallbackCrumbOrder.Num();
}

void UHomeWorldFallbackGlideComponent::CacheMovementDefaults()
{
	if (!CachedCharacter || !CachedMovement)
	{
		return;
	}
	bSavedOrientRotationToMovement = CachedMovement->bOrientRotationToMovement;
	bSavedUseControllerRotationYaw = CachedCharacter->bUseControllerRotationYaw;
	SavedMovementMode = CachedMovement->MovementMode;
}

void UHomeWorldFallbackGlideComponent::ApplyGlideMovementLock()
{
	if (!CachedCharacter || !CachedMovement)
	{
		return;
	}
	CacheMovementDefaults();
	CachedMovement->StopMovementImmediately();
	CachedMovement->SetMovementMode(MOVE_None);
	CachedMovement->bOrientRotationToMovement = false;
	CachedCharacter->bUseControllerRotationYaw = false;
}

void UHomeWorldFallbackGlideComponent::RestoreMovement()
{
	if (!CachedCharacter || !CachedMovement)
	{
		return;
	}
	CachedMovement->SetMovementMode(SavedMovementMode);
	CachedMovement->bOrientRotationToMovement = bSavedOrientRotationToMovement;
	CachedCharacter->bUseControllerRotationYaw = bSavedUseControllerRotationYaw;
	CachedMovement->Velocity = FVector::ZeroVector;
}

bool UHomeWorldFallbackGlideComponent::StartGlide()
{
	if (bIsGliding)
	{
		LOG_FALLBACK(TEXT("StartGlide skipped — already gliding"));
		return false;
	}

	if (!CachedCharacter)
	{
		CachedCharacter = Cast<ACharacter>(GetOwner());
		if (CachedCharacter)
		{
			CachedMovement = CachedCharacter->GetCharacterMovement();
		}
	}
	if (!CachedCharacter || !CachedMovement)
	{
		LOG_FALLBACK(TEXT("StartGlide failed — owner is not a Character"));
		return false;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	if (bRequireDayPhase)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			const EHomeWorldTimeOfDayPhase Phase = TimeOfDay->GetCurrentPhase();
			if (TimeOfDay->GetIsNight())
			{
				LOG_FALLBACK(TEXT("StartGlide blocked — night phase (day/body glide only)"));
				return false;
			}
			if (Phase == EHomeWorldTimeOfDayPhase::Dusk)
			{
				LOG_FALLBACK(TEXT("StartGlide blocked — dusk buffer (no new glide start)"));
				return false;
			}
		}
	}

	if (!ResolveCrumbPath(World, CrumbLocations))
	{
		return false;
	}

	const float ClampedDuration = FMath::Clamp(GlideDurationSeconds, 25.0f, 40.0f);
	float TotalPathLength = 0.0f;
	for (int32 Index = 1; Index < CrumbLocations.Num(); ++Index)
	{
		TotalPathLength += FVector::Dist(CrumbLocations[Index - 1], CrumbLocations[Index]);
	}
	if (TotalPathLength <= KINDA_SMALL_NUMBER)
	{
		LOG_FALLBACK(TEXT("StartGlide failed — zero path length"));
		return false;
	}

	ApplyGlideMovementLock();
	CachedCharacter->SetActorLocation(CrumbLocations[0]);

	CurrentSegmentIndex = 0;
	SegmentAlpha = 0.0f;
	const float SegmentLength = FVector::Dist(CrumbLocations[0], CrumbLocations[1]);
	SegmentDuration = (SegmentLength / TotalPathLength) * ClampedDuration;
	SegmentDuration = FMath::Max(SegmentDuration, 0.5f);

	bIsGliding = true;
	SetComponentTickEnabled(true);

	LOG_FALLBACK(TEXT("StartGlide — %d crumbs, duration %.1fs, segment 0 -> 1 (%.1fs)"),
		CrumbLocations.Num(), ClampedDuration, SegmentDuration);
	return true;
}

void UHomeWorldFallbackGlideComponent::CancelGlide()
{
	if (!bIsGliding)
	{
		return;
	}
	LOG_FALLBACK(TEXT("CancelGlide — restoring walk"));
	FinishGlide(false);
}

void UHomeWorldFallbackGlideComponent::AdvanceGlide(float DeltaTime)
{
	if (!CachedCharacter || CrumbLocations.Num() < 2)
	{
		FinishGlide(false);
		return;
	}

	const int32 StartIndex = CurrentSegmentIndex;
	const int32 EndIndex = CurrentSegmentIndex + 1;
	if (!CrumbLocations.IsValidIndex(StartIndex) || !CrumbLocations.IsValidIndex(EndIndex))
	{
		FinishGlide(true);
		return;
	}

	SegmentAlpha += (SegmentDuration > KINDA_SMALL_NUMBER) ? (DeltaTime / SegmentDuration) : 1.0f;
	SegmentAlpha = FMath::Clamp(SegmentAlpha, 0.0f, 1.0f);

	const FVector StartLoc = CrumbLocations[StartIndex];
	const FVector EndLoc = CrumbLocations[EndIndex];
	const FVector NewLoc = FMath::Lerp(StartLoc, EndLoc, SegmentAlpha);
	CachedCharacter->SetActorLocation(NewLoc);

	const FVector FaceDir = (EndLoc - StartLoc).GetSafeNormal();
	if (!FaceDir.IsNearlyZero())
	{
		const FRotator FaceRot = FaceDir.Rotation();
		CachedCharacter->SetActorRotation(FRotator(0.0f, FaceRot.Yaw, 0.0f));
	}

	if (SegmentAlpha >= 1.0f - KINDA_SMALL_NUMBER)
	{
		if (EndIndex >= CrumbLocations.Num() - 1)
		{
			LOG_FALLBACK(TEXT("Reached CRUMB_Landing — glide complete"));
			FinishGlide(true);
			return;
		}

		CurrentSegmentIndex = EndIndex;
		SegmentAlpha = 0.0f;

		const float ClampedDuration = FMath::Clamp(GlideDurationSeconds, 25.0f, 40.0f);
		float TotalPathLength = 0.0f;
		for (int32 Index = 1; Index < CrumbLocations.Num(); ++Index)
		{
			TotalPathLength += FVector::Dist(CrumbLocations[Index - 1], CrumbLocations[Index]);
		}
		const float NextSegmentLength = FVector::Dist(CrumbLocations[CurrentSegmentIndex], CrumbLocations[CurrentSegmentIndex + 1]);
		SegmentDuration = (NextSegmentLength / TotalPathLength) * ClampedDuration;
		SegmentDuration = FMath::Max(SegmentDuration, 0.5f);

		LOG_FALLBACK(TEXT("Segment %d -> %d (%.1fs)"), CurrentSegmentIndex, CurrentSegmentIndex + 1, SegmentDuration);
	}
}

void UHomeWorldFallbackGlideComponent::FinishGlide(bool bCompleted)
{
	bIsGliding = false;
	SetComponentTickEnabled(false);
	RestoreMovement();
	CrumbLocations.Reset();
	CurrentSegmentIndex = 0;
	SegmentAlpha = 0.0f;

	if (bCompleted)
	{
		LOG_FALLBACK(TEXT("OnGlideCompleted fired"));
		OnGlideCompleted.Broadcast();
	}
}

void UHomeWorldFallbackGlideComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bIsGliding)
	{
		AdvanceGlide(DeltaTime);
	}
}
