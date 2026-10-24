// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldBonkArc.h"

namespace
{
	const FVector GRoutePadOrigin(0.f, 0.f, 44950.f);
	const FVector GRoutePadExtent(5000.f, 7000.f, 50.f);
	const float GRouteHalf = 96.f;
	const float GRouteRadius = 42.f;
	const float GRouteLaunchZ = 45000.f - 320.f + GRouteHalf;

	FVector RimLanding(const FVector& From)
	{
		const FVector Rim = HomeWorldBonk::NearestRimTarget(From, GRoutePadOrigin, GRoutePadExtent);
		FVector Land = HomeWorldBonk::LandingOnPad(Rim, GRoutePadOrigin, GRoutePadExtent, GRouteHalf);
		Land.Z = GRoutePadOrigin.Z + FMath::Abs(GRoutePadExtent.Z) + GRouteHalf;
		return Land;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkRouteTest,
	"HomeWorld.Opening.BonkRoute",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkRouteTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	const FVector EastFrom(5250.f, 0.f, GRouteLaunchZ);
	const FVector WestFrom(-5250.f, 0.f, GRouteLaunchZ);
	const FVector EastLand = RimLanding(EastFrom);
	const FVector WestLand = RimLanding(WestFrom);
	const HomeWorldBonk::FArc East = HomeWorldBonk::MakeArc(
		EastFrom, EastLand, GRoutePadOrigin, GRoutePadExtent, GRouteHalf, GRouteRadius);
	const HomeWorldBonk::FArc West = HomeWorldBonk::MakeArc(
		WestFrom, WestLand, GRoutePadOrigin, GRoutePadExtent, GRouteHalf, GRouteRadius);

	TestEqual(TEXT("+X lands 5 m inside the east rim"), static_cast<float>(East.Land.X), 4500.f, 0.1f);
	TestEqual(TEXT("+X keeps the fall's Y"), static_cast<float>(East.Land.Y), 0.f, 0.1f);
	TestFalse(TEXT("+X is the normal arc"), East.bDrop);
	TestTrue(TEXT("+X starts at the body"), HomeWorldBonk::PointOnArc(East, 0.f).Equals(EastFrom, 0.1f));
	TestTrue(TEXT("+X ends on the east rim"), HomeWorldBonk::PointOnArc(East, 1.f).Equals(East.Land, 0.1f));
	TestTrue(TEXT("+X stays on the east side"), East.Approach.X > 0.f && East.Land.X > 0.f);

	TestEqual(TEXT("-X lands 5 m inside the west rim"), static_cast<float>(West.Land.X), -4500.f, 0.1f);
	TestEqual(TEXT("-X keeps the fall's Y"), static_cast<float>(West.Land.Y), 0.f, 0.1f);
	TestFalse(TEXT("-X is the normal arc"), West.bDrop);
	TestTrue(TEXT("-X starts at the body"), HomeWorldBonk::PointOnArc(West, 0.f).Equals(WestFrom, 0.1f));
	TestTrue(TEXT("-X ends on the west rim"), HomeWorldBonk::PointOnArc(West, 1.f).Equals(West.Land, 0.1f));
	TestTrue(TEXT("-X stays on the west side"), West.Approach.X < 0.f && West.Land.X < 0.f);

	TestFalse(TEXT("the two rims are different landings"), East.Land.Equals(West.Land, 1.f));
	const FVector CottageDoor(-950.f, -1000.f, 45102.f);
	TestFalse(TEXT("+X does not aim at the cottage door"), East.Land.Equals(CottageDoor, 50.f));
	TestFalse(TEXT("-X does not aim at the cottage door"), West.Land.Equals(CottageDoor, 50.f));
	return true;
}

#endif
