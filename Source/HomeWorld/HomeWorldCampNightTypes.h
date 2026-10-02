// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldCampNightTypes.generated.h"

/**
 * T0 #14 / #15 / #16 - the camp-night laws, as pure data and pure functions.
 *
 * WHY A SEPARATE TYPES HEADER
 *
 * VISION_BOARD V2b ("gather by day, tend by night") turned three questions that had no owner into
 * load-bearing rules: what a spirit may touch, whether "calmed" is the same as "asleep", and what
 * opens the door to the captive. Everything here is deliberately world-free - no UWorld, no
 * SpawnActor, no overlap - so the laws can be asserted directly in automation tests rather than
 * inferred from a level that does not exist yet.
 *
 * THE CAMP HAS THREE ACTORS AND THEY ARE NOT THE SAME JOB (Lead, 2026-10-02)
 *
 *     "A guard will be awake that you need to help ease their thoughts so that they fall asleep,
 *      the other two will be asleep and you can ease their thoughts too to keep them sleeping."
 *
 * The guard moves AWAKE -> ASLEEP. The two sleepers are eased to STAY asleep. So every actor
 * needs easing, and every actor needs to be asleep, but only one of them changes state because
 * of it. That is why SatisfiesFreedomGate() requires BOTH flags rather than a single state enum:
 *
 *   - asleep but never eased -> the care was skipped -> the door stays shut
 *   - eased but still awake -> the act is unfinished -> the door stays shut
 *
 * THE FAIL-OPEN PROBLEM, AND WHY IT IS CONTAINED RATHER THAN REMOVED
 *
 * UHomeWorldSpiritStealthComponent historically soft-latched #14 when the camp actor was absent
 * from the level, so a reviewer was never hard-blocked by missing content. That is defensible as
 * gameplay and indefensible as evidence: a check that cannot fail is not proving anything, and
 * #14 was able to report itself complete with zero actors in the world.
 *
 * Both behaviours are kept and they are kept DISTINGUISHABLE. bSoftLatch marks a count that was
 * granted without a real actor. SatisfiesFreedomGateStrict() ignores soft latches entirely and so
 * is what automation tests and the prove scripts read; SatisfiesFreedomGate() is the gameplay
 * path. The soft path logs SOFT_LATCH_ONLY so the difference is visible in the log rather than
 * hidden in a return value.
 */

/** The three camp actors that must be calm, plus the captive they are guarding. */
UENUM(BlueprintType)
enum class EHomeWorldCampRole : uint8
{
	/** AWAKE with a lit blue torch. Eased awake->asleep. Counts in the gate. */
	Guard,
	/** Starts ASLEEP. Eased to stay asleep. Counts in the gate. Two of these exist. */
	Sleeper,
	/** Your companion, held. Gated on all three above. Does NOT count in its own gate. */
	Captive,
};

/** What a spirit form is reaching for. Kept separate from role on purpose - see GetSpiritTouchVerdict. */
UENUM(BlueprintType)
enum class EHomeWorldSpiritTouchTarget : uint8
{
	/** Garden soil and plant slots. Night tending, must #12. */
	Soil,
	/** Rope and lashings. Unbinding is the rescue, must #16. */
	Lashings,
	/** An actor's body - the guard's, a sleeper's, the captive's. */
	ActorBody,
	/** An actor's attention. This is how all three get eased. */
	ActorMind,
};

UENUM(BlueprintType)
enum class EHomeWorldSpiritTouchVerdict : uint8
{
	Allowed,
	Refused,
};

/** One camp actor's trackable state. Plain data; the laws live in the methods. */
USTRUCT(BlueprintType)
struct HOMEWORLD_API FHomeWorldCampActorCalm
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	EHomeWorldCampRole Role = EHomeWorldCampRole::Sleeper;

	/** Their thoughts were eased. Required for EVERY actor, including the ones already asleep. */
	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	bool bEased = false;

	/** They are asleep right now. Can be lost - a sleeper that wakes is no longer asleep. */
	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	bool bAsleep = false;

	/** Killed. Anti-case: a dead actor is not a calmed one and must never open the gate. */
	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	bool bKilled = false;

	/** Defeated and converted into a vendor/helper/pet. Anti-case: conversion is not care. */
	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	bool bConverted = false;

	/** Counted without a real actor in the world. Excluded from the strict gate. */
	UPROPERTY(BlueprintReadOnly, Category = "CampNight")
	bool bSoftLatch = false;

	/**
	 * The gameplay half of the gate: eased, asleep, alive, and not merely converted.
	 *
	 * bKilled and bConverted are both load-bearing negatives. EConvertedFoeRole already has five
	 * roles and conversion is what happens to foes you DEFEAT, so treating a converted actor as a
	 * calmed one lets the player defeat all three and unlock the captive - which inverts the beat,
	 * because the whole design is that the gentle path is the only path.
	 */
	bool SatisfiesFreedomGate() const
	{
		return bEased && bAsleep && !bKilled && !bConverted;
	}

	/** The evidence half: as above, and additionally not granted by a soft latch. */
	bool SatisfiesFreedomGateStrict() const
	{
		return SatisfiesFreedomGate() && !bSoftLatch;
	}
};

namespace HomeWorldCampNight
{
	/** The number of actors the captive's freedom depends on: one guard + two sleepers. */
	HOMEWORLD_API int32 GetGatedActorCount();

	/** The guard starts awake; the sleepers start asleep. The captive is neither. */
	HOMEWORLD_API bool StartsAsleep(EHomeWorldCampRole Role);

	/** Every one of the three must be eased, including the two already asleep. */
	HOMEWORLD_API bool RequiresEasing(EHomeWorldCampRole Role);

	/** Guard and Sleeper count in the gate. The Captive is what the gate opens, not part of it. */
	HOMEWORLD_API bool CountsInFreedomGate(EHomeWorldCampRole Role);

	HOMEWORLD_API const TCHAR* GetRoleLogName(EHomeWorldCampRole Role);

	/**
	 * MUST #15 - what a spirit form may touch.
	 *
	 * The law in one line: a spirit has no hands. It may work on what holds and carries (soil,
	 * rope) and it may apply care to a mind, but it may not touch an actor's body.
	 *
	 * ActorMind being Allowed is the exception that lets #14 and #16 exist at all - easing a
	 * guard awake->asleep is the rescue's whole content, and a blanket refusal would delete it. A
	 * blanket ALLOWANCE would be worse: a spirit that can grab a guard can drag a guard, and the
	 * beat becomes about moving bodies instead of easing minds.
	 */
	HOMEWORLD_API EHomeWorldSpiritTouchVerdict GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget Target);

	/** Why a touch was allowed or refused. Logged on every call - a silent refusal reads as a broken game. */
	HOMEWORLD_API const TCHAR* GetSpiritTouchReason(EHomeWorldSpiritTouchTarget Target);

	/** A stable tag for logs and automation assertions, e.g. "SOIL". */
	HOMEWORLD_API const TCHAR* GetSpiritTouchTargetLogName(EHomeWorldSpiritTouchTarget Target);
}