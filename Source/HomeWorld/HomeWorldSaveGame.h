// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "HomeWorldSaveGame.generated.h"

/**
 * Save game data for role persistence (Day 15) and spirit roster (Day 21).
 * Serializes family roles by spawn index and spirit IDs; used by UHomeWorldSaveGameSubsystem.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldSaveGame : public USaveGame
{
	GENERATED_BODY()

public:
	/** Saved family roles by spawn index (EHomeWorldFamilyRole as byte). */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	TArray<uint8> SavedRoleBySpawnIndex;

	/** Saved spirit IDs in the roster. */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	TArray<FName> SavedSpiritIds;
};
