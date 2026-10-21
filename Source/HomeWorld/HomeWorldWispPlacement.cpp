// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldWispPlacement.h"

#include "HomeWorldRuneShapeComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Actor.h"

namespace
{
	/** Mesh bounds of the object, rune ribbons excluded. Skeletal bodies cover the dog. */
	bool TargetBounds(const AActor* Target, FBox& OutBox)
	{
		OutBox = FBox(ForceInit);
		if (!Target)
		{
			return false;
		}
		TInlineComponentArray<UStaticMeshComponent*> Meshes;
		Target->GetComponents(Meshes);
		for (const UStaticMeshComponent* Mesh : Meshes)
		{
			if (!Mesh || !Mesh->GetStaticMesh() || !Mesh->IsVisible())
			{
				continue;
			}
			if (Mesh->GetTypedOuter<UHomeWorldRuneShapeComponent>())
			{
				continue;
			}
			const FBoxSphereBounds& Bounds = Mesh->Bounds;
			if (Bounds.BoxExtent.IsNearlyZero())
			{
				continue;
			}
			OutBox += FBox(Bounds.Origin - Bounds.BoxExtent, Bounds.Origin + Bounds.BoxExtent);
		}
		if (!OutBox.IsValid)
		{
			TInlineComponentArray<USkeletalMeshComponent*> Bodies;
			Target->GetComponents(Bodies);
			for (const USkeletalMeshComponent* Body : Bodies)
			{
				if (!Body || !Body->GetSkeletalMeshAsset() || !Body->IsVisible())
				{
					continue;
				}
				const FBoxSphereBounds& Bounds = Body->Bounds;
				if (Bounds.BoxExtent.IsNearlyZero())
				{
					continue;
				}
				OutBox += FBox(Bounds.Origin - Bounds.BoxExtent, Bounds.Origin + Bounds.BoxExtent);
			}
		}
		if (!OutBox.IsValid)
		{
			FVector Origin = FVector::ZeroVector;
			FVector Extent = FVector::ZeroVector;
			Target->GetActorBounds(false, Origin, Extent);
			if (Extent.IsNearlyZero())
			{
				return false;
			}
			OutBox = FBox(Origin - Extent, Origin + Extent);
		}
		return OutBox.IsValid != 0;
	}

	/** The viewer's right, horizontal. */
	FVector ViewerRight(const FVector& Center, const FVector& ViewerWorld)
	{
		FVector Look = Center - ViewerWorld;
		Look.Z = 0.f;
		if (!Look.Normalize())
		{
			Look = FVector(1.f, 0.f, 0.f);
		}
		return FVector::CrossProduct(FVector::UpVector, Look).GetSafeNormal();
	}
}

bool HomeWorldWisp::HoverPoint(
	const AActor* Target,
	const FVector& ViewerWorld,
	float HeadZ,
	float TimeSeconds,
	FVector& OutWorld)
{
	FBox Box(ForceInit);
	if (!TargetBounds(Target, Box))
	{
		return false;
	}
	const FVector Center = Box.GetCenter();
	const FVector Extent = Box.GetExtent();
	const FVector Right = ViewerRight(Center, ViewerWorld);
	const float TopZ = Center.Z + Extent.Z;
	const float Bob = FMath::Sin(TimeSeconds * 4.f) * 6.f;
	const bool bBelowHead = TopZ < HeadZ;
	float Side = HoverSideCm;
	if (bBelowHead)
	{
		const float SideReach = FMath::Abs(Extent.X * Right.X) + FMath::Abs(Extent.Y * Right.Y);
		Side = FMath::Min(SideReach + HoverAwayCm, HoverAwayMaxCm);
	}
	OutWorld = Center + Right * Side;
	OutWorld.Z = bBelowHead ? TopZ + HoverAboveCm + Bob : HeadZ + Bob;
	return true;
}

bool HomeWorldWisp::MeasureBounds(const AActor* Target, FVector& OutCenter, FVector& OutExtent)
{
	FBox Box(ForceInit);
	if (!TargetBounds(Target, Box))
	{
		return false;
	}
	OutCenter = Box.GetCenter();
	OutExtent = Box.GetExtent();
	return true;
}

bool HomeWorldWisp::HeartPoint(
	const AActor* Target,
	const FVector& ViewerWorld,
	float BaseZ,
	FVector& OutWorld)
{
	FBox Box(ForceInit);
	if (!TargetBounds(Target, Box))
	{
		return false;
	}
	const FVector Center = Box.GetCenter();
	const FVector Extent = Box.GetExtent();
	const FVector Right = ViewerRight(Center, ViewerWorld);
	// The heart's width lies on the same axis as this side step, so its near edge
	// needs the half-width plus a gap before the object's face starts.
	const float SideReach = FMath::Abs(Extent.X * Right.X) + FMath::Abs(Extent.Y * Right.Y);
	const float Side = FMath::Clamp(
		SideReach + HeartHalfWidthCm + HeartGapCm,
		HeartSideMinCm,
		HeartSideMaxCm);
	OutWorld = Center + Right * Side;
	OutWorld.Z = BaseZ;
	return true;
}
