// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldBonkArc.h"

namespace
{
	const FVector GPadOrigin(0.f, 0.f, 45000.f);
	const FVector GPadExtent(5000.f, 7000.f, 50.f);
	const float GHalf = 90.f;
	const float GRadius = 40.f;
	const float GStandingZ = 45140.f;

	bool StaysAbovePad(const HomeWorldBonk::FArc& Arc)
	{
		for (int32 Step = 0; Step <= 64; ++Step)
		{
			const FVector Point = HomeWorldBonk::PointOnArc(Arc, static_cast<float>(Step) / 64.f);
			if (HomeWorldBonk::IsInsidePadXY(Point, GPadOrigin, GPadExtent)
				&& Point.Z < Arc.Land.Z - 40.f)
			{
				return false;
			}
		}
		return true;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkArcLandingTest,
	"HomeWorld.Opening.BonkArc",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkArcLandingTest::RunTest(const FString& Parameters)
{
	const FVector RimTarget(-5000.f, 0.f, GStandingZ);
	const FVector RimLand = HomeWorldBonk::LandingOnPad(RimTarget, GPadOrigin, GPadExtent, GHalf);
	TestTrue(TEXT("a rim target lands 5 m inside"), FMath::IsNearlyEqual(RimLand.X, -4500.f, 0.1f));
	TestTrue(TEXT("a rim target keeps its Y"), FMath::IsNearlyEqual(RimLand.Y, 0.f, 0.1f));
	TestTrue(TEXT("a rim target keeps the standing height"), FMath::IsNearlyEqual(RimLand.Z, GStandingZ, 0.1f));

	const FVector Inland = HomeWorldBonk::LandingOnPad(FVector(-2000.f, 250.f, GStandingZ), GPadOrigin, GPadExtent, GHalf);
	TestTrue(TEXT("an inland target stays put"), FMath::IsNearlyEqual(Inland.X, -2000.f, 0.1f));
	TestTrue(TEXT("an inland target keeps its Y"), FMath::IsNearlyEqual(Inland.Y, 250.f, 0.1f));

	const FVector Tiny = HomeWorldBonk::LandingOnPad(
		FVector(80.f, 0.f, 200.f), FVector::ZeroVector, FVector(80.f, 80.f, 10.f), GHalf);
	TestTrue(TEXT("a narrow pad lands inside itself"), FMath::Abs(Tiny.X) <= 40.f);
	TestTrue(TEXT("a narrow pad does not push past center"), FMath::IsNearlyEqual(Tiny.X, 40.f, 0.1f));

	const FVector Empty = HomeWorldBonk::LandingOnPad(
		FVector(40.f, -20.f, 10.f), FVector(5.f, 6.f, 0.f), FVector::ZeroVector, GHalf);
	TestTrue(TEXT("a missing pad extent lands on the origin X"), FMath::IsNearlyEqual(Empty.X, 5.f, 0.1f));
	TestTrue(TEXT("a missing pad extent lands on the origin Y"), FMath::IsNearlyEqual(Empty.Y, 6.f, 0.1f));

	const FVector From(-5080.f, 0.f, GStandingZ - 320.f);
	const HomeWorldBonk::FArc Fall = HomeWorldBonk::MakeArc(From, RimTarget, GPadOrigin, GPadExtent, GHalf, GRadius);
	TestTrue(TEXT("the fall lands 5 m inland"), FMath::IsNearlyEqual(Fall.Land.X, -4500.f, 0.1f));
	TestTrue(TEXT("the crest is the shallow cap"), FMath::IsNearlyEqual(Fall.Approach.Z, GStandingZ + HomeWorldBonk::CrestCm, 0.1f));
	TestTrue(TEXT("the crest is not a launch"), Fall.Approach.Z <= GStandingZ + HomeWorldBonk::CrestCm + 0.1f);
	TestTrue(TEXT("the climb stays beside the pad"), Fall.Approach.X < GPadOrigin.X - GPadExtent.X);
	const float Climb = Fall.Approach.Z - Fall.From.Z;
	const float Run = FMath::Max(FVector::Dist2D(Fall.From, Fall.Approach), 1.f);
	TestTrue(TEXT("the climb slope stays shallow"), Climb / Run <= HomeWorldBonk::MaxRisePerRun + 0.02f);
	TestTrue(TEXT("the swoop is above the pad when it crosses the rim"), StaysAbovePad(Fall));
	TestTrue(TEXT("the arc starts at the body"), Fall.From.Equals(HomeWorldBonk::PointOnArc(Fall, 0.f), 0.1f));
	TestTrue(TEXT("the arc ends on the landing"), Fall.Land.Equals(HomeWorldBonk::PointOnArc(Fall, 1.f), 0.1f));
	TestTrue(TEXT("the flight has a duration"), Fall.DurationSec >= HomeWorldBonk::MinDurationSec && Fall.DurationSec <= HomeWorldBonk::MaxDurationSec);

	const FVector JustOutside(-6300.f, 0.f, GStandingZ - 320.f);
	const HomeWorldBonk::FArc Just = HomeWorldBonk::MakeArc(JustOutside, RimTarget, GPadOrigin, GPadExtent, GHalf, GRadius);
	const float JustRise = Just.Approach.Z - Just.From.Z;
	const float JustRun = FMath::Max(FVector::Dist2D(Just.From, Just.Approach), 1.f);
	TestTrue(TEXT("a longer fall line stays at the slope cap"), JustRise / JustRun <= HomeWorldBonk::MaxRisePerRun + 0.02f);
	TestTrue(TEXT("a longer fall line crests before the rim"), Just.Approach.X < GPadOrigin.X - GPadExtent.X);
	TestTrue(TEXT("a longer fall line stays above the pad"), StaysAbovePad(Just));

	const FVector Far(-20000.f, 0.f, GStandingZ - 100.f);
	const HomeWorldBonk::FArc Runway = HomeWorldBonk::MakeArc(Far, RimTarget, GPadOrigin, GPadExtent, GHalf, GRadius);
	TestTrue(TEXT("a long fall line still crests low"), Runway.Approach.Z <= GStandingZ + HomeWorldBonk::CrestCm + 0.1f);
	TestTrue(TEXT("a long fall line still lands inland"), FMath::IsNearlyEqual(Runway.Land.X, -4500.f, 0.1f));
	TestTrue(TEXT("a long fall line stays above the pad"), StaysAbovePad(Runway));

	const FVector Deep(-5080.f, 0.f, GStandingZ - 5000.f);
	const HomeWorldBonk::FArc Capped = HomeWorldBonk::MakeArc(Deep, RimTarget, GPadOrigin, GPadExtent, GHalf, GRadius);
	const float Lead = FVector::Dist2D(Capped.From, Capped.Approach);
	TestTrue(TEXT("a deep fall does not tour the island"), Lead <= HomeWorldBonk::MaxLeadCm + HomeWorldBonk::MinOutsideGapCm + 1.f);
	TestTrue(TEXT("a deep fall still crests at the cap"), FMath::IsNearlyEqual(Capped.Approach.Z, GStandingZ + HomeWorldBonk::CrestCm, 0.1f));
	TestTrue(TEXT("a deep fall has a finite landing"), FMath::IsFinite(Capped.Land.X) && FMath::IsFinite(Capped.Land.Z));

	return true;
}

#endif
