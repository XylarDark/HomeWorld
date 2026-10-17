// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldStrokeCheck.generated.h"

/** The four ease steps, in the order the player meets them. Docs/VIRTUE_ATTRIBUTE_BIBLE.md. */
UENUM(BlueprintType)
enum class EHomeWorldStrokeStep : uint8
{
	Grace,
	Wrath,
	Paradox,
	ParadoxExtraPoint
};

UENUM(BlueprintType)
enum class EHomeWorldStrokeResult : uint8
{
	Match,
	Miss,
	/** Started outside the wind-up. A wrong shape stays Miss. */
	Late
};

USTRUCT(BlueprintType)
struct FHomeWorldStrokeSample
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, Category = "Stroke")
	FVector2D Point = FVector2D::ZeroVector;

	UPROPERTY(BlueprintReadWrite, Category = "Stroke")
	float Time = 0.f;
};

namespace HomeWorldStroke
{
	HOMEWORLD_API const TArray<FVector2D>& GraceShape();

	HOMEWORLD_API const TArray<FVector2D>& ParadoxShape();

	/** A wrong shape is a miss. A start outside the wind-up is late. Grace ignores the window. Wrath ignores the shape. */
	HOMEWORLD_API EHomeWorldStrokeResult Evaluate(
		EHomeWorldStrokeStep Step,
		const TArray<FHomeWorldStrokeSample>& Stroke,
		float WindowMin,
		float WindowMax,
		const FVector2D& ExtraPoint);

	/** True when a sample sits on the point. */
	HOMEWORLD_API bool PassesThroughPoint(
		const TArray<FHomeWorldStrokeSample>& Stroke,
		const FVector2D& Point);

	/** A short step away from the focus. Z is unchanged. */
	HOMEWORLD_API FVector WeakHitStep(const FVector& From, const FVector& Focus);

	/**
	 * The greybox drawing rect, as a fraction of the viewport.
	 * Mouse samples and the HUD use this same rect, in the 0–1 space of the shapes.
	 */
	HOMEWORLD_API FVector2D MapMouseToStrokeUnit(const FVector2D& MousePx, const FVector2D& ViewportPx);
	HOMEWORLD_API FVector2D StrokeUnitToScreen(const FVector2D& Unit, const FVector2D& ViewportPx);
}
