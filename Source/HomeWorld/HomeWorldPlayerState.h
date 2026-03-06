// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "HomeWorldPlayerState.generated.h"

class UWorld;

/** Defend (waves at home) combat style: ranged from defenses or ground AOE. See docs/tasks/DEFEND_COMBAT.md. */
UENUM(BlueprintType)
enum class EDefendCombatMode : uint8
{
	Ranged     UMETA(DisplayName = "Ranged (from defenses)"),
	GroundAOE  UMETA(DisplayName = "Ground AOE")
};

/** Planetoid (away from home) combat style: combos or single-target. See docs/tasks/PLANETOID_COMBAT.md. */
UENUM(BlueprintType)
enum class EPlanetoidCombatStyle : uint8
{
	Combo        UMETA(DisplayName = "Combo"),
	SingleTarget UMETA(DisplayName = "Single-target")
};

/**
 * Replication anchor for co-op (2-8p). Use for player name, role, score, etc.
 * Keep minimal until Week 2+; add replicated properties as needed.
 * Spiritual power: collected at night (Phase 2) per VISION; see AHomeWorldSpiritualCollectible.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldPlayerState : public APlayerState
{
	GENERATED_BODY()

public:
	AHomeWorldPlayerState();

	/** Spiritual power/artefacts collected at night (Phase 2). Stub for T2 night collectible. */
	UFUNCTION(BlueprintCallable, Category = "Spiritual", meta = (DisplayName = "Get Spiritual Power"))
	int32 GetSpiritualPowerCollected() const { return SpiritualPowerCollected; }

	/** Add spiritual power (e.g. from overlapping a night collectible). */
	UFUNCTION(BlueprintCallable, Category = "Spiritual", meta = (DisplayName = "Add Spiritual Power"))
	void AddSpiritualPower(int32 Amount);

	/** Set spiritual power (e.g. on load from SaveGame). Use for restore only. */
	void SetSpiritualPowerCollected(int32 Value);

	/** Spend spiritual power (e.g. ability cost or upgrade). Returns true if sufficient and deducted. */
	UFUNCTION(BlueprintCallable, Category = "Spiritual", meta = (DisplayName = "Spend Spiritual Power"))
	bool SpendSpiritualPower(int32 Amount);

	/** Spiritual artefacts collected at night (Phase 2). Second type for T2 night collectible. */
	UFUNCTION(BlueprintCallable, Category = "Spiritual", meta = (DisplayName = "Get Spiritual Artefacts"))
	int32 GetSpiritualArtefactsCollected() const { return SpiritualArtefactsCollected; }

	/** Add spiritual artefact (e.g. from overlapping a night artefact collectible). */
	UFUNCTION(BlueprintCallable, Category = "Spiritual", meta = (DisplayName = "Add Spiritual Artefact"))
	void AddSpiritualArtefact(int32 Amount);

	/** Day restoration: true when player has performed a qualifying day activity (e.g. consume meal) this day; cleared at dawn. Used for buff display at night and future astral buffs. See DAY_RESTORATION_LOOP.md. */
	UFUNCTION(BlueprintCallable, Category = "Day Restoration", meta = (DisplayName = "Get Has Day Restoration Buff"))
	bool GetHasDayRestorationBuff() const { return bHasDayRestorationBuff; }

	/** Set day restoration buff (e.g. after consuming a meal). Cleared at dawn by GameMode. */
	UFUNCTION(BlueprintCallable, Category = "Day Restoration", meta = (DisplayName = "Set Day Restoration Buff"))
	void SetDayRestorationBuff(bool bActive);

	/** Clear day restoration buff (e.g. when advancing to dawn). */
	void ClearDayRestorationBuff() { SetDayRestorationBuff(false); }

	/** Meals/restoration count this day; shown on HUD as "Restored today: N". Reset at dawn. See DAY_RESTORATION_LOOP.md, T4. */
	UFUNCTION(BlueprintCallable, Category = "Day Restoration", meta = (DisplayName = "Get Meals Consumed Today"))
	int32 GetMealsConsumedToday() const { return MealsConsumedToday; }

	/** Increment when player uses hw.RestoreMeal / ConsumeMealRestore. */
	void IncrementMealsConsumedToday();

	/** Reset at dawn (call alongside ClearDayRestorationBuff). */
	void ResetMealsConsumedToday() { MealsConsumedToday = 0; }

	/** Meals shared with family this day (caretaker stub). Incremented when RestoreMeal used and Family-tagged actors exist. Reset at dawn. See DAY_RESTORATION_LOOP.md, T2. */
	UFUNCTION(BlueprintCallable, Category = "Day Restoration", meta = (DisplayName = "Get Meals With Family Today"))
	int32 GetMealsWithFamilyToday() const { return MealsWithFamilyToday; }

	void IncrementMealsWithFamilyToday();

	/** Reset at dawn (call alongside ResetMealsConsumedToday). */
	void ResetMealsWithFamilyToday() { MealsWithFamilyToday = 0; }

	/** Love/bond metric: 0–N, earned during the day (meals, care, building, child); scales night bonuses. Cleared at dawn. See DAY_LOVE_OR_BOND.md. */
	UFUNCTION(BlueprintCallable, Category = "Love/Bond", meta = (DisplayName = "Get Love Level"))
	int32 GetLoveLevel() const { return LoveLevel; }

	/** Set love level (e.g. from persistence or debug). */
	UFUNCTION(BlueprintCallable, Category = "Love/Bond", meta = (DisplayName = "Set Love Level"))
	void SetLoveLevel(int32 Level);

	/** Add points toward love level (e.g. meal, care, building). Clamps to non-negative. */
	UFUNCTION(BlueprintCallable, Category = "Love/Bond", meta = (DisplayName = "Add Love Points"))
	void AddLovePoints(int32 Points);

	/** Clear at dawn (call alongside ClearDayRestorationBuff). */
	void ClearLoveLevel() { SetLoveLevel(0); }

	/** Set a short-lived HUD message when SpiritBurst is blocked (e.g. insufficient spiritual power). WorldTime = GetWorld()->GetTimeSeconds() when blocked. HUD shows it for a few seconds. */
	void SetSpiritBurstBlockMessage(const FString& Message, float WorldTime);

	/** Message to show when SpiritBurst was recently blocked; empty if none or expired. */
	UFUNCTION(BlueprintCallable, Category = "SpiritBurst")
	FString GetSpiritBurstBlockMessageForHUD(UWorld* World, float DisplayDurationSeconds = 4.0f) const;

	/** Defend (waves at home) combat style: Ranged from defenses or Ground AOE. Placeholder for future ability classification. See DEFEND_COMBAT.md. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Defend")
	EDefendCombatMode GetDefendCombatMode() const { return DefendCombatMode; }

	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Defend")
	void SetDefendCombatMode(EDefendCombatMode Mode);

	/** Planetoid (away from home) combat style: Combo or Single-target. Placeholder for future ability classification. See PLANETOID_COMBAT.md. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	EPlanetoidCombatStyle GetPlanetoidCombatStyle() const { return PlanetoidCombatStyle; }

	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	void SetPlanetoidCombatStyle(EPlanetoidCombatStyle Style);

	/** Current combo hit count (0 when not in combo or after reset). Used for combo scaling; stub only. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	int32 GetComboHitCount() const { return ComboHitCount; }

	/** Increment combo count (e.g. from a hit event). Stub; no scaling logic. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	void AddComboHit();

	/** Clear combo count (e.g. on timeout or miss). */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Planetoid")
	void ResetComboHitCount();

private:
	UPROPERTY()
	int32 SpiritualPowerCollected = 0;

	UPROPERTY()
	int32 SpiritualArtefactsCollected = 0;

	/** True when player has earned day restoration this day (e.g. consumed meal); cleared at dawn. */
	UPROPERTY()
	bool bHasDayRestorationBuff = false;

	/** Number of meals/restorations consumed this day; shown on HUD during day. Reset at dawn. */
	UPROPERTY()
	int32 MealsConsumedToday = 0;

	/** Meals shared with family this day (caretaker stub). Reset at dawn. */
	UPROPERTY()
	int32 MealsWithFamilyToday = 0;

	/** Love/bond level (0–N) earned this day; scales night bonuses. Cleared at dawn. See DAY_LOVE_OR_BOND.md. */
	UPROPERTY()
	int32 LoveLevel = 0;

	/** Last SpiritBurst block reason (e.g. "Not enough spiritual power"); cleared after display duration. */
	UPROPERTY()
	FString LastSpiritBurstBlockMessage;

	/** World time when LastSpiritBurstBlockMessage was set (for HUD display duration). */
	UPROPERTY()
	float LastSpiritBurstBlockWorldTime = 0.f;

	/** Current defend combat style (ranged from defenses vs ground AOE). Placeholder for T1 defend combat stub. */
	UPROPERTY(EditAnywhere, Category = "HomeWorld|Defend")
	EDefendCombatMode DefendCombatMode = EDefendCombatMode::Ranged;

	/** Planetoid combat style (combo vs single-target). Placeholder for T2 planetoid combat stub. */
	UPROPERTY(EditAnywhere, Category = "HomeWorld|Planetoid")
	EPlanetoidCombatStyle PlanetoidCombatStyle = EPlanetoidCombatStyle::SingleTarget;

	/** Combo hit count for combo-style planetoid combat; reset on timeout or miss. Stub only. */
	UPROPERTY()
	int32 ComboHitCount = 0;
};
