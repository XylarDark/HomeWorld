// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/TargetPoint.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTestWorld.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningLookCursorTest,
	"HomeWorld.Opening.LookCursor",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningLookCursorTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening look cursor"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	ATargetPoint* OffLook = Scope.World->SpawnActor<ATargetPoint>(FVector(100.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	ATargetPoint* LookedAt = Scope.World->SpawnActor<ATargetPoint>(FVector(200.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("the nearer actor"), OffLook) || !TestNotNull(TEXT("the looked-at actor"), LookedAt))
	{
		return false;
	}

	TestTrue(TEXT("280 cm is in reach"), AHomeWorldCharacter::IsOpeningInteractInReach(280.f));
	TestFalse(TEXT("past 280 cm does not perch"), AHomeWorldCharacter::IsOpeningInteractInReach(281.f));

	TestTrue(TEXT("the box is centered on the screen"),
		AHomeWorldCharacter::IsOpeningLookInside(0.f, 0.f, 0.f));
	TestTrue(TEXT("a target at the box edge still locks"),
		AHomeWorldCharacter::IsOpeningLookInside(0.f, 0.3f, 0.f));
	TestFalse(TEXT("outside the passed box does not lock"),
		AHomeWorldCharacter::IsOpeningLookInside(0.f, 0.31f, 0.f));
	TestFalse(TEXT("outside the passed box horizontally does not lock"),
		AHomeWorldCharacter::IsOpeningLookInside(0.31f, 0.f, 0.f));
	TestTrue(TEXT("in front of the body can lock"),
		AHomeWorldCharacter::IsInFrontOfBody(FVector(1.f, 0.f, 0.f), FVector(1.f, 0.f, 0.f)));
	TestFalse(TEXT("behind the body does not lock"),
		AHomeWorldCharacter::IsInFrontOfBody(FVector(1.f, 0.f, 0.f), FVector(-1.f, 0.f, 0.f)));

	TArray<FOpeningLookCandidate> None;
	TestTrue(TEXT("nothing in reach leaves the wisp home"),
		AHomeWorldCharacter::PickOpeningLookTarget(OffLook, None) == nullptr);

	TArray<FOpeningLookCandidate> Both;
	Both.Add({OffLook, 0.64f});
	Both.Add({LookedAt, 0.01f});
	TestTrue(TEXT("the looked-at actor wins over a nearer one off the point"),
		AHomeWorldCharacter::PickOpeningLookTarget(nullptr, Both) == LookedAt);

	TArray<FOpeningLookCandidate> Held;
	Held.Add({LookedAt, 0.16f});
	Held.Add({OffLook, 0.1296f});
	TestTrue(TEXT("a slightly closer look takes the wisp at once"),
		AHomeWorldCharacter::PickOpeningLookTarget(LookedAt, Held) == OffLook);

	TArray<FOpeningLookCandidate> Taken;
	Taken.Add({LookedAt, 0.16f});
	Taken.Add({OffLook, 0.04f});
	TestTrue(TEXT("a clearly closer look takes the wisp"),
		AHomeWorldCharacter::PickOpeningLookTarget(LookedAt, Taken) == OffLook);

	TArray<FOpeningLookCandidate> Left;
	Left.Add({OffLook, 0.2f});
	TestTrue(TEXT("a perch that left range does not keep the wisp"),
		AHomeWorldCharacter::PickOpeningLookTarget(LookedAt, Left) == OffLook);
	return true;
}

#endif
