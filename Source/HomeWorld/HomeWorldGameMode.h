// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "HomeWorldPlanetoidTypes.h"
#include "HomeWorldGameMode.generated.h"

class AActor;
class APlayerController;

/** T2: Stub role assigned to a converted foe (vendor, helper, quest giver, pet, worker). Per VISION: converted foes become one of these. */
UENUM(BlueprintType)
enum class EConvertedFoeRole : uint8
{
	Vendor,
	Helper,
	QuestGiver,
	Pet,
	Worker,
	Max UMETA(Hidden)
};

/**
 * Called when the player's astral form is defeated at night: advance time to dawn and respawn at start.
 * Does not call ReportDeathAndAddSpirit (permanent death). See docs/tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AHomeWorldGameMode();

	/** Astral return on death: advance to dawn and respawn player at start (bed). Call from astral-defeat logic or hw.AstralDeath. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral")
	void OnAstralDeath(APlayerController* PlayerController);

	/** Request astral death for the local player (advance to dawn + respawn). Call from character, ability, or damage path. No-op if World or GameMode invalid. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral", meta = (WorldContext = "WorldContextObject"))
	static void RequestAstralDeath(UObject* WorldContextObject);

	/** List 61: Can the player enter astral during the day? MVP = always true (no gate). Future: tutorial complete, love level threshold, or config. See ASTRAL_DEATH_AND_DAY_SAFETY.md §3 (progression gate). */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral")
	bool CanEnterAstralByDay(APlayerController* PlayerController = nullptr) const;

	/** List 61: Enter astral during the day (stub). When phase is Day or Dusk, sets phase to Night and bAstralByDay so return restores Day. Respects CanEnterAstralByDay(). Call from hw.EnterAstral or in-world trigger. See ASTRAL_DEATH_AND_DAY_SAFETY.md, MVP_FULL_SCOPE_10_LISTS List 61. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral")
	void EnterAstralByDay();

	/** True when player entered astral via EnterAstralByDay (return from astral restores Day instead of Dawn). Cleared when returning. */
	bool bAstralByDay = false;

	/** True when current astral session was entered during day (return restores Day). For PIE and Blueprint. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral")
	bool GetAstralByDay() const { return bAstralByDay; }

	/** Act 2 prep: Log Defend phase status (phase, DefendPosition count, Family count, family-moved-this-night). Use from hw.Defend.Status in PIE. See DAY12_ROLE_PROTECTOR.md. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Defend")
	void LogDefendStatus() const;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	/** When TimeOfDay is night (Phase 2), trigger once per night: spawn placeholder and log. Reset when phase leaves night. See docs/tasks/NIGHT_ENCOUNTER.md. */
	void TryTriggerNightEncounter();

	/** Distance in front of player to spawn night encounter placeholder (units). Configurable in Blueprint/Editor. Default 500. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "50", ClampMax = "5000"))
	float NightEncounterSpawnDistance = 500.f;

	/** Height offset above spawn plane for night encounter (units). Default 50. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "-500", ClampMax = "500"))
	float NightEncounterSpawnHeightOffset = 50.f;

	/** If > 0, spawn a second encounter placeholder at this distance (e.g. second type). 0 = disabled. Configurable in Blueprint. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "0", ClampMax = "5000"))
	float NightEncounterSecondSpawnDistance = 0.f;

	/** If > 0, spawn a second "wave" of placeholder(s) after this many seconds when night starts. 0 = no wave 2. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "0", ClampMax = "120"))
	float NightEncounterWave2DelaySeconds = 0.f;

	/** T5: Number of wave-2 placeholders to spawn (difficulty stub: more enemies). Wave 2 uses Sphere mesh as "different type" stub. Default 2. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "1", ClampMax = "10"))
	int32 NightEncounterWave2SpawnCount = 2;

	/** If > 0, spawn wave 3 this many seconds after wave 2 spawns. 0 = no wave 3. Configurable in Blueprint. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "0", ClampMax = "120"))
	float NightEncounterWave3DelaySeconds = 0.f;

	/** T5: Number of wave-3 placeholders to spawn (distinct from wave 2). Wave 3 uses Cylinder mesh. Default 3. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "1", ClampMax = "10"))
	int32 NightEncounterWave3SpawnCount = 3;

	/** True after we have triggered spawn this "night"; reset when GetIsNight() becomes false. */
	bool bNightEncounterTriggered = false;

	/** Current night encounter wave (1, 2, or 3 when waves have spawned). 0 when not night or no encounter yet. Reset when leaving night. T5: for HUD/log display. */
	int32 CurrentNightEncounterWave = 0;

	/** Timer for delayed wave 2 spawn; cleared when leaving night. */
	FTimerHandle NightEncounterWave2TimerHandle;

	/** Timer for delayed wave 3 spawn; cleared when leaving night. */
	FTimerHandle NightEncounterWave3TimerHandle;

	/** T3: If > 0, spawn "planetoid pack" placeholder(s) away from home when night starts (distance from player). 0 = disabled. See docs/tasks/NIGHT_ENCOUNTER.md §1.1. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "0", ClampMax = "10000"))
	float PlanetoidPackSpawnDistance = 2000.f;

	/** T5: Number of planetoid packs to spawn away from home (1 = single pack; 2+ = multiple packs at angular spread). Configurable in Blueprint/Editor. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "1", ClampMax = "10"))
	int32 PlanetoidPackCount = 1;

	/** True after we have spawned the planetoid pack(s) this night; reset when GetIsNight() becomes false. */
	bool bPlanetoidPackSpawnedThisNight = false;

	/** T5: If > 0 and no KeyPoint-tagged actors in level, spawn one "key-point boss" placeholder at this distance from player when night starts. 0 = disabled. See docs/tasks/NIGHT_ENCOUNTER.md §1.2. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|NightEncounter", meta = (ClampMin = "0", ClampMax = "10000"))
	float KeyPointBossSpawnDistance = 0.f;

	/** True after we have spawned the key-point boss placeholder this night; reset when GetIsNight() becomes false. */
	bool bKeyPointBossSpawnedThisNight = false;

public:
	/** Current night encounter wave number (1, 2, or 3 when at night and encounter triggered). 0 otherwise. For HUD and log. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|NightEncounter")
	int32 GetCurrentNightEncounterWave() const { return CurrentNightEncounterWave; }

	/** Called when wave-2 delay timer fires; spawns NightEncounterWave2SpawnCount placeholders (Sphere mesh, difficulty stub). */
	void SpawnNightEncounterWave2();

	/** Called when wave-3 delay timer fires; spawns NightEncounterWave3SpawnCount placeholders (Cylinder mesh, wave 3 distinct behavior). */
	void SpawnNightEncounterWave3();

	/** T1 Conversion stub: call when a foe is "defeated" (placeholder removed or sin reduced to zero). Logs conversion (strip sin → loved) and increments ConvertedFoesThisNight. See docs/tasks/CONVERSION_NOT_KILL.md. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Conversion")
	void ReportFoeConverted(AActor* Foe);

	/** Number of foes converted this night (reset when phase leaves Night). For HUD/log and future extension (rewards, role assignment). */
	int32 ConvertedFoesThisNight = 0;

	/** Current count of foes converted this night (0 when not night or after reset). */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Conversion")
	int32 GetConvertedFoesThisNight() const { return ConvertedFoesThisNight; }

	/** T2: Stub role assigned to the converted foe at the given index this night (0-based). Returns role for that conversion; invalid index returns Vendor as safe default. Cleared when phase leaves Night. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Conversion")
	EConvertedFoeRole GetConvertedFoeRole(int32 Index) const;

	/** T3: Display name for converted foe role (HUD and log). */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Conversion")
	static FString GetConvertedFoeRoleDisplayName(EConvertedFoeRole InRole);

	/** T2: Roles assigned to converted foes this night (same order as conversion). Cleared when phase leaves Night. */
	UPROPERTY()
	TArray<EConvertedFoeRole> ConvertedFoeRolesThisNight;

	/** T3 Act 2 stub: true after we have logged "Defend phase active" this night; reset when GetIsNight() becomes false. */
	bool bDefendPhaseLogged = false;

	/** T3 Act 2: true after we have logged Defend positions this night; reset when GetIsNight() becomes false. */
	bool bDefendPositionsLogged = false;

	void TryLogDefendPhaseActive();

	/** T3: When DefendActive (night), discover actors with tag "DefendPosition" and log count/locations once per night. See DAY12_ROLE_PROTECTOR.md. */
	void TryLogDefendPositions();

	/** T3: When DefendActive (night), teleport actors with tag "Family" to DefendPosition-tagged actors (round-robin). Once per night. See DAY12_ROLE_PROTECTOR.md. */
	void TryMoveFamilyToDefendPositions();

	/** T3: When dawn arrives (transition from Night to non-Night), teleport Family-tagged actors to GatherPosition-tagged actors or GatherReturnOffset. Once per dawn. See DAY12_ROLE_PROTECTOR.md. */
	void TryReturnFamilyFromDefendAtDawn();

	/** True after we have moved family to DefendPosition this night; reset when GetIsNight() becomes false. */
	bool bFamilyMovedToDefendThisNight = false;

	/** T3: True after we have run return-from-Defend at dawn this cycle; reset when entering Night again. */
	bool bFamilyReturnedThisDawn = false;

	/** T3: If no GatherPosition-tagged actors exist, teleport family to this world offset (e.g. home area). Used by TryReturnFamilyFromDefendAtDawn. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|Defend", meta = (DisplayName = "Gather Return Offset"))
	FVector GatherReturnOffset = FVector(500.f, 0.f, 100.f);

	/** T3: True when Defend phase (night) was active last tick; used to detect transition to dawn and log Defend phase end. */
	bool bWasDefendPhaseActiveLastTick = false;

	/** T8: Offsets from home (player location when night starts) at which to spawn defense-position placeholders. Empty = use level-placed DefendPosition actors only. See docs/tasks/DEFEND_DEFENSES.md. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|Defend")
	TArray<FVector> DefensePositionOffsets;

	/** T8: True after we have spawned defense position placeholders from DefensePositionOffsets this night; reset when GetIsNight() becomes false. */
	bool bDefensePositionsSpawnedThisNight = false;

	/** T4: Spiritual power regen at night — seconds between each regen tick. 0 = disabled. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|Spiritual", meta = (ClampMin = "0", ClampMax = "120"))
	float SpiritualPowerRegenIntervalSeconds = 5.f;

	/** T4: Spiritual power added per regen tick at night (when interval > 0). */
	UPROPERTY(EditDefaultsOnly, BlueprintReadWrite, Category = "HomeWorld|Spiritual", meta = (ClampMin = "0", ClampMax = "10"))
	int32 SpiritualPowerRegenAmount = 1;

	/** Accumulator for next regen tick; reset when leaving night. */
	float NightSpiritualPowerRegenAccumulator = 0.f;

	/** T4: When at night and interval > 0, add SpiritualPowerRegenAmount to each player every SpiritualPowerRegenIntervalSeconds. Observable on HUD and in log. */
	void TrySpiritualPowerRegenAtNight(float DeltaTime);

	/** T3 Homestead-on-planetoid stub: true when the current level is considered a planetoid (homestead has "landed"). Set once in BeginPlay from level name. See docs/tasks/PLANETOID_HOMESTEAD.md. */
	bool bHomesteadLandedOnPlanetoid = false;

	/** Set by hw.Planetoid.Complete; true when current planetoid is marked complete (for "complete → travel to next" flow). See docs/tasks/PLANETOID_HOMESTEAD.md §5. */
	bool bPlanetoidComplete = false;

public:
	/** T3: True when homestead has landed on the current planetoid (set in BeginPlay from level name). For downstream systems (venture-out, completion). */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	bool GetHomesteadLandedOnPlanetoid() const { return bHomesteadLandedOnPlanetoid; }

	/** True when current planetoid has been marked complete (e.g. via hw.Planetoid.Complete). For PIE testing and downstream transition-to-next flow. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	bool GetPlanetoidComplete() const { return bPlanetoidComplete; }

	/** Set planetoid complete flag (e.g. from console command). Logs and sets bPlanetoidComplete so pie_test_runner or transition logic can verify. */
	void SetPlanetoidComplete(bool bComplete) { bPlanetoidComplete = bComplete; }

	/** T4 (list 37): Current zone alignment (fight / harvest / empower). Read at runtime for branching; set via hw.Planetoid.ZoneAlignment or config. Per PLANETOID_BIOMES.md §3. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HomeWorld|Planetoid")
	EPlanetoidAlignment CurrentZoneAlignment = EPlanetoidAlignment::Neutral;

	/** T4 (list 37): Current zone biome for this planetoid. Read at runtime with CurrentZoneAlignment for fight/harvest/empower behaviour. Per PLANETOID_BIOMES.md §1–2. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "HomeWorld|Planetoid")
	EBiomeType CurrentZoneBiome = EBiomeType::Forest;

	/** T4: Current zone alignment (Corrupted = fight, Neutral = harvest, Positive = empower). Use in PIE or Blueprint to branch behaviour. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	EPlanetoidAlignment GetCurrentZoneAlignment() const { return CurrentZoneAlignment; }

	/** T4: Current zone biome (Desert, Forest, Marsh, Canyon). Use with GetCurrentZoneAlignment for per-biome alignment behaviour. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	EBiomeType GetCurrentZoneBiome() const { return CurrentZoneBiome; }

	/** T4: Set current zone alignment (e.g. from console hw.Planetoid.ZoneAlignment). Logs and updates CurrentZoneAlignment. */
	void SetCurrentZoneAlignment(EPlanetoidAlignment InAlignment) { CurrentZoneAlignment = InAlignment; }

	/** T4: Set current zone biome (e.g. from console or level config). */
	void SetCurrentZoneBiome(EBiomeType InBiome) { CurrentZoneBiome = InBiome; }
};
