// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBonkArc.h"

#include "CollisionQueryParams.h"
#include "CollisionShape.h"
#include "Components/PrimitiveComponent.h"
#include "Engine/World.h"

namespace
{
	// Object channels a pawn blocks. Visibility and Camera are traces, not these.
	const ECollisionChannel GBlockChannels[] = {
		ECC_WorldStatic,
		ECC_WorldDynamic,
		ECC_Pawn,
		ECC_PhysicsBody,
		ECC_Vehicle,
		ECC_Destructible
	};

	FCollisionShape MakeBody(float Radius, float Half)
	{
		const float ShapeRadius = FMath::Max(Radius, 1.f);
		// A Chaos capsule wants the half-height to include the radius.
		const float ShapeHalf = FMath::Max(Half, ShapeRadius);
		return FCollisionShape::MakeCapsule(ShapeRadius, ShapeHalf);
	}

	float SegmentT(const FVector& From, const FVector& Land, float X, float Y)
	{
		const FVector2D Delta(Land.X - From.X, Land.Y - From.Y);
		const float LenSq = Delta.SizeSquared();
		if (LenSq < 1.f)
		{
			return 0.f;
		}
		const FVector2D Rel(X - From.X, Y - From.Y);
		return FMath::Clamp(FVector2D::DotProduct(Rel, Delta) / LenSq, 0.f, 1.f);
	}

	// The chord reports a side. This reads the surface under that point.
	bool HighestSurface(
		UWorld* World,
		const FVector2D& XY,
		float ProbeTop,
		float ProbeBottom,
		float Half,
		const FCollisionShape& Body,
		const FCollisionQueryParams& Params,
		float& OutTop)
	{
		const FVector Start(XY.X, XY.Y, ProbeTop);
		const FVector End(XY.X, XY.Y, ProbeBottom);
		bool bHit = false;
		float Best = 0.f;
		for (const ECollisionChannel Channel : GBlockChannels)
		{
			FHitResult Hit;
			if (!World->SweepSingleByChannel(
				Hit, Start, End, FQuat::Identity, Channel, Body, Params))
			{
				continue;
			}

			float Top = Hit.ImpactPoint.Z;
			if (Hit.bStartPenetrating)
			{
				const UPrimitiveComponent* Prim = Hit.GetComponent();
				if (!Prim)
				{
					continue;
				}
				const float BoundsTop = Prim->Bounds.GetBox().Max.Z;
				FHitResult Retry;
				const FVector RetryStart(XY.X, XY.Y, BoundsTop + Half + 100.f);
				if (BoundsTop > ProbeTop
					&& World->SweepSingleByChannel(
						Retry, RetryStart, End, FQuat::Identity, Channel, Body, Params)
					&& !Retry.bStartPenetrating)
				{
					Top = Retry.ImpactPoint.Z;
				}
				else
				{
					Top = BoundsTop;
				}
			}

			Best = bHit ? FMath::Max(Best, Top) : Top;
			bHit = true;
		}
		if (!bHit)
		{
			return false;
		}
		OutTop = Best;
		return true;
	}
}

namespace HomeWorldBonk
{
FClearance MeasureClearance(
	UWorld* World,
	const FVector& From,
	const FVector& Land,
	float BodyHalfHeightCm,
	float BodyRadiusCm,
	const AActor* IgnoreActor)
{
	FClearance Result;
	const float Half = FMath::Max(BodyHalfHeightCm, 0.f);
	const float Radius = FMath::Max(BodyRadiusCm, 1.f);
	Result.ApexZ = Land.Z + CrestCm;
	if (!World)
	{
		return Result;
	}

	const FCollisionShape Body = MakeBody(Radius, Half);
	FCollisionQueryParams Params(NAME_None, false, IgnoreActor);
	if (IgnoreActor)
	{
		Params.AddIgnoredActor(IgnoreActor);
	}

	const float ProbeTop = FMath::Max(From.Z, Land.Z) + Half + ClearanceMarginCm + 20000.f;
	const float ProbeBottom = FMath::Min(From.Z, Land.Z) - Half - 500.f;
	const float Feet = Land.Z - Half;
	const float Span = FMath::Max(FVector::Dist2D(From, Land), 1.f);
	const float WantedStep = FMath::Max(Radius, 20.f);
	const int32 GridCount = FMath::Clamp(FMath::CeilToInt(Span / WantedStep), 1, 96);

	bool bRaised = false;
	float FirstT = 1.f;
	float LastT = 0.f;
	float RequiredCenter = Result.ApexZ;

	auto Accept = [&](float T, float Top)
	{
		if (Top <= Feet + ClearanceFloorSlackCm)
		{
			return;
		}
		bRaised = true;
		RequiredCenter = FMath::Max(RequiredCenter, Top + ClearanceMarginCm + Half);
		const float Clamped = FMath::Clamp(T, 0.f, 1.f);
		FirstT = FMath::Min(FirstT, Clamped);
		LastT = FMath::Max(LastT, Clamped);
	};

	auto Probe = [&](float T)
	{
		const float Clamped = FMath::Clamp(T, 0.f, 1.f);
		const FVector Point = FMath::Lerp(From, Land, Clamped);
		float Top = 0.f;
		if (HighestSurface(
			World, FVector2D(Point.X, Point.Y), ProbeTop, ProbeBottom, Half, Body, Params, Top))
		{
			Accept(Clamped, Top);
		}
	};

	// Full-capsule sweep along the flight, then again at the higher end so a
	// low chord cannot slip under a wall. Each blocker is probed for its top.
	// The grid catches anything both chords fly over. SweepMulti stops at the
	// first blocker, so the chord repeats and ignores what it already found.
	auto SweepChord = [&](const FVector& Start, const FVector& End)
	{
		FCollisionQueryParams ChordParams = Params;
		for (const ECollisionChannel Channel : GBlockChannels)
		{
			for (int32 Step = 0; Step < 64; ++Step)
			{
				FHitResult Hit;
				if (!World->SweepSingleByChannel(
					Hit, Start, End, FQuat::Identity, Channel, Body, ChordParams))
				{
					break;
				}
				if (const AActor* HitActor = Hit.GetActor())
				{
					ChordParams.AddIgnoredActor(HitActor);
				}
				Probe(Hit.Time);
				if (const UPrimitiveComponent* Prim = Hit.GetComponent())
				{
					const FVector Center = Prim->Bounds.GetBox().GetCenter();
					Probe(SegmentT(From, Land, Center.X, Center.Y));
				}
				if (!Hit.GetActor())
				{
					break;
				}
			}
		}
	};

	SweepChord(From, Land);
	if (FMath::Abs(From.Z - Land.Z) > 1.f)
	{
		const float HighZ = FMath::Max(From.Z, Land.Z);
		SweepChord(FVector(From.X, From.Y, HighZ), FVector(Land.X, Land.Y, HighZ));
	}

	for (int32 Index = 0; Index <= GridCount; ++Index)
	{
		Probe(static_cast<float>(Index) / static_cast<float>(GridCount));
	}

	if (!bRaised)
	{
		return Result;
	}

	// One grid step, so the cruise is already at the apex on the sample before
	// the first hit and stays there through the sample after the last.
	const float ActualStep = Span / static_cast<float>(GridCount);
	const float PadT = FMath::Clamp(FMath::Max(ActualStep, Radius) / Span, 0.f, 0.5f);
	Result.bRaised = true;
	Result.ApexZ = RequiredCenter;
	Result.ApproachT = FMath::Clamp(FirstT - PadT, 0.f, 1.f);
	Result.DropT = FMath::Clamp(LastT + PadT, Result.ApproachT, 1.f);
	return Result;
}
}
