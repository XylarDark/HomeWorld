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
	Miss
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

	/** Wrong shape and a late start are both a miss. Grace ignores the window. Wrath ignores the shape. */
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
}
