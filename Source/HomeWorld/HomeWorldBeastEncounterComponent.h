// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldBeastEncounterComponent.generated.h"

class AHomeWorldCharacter;

/**
 * Lead 2026-10-07 bull rules (Docs/context/HOMEWORLD_ROUTE.md, docs/01_GDD_MVP V4):
 * - A threat meter boots you back to the homestead on a charge if you get too
 *   close or fill it without leaving the beast's area ("charge-and-boot" --
 *   Lead pick 2026-10-07 over flee-to-edge and the Animal Crossing warmth form).
 * - Walking toward it carrying an herb suppresses the boot; sudden movement
 *   builds threat; standing still lets it approach, eat, and be tamed.
 * - Tamed, the bull is rideable; turn authority is inversely related to travel
 *   speed (near-zero at 3x sprint, full at walk/stop) -- real-animal handling.
 *
 * All frame inputs arrive explicitly in FHomeWorldBeastEncounterFrame so the
 * rules are testable without a GameInstance fixture (the known created-world
 * inventory gap -- Docs/TaskLists/T0_EXECUTION_QUEUE.md item 4).
 */

UENUM(BlueprintType)
enum class EHomeWorldBeastEncounterOutcome : uint8
{
	/** Nothing happened this frame (out of range and calm, or beast tamed). */
	Idle,
	/** Sudden movement inside the area is filling the meter. */
	ThreatRising,
	/** Standing still (or leaving the area) is bleeding the meter off. */
	ThreatDecaying,
	/** Standing still with an offering: the beast approaches, eats, is tamed. */
	TameWindow,
	/** Meter is full but an offering is held, so the charge-and-boot cannot fire. */
	OfferSuppressedBoot,
	/** Meter full or too close with no offering: charge -> boot home. Caller runs the eject. */
	BootCharged
};

/** One sampled encounter frame. Plain data so tests drive it directly. */
USTRUCT(BlueprintType)
struct FHomeWorldBeastEncounterFrame
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Beast")
	float DeltaSeconds = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Beast")
	float PlayerSpeedCm = 0.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Beast")
	float DistanceCm = 0.f;

	/**
	 * True while the player carries an offering. Agent extension, Lead-flagged:
	 * the route says "an herb", but the V4 food offer accepts RES_BERRY too, so
	 * both count here -- otherwise a berry offering could be charged mid-offer.
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Beast")
	bool bCarriesOfferFood = false;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Beast")
	bool bBeastTamed = false;
};

UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldBeastEncounterComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldBeastEncounterComponent();

	/**
	 * Advance the threat meter for one frame and return what happened.
	 * Pure function of Frame + the tunables below; touches no world state.
	 * On BootCharged the meter resets to 0, so the next charge needs a full
	 * refill (spacing instead of a session latch -- the charge is repeatable).
	 */
	UFUNCTION(BlueprintCallable, Category = "Beast")
	EHomeWorldBeastEncounterOutcome AdvanceThreat(const FHomeWorldBeastEncounterFrame& Frame);

	UFUNCTION(BlueprintCallable, Category = "Beast")
	float GetThreat() const { return Threat; }

	/**
	 * Real-animal handling (Lead 2026-10-07): turn authority is inversely
	 * related to travel speed -- 1.0 at a standstill, 0.0 at the bull's max
	 * speed (3x player sprint, per route). The rider steers by managing
	 * momentum, not by steering at speed. Returns clamped [0,1]; a MaxSpeedCm
	 * of 0 or less means "no travel possible", i.e. full authority.
	 */
	static float TurnAuthorityForSpeed(float SpeedCm, float MaxSpeedCm);

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
	/** Player within AggroRadiusCm -> sample frame, advance, deliver BootCharged via the existing eject service. */
	void SampleAndAdvance(AHomeWorldCharacter* Player, float DeltaTime);

	/** Threat area of the beast, in cm. Route: boot happens "without leaving its area". */
	UPROPERTY(EditDefaultsOnly, Category = "Beast", meta = (ClampMin = "100.0"))
	float AggroRadiusCm = 900.f;

	/** "Get too close" radius -- instant charge when no offering is held. Agent-proposed, Lead-flagged. */
	UPROPERTY(EditDefaultsOnly, Category = "Beast", meta = (ClampMin = "50.0"))
	float TooCloseRadiusCm = 350.f;

	/** Meter fill while moving inside the area (0.25 -> 4 s of running to a boot). Agent-proposed, Lead-flagged. */
	UPROPERTY(EditDefaultsOnly, Category = "Beast", meta = (ClampMin = "0.01"))
	float ThreatFillPerSecond = 0.25f;

	/** Meter decay while still or outside the area (0.5 -> 2 s to calm). Agent-proposed, Lead-flagged. */
	UPROPERTY(EditDefaultsOnly, Category = "Beast", meta = (ClampMin = "0.01"))
	float ThreatDecayPerSecond = 0.5f;

	/** At or below this speed the player counts as standing still. Agent-proposed, Lead-flagged. */
	UPROPERTY(EditDefaultsOnly, Category = "Beast", meta = (ClampMin = "0.0"))
	float StillSpeedCm = 150.f;

	UPROPERTY(VisibleAnywhere, Category = "Beast")
	float Threat = 0.f;

	/** Last outcome delivered to the caller, for transition-only logging. */
	EHomeWorldBeastEncounterOutcome LastOutcome = EHomeWorldBeastEncounterOutcome::Idle;
};
