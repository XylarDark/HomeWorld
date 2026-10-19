// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldWispPlacement.h"

#include "HomeWorldRuneShapeComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/Actor.h"

bool HomeWorldWisp::HoverPoint(
	const AActor* Target,
	const FVector& ViewerWorld,
	float HeadZ,
	float TimeSeconds,
	FVector& OutWorld)
{
	if (!Target)
	{
		return false;
	}
	FBox Box(ForceInit);
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
		Box += FBox(Bounds.Origin - Bounds.BoxExtent, Bounds.Origin + Bounds.BoxExtent);
	}
	if (!Box.IsValid)
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
			Box += FBox(Bounds.Origin - Bounds.BoxExtent, Bounds.Origin + Bounds.BoxExtent);
		}
	}
	if (!Box.IsValid)
	{
		FVector Origin = FVector::ZeroVector;
		FVector Extent = FVector::ZeroVector;
		Target->GetActorBounds(false, Origin, Extent);
		if (Extent.IsNearlyZero())
		{
			return false;
		}
		Box = FBox(Origin - Extent, Origin + Extent);
	}
	const FVector Center = Box.GetCenter();
	const FVector Extent = Box.GetExtent();
	FVector Look = Center - ViewerWorld;
	Look.Z = 0.f;
	if (!Look.Normalize())
	{
		Look = FVector(1.f, 0.f, 0.f);
	}
	const FVector Right = FVector::CrossProduct(FVector::UpVector, Look).GetSafeNormal();
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
