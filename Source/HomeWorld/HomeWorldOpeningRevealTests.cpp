// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldOpeningReveal.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningRevealChildArrivesFirst,
	"HomeWorld.Systems.Opening.ChildArrivesFirst",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningRevealChildArrivesFirst::RunTest(const FString& Parameters)
{
	const FVector Start(-800.f, -840.f, 45000.f);
	const FVector Spirit(-400.f, -900.f, 45100.f);
	const FVector Step = AHomeWorldOpeningReveal::StepToward(Start, Spirit, 100.f);
	TestTrue(TEXT("the child leaves the door"), FVector::Dist2D(Step, Start) > 50.f);
	TestTrue(TEXT("the step is toward the spirit"), FVector::Dist2D(Step, Spirit) < FVector::Dist2D(Start, Spirit));
	TestEqual(TEXT("the child stays on the floor"), Step.Z, Start.Z);

	const float ChildDistance = 412.f;
	const float TooClose = ChildDistance * (AHomeWorldOpeningReveal::PlayerMaxSpeed / AHomeWorldOpeningReveal::ChildRunSpeed) - 50.f;
	const float FarEnough = ChildDistance * (AHomeWorldOpeningReveal::PlayerMaxSpeed / AHomeWorldOpeningReveal::ChildRunSpeed) + 50.f;
	TestFalse(TEXT("a short gap lets the player win at full speed"), AHomeWorldOpeningReveal::ChildArrivesFirst(TooClose, ChildDistance));
	TestTrue(TEXT("the longer gap lets the child arrive first"), AHomeWorldOpeningReveal::ChildArrivesFirst(FarEnough, ChildDistance));

	const FVector Door(-800.f, -860.f, 45000.f);
	const FVector Halfway(-700.f, -2900.f, 45075.f);
	const FVector Beside = AHomeWorldOpeningReveal::StandNear(Door, Halfway, 180.f);
	TestEqual(TEXT("the child stays on the floor beside the spirit"), Beside.Z, Door.Z);
	TestTrue(TEXT("the child stops short of the sphere"), FVector::Dist2D(Beside, Halfway) > 150.f);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningRevealChildRaceRoute,
	"HomeWorld.Systems.Opening.ChildRaceRoute",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningRevealChildRaceRoute::RunTest(const FString& Parameters)
{
	const FVector Dog(-390.f, 2000.f, 45000.f);
	const TArray<FVector> Route = AHomeWorldOpeningReveal::ChildRaceRoute(Dog, 45000.f);
	TestEqual(TEXT("four legs out the back door"), Route.Num(), 4);
	if (Route.Num() != 4)
	{
		return false;
	}
	const FVector Room(-400.f, 800.f, 45000.f);
	TestTrue(TEXT("the race starts at the room, no jump"), FVector::Dist2D(Route[0], Room) <= 200.f);
	TestTrue(TEXT("the race leaves by the back door inside point"),
		FVector::Dist2D(Route[1], FVector(-390.f, 900.f, 45000.f)) <= 1.f);
	TestTrue(TEXT("the race leaves by the back door outside point"),
		FVector::Dist2D(Route[2], FVector(-390.f, 1200.f, 45000.f)) <= 1.f);
	const FVector Yard = Route.Last();
	TestTrue(TEXT("the yard is the dog offset"), FVector::Dist2D(Yard, Dog + FVector(150.f, -610.f, 0.f)) <= 1.f);
	const float YardToDog = FVector::Dist2D(Yard, Dog);
	TestTrue(TEXT("the child waits outside the knock ring"), YardToDog > 400.f);
	TestTrue(TEXT("the child waits inside the Grace ring"), YardToDog < 900.f);
	TestTrue(TEXT("the yard leaves the lane room to pass"), FMath::Abs(Yard.X - Dog.X) >= 100.f);
	for (int32 Leg = 0; Leg < Route.Num(); ++Leg)
	{
		TestEqual(TEXT("the race stays on the floor"), Route[Leg].Z, 45000.0);
		if (Leg > 0)
		{
			const float Gap = FVector::Dist2D(Route[Leg - 1], Route[Leg]);
			TestTrue(TEXT("no teleport between legs"), Gap <= 900.f);
			TestTrue(TEXT("no stalled leg"), Gap >= 50.f);
		}
	}
	return true;
}

#endif
