// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldCampNightTypes.h"
#include "HomeWorldSpiritStealthTypes.h"
#include "HomeWorldSpiritStealthComponent.generated.h"

class AHomeWorldSpiritLitVolume;

class UPointLightComponent;
class USkeletalMeshComponent;

/**
 * SS-A/SS-B: spirit-form lit / alert (A2 pressure) + readable hidden/revealed feel. Logs STEALTH:* — no kill, no kidnap, no homestead combat.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldSpiritStealthComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldSpiritStealthComponent();

	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-A")
	bool IsSpiritLit() const { return LitOverlapCount > 0 || bForceLitCheat; }

	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-A")
	float GetAlertLevel() const { return AlertLevel; }

	/** SS-B: true when spirit is unlit (hidden fantasy cue active). */
	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-B")
	bool IsSpiritHiddenCueActive() const;

	/** SS-B: true when lit or alert is rising (revealed fantasy cue). */
	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-B")
	bool IsSpiritRevealedCueActive() const;

	void NotifyLitVolumeEntered(EHomeWorldSpiritLitSourceKind SourceKind, AHomeWorldSpiritLitVolume* Volume);
	void NotifyLitVolumeExited(AHomeWorldSpiritLitVolume* Volume);

	/** Optional haste hook — once per lit session while alert is rising. */
	void NotifyInteractWhileLit();

	/** hw.Stealth.ForceLit — debug only. */
	void SetForceLitCheat(bool bForce);

	void LogStatus() const;


	/**
	 * ⚠️ LEGACY — NOT THE #14 GATE. Use TryEaseCampActor(EHomeWorldCampRole::Guard, 0).
	 *
	 * This is the old "avoid the guard and move on" reading. The Lead corrected #14 on
	 * 2026-10-02: the guard is not avoided and left running, they are eased awake->asleep
	 * and they are one of the three the gate waits for. Nothing in the codebase calls this
	 * any more; it is kept callable only so existing Blueprint graphs keep resolving.
	 */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool TryAvoidNodeGuard();

	/**
	 * ⚠️ LEGACY — NOT THE #14 GATE. Use TryEaseCampActor(EHomeWorldCampRole::Sleeper, N).
	 *
	 * Still the right *idea* — soothe is not convert — but it bumps a counter that no gate
	 * reads any more. Kept callable only so existing Blueprint graphs keep resolving.
	 */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool TrySootheNodeSleeper();

	/** ⚠️ LEGACY counter. Reads nothing; kept for existing Blueprint graphs. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	int32 GetGuardsAvoidedThisSession() const { return GuardsAvoidedCount; }

	/** ⚠️ LEGACY counter. Reads nothing; kept for existing Blueprint graphs. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	int32 GetSleepersSoothedThisSession() const { return SleepersSoothedCount; }

	/**
	 * MUST #14 beat complete.
	 *
	 * REDIRECTED 2026-10-02. This used to be `GuardsAvoidedCount >= 1 && SleepersSoothedCount >= 2`,
	 * which is the old "avoid 1 guard; soothe 2 sleepers" reading. The Lead corrected it: all three
	 * camp actors are CALMED, the guard included. It now defers to the three-actor gate.
	 */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool IsCampNightBeatComplete() const;

	// ---------------------------------------------------------------------------------
	// T0 #14 / #15 / #16 - the three-actor camp night.
	//
	// Added 2026-10-02. The counters above are the original "avoid 1 guard; soothe 2
	// sleepers" reading and they are NOT the law any more. The Lead's correction is:
	//
	//   "A guard will be awake that you need to help ease their thoughts so that they
	//    fall asleep, the other two will be asleep and you can ease their thoughts too
	//    to keep them sleeping."
	//
	// All three are CALMED. The guard moves awake->asleep; the two sleepers are eased to
	// stay asleep. So the gate is no longer a count of two different verbs - it is three
	// actors each of whom must be BOTH eased AND asleep.
	//
	// IsCampNightBeatComplete() above is retained for compatibility but is redirected to
	// IsFreedomUnlocked(). Do not add new callers of the counter fields; they are the old
	// shape and they cannot express the three-actor law.
	// ---------------------------------------------------------------------------------

	/**
	 * Ease one camp actor's thoughts. The care verb, and the only way to set bEased.
	 *
	 * Soft-latches when no actor is present in the world, exactly as the old counters do,
	 * so a reviewer is never hard-blocked by missing content - but it sets bSoftLatch,
	 * which IsFreedomUnlockedStrict() rejects.
	 */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool TryEaseCampActor(EHomeWorldCampRole Role, int32 Ordinal = 0);

	/** A sleeper that wakes stops counting. "Keep them sleeping" has to be able to fail. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	void NotifyCampActorWoke(EHomeWorldCampRole Role, int32 Ordinal = 0);

	/** Anti-case. A dead actor is not a calmed one and never opens the gate. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	void NotifyCampActorKilled(EHomeWorldCampRole Role, int32 Ordinal = 0);

	/**
	 * Anti-case. Conversion is what happens to foes you DEFEAT; it is not care.
	 * EConvertedFoeRole already has five roles, so conflating the two would let the
	 * player defeat all three and unlock the captive, inverting the beat.
	 */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	void NotifyCampActorConverted(EHomeWorldCampRole Role, int32 Ordinal = 0);

	/** The gameplay gate: all three eased and asleep, soft latches tolerated. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool IsFreedomUnlocked() const;

	/** The evidence gate: as above, and no soft latch. Tests and prove scripts read THIS. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool IsFreedomUnlockedStrict() const;

	/** MUST #16. Frees the companion only when IsFreedomUnlocked() passes. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool TryFreeCaptive();

	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool IsCaptiveFreed() const { return bCaptiveFreed; }

	/** MUST #15. Logs every verdict - a refusal the player cannot see reads as a broken game. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|Touch")
	EHomeWorldSpiritTouchVerdict EvaluateSpiritTouch(EHomeWorldSpiritTouchTarget Target) const;

	/** How many of the three are eased AND asleep, ignoring soft latches. 0..3. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	int32 GetCalmedActorCount() const;

	/** Read-only view of one actor's state. Ordinal 0 is the only guard; sleepers take 0 and 1. */
	UFUNCTION(BlueprintCallable, Category = "Stealth|T0|CampNight")
	bool GetCampActorState(EHomeWorldCampRole Role, int32 Ordinal, bool& bOutEased, bool& bOutAsleep) const;

	const FHomeWorldCampActorCalm* FindCampActor(EHomeWorldCampRole Role, int32 Ordinal) const;
	FHomeWorldCampActorCalm* FindCampActor(EHomeWorldCampRole Role, int32 Ordinal);

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void UpdateAlert(float DeltaTime);
	void TryLogClear();
	void UpdateFeelVisuals();
	void EnsureFeelLight();
	void ApplyMeshFeelTint(bool bRevealed, float Alert01);

	UPROPERTY(Transient)
	TObjectPtr<UPointLightComponent> FeelLight;

	UPROPERTY(Transient)
	bool bFeelLightSpawned = false;

	UPROPERTY(Transient)
	bool bLastRevealedCue = false;

	UPROPERTY(Transient)
	int32 LitOverlapCount = 0;

	UPROPERTY(Transient)
	float AlertLevel = 0.f;

	UPROPERTY(Transient)
	bool bLoggedAlertThisLitSession = false;

	UPROPERTY(Transient)
	bool bLoggedQuickWindowThisLitSession = false;

	UPROPERTY(Transient)
	bool bWasLitLastFrame = false;

	UPROPERTY(Transient)
	bool bForceLitCheat = false;

	UPROPERTY(Transient)
	EHomeWorldSpiritLitSourceKind LastEnterSourceKind = EHomeWorldSpiritLitSourceKind::Campfire;


	/** T0 #14: guards avoided this session (need 1). */
	UPROPERTY(Transient)
	int32 GuardsAvoidedCount = 0;

	/** T0 #14: sleepers soothed this session (need 2). Not convert count. */
	UPROPERTY(Transient)
	int32 SleepersSoothedCount = 0;

	/**
	 * The three camp actors, in gate order: Guard, Sleeper A, Sleeper B.
	 *
	 * Built in the constructor so the gate is never evaluated against an empty array -
	 * an empty array trivially satisfies "all of them", which is the fail-open this whole
	 * structure exists to prevent.
	 */
	UPROPERTY(Transient)
	TArray<FHomeWorldCampActorCalm> CampActors;

	/** T0 #16. Set once the freedom gate has been passed and the lashings opened. */
	UPROPERTY(Transient)
	bool bCaptiveFreed = false;

	/**
	 * Emitted once when a soft latch is the only reason the gameplay gate would pass.
	 *
	 * `mutable` because IsFreedomUnlocked() is const and still owes the log a line. The
	 * alternative - a const_cast - would be worse: it would hide a write behind a const
	 * method that claims to only read.
	 */
	UPROPERTY(Transient)
	mutable bool bLoggedSoftLatchOnly = false;

	static constexpr float AlertRisePerSecond = 0.35f;
	static constexpr float AlertDecayPerSecond = 0.55f;
	static constexpr float AlertThreshold = 0.72f;
};
