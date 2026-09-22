// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCraftSubsystem.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldCraftStation.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldStoreTransferComponent.h"
#include "Engine/World.h"
#include "Engine/GameInstance.h"
#include "EngineUtils.h"

namespace
{
	struct FRecipeCostLine
	{
		FName ResourceId;
		int32 Amount;
	};

	bool GetFixedCosts(EHomeWorldCraftRecipeId Recipe, TArray<FRecipeCostLine>& OutCosts)
	{
		OutCosts.Reset();
		switch (Recipe)
		{
		case EHomeWorldCraftRecipeId::Campfire:
			OutCosts.Add({HomeWorldInventory::RES_WOOD, 1});
			OutCosts.Add({HomeWorldInventory::RES_STONE, 1});
			OutCosts.Add({HomeWorldInventory::RES_FIBER, 1});
			return true;
		case EHomeWorldCraftRecipeId::Tent:
			OutCosts.Add({HomeWorldInventory::RES_WOOD, 3});
			OutCosts.Add({HomeWorldInventory::RES_FIBER, 2});
			return true;
		case EHomeWorldCraftRecipeId::Torch:
			OutCosts.Add({HomeWorldInventory::RES_WOOD, 1});
			OutCosts.Add({HomeWorldInventory::RES_FIBER, 1});
			return true;
		case EHomeWorldCraftRecipeId::FishGear:
			OutCosts.Add({HomeWorldInventory::RES_FIBER, 1});
			OutCosts.Add({HomeWorldInventory::RES_BERRY, 1});
			return true;
		default:
			return false;
		}
	}

	bool RecipeUsesAlternateFood(EHomeWorldCraftRecipeId Recipe, FName& OutPreferred, FName& OutAlternate)
	{
		if (Recipe == EHomeWorldCraftRecipeId::TameBait)
		{
			OutPreferred = HomeWorldInventory::RES_BERRY;
			OutAlternate = HomeWorldInventory::RES_HERB;
			return true;
		}
		if (Recipe == EHomeWorldCraftRecipeId::HealSalve)
		{
			OutPreferred = HomeWorldInventory::RES_HERB;
			OutAlternate = HomeWorldInventory::RES_SEED;
			return true;
		}
		return false;
	}
}

int32 UHomeWorldCraftSubsystem::CountStoredForResource(UWorld* World, const FName ResourceId) const
{
	if (!World)
	{
		return 0;
	}
	const FName Id = HomeWorldInventory::NormalizeResourceId(ResourceId);
	int32 Total = 0;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (UHomeWorldStoreTransferComponent* Store = It->FindComponentByClass<UHomeWorldStoreTransferComponent>())
		{
			if (HomeWorldInventory::NormalizeResourceId(Store->GetResourceId()) == Id)
			{
				Total += Store->GetStoredCount();
			}
		}
	}
	return Total;
}

bool UHomeWorldCraftSubsystem::SpendOneFromStored(UWorld* World, const FName ResourceId)
{
	if (!World)
	{
		return false;
	}
	const FName Id = HomeWorldInventory::NormalizeResourceId(ResourceId);
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		UHomeWorldStoreTransferComponent* Store = It->FindComponentByClass<UHomeWorldStoreTransferComponent>();
		if (!Store || HomeWorldInventory::NormalizeResourceId(Store->GetResourceId()) != Id)
		{
			continue;
		}
		if (Store->GetStoredCount() <= 0)
		{
			continue;
		}
		Store->ConfigureResource(Id);
		// Direct decrement — craft pulls from homestead stored without round-tripping inventory.
		const int32 NewCount = Store->GetStoredCount() - 1;
		Store->SetStoredCountForCraft(NewCount);
		UE_LOG(LogTemp, Log, TEXT("CRAFT: spend stored %s (stored now %d)"), *Id.ToString(), NewCount);
		return true;
	}
	return false;
}

bool UHomeWorldCraftSubsystem::CanAffordRecipe(
	UWorld* World,
	UHomeWorldInventorySubsystem* Inv,
	const EHomeWorldCraftRecipeId Recipe) const
{
	if (!Inv || !World)
	{
		return false;
	}

	FName AltA = NAME_None;
	FName AltB = NAME_None;
	if (RecipeUsesAlternateFood(Recipe, AltA, AltB))
	{
		const int32 HaveA = CountStoredForResource(World, AltA) + Inv->GetResource(AltA);
		const int32 HaveB = CountStoredForResource(World, AltB) + Inv->GetResource(AltB);
		return HaveA >= 1 || HaveB >= 1;
	}

	TArray<FRecipeCostLine> Costs;
	if (!GetFixedCosts(Recipe, Costs))
	{
		return false;
	}
	for (const FRecipeCostLine& Line : Costs)
	{
		const int32 Have = CountStoredForResource(World, Line.ResourceId) + Inv->GetResource(Line.ResourceId);
		if (Have < Line.Amount)
		{
			return false;
		}
	}
	return true;
}

bool UHomeWorldCraftSubsystem::SpendForRecipe(
	UWorld* World,
	UHomeWorldInventorySubsystem* Inv,
	const EHomeWorldCraftRecipeId Recipe)
{
	if (!Inv || !World)
	{
		return false;
	}

	FName AltA = NAME_None;
	FName AltB = NAME_None;
	if (RecipeUsesAlternateFood(Recipe, AltA, AltB))
	{
		const int32 StoredA = CountStoredForResource(World, AltA);
		const int32 InvA = Inv->GetResource(AltA);
		const int32 StoredB = CountStoredForResource(World, AltB);
		const int32 InvB = Inv->GetResource(AltB);
		if (StoredA + InvA >= 1)
		{
			if (StoredA > 0 && SpendOneFromStored(World, AltA))
			{
				return true;
			}
			if (InvA >= 1)
			{
				if (Inv->SpendResource(AltA, 1))
				{
					UE_LOG(LogTemp, Log, TEXT("CRAFT: spend inventory-only for %s"), *AltA.ToString());
					return true;
				}
			}
		}
		if (StoredB + InvB >= 1)
		{
			if (StoredB > 0 && SpendOneFromStored(World, AltB))
			{
				return true;
			}
			if (InvB >= 1 && Inv->SpendResource(AltB, 1))
			{
				UE_LOG(LogTemp, Log, TEXT("CRAFT: spend inventory-only for %s"), *AltB.ToString());
				return true;
			}
		}
		return false;
	}

	TArray<FRecipeCostLine> Costs;
	if (!GetFixedCosts(Recipe, Costs))
	{
		return false;
	}

	for (const FRecipeCostLine& Line : Costs)
	{
		int32 Remaining = Line.Amount;
		while (Remaining > 0)
		{
			const int32 Stored = CountStoredForResource(World, Line.ResourceId);
			if (Stored > 0 && SpendOneFromStored(World, Line.ResourceId))
			{
				--Remaining;
				continue;
			}
			if (Inv->SpendResource(Line.ResourceId, 1))
			{
				UE_LOG(LogTemp, Log, TEXT("CRAFT: spend inventory-only for %s"), *Line.ResourceId.ToString());
				--Remaining;
				continue;
			}
			UE_LOG(LogTemp, Warning, TEXT("CRAFT: spend fail mid-recipe %s"), HomeWorldCraft::GetCraftLogLabel(Recipe));
			return false;
		}
	}
	return true;
}

AHomeWorldCraftStation* UHomeWorldCraftSubsystem::SpawnPlaceableStation(
	UWorld* World,
	const EHomeWorldCraftStationKind Kind,
	const FVector& Location,
	const FRotator& Rotation,
	const FString& ActorLabel) const
{
	if (!World)
	{
		return nullptr;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
	AHomeWorldCraftStation* Station = World->SpawnActor<AHomeWorldCraftStation>(
		AHomeWorldCraftStation::StaticClass(), Location, Rotation, Params);
	if (!Station)
	{
		return nullptr;
	}
	Station->StationKind = Kind;
	if (Kind == EHomeWorldCraftStationKind::Campfire)
	{
		Station->Tags.AddUnique(FName(TEXT("GC_Campfire")));
	}
	else if (Kind == EHomeWorldCraftStationKind::Kitchen)
	{
		Station->Tags.AddUnique(FName(TEXT("GC_Kitchen")));
	}
	Station->Tags.AddUnique(FName(*ActorLabel));
	return Station;
}

void UHomeWorldCraftSubsystem::UnlockCottageIfNeeded(AHomeWorldCharacter* Character)
{
	if (bCottageUnlocked)
	{
		return;
	}
	if (!bTentPlaced)
	{
		return;
	}
	bCottageUnlocked = true;
	UE_LOG(LogTemp, Log, TEXT("PROGRESS:COTTAGE_UNLOCK"));
}

void UHomeWorldCraftSubsystem::ApplyRecipeOutcome(
	AHomeWorldCharacter* Character,
	const EHomeWorldCraftRecipeId Recipe,
	AHomeWorldCraftStation* StationContext)
{
	UWorld* World = Character ? Character->GetWorld() : (StationContext ? StationContext->GetWorld() : nullptr);
	if (!World)
	{
		return;
	}

	const TCHAR* Label = HomeWorldCraft::GetCraftLogLabel(Recipe);
	UE_LOG(LogTemp, Log, TEXT("CRAFT: %s"), Label);

	switch (Recipe)
	{
	case EHomeWorldCraftRecipeId::Campfire:
	{
		bCampfirePlaced = true;
		FVector Loc = Character ? Character->GetActorLocation() : StationContext->GetActorLocation();
		FRotator Rot = Character ? Character->GetActorRotation() : StationContext->GetActorRotation();
		if (Character)
		{
			Loc += Character->GetActorForwardVector() * 220.f;
		}
		SpawnPlaceableStation(World, EHomeWorldCraftStationKind::Campfire, Loc, Rot, TEXT("GP_Craft_Campfire"));
		break;
	}
	case EHomeWorldCraftRecipeId::Tent:
	{
		bTentPlaced = true;
		FVector Loc = Character ? Character->GetActorLocation() : StationContext->GetActorLocation();
		if (Character)
		{
			Loc += Character->GetActorForwardVector() * 180.f + FVector(0.f, 120.f, 0.f);
		}
		SpawnPlaceableStation(World, EHomeWorldCraftStationKind::TentPlaceable, Loc, FRotator::ZeroRotator, TEXT("GP_Craft_Tent"));
		UnlockCottageIfNeeded(Character);
		break;
	}
	default:
		UE_LOG(LogTemp, Log, TEXT("CRAFT: %s stub ok (consumable placeholder)"), Label);
		break;
	}
}

bool UHomeWorldCraftSubsystem::TryCraftRecipe(
	AHomeWorldCharacter* Character,
	const EHomeWorldCraftRecipeId Recipe,
	AHomeWorldCraftStation* StationContext)
{
	if (!Character)
	{
		return false;
	}
	UWorld* World = Character->GetWorld();
	UGameInstance* GI = World ? World->GetGameInstance() : nullptr;
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv || !World)
	{
		UE_LOG(LogTemp, Warning, TEXT("CRAFT: fail — no inventory"));
		return false;
	}

	if (Recipe == EHomeWorldCraftRecipeId::Campfire && bCampfirePlaced)
	{
		UE_LOG(LogTemp, Log, TEXT("CRAFT: campfire already placed"));
		return false;
	}
	if (Recipe == EHomeWorldCraftRecipeId::Tent)
	{
		if (!bCampfirePlaced)
		{
			UE_LOG(LogTemp, Log, TEXT("CRAFT: tent blocked — craft campfire first"));
			return false;
		}
		if (bTentPlaced)
		{
			UE_LOG(LogTemp, Log, TEXT("CRAFT: tent already placed"));
			return false;
		}
	}

	if (!CanAffordRecipe(World, Inv, Recipe))
	{
		UE_LOG(LogTemp, Log, TEXT("CRAFT: fail — insufficient RES for %s"), HomeWorldCraft::GetCraftLogLabel(Recipe));
		return false;
	}

	if (!SpendForRecipe(World, Inv, Recipe))
	{
		return false;
	}

	ApplyRecipeOutcome(Character, Recipe, StationContext);
	return true;
}

bool UHomeWorldCraftSubsystem::TryCottageUnlockAtCampfire(AHomeWorldCharacter* Character)
{
	if (!bTentPlaced || bCottageUnlocked)
	{
		return false;
	}
	UnlockCottageIfNeeded(Character);
	return bCottageUnlocked;
}

bool UHomeWorldCraftSubsystem::TryInteractAtStation(AHomeWorldCharacter* Character, AHomeWorldCraftStation* Station)
{
	if (!Character || !Station)
	{
		return false;
	}

	const EHomeWorldCraftStationKind Kind = Station->GetStationKind();
	if (Kind == EHomeWorldCraftStationKind::TentPlaceable)
	{
		return false;
	}

	if (Kind == EHomeWorldCraftStationKind::Kitchen || (bCottageUnlocked && Kind == EHomeWorldCraftStationKind::Campfire))
	{
		if (bCottageUnlocked && Kind == EHomeWorldCraftStationKind::Campfire)
		{
			UE_LOG(LogTemp, Log, TEXT("CRAFT: kitchen rebind TODO — use GP_Craft_Kitchen when placed (GC-C)"));
		}
		// Kitchen accepts same recipe IDs; demo loop already complete — allow stub crafts only via cheats.
		if (TryCottageUnlockAtCampfire(Character))
		{
			return true;
		}
		return false;
	}

	if (Kind == EHomeWorldCraftStationKind::HubBootstrap)
	{
		if (!bCampfirePlaced)
		{
			return TryCraftRecipe(Character, EHomeWorldCraftRecipeId::Campfire, Station);
		}
		if (!bTentPlaced && bCampfirePlaced)
		{
			UE_LOG(LogTemp, Log, TEXT("CRAFT: use campfire station for tent"));
			return true;
		}
		return TryCottageUnlockAtCampfire(Character);
	}

	if (Kind == EHomeWorldCraftStationKind::Campfire)
	{
		if (!bCampfirePlaced)
		{
			return TryCraftRecipe(Character, EHomeWorldCraftRecipeId::Campfire, Station);
		}
		if (!bTentPlaced)
		{
			return TryCraftRecipe(Character, EHomeWorldCraftRecipeId::Tent, Station);
		}
		if (!bCottageUnlocked)
		{
			return TryCottageUnlockAtCampfire(Character);
		}
		UE_LOG(LogTemp, Log, TEXT("CRAFT: kitchen rebind TODO — cottage unlocked; kitchen station when GC-C content lands"));
		return true;
	}

	return false;
}
