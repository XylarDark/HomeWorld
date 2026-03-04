// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldSaveGameSubsystem.generated.h"

/**
 * Game instance subsystem for saving/loading game state (Day 15 role persistence, Day 21 spirit roster).
 * Persists family roles and spirit roster via UHomeWorldSaveGame to a slot.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldSaveGameSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Default slot name when not specified. */
	static const TCHAR* DefaultSlotName;

	/** Save current family roles and spirit roster to the given slot. Pass empty SlotName for default "HomeWorldSave". UserIndex 0 = primary. */
	UFUNCTION(BlueprintCallable, Category = "Save", meta = (DisplayName = "Save Game To Slot"))
	bool SaveGameToSlot(const FString& SlotName, int32 UserIndex);

	/** Load family roles and spirit roster from the given slot. Pass empty SlotName for default. Returns true if load succeeded. */
	UFUNCTION(BlueprintCallable, Category = "Save", meta = (DisplayName = "Load Game From Slot"))
	bool LoadGameFromSlot(const FString& SlotName, int32 UserIndex);

	/** Returns true if a save exists in the given slot. Pass empty SlotName for default. */
	UFUNCTION(BlueprintCallable, Category = "Save", meta = (DisplayName = "Does Save Game Exist"))
	bool DoesSaveGameExist(const FString& SlotName, int32 UserIndex) const;
};
