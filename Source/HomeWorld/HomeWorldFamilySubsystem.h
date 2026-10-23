// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"

class AActor;
class UWorld;

#include "HomeWorldFamilySubsystem.generated.h"

/** Role names for family members (Protector, Healer, Child, Gatherer, Partner). */
UENUM(BlueprintType)
enum class EHomeWorldFamilyRole : uint8
{
	Gatherer,
	Protector,
	Healer,
	Child,
	/** MVP tutorial step 3: romantic partner for "complete one love task with partner". Identify by role (e.g. spawn index 0) or tag "Partner". */
	Partner
};

/** Derived party. Not saved. Solo is both flags false. Docs/41_COMPANION_PARTY_DESIGN.md. */
UENUM(BlueprintType)
enum class EHomeWorldPartySetup : uint8
{
	Solo,
	Partner,
	Child,
	AllThree
};

/** Why an outing ended. Each one clears both flags. Docs/41 section 5. */
UENUM(BlueprintType)
enum class EHomeWorldPartyAbsence : uint8
{
	Stroke,
	Camp,
	Cave,
	Night,
	Rescue,
	Dusk,
	Bed,
	Bonk
};

/** Result of the home interact. A refusal leaves the flags as they were. */
UENUM(BlueprintType)
enum class EHomeWorldPartyToggle : uint8
{
	Refused,
	Invited,
	SentHome
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

	/** Item 5: write roles and the party record into this system's save slice. */
	void WriteSaveSlice(TArray<uint8>& OutBytes) const;

	/** Item 5: restore from this system's save slice. False (and no change) if the bytes do not read. */
	bool ReadSaveSlice(const TArray<uint8>& InBytes);

	/**
	 * Party record from Docs/41_COMPANION_PARTY_DESIGN.md. Roles stay roles.
	 * The four setups are derived from the two flags. Missing flags are solo.
	 */
	UFUNCTION(BlueprintPure, Category = "Family|Party")
	bool IsPartnerOut() const { return bPartnerOut; }

	UFUNCTION(BlueprintPure, Category = "Family|Party")
	bool IsChildOut() const { return bChildOut; }

	UFUNCTION(BlueprintPure, Category = "Family|Party")
	EHomeWorldPartySetup GetPartySetup() const;

	UFUNCTION(BlueprintPure, Category = "Family|Party")
	bool IsRescueComplete() const { return bRescueComplete; }

	/** Until the rescue is done, both flags stay false. */
	UFUNCTION(BlueprintCallable, Category = "Family|Party")
	void SetRescueComplete(bool bComplete);

	/**
	 * Invite one person. A refusal leaves both flags as they were.
	 * Night, dusk-into-defend, and spirit form refuse. Camp refuses the partner. Cave refuses the child.
	 */
	UFUNCTION(BlueprintCallable, Category = "Family|Party")
	bool TryInvitePartner(bool bNightOrDefend, bool bSpiritForm, bool bAtCamp, UWorld* World = nullptr);

	UFUNCTION(BlueprintCallable, Category = "Family|Party")
	bool TryInviteChild(bool bNightOrDefend, bool bSpiritForm, bool bAtCave, UWorld* World = nullptr);

	/**
	 * Home interact. At home, by day, in the body, after the rescue: invite, or send that person home
	 * if they are already out. Anywhere else, at night, in spirit, or before the rescue: refuse.
	 */
	EHomeWorldPartyToggle ToggleMemberAtHome(AActor* Target, bool bAtHome, bool bNightOrDefend, bool bSpiritForm, UWorld* World);

	/** Where that person was standing when they were invited. Not saved. */
	void RememberPartnerHome(const FVector& Location);
	void RememberChildHome(const FVector& Location);

	/**
	 * Load rules, in order: an unfinished rescue forces solo; night or spirit form forces solo
	 * and places anyone who was out on the remembered home anchor. Otherwise the restored flags stay.
	 * A null world clears the flags and does not move anyone.
	 */
	void ApplyLoadForces(bool bRescueDone, bool bNightOrSpirit, UWorld* World);

	/** True when this actor is the partner or the child and that flag is still Out. */
	bool IsActorOut(const AActor* Actor) const;

	/**
	 * End the trip. Both flags clear. Anyone who was out is placed on the remembered home anchor.
	 * Already-solo is a no-op, so a stroke or a night tick can call it freely.
	 */
	void EndOuting(EHomeWorldPartyAbsence Reason, UWorld* World);

private:
	void PlaceMemberHome(UWorld* World, bool bPartner) const;
	void RememberTaggedHome(UWorld* World, FName Tag, FVector& OutHome, bool& bOutHasHome);

	UPROPERTY()
	TArray<EHomeWorldFamilyRole> RoleBySpawnIndex;

	bool bPartnerOut = false;
	bool bChildOut = false;
	bool bRescueComplete = false;
	bool bHasPartnerHome = false;
	bool bHasChildHome = false;
	FVector PartnerHome = FVector::ZeroVector;
	FVector ChildHome = FVector::ZeroVector;
};
