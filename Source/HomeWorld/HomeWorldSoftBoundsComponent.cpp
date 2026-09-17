// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSoftBoundsComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/World.h"

#define LOG_BOUNDS(Format, ...) UE_LOG(LogTemp, Log, TEXT("BOUNDS: " Format), ##__VA_ARGS__)

UHomeWorldSoftBoundsComponent::UHomeWorldSoftBoundsComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UHomeWorldSoftBoundsComponent::BeginPlay()
{
	Super::BeginPlay();
	CachedCharacter = Cast<ACharacter>(GetOwner());
	LOG_BOUNDS("Soft walk bounds active center=(%.0f,%.0f,%.0f) radius=%.0f cm",
		BoundsCenter.X, BoundsCenter.Y, BoundsCenter.Z, BoundsRadiusXY);
}

bool UHomeWorldSoftBoundsComponent::IsInsideBounds(const FVector& Location) const
{
	const FVector Delta = Location - BoundsCenter;
	const float DistXY = FVector(Delta.X, Delta.Y, 0.f).Size();
	if (DistXY > BoundsRadiusXY)
	{
		return false;
	}
	if (Location.Z < MinZ || Location.Z > MaxZ)
	{
		return false;
	}
	return true;
}

void UHomeWorldSoftBoundsComponent::ApplySoftPushback(float DeltaTime)
{
	if (!bBoundsEnabled || !CachedCharacter)
	{
		return;
	}

	const FVector Location = CachedCharacter->GetActorLocation();
	if (IsInsideBounds(Location))
	{
		return;
	}

	FVector PushDir = BoundsCenter - Location;
	PushDir.Z = 0.f;
	if (PushDir.IsNearlyZero())
	{
		PushDir = FVector(1.f, 0.f, 0.f);
	}
	PushDir.Normalize();

	if (Location.Z < MinZ || Location.Z > MaxZ)
	{
		const float ZDelta = BoundsCenter.Z - Location.Z;
		PushDir.Z = FMath::Clamp(ZDelta / FMath::Max(BoundsRadiusXY, 1.f), -0.5f, 0.5f);
		PushDir.Normalize();
	}

	CachedCharacter->AddMovementInput(PushDir, PushbackStrength);

	if (UWorld* World = GetWorld())
	{
		const float Now = World->GetTimeSeconds();
		if (Now - LastPushbackLogTime > 2.f)
		{
			LastPushbackLogTime = Now;
			LOG_BOUNDS("soft pushback at (%.0f,%.0f,%.0f) toward hub", Location.X, Location.Y, Location.Z);
		}
	}
}

void UHomeWorldSoftBoundsComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	ApplySoftPushback(DeltaTime);
}
