// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldSpiritRosterSubsystem.generated.h"

/**
 * Game instance subsystem for the spirit roster (Day 21).
 * When a character dies, game code adds them as a spirit via AddSpirit.
 * Day 22 uses this list for "assign spirit to node."
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldSpiritRosterSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Add a spirit to the roster (e.g. on character death). Id should be unique (e.g. spawn ID or instance name). */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Add Spirit"))
	void AddSpirit(FName SpiritId);

	/** Get all spirit IDs in the roster. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Get Spirits"))
	TArray<FName> GetSpirits() const;

	/** Remove spirit from roster (e.g. when unassigning and reclaiming in Day 23). Returns true if found and removed. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Remove Spirit"))
	bool RemoveSpirit(FName SpiritId);

	/** Number of spirits in the roster. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Get Spirit Count"))
	int32 GetSpiritCount() const;

	/** Write current spirit IDs into SaveGame for persistence. */
	void SerializeToSaveGame(class UHomeWorldSaveGame* Out) const;

	/** Restore spirit roster from SaveGame (replaces current in-memory state). */
	void DeserializeFromSaveGame(const class UHomeWorldSaveGame* In);

	/** Item 5: write the roster into this system's save slice. */
	void WriteSaveSlice(TArray<uint8>& OutBytes) const;

	/** Item 5: restore from this system's save slice. False (and no change) if the bytes do not read. */
	bool ReadSaveSlice(const TArray<uint8>& InBytes);

private:
	UPROPERTY()
	TArray<FName> SpiritIds;
};
