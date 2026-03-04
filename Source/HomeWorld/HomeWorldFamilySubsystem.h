// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldFamilySubsystem.generated.h"

/** Role names for family members (Protector, Healer, Child, Gatherer). */
UENUM(BlueprintType)
enum class EHomeWorldFamilyRole : uint8
{
	Gatherer,
	Protector,
	Healer,
	Child
};

/**
 * Game instance subsystem for family member role assignment and persistence (Day 15).
 * Maps spawn index (or stable ID) to role so State Tree and behavior can key off role.
 * SaveGame serialization can be added later.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldFamilySubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Set role for a family member by spawn index (0-based). Grows array as needed. */
	UFUNCTION(BlueprintCallable, Category = "Family", meta = (DisplayName = "Set Role For Index"))
	void SetRoleForIndex(int32 SpawnIndex, EHomeWorldFamilyRole Role);

	/** Get role for spawn index. Returns Gatherer if index out of range or not set. */
	UFUNCTION(BlueprintCallable, Category = "Family", meta = (DisplayName = "Get Role For Index"))
	EHomeWorldFamilyRole GetRoleForIndex(int32 SpawnIndex) const;

	/** Number of family members with assigned roles. */
	UFUNCTION(BlueprintCallable, Category = "Family", meta = (DisplayName = "Get Member Count"))
	int32 GetMemberCount() const;

	/** Write current role-by-index into SaveGame for persistence. */
	void SerializeToSaveGame(class UHomeWorldSaveGame* Out) const;

	/** Restore role-by-index from SaveGame (replaces current in-memory state). */
	void DeserializeFromSaveGame(const class UHomeWorldSaveGame* In);

private:
	UPROPERTY()
	TArray<EHomeWorldFamilyRole> RoleBySpawnIndex;
};
