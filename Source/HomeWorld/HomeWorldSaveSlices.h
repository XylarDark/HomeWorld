// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class UGameInstance;
class UWorld;
class UHomeWorldSaveGame;

/**
 * Refactor item 5 — save slices (Lead's locked answers, "Headless v3: A").
 *
 * 1. The save holds a map from a fixed FName key to a byte blob. Each system writes and
 *    reads only its own slice.
 * 2. An old save that has no slices is read once from the flat Saved* fields. After that
 *    only slices are written. The flat fields stay readable; a later bite deletes them.
 * 3. The keys are the fixed names in Key below, and only those. Quest systems keep their
 *    quest id; no key may also be a quest id.
 * 4. Nothing new is added to the save: the slices carry exactly what the flat fields did.
 *
 * GetFieldToKeyTable() names, for every flat Saved* field, the one slice that now owns it.
 * HomeWorld.Save.Slices.FieldToKeyTable fails if a field is unmapped or mapped twice.
 */
namespace HomeWorldSaveSlices
{
	/** THE key list. One place; add a system here and in the field table, nowhere else. */
	namespace Key
	{
		inline const TCHAR* const Family = TEXT("Family");
		inline const TCHAR* const SpiritRoster = TEXT("SpiritRoster");
		inline const TCHAR* const TimeOfDay = TEXT("TimeOfDay");
		inline const TCHAR* const PlayerState = TEXT("PlayerState");
		inline const TCHAR* const Inventory = TEXT("Inventory");
		inline const TCHAR* const Tame = TEXT("Tame");
		inline const TCHAR* const Heal = TEXT("Heal");
		inline const TCHAR* const Nurture = TEXT("Nurture");
	}

	/** The keys above, in that order. */
	HOMEWORLD_API const TArray<FName>& GetKeys();

	/** One row: a flat UHomeWorldSaveGame property name and the slice key that owns it. */
	struct FFieldToKey
	{
		FName Field;
		FName Key;
	};

	/** Every flat Saved* field of UHomeWorldSaveGame, each mapped to exactly one key. */
	HOMEWORLD_API const TArray<FFieldToKey>& GetFieldToKeyTable();

	/** True when Save carries a slice under Key. */
	HOMEWORLD_API bool HasSlice(const UHomeWorldSaveGame* Save, FName Key);

	/** Write every system's state into Save as slices. The flat fields are left at their defaults. */
	HOMEWORLD_API void CaptureToSave(UHomeWorldSaveGame* Save, UGameInstance* GI, UWorld* World);

	/**
	 * Read Save into the live systems: each system from its own slice, or, for an old save
	 * with no slices at all, once from the flat fields. A key missing from a sliced save
	 * leaves that system as it is. Load forces (party sent home at night, etc.) are
	 * not part of this; LoadGameFromSlot applies them afterwards.
	 */
	HOMEWORLD_API void ApplyFromSave(const UHomeWorldSaveGame* Save, UGameInstance* GI, UWorld* World);

	/**
	 * FName as its string, so a slice reads back in another process (a raw FName archives
	 * as a name-table index that only means something in the process that wrote it).
	 */
	HOMEWORLD_API void SerializeName(FArchive& Ar, FName& Name);
	HOMEWORLD_API void SerializeNames(FArchive& Ar, TArray<FName>& Names);

	/** The TimeOfDay phase stored in Save (EHomeWorldTimeOfDayPhase as uint8). */
	HOMEWORLD_API uint8 GetSavedPhase(const UHomeWorldSaveGame* Save);
}
