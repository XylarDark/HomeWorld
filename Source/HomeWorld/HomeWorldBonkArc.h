// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class AActor;
class UWorld;

// The return flight shared by every bonk. The landing is the pad edge nearest
// the body, set in from the rim. A clear shot uses the normal arc. No
// clearance pops the body straight up, then plays that same arc from the air.
namespace HomeWorldBonk
{
	// How far inside the pad the body is set down, in cm. A narrower pad uses
	// half of its shorter half-extent so the landing stays on the pad.
	inline constexpr float LandingInsetCm = 500.f;
	// Highest the clear-corridor swoop crests above the standing height.
	// A blocker may force the cruise higher. It never forces it lower.
	inline constexpr float CrestCm = 150.f;
	// Capsule bottom stays this far above the tallest blocker, in cm.
	inline constexpr float ClearanceMarginCm = 100.f;
	// A surface this close to the landing feet is the pad, not something to fly over.
	inline constexpr float ClearanceFloorSlackCm = 40.f;
	// Climb budget: 45 cm of rise for each 100 cm of run. Steeper than this
	// grows a lead beside the pad instead of a vertical launch.
	inline constexpr float MaxRisePerRun = 0.45f;
	inline constexpr float MaxLeadCm = 1600.f;
	inline constexpr float MinOutsideGapCm = 120.f;
	inline constexpr float SpeedCmPerSec = 750.f;
	inline constexpr float MinDurationSec = 1.0f;
	inline constexpr float MaxDurationSec = 3.2f;

	struct FArc
	{
		FVector From = FVector::ZeroVector;
		FVector Approach = FVector::ZeroVector;
		FVector Land = FVector::ZeroVector;
		// Cruise end. The path drops from here to Land when bDrop is set.
		FVector Drop = FVector::ZeroVector;
		bool bDrop = false;
		float Split = 0.5f;
		float DropSplit = 1.f;
		float DurationSec = 1.f;
	};

	// What the launch sweep found between From and Land. ApexZ is the actor
	// center. ApproachT and DropT are 0-1 along that straight segment.
	struct FClearance
	{
		bool bRaised = false;
		float ApexZ = 0.f;
		float ApproachT = 0.f;
		float DropT = 1.f;
	};

	inline bool IsInsidePadXY(const FVector& Point, const FVector& PadOrigin, const FVector& PadExtent, float SlackCm = 0.f)
	{
		return FMath::Abs(Point.X - PadOrigin.X) <= FMath::Abs(PadExtent.X) + SlackCm
			&& FMath::Abs(Point.Y - PadOrigin.Y) <= FMath::Abs(PadExtent.Y) + SlackCm;
	}

	inline FVector LandingOnPad(const FVector& Target, const FVector& PadOrigin, const FVector& PadExtent, float BodyHalfHeightCm)
	{
		const float HalfX = FMath::Max(FMath::Abs(PadExtent.X), 0.f);
		const float HalfY = FMath::Max(FMath::Abs(PadExtent.Y), 0.f);
		const float HalfZ = FMath::Max(FMath::Abs(PadExtent.Z), 0.f);
		const float InsetX = FMath::Min(LandingInsetCm, HalfX * 0.5f);
		const float InsetY = FMath::Min(LandingInsetCm, HalfY * 0.5f);
		FVector Land = Target;
		if (HalfX <= KINDA_SMALL_NUMBER)
		{
			Land.X = PadOrigin.X;
		}
		else
		{
			Land.X = FMath::Clamp(Target.X, PadOrigin.X - HalfX + InsetX, PadOrigin.X + HalfX - InsetX);
		}
		if (HalfY <= KINDA_SMALL_NUMBER)
		{
			Land.Y = PadOrigin.Y;
		}
		else
		{
			Land.Y = FMath::Clamp(Target.Y, PadOrigin.Y - HalfY + InsetY, PadOrigin.Y + HalfY - InsetY);
		}
		const float PadTop = PadOrigin.Z + HalfZ;
		if (Target.Z < PadTop)
		{
			Land.Z = PadTop + FMath::Max(BodyHalfHeightCm, 0.f);
		}
		return Land;
	}

	// The closest point on the pad footprint. LandingOnPad then sets it in from the rim.
	inline FVector NearestRimTarget(const FVector& From, const FVector& PadOrigin, const FVector& PadExtent)
	{
		const float HalfX = FMath::Max(FMath::Abs(PadExtent.X), 0.f);
		const float HalfY = FMath::Max(FMath::Abs(PadExtent.Y), 0.f);
		FVector Target = From;
		if (HalfX <= KINDA_SMALL_NUMBER)
		{
			Target.X = PadOrigin.X;
		}
		else
		{
			Target.X = FMath::Clamp(From.X, PadOrigin.X - HalfX, PadOrigin.X + HalfX);
		}
		if (HalfY <= KINDA_SMALL_NUMBER)
		{
			Target.Y = PadOrigin.Y;
		}
		else
		{
			Target.Y = FMath::Clamp(From.Y, PadOrigin.Y - HalfY, PadOrigin.Y + HalfY);
		}
		Target.Z = PadOrigin.Z + FMath::Max(FMath::Abs(PadExtent.Z), 0.f);
		return Target;
	}

	inline FVector SegmentEnterPoint(const FVector& From, const FVector& Land, const FVector& PadOrigin, const FVector& PadExtent)
	{
		const FVector Delta = Land - From;
		float T0 = 0.f;
		float T1 = 1.f;
		const float P[2] = {From.X, From.Y};
		const float D[2] = {Delta.X, Delta.Y};
		const float BMin[2] = {
			PadOrigin.X - FMath::Abs(PadExtent.X),
			PadOrigin.Y - FMath::Abs(PadExtent.Y)};
		const float BMax[2] = {
			PadOrigin.X + FMath::Abs(PadExtent.X),
			PadOrigin.Y + FMath::Abs(PadExtent.Y)};
		for (int32 Axis = 0; Axis < 2; ++Axis)
		{
			if (FMath::Abs(D[Axis]) < KINDA_SMALL_NUMBER)
			{
				if (P[Axis] < BMin[Axis] || P[Axis] > BMax[Axis])
				{
					return Land;
				}
				continue;
			}
			const float Inv = 1.f / D[Axis];
			float Ta = (BMin[Axis] - P[Axis]) * Inv;
			float Tb = (BMax[Axis] - P[Axis]) * Inv;
			if (Ta > Tb)
			{
				const float Swap = Ta;
				Ta = Tb;
				Tb = Swap;
			}
			T0 = FMath::Max(T0, Ta);
			T1 = FMath::Min(T1, Tb);
			if (T0 > T1)
			{
				return Land;
			}
		}
		return FMath::Lerp(From, Land, FMath::Clamp(T0, 0.f, 1.f));
	}

	// Capsule sweep from the hit to the landing. Ignores the pawn. A clear shot
	// leaves bRaised false. No clearance is the pop in front of the normal arc.
	FClearance MeasureClearance(
		UWorld* World,
		const FVector& From,
		const FVector& Land,
		float BodyHalfHeightCm,
		float BodyRadiusCm,
		const AActor* IgnoreActor);

	inline FArc MakeArc(
		const FVector& From,
		const FVector& Target,
		const FVector& PadOrigin,
		const FVector& PadExtent,
		float BodyHalfHeightCm,
		float BodyRadiusCm)
	{
		FArc Arc;
		Arc.From = From;
		Arc.bDrop = false;
		Arc.Land = LandingOnPad(Target, PadOrigin, PadExtent, BodyHalfHeightCm);

		const float HalfX = FMath::Max(FMath::Abs(PadExtent.X), 0.f);
		const float HalfY = FMath::Max(FMath::Abs(PadExtent.Y), 0.f);
		const FVector2D Delta(From.X - PadOrigin.X, From.Y - PadOrigin.Y);
		const float NormX = (HalfX > KINDA_SMALL_NUMBER) ? Delta.X / HalfX : 0.f;
		const float NormY = (HalfY > KINDA_SMALL_NUMBER) ? Delta.Y / HalfY : 0.f;
		FVector2D Outward(-1.f, 0.f);
		if (FMath::Abs(NormX) >= FMath::Abs(NormY))
		{
			const float Sign = (NormX < 0.f) ? -1.f : 1.f;
			Outward = FVector2D(Sign, 0.f);
		}
		else
		{
			const float Sign = (NormY < 0.f) ? -1.f : 1.f;
			Outward = FVector2D(0.f, Sign);
		}
		const FVector2D Tangent(-Outward.Y, Outward.X);
		const float Gap = FMath::Max(MinOutsideGapCm, BodyRadiusCm + 80.f);
		const float CrestZ = Arc.Land.Z + CrestCm;
		const float Climb = FMath::Max(0.f, CrestZ - From.Z);
		const float RunNeeded = (MaxRisePerRun > KINDA_SMALL_NUMBER) ? (Climb / MaxRisePerRun) : 0.f;
		const bool bOutside = !IsInsidePadXY(From, PadOrigin, PadExtent);

		if (!bOutside)
		{
			Arc.Approach = FMath::Lerp(From, Arc.Land, 0.5f);
			Arc.Approach.Z = FMath::Max(Arc.Approach.Z, CrestZ);
		}
		else
		{
			const FVector Rim = SegmentEnterPoint(From, Arc.Land, PadOrigin, PadExtent);
			const float RunHave = FVector::Dist2D(From, Rim);
			// Stop the crest short of the rim so the outside gap does not eat the runway.
			const float Room = FMath::Max(0.f, RunHave - Gap);
			if (Room + 1.f >= RunNeeded)
			{
				const FVector TowardRim = (Rim - From).GetSafeNormal2D();
				Arc.Approach = From + TowardRim * RunNeeded;
				Arc.Approach.Z = CrestZ;
			}
			else
			{
				const float Lead = FMath::Min(MaxLeadCm, RunNeeded);
				Arc.Approach.X = From.X + Outward.X * Gap + Tangent.X * Lead;
				Arc.Approach.Y = From.Y + Outward.Y * Gap + Tangent.Y * Lead;
				Arc.Approach.Z = CrestZ;
			}
		}

		const float LenA = FVector::Dist(Arc.From, Arc.Approach);
		const float LenB = FVector::Dist(Arc.Approach, Arc.Land);
		const float Total = LenA + LenB;
		Arc.Split = (Total > 1.f) ? FMath::Clamp(LenA / Total, 0.05f, 0.95f) : 0.5f;
		Arc.DurationSec = FMath::Clamp(
			(Total > 1.f) ? (Total / SpeedCmPerSec) : MinDurationSec,
			MinDurationSec,
			MaxDurationSec);
		return Arc;
	}

	inline FVector PointOnArc(const FArc& Arc, float T)
	{
		const float Clamped = FMath::Clamp(T, 0.f, 1.f);
		if (Arc.bDrop)
		{
			const float Split = FMath::Clamp(Arc.Split, 0.02f, 0.90f);
			const float DropSplit = FMath::Clamp(Arc.DropSplit, Split, 0.98f);
			if (Clamped <= Split)
			{
				const float Denom = FMath::Max(Split, KINDA_SMALL_NUMBER);
				return FMath::Lerp(Arc.From, Arc.Approach, FMath::Min(Clamped / Denom, 1.f));
			}
			if (Clamped <= DropSplit)
			{
				const float Denom = FMath::Max(DropSplit - Split, KINDA_SMALL_NUMBER);
				return FMath::Lerp(Arc.Approach, Arc.Drop, (Clamped - Split) / Denom);
			}
			const float Denom = FMath::Max(1.f - DropSplit, KINDA_SMALL_NUMBER);
			return FMath::Lerp(Arc.Drop, Arc.Land, (Clamped - DropSplit) / Denom);
		}

		const float Split = FMath::Clamp(Arc.Split, 0.05f, 0.95f);
		if (Clamped <= Split)
		{
			return FMath::Lerp(Arc.From, Arc.Approach, Clamped / Split);
		}
		return FMath::Lerp(Arc.Approach, Arc.Land, (Clamped - Split) / (1.f - Split));
	}
}
