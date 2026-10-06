// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldResourcePile.h"
#include "HomeWorldGatherSiteTypes.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"

AHomeWorldResourcePile::AHomeWorldResourcePile()
{
	PrimaryActorTick.bCanEverTick = true;

	OverlapVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("OverlapVolume"));
	OverlapVolume->SetBoxExtent(FVector(50.0f, 50.0f, 50.0f));
	OverlapVolume->SetCollisionProfileName(FName("BlockAllDynamic"));
	OverlapVolume->SetGenerateOverlapEvents(false);
	RootComponent = OverlapVolume;

	Tags.Add(FName("ResourcePile"));
}

void AHomeWorldResourcePile::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	TickCooldown(DeltaSeconds);

	// No dawn reset: a depleted node stays depleted for the rest of the session
	// (interview #11, 3A). Tick still runs because TickCooldown owns the countdown.
}

void AHomeWorldResourcePile::TickCooldown(float DeltaTime)
{
	if (CooldownRemaining > 0.f)
	{
		CooldownRemaining = FMath::Max(0.f, CooldownRemaining - DeltaTime);
	}
}

bool AHomeWorldResourcePile::IsHarvestAvailable() const
{
	if (bDepletedUntilDawn)
	{
		return false;
	}
	if (CooldownRemaining > 0.f)
	{
		return false;
	}
	if (GatherSiteKind != EHomeWorldGatherSiteKind::None)
	{
		return true;
	}
	if (!ResourceType.IsNone())
	{
		return true;
	}
	return HomeWorldGatherSite::InferSiteKindFromActor(this) != EHomeWorldGatherSiteKind::None;
}

FName AHomeWorldResourcePile::ResolveHarvestResourceId()
{
	EHomeWorldGatherSiteKind Site = GatherSiteKind;
	if (Site == EHomeWorldGatherSiteKind::None)
	{
		Site = HomeWorldGatherSite::InferSiteKindFromActor(this);
	}
	if (Site != EHomeWorldGatherSiteKind::None)
	{
		bool bHerbNext = bFlowerNextHarvestIsHerb;
		const FName FromSite = HomeWorldGatherSite::ResolveResourceForSite(Site, bHerbNext);
		if (Site == EHomeWorldGatherSiteKind::Flowers)
		{
			bFlowerNextHarvestIsHerb = bHerbNext;
		}
		if (!FromSite.IsNone())
		{
			return FromSite;
		}
	}
	return HomeWorldInventory::NormalizeResourceId(ResourceType);
}

bool AHomeWorldResourcePile::TryHarvest(UHomeWorldInventorySubsystem* Inventory)
{
	if (!Inventory || !IsHarvestAvailable())
	{
		if (bDepletedUntilDawn)
		{
			UE_LOG(LogTemp, Log, TEXT("GATHER: node '%s' depleted"), *GetName());
		}
		return false;
	}

	const FName Normalized = ResolveHarvestResourceId();
	if (Normalized.IsNone() || !HomeWorldInventory::IsValidResourceId(Normalized))
	{
		UE_LOG(LogTemp, Warning, TEXT("GATHER: node '%s' has no valid site→RES mapping"), *GetName());
		return false;
	}
	if (!Inventory->TryAddResource(Normalized, AmountPerHarvest))
	{
		return false;
	}

	const TCHAR* Flavor = HomeWorldGatherSite::GetGatherFlavorForResource(Normalized);
	if (Flavor && Flavor[0] != 0)
	{
		UE_LOG(LogTemp, Log, TEXT("GATHER: %s (%s)"), *Normalized.ToString(), Flavor);
	}

	// A successful harvest empties the node for good (interview #11, 3A). Nothing
	// in Source clears bDepletedUntilDawn, and both deprecated switches
	// (bDepleteUntilDawn, HarvestCooldownSeconds) are no longer read at all.
	bDepletedUntilDawn = true;

	return true;
}
