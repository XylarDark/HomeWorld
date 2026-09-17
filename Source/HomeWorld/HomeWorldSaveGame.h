// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/SaveGame.h"
#include "HomeWorldInventoryTypes.h"
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

	/** Saved TimeOfDay phase (EHomeWorldTimeOfDayPhase as uint8: Day=0, Dusk=1, Night=2, Dawn=3). Restored on hw.Load. */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	uint8 SavedTimeOfDayPhase = 0;

	/** Spiritual power count (night collectible). Restored to PlayerState on hw.Load. */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	int32 SavedSpiritualPowerCollected = 0;

	/** Day restoration buff (set when player consumed a meal this day). Restored to PlayerState on hw.Load. See DAY_RESTORATION_LOOP.md. */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	bool bSavedHasDayRestorationBuff = false;

	/** Love/bond level (0–N) earned this day; scales night bonuses. Restored to PlayerState on hw.Load. See DAY_LOVE_OR_BOND.md. */
	UPROPERTY(VisibleAnywhere, Category = "Save")
	int32 SavedLoveLevel = 0;

	/** NP-E V8 — six-slot inventory snapshot at dawn. */
	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	TArray<FHomeWorldInventorySlot> SavedInventorySlots;

	/** NP-E V8 — beast tame state (EHomeWorldBeastTameState as uint8). */
	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	uint8 SavedBeastTameState = 0;

	/** NP-E V8 — spirit heal ids (Spirit_A/B/C) parallel to SavedSpiritHealStates. */
	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	TArray<FName> SavedSpiritHealIds;

	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	TArray<uint8> SavedSpiritHealStates;

	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	bool bSavedN1Nurtured = false;

	UPROPERTY(VisibleAnywhere, Category = "Save|NP-E")
	bool bSavedN2Nurtured = false;
};
