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

#endif
