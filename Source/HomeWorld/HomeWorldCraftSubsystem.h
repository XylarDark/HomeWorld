// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldCraftTypes.h"
#include "HomeWorldCraftSubsystem.generated.h"

class AHomeWorldCharacter;
class AHomeWorldCraftStation;
class UHomeWorldInventorySubsystem;

/**
 * GC-B: named hearth recipes, Stored-first spend, demo progression (campfire → tent → cottage unlock).
 */
UCLASS()
class HOMEWORLD_API UHomeWorldCraftSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	bool HasCampfirePlaced() const { return bCampfirePlaced; }
	bool HasTentPlaced() const { return bTentPlaced; }
	bool IsCottageUnlocked() const { return bCottageUnlocked; }

	/** Interact at a craft station (hub / campfire / kitchen). Returns true when handled. */
	bool TryInteractAtStation(AHomeWorldCharacter* Character, AHomeWorldCraftStation* Station);

	/** Craft a named recipe at the current station context (cheat / explicit calls). */
	bool TryCraftRecipe(AHomeWorldCharacter* Character, EHomeWorldCraftRecipeId Recipe, AHomeWorldCraftStation* StationContext);

	/** After tent exists: second campfire interact can unlock without another spend. */
	bool TryCottageUnlockAtCampfire(AHomeWorldCharacter* Character);

private:
	UPROPERTY()
	bool bCampfirePlaced = false;

	UPROPERTY()
	bool bTentPlaced = false;

	UPROPERTY()
	bool bCottageUnlocked = false;

	bool CanAffordRecipe(UWorld* World, UHomeWorldInventorySubsystem* Inv, EHomeWorldCraftRecipeId Recipe) const;
	bool SpendForRecipe(UWorld* World, UHomeWorldInventorySubsystem* Inv, EHomeWorldCraftRecipeId Recipe);
	int32 CountStoredForResource(UWorld* World, FName ResourceId) const;
	bool SpendOneFromStored(UWorld* World, FName ResourceId);
	void ApplyRecipeOutcome(AHomeWorldCharacter* Character, EHomeWorldCraftRecipeId Recipe, AHomeWorldCraftStation* StationContext);
	void UnlockCottageIfNeeded(AHomeWorldCharacter* Character);
	AHomeWorldCraftStation* SpawnPlaceableStation(
		UWorld* World,
		EHomeWorldCraftStationKind Kind,
		const FVector& Location,
		const FRotator& Rotation,
		const FString& ActorLabel) const;
};
