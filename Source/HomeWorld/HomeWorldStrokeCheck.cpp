// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldStrokeCheck.h"

namespace HomeWorldStroke
{
	static constexpr int32 SampleCount = 8;
	static constexpr float MatchDistance = 0.15f;
	static constexpr float PointEpsilon = 0.05f;

	const TArray<FVector2D>& GraceShape()
	{
		static TArray<FVector2D> Shape;
		if (Shape.Num() == 0)
		{
			Shape.Add(FVector2D(0.f, 0.f));
			Shape.Add(FVector2D(0.f, 1.f));
		}
		return Shape;
	}

	const TArray<FVector2D>& ParadoxShape()
	{
		static TArray<FVector2D> Shape;
		if (Shape.Num() == 0)
		{
			Shape.Add(FVector2D(0.f, 0.f));
			Shape.Add(FVector2D(1.f, 1.f));
		}
		return Shape;
	}

	static void BoundsOf(const TArray<FVector2D>& Points, FVector2D& OutMin, float& OutScale)
	{
		OutMin = Points[0];
		FVector2D Max = Points[0];
		for (const FVector2D& Point : Points)
		{
			OutMin.X = FMath::Min(OutMin.X, Point.X);
			OutMin.Y = FMath::Min(OutMin.Y, Point.Y);
			Max.X = FMath::Max(Max.X, Point.X);
			Max.Y = FMath::Max(Max.Y, Point.Y);
		}
		const FVector2D Size = Max - OutMin;
		OutScale = FMath::Max(Size.X, Size.Y);
		if (OutScale < KINDA_SMALL_NUMBER)
		{
			OutScale = 1.f;
		}
	}

	static TArray<FVector2D> Resample(const TArray<FVector2D>& Points, int32 Count)
	{
		TArray<FVector2D> Out;
		Out.Reserve(Count);
		if (Points.Num() == 0 || Count <= 0)
		{
			return Out;
		}
		if (Points.Num() == 1 || Count == 1)
		{
			Out.Add(Points[0]);
			return Out;
		}
		TArray<float> Lengths;
		Lengths.Reserve(Points.Num());
		Lengths.Add(0.f);
		for (int32 Index = 1; Index < Points.Num(); ++Index)
		{
			Lengths.Add(Lengths[Index - 1] + FVector2D::Distance(Points[Index - 1], Points[Index]));
		}
		const float Total = Lengths.Last();
		if (Total < KINDA_SMALL_NUMBER)
		{
			for (int32 Index = 0; Index < Count; ++Index)
			{
				Out.Add(Points[0]);
			}
			return Out;
		}
		int32 Segment = 1;
		for (int32 Index = 0; Index < Count; ++Index)
		{
			const float Distance = Total * (static_cast<float>(Index) / static_cast<float>(Count - 1));
			while (Segment < Lengths.Num() - 1 && Lengths[Segment] < Distance)
			{
				++Segment;
			}
			const float Span = Lengths[Segment] - Lengths[Segment - 1];
			const float Alpha = Span < KINDA_SMALL_NUMBER ? 0.f : (Distance - Lengths[Segment - 1]) / Span;
			Out.Add(FMath::Lerp(Points[Segment - 1], Points[Segment], Alpha));
		}
		return Out;
	}

	static TArray<FVector2D> Normalize(const TArray<FVector2D>& Points)
	{
		FVector2D Min;
		float Scale = 1.f;
		BoundsOf(Points, Min, Scale);
		TArray<FVector2D> Out;
		Out.Reserve(Points.Num());
		for (const FVector2D& Point : Points)
		{
			Out.Add((Point - Min) / Scale);
		}
		return Out;
	}

	static bool ShapeMatches(const TArray<FVector2D>& Stroke, const TArray<FVector2D>& Pattern)
	{
		if (Stroke.Num() < 2 || Pattern.Num() < 2)
		{
			return false;
		}
		const TArray<FVector2D> FromStroke = Resample(Normalize(Stroke), SampleCount);
		const TArray<FVector2D> FromPattern = Resample(Normalize(Pattern), SampleCount);
		float Total = 0.f;
		for (int32 Index = 0; Index < SampleCount; ++Index)
		{
			Total += FVector2D::Distance(FromStroke[Index], FromPattern[Index]);
		}
		return (Total / static_cast<float>(SampleCount)) <= MatchDistance;
	}

	bool PassesThroughPoint(const TArray<FHomeWorldStrokeSample>& Stroke, const FVector2D& Point)
	{
		for (const FHomeWorldStrokeSample& Sample : Stroke)
		{
			if (FVector2D::Distance(Sample.Point, Point) <= PointEpsilon)
			{
				return true;
			}
		}
		return false;
	}

	static bool StartsInside(const TArray<FHomeWorldStrokeSample>& Stroke, float WindowMin, float WindowMax)
	{
		if (Stroke.Num() == 0)
		{
			return false;
		}
		const float Start = Stroke[0].Time;
		return Start >= WindowMin && Start <= WindowMax;
	}

	static TArray<FVector2D> PointsOf(const TArray<FHomeWorldStrokeSample>& Stroke)
	{
		TArray<FVector2D> Points;
		Points.Reserve(Stroke.Num());
		for (const FHomeWorldStrokeSample& Sample : Stroke)
		{
			Points.Add(Sample.Point);
		}
		return Points;
	}

	EHomeWorldStrokeResult Evaluate(
		EHomeWorldStrokeStep Step,
		const TArray<FHomeWorldStrokeSample>& Stroke,
		float WindowMin,
		float WindowMax,
		const FVector2D& ExtraPoint)
	{
		const bool bNeedsShape = Step != EHomeWorldStrokeStep::Wrath;
		const bool bNeedsWindow = Step != EHomeWorldStrokeStep::Grace;
		const bool bNeedsExtra = Step == EHomeWorldStrokeStep::ParadoxExtraPoint;
		if (bNeedsShape && !ShapeMatches(PointsOf(Stroke), Step == EHomeWorldStrokeStep::Grace ? GraceShape() : ParadoxShape()))
		{
			return EHomeWorldStrokeResult::Miss;
		}
		if (bNeedsWindow && !StartsInside(Stroke, WindowMin, WindowMax))
		{
			return EHomeWorldStrokeResult::Late;
		}
		if (bNeedsExtra && !PassesThroughPoint(Stroke, ExtraPoint))
		{
			return EHomeWorldStrokeResult::Miss;
		}
		return EHomeWorldStrokeResult::Match;
	}

	FVector WeakHitStep(const FVector& From, const FVector& Focus)
	{
		static constexpr float StepCm = 300.f;
		FVector Away = From - Focus;
		Away.Z = 0.f;
		if (Away.IsNearlyZero())
		{
			Away = FVector(-1.f, 0.f, 0.f);
		}
		return Away.GetSafeNormal() * StepCm;
	}

	static constexpr float ScreenRectOriginX = 0.08f;
	static constexpr float ScreenRectOriginY = 0.15f;
	static constexpr float ScreenRectSize = 0.28f;

	static float RectSide(const FVector2D& ViewportPx)
	{
		return FMath::Min(ViewportPx.X, ViewportPx.Y) * ScreenRectSize;
	}

	static FVector2D RectOrigin(const FVector2D& ViewportPx)
	{
		return FVector2D(ViewportPx.X * ScreenRectOriginX, ViewportPx.Y * ScreenRectOriginY);
	}

	FVector2D MapMouseToStrokeUnit(const FVector2D& MousePx, const FVector2D& ViewportPx)
	{
		const float Side = RectSide(ViewportPx);
		if (Side < KINDA_SMALL_NUMBER)
		{
			return FVector2D::ZeroVector;
		}
		return (MousePx - RectOrigin(ViewportPx)) / Side;
	}

	FVector2D StrokeUnitToScreen(const FVector2D& Unit, const FVector2D& ViewportPx)
	{
		return RectOrigin(ViewportPx) + Unit * RectSide(ViewportPx);
	}
}
