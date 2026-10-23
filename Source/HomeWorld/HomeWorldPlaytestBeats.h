// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldQuestLog.h"

/**
 * hw.Playtest.FastForward beats as one record each, next to the interaction spec
 * (HomeWorldInteractResolver.h). A beat row says which word starts it, where the
 * runner hands over, what the stop looks for, the standoff intent, whether the gaze
 * is derived from the target's bounds, and which earlier verbs must already have
 * succeeded (by the quest fact each one publishes). A new situation is one row, not
 * a new branch in DebugFastForwardOpening.
 */
namespace HomeWorldPlaytestBeats
{
	/** Stop ids. The values are the ones hw.Playtest.FastForward has always used. */
	enum class EBeat : int32
	{
		None = 0,
		Spirit = 1,
		Herbs,
		Backpack,
		Kettle,
		Station,
		Dog,
		Fish,
		Sleep,
		Night,
		Collect,
		Heal,
		Glider,
		Delivery,
		DayCamp,
		DawnGlide,
		NightGlide,
		Stealth,
		Ease,
		Shrine,
		Stress,
	};

	/** How the stop finds its target. */
	enum class ETarget : uint8
	{
		None,
		Reveal,		// the opening reveal actor (the spirit)
		Dog,		// the opening dog actor
		Tagged,		// Tag, then AltTag
		Named,		// actor name, exact
		CopseWisp,	// the pawn's copse night wisp
	};

	/** How the stop places the body. */
	enum class EStand : uint8
	{
		None,		// no placement (the target is only measured)
		Bounds,		// StandoffCm from the target, gaze from the target's bounds
		PondEdge,	// the pond rim walk (HomeWorldPlacement::PondStandoffCm)
	};

	struct FRow
	{
		EBeat Beat = EBeat::None;
		const TCHAR* Word = nullptr;
		/** Runner step the player takes himself (the runner stops before it). 0 = no skip. */
		int32 SkipStep = 0;
		/** For SkipStep 0: the runner step after which the stop is ready. 0 = no runner. */
		int32 ReadyAfterStep = 0;
		float StandoffCm = 260.f;
		ETarget Target = ETarget::None;
		const TCHAR* Tag = nullptr;
		const TCHAR* AltTag = nullptr;
		const TCHAR* Name = nullptr;
		EStand Stand = EStand::Bounds;
		bool bGazeFromBounds = true;
		/** Spawn the night props before looking for the target. */
		bool bNightProps = false;
		/** Put the night wisps in the backpack before looking for the target. */
		bool bCarryWisps = false;
		const TCHAR* Note = TEXT("");
		/** Facts the earlier verbs published when they succeeded, in runner order. */
		TArray<EHomeWorldOpeningFact> Requires;
	};

	/** Every beat, in stop-id order (row i is beat i + 1). */
	const TArray<FRow>& Rows();
	const FRow* RowFor(int32 Beat);

	/** Beat words (lowercased, '_' and ' ' folded out) to a stop id. Empty = night. 0 = unknown. */
	int32 FromText(const FString& Text);

	/** The beat's word. Unknown ids read "night", as they always have. */
	const TCHAR* WordFor(int32 Beat);
	/** Standoff intent. Unknown ids read 260 cm, as they always have. */
	float StandoffCm(int32 Beat);
	int32 SkipStep(int32 Beat);
	int32 ReadyAfterStep(int32 Beat);

	/** "spirit, herbs, ..." in stop-id order, for the list and unknown-beat logs. */
	FString ListText();
}
