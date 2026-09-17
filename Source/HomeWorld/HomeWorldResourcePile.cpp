// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldResourcePile.h"
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
	return !ResourceType.IsNone();
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

	const FName Normalized = HomeWorldInventory::NormalizeResourceId(ResourceType);
	if (!Inventory->TryAddResource(Normalized, AmountPerHarvest))
	{
		return false;
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
