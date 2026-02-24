// Copyright HomeWorld. All Rights Reserved.

#include "BuildPlacementSupport.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "CollisionQueryParams.h"

bool UBuildPlacementSupport::GetPlacementHit(UObject* WorldContextObject, float MaxDistance, FHitResult& OutHit)
{
	UWorld* World = GEngine ? GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::LogAndReturnNull) : nullptr;
	if (!World)
	{
		return false;
	}

	APlayerController* PC = World->GetFirstPlayerController();
	if (!PC)
	{
		return false;
	}

	FVector ViewLocation;
	FRotator ViewRotation;
	PC->GetPlayerViewPoint(ViewLocation, ViewRotation);

	const FVector TraceStart = ViewLocation;
	const FVector TraceEnd = ViewLocation + ViewRotation.Vector() * FMath::Max(0.0f, MaxDistance);

	FCollisionQueryParams Params(NAME_None, false);
	const bool bHit = World->LineTraceSingleByChannel(
		OutHit,
		TraceStart,
		TraceEnd,
		ECC_Visibility,
		Params
	);

	return bHit;
}

bool UBuildPlacementSupport::GetPlacementTransform(UObject* WorldContextObject, float MaxDistance, FHitResult& OutHit, FTransform& OutTransform)
{
	if (!GetPlacementHit(WorldContextObject, MaxDistance, OutHit))
	{
		return false;
	}
	// Placement pose: location at impact, rotation aligned to surface normal (Z up when normal is vertical).
	const FVector Loc = OutHit.ImpactPoint;
	const FVector Normal = OutHit.ImpactNormal.GetSafeNormal();
	const FRotator Rot = Normal.IsNearlyZero() ? FRotator::ZeroRotator : FRotationMatrix::MakeFromZ(Normal).Rotator();
	OutTransform = FTransform(Rot, Loc, FVector::OneVector);
	return true;
}
