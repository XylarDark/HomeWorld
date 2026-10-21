// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class AActor;

/** One hover rule for a shoulder wisp on an interactable. */
namespace HomeWorldWisp
{
	/** Horizontal step for a prop that reaches the head, cm from the mesh center. */
	inline constexpr float HoverSideCm = 40.f;

	/** How far past the right face a short prop's wisp sits, cm. */
	inline constexpr float HoverAwayCm = 36.f;

	/** Cap on that offset, cm from the mesh center, so a wide box cannot throw the wisp. */
	inline constexpr float HoverAwayMaxCm = 160.f;

	/** Gap above a short prop, cm. The wisp floats above it, not beside it. */
	inline constexpr float HoverAboveCm = 40.f;

	/** Drawn heart half-width, cm. The rune's near edge must clear the object by this much. */
	inline constexpr float HeartHalfWidthCm = 83.f;

	/** Air between the heart's near edge and the object's face, cm. */
	inline constexpr float HeartGapCm = 35.f;

	/** Floor and cap on the side offset, cm from the object's center. */
	inline constexpr float HeartSideMinCm = 140.f;
	inline constexpr float HeartSideMaxCm = 360.f;

	/** The heart center never sits closer than this above the object's top, cm. */
	inline constexpr float HeartAboveCm = 30.f;

	/**
	 * Rune ribbons are ignored.
	 * If the mesh top reaches head height, the wisp stays at head height, 40 cm to the viewer's right of center.
	 * If the top is below the head, the wisp floats above that top and past the right face.
	 */
	bool HoverPoint(
		const AActor* Target,
		const FVector& ViewerWorld,
		float HeadZ,
		float TimeSeconds,
		FVector& OutWorld);

	/** The mesh bounds the hover and heart rules measure, rune ribbons excluded. */
	bool MeasureBounds(const AActor* Target, FVector& OutCenter, FVector& OutExtent);

	/**
	 * The trace heart sits beside the object and turns with the view.
	 * BaseZ is the player's head. The caller raises the center so the drawn
	 * shape stays above the floor and out of the object.
	 */
	bool HeartPoint(
		const AActor* Target,
		const FVector& ViewerWorld,
		float BaseZ,
		FVector& OutWorld);
}
