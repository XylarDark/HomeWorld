// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldBonkArc.h"

// Defined in HomeWorldCharacter.cpp with external linkage (the route lock allows no header change).
namespace HomeWorldBonkRoute
{
	FVector Waypoint(const HomeWorldBonk::FArc& Arc);
	int32 LegAt(const HomeWorldBonk::FArc& Arc, const FVector& Location);
	HomeWorldBonk::FArc MakeRoute(
		const FVector& From,
		const FVector& Land,
		const FVector& PadOrigin,
		const FVector& PadExtent,
		float BodyHalfHeightCm,
		float BodyRadiusCm);
	FVector PointOnRoute(const HomeWorldBonk::FArc& Arc, float T);
}

namespace
{
	// L_SizeTest: SM_Size_WalkPad bounds z 44900..45000, C1 by the cottage door.
	const FVector GRoutePadOrigin(0.f, 0.f, 44950.f);
	const FVector GRoutePadExtent(5000.f, 7000.f, 50.f);
	const FVector GRouteC1(-950.f, -1000.f, 45102.f);
	const float GRouteHalf = 96.f;
	const float GRouteRadius = 42.f;
	// A fall off the rim starts the return once the feet are 320 cm under the pad top.
	const float GRouteLaunchZ = 45000.f - 320.f + GRouteHalf;
	const int32 GRouteSteps = 512;

	bool InCabinFootprint(const FVector& Point)
	{
		return Point.X >= -1600.f && Point.X <= 1015.f && Point.Y >= -820.f && Point.Y <= 1515.f;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkRouteTest,
	"HomeWorld.Opening.BonkRoute",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkRouteTest::RunTest(const FString& Parameters)
{
	// +X: off the east rim, climb to the waypoint (4000, -1000) at the arc height, then due west along y -1000.
	const FVector EastFrom(5250.f, 0.f, GRouteLaunchZ);
	const HomeWorldBonk::FArc East = HomeWorldBonkRoute::MakeRoute(
		EastFrom, GRouteC1, GRoutePadOrigin, GRoutePadExtent, GRouteHalf, GRouteRadius);
	const FVector Turn = HomeWorldBonkRoute::Waypoint(East);
	const float ArcZ = static_cast<float>(GRouteC1.Z) + HomeWorldBonk::CrestCm;
	TestEqual(TEXT("+X lands on C1"), East.Land, GRouteC1, 5.f);
	TestEqual(TEXT("+X waypoint x"), static_cast<float>(Turn.X), 4000.f, 0.1f);
	TestEqual(TEXT("+X waypoint y is the landing line"), static_cast<float>(Turn.Y), -1000.f, 0.1f);
	TestEqual(TEXT("+X waypoint is at the arc height"), static_cast<float>(Turn.Z), ArcZ, 0.1f);
	TestEqual(TEXT("+X the climb crests at the arc height"), static_cast<float>(East.Approach.Z), ArcZ, 0.1f);
	TestTrue(TEXT("+X the climb stays outside the east rim"), East.Approach.X > GRoutePadOrigin.X + GRoutePadExtent.X);
	TestEqual(TEXT("+X leg at launch"), HomeWorldBonkRoute::LegAt(East, EastFrom), 1);
	TestEqual(TEXT("+X leg at the crest"), HomeWorldBonkRoute::LegAt(East, East.Approach), 1);
	TestEqual(TEXT("+X leg at the waypoint"), HomeWorldBonkRoute::LegAt(East, Turn), 2);
	TestEqual(TEXT("+X leg halfway home"), HomeWorldBonkRoute::LegAt(East, FMath::Lerp(Turn, GRouteC1, 0.5f)), 2);
	TestEqual(TEXT("+X leg at C1"), HomeWorldBonkRoute::LegAt(East, GRouteC1), 2);
	TestTrue(TEXT("+X the route starts at the body"), HomeWorldBonkRoute::PointOnRoute(East, 0.f).Equals(EastFrom, 0.1f));
	TestTrue(TEXT("+X the route ends on C1"), HomeWorldBonkRoute::PointOnRoute(East, 1.f).Equals(GRouteC1, 0.1f));
	TestTrue(TEXT("+X the flight has a duration"),
		East.DurationSec >= HomeWorldBonk::MinDurationSec && East.DurationSec <= HomeWorldBonk::MaxDurationSec);

	int32 Leg2Samples = 0;
	int32 OffLine = 0;
	int32 InCabin = 0;
	int32 ThroughPad = 0;
	int32 BackToLeg1 = 0;
	float WorstOffLine = 0.f;
	bool bSeenLeg2 = false;
	for (int32 Step = 0; Step <= GRouteSteps; ++Step)
	{
		const FVector Point = HomeWorldBonkRoute::PointOnRoute(East, static_cast<float>(Step) / GRouteSteps);
		const int32 Leg = HomeWorldBonkRoute::LegAt(East, Point);
		if (InCabinFootprint(Point))
		{
			++InCabin;
		}
		if (HomeWorldBonk::IsInsidePadXY(Point, GRoutePadOrigin, GRoutePadExtent)
			&& Point.Z - GRouteHalf < GRoutePadOrigin.Z + GRoutePadExtent.Z)
		{
			++ThroughPad;
		}
		if (Leg == 2)
		{
			bSeenLeg2 = true;
			++Leg2Samples;
			const float Off = static_cast<float>(FMath::Abs(Point.Y + 1000.0));
			WorstOffLine = FMath::Max(WorstOffLine, Off);
			if (Off > 1.f)
			{
				++OffLine;
			}
		}
		else if (bSeenLeg2)
		{
			++BackToLeg1;
		}
	}
	AddInfo(FString::Printf(TEXT("+X leg-2 samples %d of %d, worst |y+1000| %.2f cm"), Leg2Samples, GRouteSteps + 1, WorstOffLine));
	TestTrue(TEXT("+X most of the flight is the straight run home"), Leg2Samples > GRouteSteps / 3);
	TestEqual(TEXT("+X leg-2 samples off y -1000"), OffLine, 0);
	TestEqual(TEXT("+X samples inside the cabin footprint"), InCabin, 0);
	TestEqual(TEXT("+X samples through the pad"), ThroughPad, 0);
	TestEqual(TEXT("+X samples back on leg 1 after leg 2"), BackToLeg1, 0);

	// -X: the existing single arc, unchanged.
	const FVector WestFrom(-5250.f, 0.f, GRouteLaunchZ);
	const HomeWorldBonk::FArc West = HomeWorldBonkRoute::MakeRoute(
		WestFrom, GRouteC1, GRoutePadOrigin, GRoutePadExtent, GRouteHalf, GRouteRadius);
	const HomeWorldBonk::FArc Single = HomeWorldBonk::MakeArc(
		WestFrom, GRouteC1, GRoutePadOrigin, GRoutePadExtent, GRouteHalf, GRouteRadius);
	TestEqual(TEXT("-X lands on C1"), West.Land, GRouteC1, 5.f);
	TestEqual(TEXT("-X keeps the single arc's crest"), West.Approach, Single.Approach, 0.1f);
	TestEqual(TEXT("-X keeps the single arc's split"), West.Split, Single.Split, 0.001f);
	TestEqual(TEXT("-X keeps the single arc's duration"), West.DurationSec, Single.DurationSec, 0.001f);
	TestEqual(TEXT("-X has no waypoint"), HomeWorldBonkRoute::Waypoint(West), Single.Approach, 0.1f);
	int32 WestDiff = 0;
	int32 WestLegged = 0;
	for (int32 Step = 0; Step <= GRouteSteps; ++Step)
	{
		const float T = static_cast<float>(Step) / GRouteSteps;
		const FVector Point = HomeWorldBonkRoute::PointOnRoute(West, T);
		if (!Point.Equals(HomeWorldBonk::PointOnArc(Single, T), 0.1f))
		{
			++WestDiff;
		}
		if (HomeWorldBonkRoute::LegAt(West, Point) != 0)
		{
			++WestLegged;
		}
	}
	TestEqual(TEXT("-X samples off the single arc"), WestDiff, 0);
	TestEqual(TEXT("-X samples reported on a leg"), WestLegged, 0);
	return true;
}

#endif
