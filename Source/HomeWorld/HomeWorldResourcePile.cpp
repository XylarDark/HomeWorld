// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldResourcePile.h"
#include "HomeWorldGatherSiteTypes.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldTimeOfDaySubsystem.h"
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

	if (bDepletedUntilDawn)
	{
		if (UWorld* World = GetWorld())
		{
			if (UHomeWorldTimeOfDaySubsystem* TOD = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
			{
				if (TOD->GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Day && !TOD->GetIsNight())
				{
					OnDawnReset();
				}
			}
		}
	}
}

void AHomeWorldResourcePile::TickCooldown(float DeltaTime)
{
	if (CooldownRemaining > 0.f)
	{
		CooldownRemaining = FMath::Max(0.f, CooldownRemaining - DeltaTime);
	}
}

void AHomeWorldResourcePile::OnDawnReset()
{
	if (bDepletedUntilDawn)
	{
		bDepletedUntilDawn = false;
		UE_LOG(LogTemp, Verbose, TEXT("GATHER: node '%s' replenished at dawn"), *GetName());
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
			UE_LOG(LogTemp, Log, TEXT("GATHER: node '%s' depleted until dawn"), *GetName());
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

	if (bDepleteUntilDawn)
	{
		bDepletedUntilDawn = true;
	}
	else if (HarvestCooldownSeconds > 0.f)
	{
		CooldownRemaining = HarvestCooldownSeconds;
	}

	return true;
}
