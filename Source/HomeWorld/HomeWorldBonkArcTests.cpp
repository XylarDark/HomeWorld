// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "CollisionShape.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "GameFramework/SpringArmComponent.h"
#include "HomeWorldBonkArc.h"
#include "HomeWorldTestWorld.h"

namespace
{
	const FVector GPadOrigin(0.f, 0.f, 45000.f);
	const FVector GPadExtent(5000.f, 7000.f, 50.f);
	const float GHalf = 90.f;
	const float GRadius = 40.f;
	const float GStandingZ = 45140.f;

	float MeasureSpringArmCm(USpringArmComponent* Boom)
	{
		Boom->TickComponent(0.016f, LEVELTICK_All, nullptr);
		const FVector ArmOrigin = Boom->GetComponentLocation() + Boom->TargetOffset;
		return FVector::Dist(Boom->GetSocketLocation(USpringArmComponent::SocketName), ArmOrigin);
	}

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

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkReentryTest,
	"HomeWorld.Opening.BonkReentry",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkReentryTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("bonk reentry"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) || !Character->GetCapsuleComponent())
	{
		return false;
	}

	const FVector PadOrigin(0.f, 0.f, 45000.f);
	const FVector PadExtent(5000.f, 7000.f, 50.f);
	const FVector From(-8000.f, 0.f, 44700.f);
	const FVector FirstTarget(-5000.f, 0.f, 45140.f);
	const FVector SecondTarget(5000.f, 1200.f, 45140.f);
	const float Half = Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
	const FVector SecondExpected = HomeWorldBonk::LandingOnPad(SecondTarget, PadOrigin, PadExtent, Half);

	Character->SetActorLocation(From);
	if (!TestEqual(TEXT("the body starts off the pad"), Character->GetActorLocation(), From, 1.f))
	{
		return false;
	}
	Character->BeginBonkReturn(FirstTarget, PadOrigin, PadExtent);
	if (!TestTrue(TEXT("the return started"), Character->IsBonkReturning()))
	{
		return false;
	}

	const HomeWorldBonk::FArc Arc = Character->BonkArc;
	TestEqual(TEXT("the arc starts at the body"), Arc.From, From, 1.f);
	TestTrue(TEXT("the second target would land somewhere else"), !Arc.Land.Equals(SecondExpected, 1.f));

	const float Partial = Arc.DurationSec * 0.4f;
	Character->TickBonkReturn(Partial);
	const float Elapsed = Character->BonkElapsed;
	const FVector Mid = Character->GetActorLocation();
	TestEqual(TEXT("the clock is part way"), Elapsed, Partial);
	TestTrue(TEXT("the flight left the start"), !Mid.Equals(From, 1.f));
	TestTrue(TEXT("the return is still in the air"), Character->IsBonkReturning());

	Character->BeginBonkReturn(SecondTarget, PadOrigin, PadExtent);
	TestEqual(TEXT("the landing stayed on the first target"), Character->BonkArc.Land, Arc.Land, 0.1f);
	TestEqual(TEXT("the climb stayed on the first arc"), Character->BonkArc.Approach, Arc.Approach, 0.1f);
	TestEqual(TEXT("the clock did not restart"), Character->BonkElapsed, Elapsed);
	TestEqual(TEXT("the body stayed where the first flight left it"), Character->GetActorLocation(), Mid, 0.1f);
	TestTrue(TEXT("the return is still in flight"), Character->IsBonkReturning());

	const float More = 0.05f;
	Character->TickBonkReturn(More);
	const float T = FMath::Clamp((Elapsed + More) / FMath::Max(Arc.DurationSec, 0.05f), 0.f, 1.f);
	TestEqual(TEXT("the flight stayed on the first arc"),
		Character->GetActorLocation(), HomeWorldBonk::PointOnArc(Arc, T), 1.f);
	TestTrue(TEXT("the clock kept going"), Character->BonkElapsed > Elapsed + 0.04f);

	Character->TickBonkReturn(Arc.DurationSec);
	TestEqual(TEXT("the flight lands on the first target"), Character->GetActorLocation(), Arc.Land, 1.f);
	TestTrue(TEXT("the flight does not land on the second target"),
		!Character->GetActorLocation().Equals(SecondExpected, 50.f));
	TestTrue(TEXT("the return has finished"), !Character->IsBonkReturning());

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkCameraTest,
	"HomeWorld.Opening.BonkCamera",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkCameraTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	// The swoop teleports the body through the cabin. A camera probe that starts
	// inside a blocker is a zero-length hit, and the stock arm then sits on the
	// pawn. A hit in front of the same box still shortens.
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("bonk camera"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SetActorLocation(FVector(1000.f, 200.f, 300.f));
	Character->SetActorRotation(FRotator::ZeroRotator);

	USpringArmComponent* Boom = Character->FindComponentByClass<USpringArmComponent>();
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!TestNotNull(TEXT("boom"), Boom) || !TestNotNull(TEXT("cube"), Cube))
	{
		return false;
	}
	TestTrue(TEXT("the probe is on"), Boom->bDoCollisionTest);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AStaticMeshActor* Wall = Scope.World->SpawnActor<AStaticMeshActor>(
		Character->GetActorLocation(), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("cabin box"), Wall) || !Wall->GetStaticMeshComponent())
	{
		return false;
	}
	UStaticMeshComponent* Mesh = Wall->GetStaticMeshComponent();
	Mesh->SetStaticMesh(Cube);
	Mesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	Mesh->SetCollisionObjectType(ECC_WorldStatic);
	Mesh->SetCollisionResponseToAllChannels(ECR_Block);
	Wall->SetActorScale3D(FVector(4.f));
	Wall->SetActorLocation(Character->GetActorLocation());
	Mesh->RecreatePhysicsState();

	FCollisionQueryParams QueryParams(NAME_None, false, Character);
	const float Probe = Boom->ProbeSize;
	const FVector InsideStart = Boom->GetComponentLocation() + Boom->TargetOffset;
	const FVector InsideEnd = InsideStart - Character->GetViewRotation().Vector() * Boom->TargetArmLength;
	FHitResult InsideHit;
	const bool bInside = Scope.World->SweepSingleByChannel(
		InsideHit,
		InsideStart,
		InsideEnd,
		FQuat::Identity,
		Boom->ProbeChannel,
		FCollisionShape::MakeSphere(Probe),
		QueryParams);
	if (!TestTrue(TEXT("the box blocks a probe that starts inside it"),
		bInside && (InsideHit.bStartPenetrating || InsideHit.Distance <= 1.f)))
	{
		return false;
	}

	const float InsideArm = MeasureSpringArmCm(Boom);
	TestTrue(TEXT("the arm stays at its flight length inside the box"),
		FMath::IsNearlyEqual(InsideArm, Boom->TargetArmLength, 1.f));

	// Engine cube is 100 cm. Scale 4 makes a 400 cm box, so the +X face is 200 cm out.
	const float Gap = 80.f;
	const float HalfExtent = 50.f * Wall->GetActorScale3D().X;
	Character->SetActorLocation(Wall->GetActorLocation() + FVector(HalfExtent + Gap, 0.f, 0.f));
	Character->SetActorRotation(FRotator::ZeroRotator);
	const FVector OutsideStart = Boom->GetComponentLocation() + Boom->TargetOffset;
	const FVector OutsideEnd = OutsideStart - Character->GetViewRotation().Vector() * Boom->TargetArmLength;
	FHitResult OutsideHit;
	const bool bOutside = Scope.World->SweepSingleByChannel(
		OutsideHit,
		OutsideStart,
		OutsideEnd,
		FQuat::Identity,
		Boom->ProbeChannel,
		FCollisionShape::MakeSphere(Probe),
		QueryParams);
	if (!TestTrue(TEXT("the wall still stops the probe"), bOutside && !OutsideHit.bStartPenetrating))
	{
		return false;
	}

	const float WalkArm = MeasureSpringArmCm(Boom);
	TestTrue(TEXT("walking keeps the shortened arm"), FMath::IsNearlyEqual(WalkArm, OutsideHit.Distance, 3.f));
	TestTrue(TEXT("walking does not sit on the body"), WalkArm > 20.f);
	TestTrue(TEXT("walking does not keep the full arm through the wall"), WalkArm < Boom->TargetArmLength - 20.f);
	return true;
}

namespace
{
	struct FBonkBlock
	{
		AStaticMeshActor* Actor = nullptr;
		FVector Center = FVector::ZeroVector;
		FVector Extent = FVector::ZeroVector;
		float Top = 0.f;
	};

	FBonkBlock SpawnBonkBlock(UWorld* World, UStaticMesh* Cube, const FVector& Location, const FVector& Scale)
	{
		FBonkBlock Block;
		if (!World || !Cube)
		{
			return Block;
		}
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* Actor = World->SpawnActor<AStaticMeshActor>(Location, FRotator::ZeroRotator, Params);
		if (!Actor || !Actor->GetStaticMeshComponent())
		{
			return Block;
		}
		UStaticMeshComponent* Mesh = Actor->GetStaticMeshComponent();
		Mesh->SetStaticMesh(Cube);
		Mesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		Mesh->SetCollisionObjectType(ECC_WorldStatic);
		Mesh->SetCollisionResponseToAllChannels(ECR_Block);
		Actor->SetActorScale3D(Scale);
		Actor->SetActorLocation(Location);
		Mesh->RecreatePhysicsState();
		FVector Origin = FVector::ZeroVector;
		FVector Extent = FVector::ZeroVector;
		Actor->GetActorBounds(true, Origin, Extent);
		Block.Actor = Actor;
		Block.Center = Origin;
		Block.Extent = Extent;
		Block.Top = Origin.Z + Extent.Z;
		return Block;
	}

	bool SegmentClearsBlock(
		const FVector& A,
		const FVector& B,
		const FBonkBlock& Block,
		float Half,
		float Radius,
		float Margin,
		bool& bCrossed)
	{
		const int32 Steps = FMath::Max(FMath::CeilToInt(FVector::Dist(A, B) / 25.f), 1);
		for (int32 Step = 0; Step <= Steps; ++Step)
		{
			const FVector Point = FMath::Lerp(A, B, static_cast<float>(Step) / static_cast<float>(Steps));
			const float Dx = FMath::Max(FMath::Abs(Point.X - Block.Center.X) - Block.Extent.X, 0.f);
			const float Dy = FMath::Max(FMath::Abs(Point.Y - Block.Center.Y) - Block.Extent.Y, 0.f);
			if (Dx * Dx + Dy * Dy > Radius * Radius)
			{
				continue;
			}
			bCrossed = true;
			if (Point.Z - Half < Block.Top + Margin - 1.5f)
			{
				return false;
			}
		}
		return true;
	}

	bool ArcClearsBlock(
		const HomeWorldBonk::FArc& Arc,
		const FBonkBlock& Block,
		float Half,
		float Radius,
		float Margin,
		bool& bCrossed)
	{
		bCrossed = false;
		if (!SegmentClearsBlock(Arc.From, Arc.Approach, Block, Half, Radius, Margin, bCrossed))
		{
			return false;
		}
		if (Arc.bDrop
			&& !SegmentClearsBlock(Arc.Approach, Arc.Drop, Block, Half, Radius, Margin, bCrossed))
		{
			return false;
		}
		const FVector Drop = Arc.bDrop ? Arc.Drop : Arc.Approach;
		if (!SegmentClearsBlock(Drop, Arc.Land, Block, Half, Radius, Margin, bCrossed))
		{
			return false;
		}
		return true;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBonkClearanceTest,
	"HomeWorld.Opening.BonkClearance",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBonkClearanceTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	TestTrue(TEXT("the clearance margin is one meter"),
		FMath::IsNearlyEqual(HomeWorldBonk::ClearanceMarginCm, 100.f, 0.01f));

	HomeWorldTestWorld::FScopedWorld Scope(TEXT("bonk clearance"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	const FVector PadOrigin(0.f, 0.f, 0.f);
	const FVector PadExtent(5000.f, 5000.f, 50.f);
	const float Half = 90.f;
	const float Radius = 40.f;
	const FVector From(-6000.f, 0.f, 80.f);
	const FVector Target(0.f, 0.f, 200.f);
	const FVector Expected = HomeWorldBonk::LandingOnPad(Target, PadOrigin, PadExtent, Half);
	const float Margin = HomeWorldBonk::ClearanceMarginCm;

	const HomeWorldBonk::FClearance Empty = HomeWorldBonk::MeasureClearance(
		Scope.World, From, Expected, Half, Radius, nullptr);
	const HomeWorldBonk::FArc Plain = HomeWorldBonk::MakeArc(
		From, Target, PadOrigin, PadExtent, Half, Radius);
	const HomeWorldBonk::FArc Same = HomeWorldBonk::MakeArc(
		From, Target, PadOrigin, PadExtent, Half, Radius, &Empty);
	TestFalse(TEXT("an empty corridor does not raise the arc"), Empty.bRaised);
	TestEqual(TEXT("a clear corridor keeps the crest point"), Same.Approach, Plain.Approach, 0.1f);
	TestEqual(TEXT("a clear corridor keeps the landing"), Same.Land, Expected, 0.1f);
	TestFalse(TEXT("a clear corridor does not drop steeply"), Same.bDrop);
	TestTrue(TEXT("the clear apex stays at the crest"),
		FMath::IsNearlyEqual(Same.Approach.Z, Same.Land.Z + HomeWorldBonk::CrestCm, 0.1f));

	HomeWorldBonk::FClearance Low;
	Low.bRaised = true;
	Low.ApexZ = Expected.Z;
	Low.ApproachT = 0.25f;
	Low.DropT = 0.75f;
	const HomeWorldBonk::FArc Held = HomeWorldBonk::MakeArc(
		From, Target, PadOrigin, PadExtent, Half, Radius, &Low);
	TestTrue(TEXT("a short blocker cannot pull the apex under the crest"),
		Held.Approach.Z >= Held.Land.Z + HomeWorldBonk::CrestCm - 0.1f
		&& Held.Drop.Z >= Held.Land.Z + HomeWorldBonk::CrestCm - 0.1f);
	TestEqual(TEXT("holding the crest still lands on the target"), Held.Land, Expected, 0.01f);

	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!TestNotNull(TEXT("cube"), Cube))
	{
		return false;
	}
	// Engine cube is 100 cm. The wall is the nearer, shorter block. The kettle
	// is closer to the pad and taller, so a crest in the middle would clip it
	// on the way down.
	const FBonkBlock Wall = SpawnBonkBlock(
		Scope.World, Cube, FVector(-2500.f, 0.f, 200.f), FVector(2.f, 4.f, 4.f));
	const FBonkBlock Kettle = SpawnBonkBlock(
		Scope.World, Cube, FVector(-400.f, 0.f, 400.f), FVector(3.f, 3.f, 8.f));
	if (!TestNotNull(TEXT("wall"), Wall.Actor) || !TestNotNull(TEXT("kettle"), Kettle.Actor))
	{
		return false;
	}
	TestTrue(TEXT("the wall top matches its scale"),
		FMath::IsNearlyEqual(Wall.Top, 400.f, 2.f));
	TestTrue(TEXT("the kettle top matches its scale"),
		FMath::IsNearlyEqual(Kettle.Top, 800.f, 2.f));
	TestTrue(TEXT("the kettle is the taller blocker"), Kettle.Top > Wall.Top);
	TestTrue(TEXT("the landing column misses both blocks"),
		FMath::Abs(Expected.X - Kettle.Center.X) > Kettle.Extent.X + Radius
		&& FMath::Abs(Expected.X - Wall.Center.X) > Wall.Extent.X + Radius);

	const HomeWorldBonk::FClearance Clearance = HomeWorldBonk::MeasureClearance(
		Scope.World, From, Expected, Half, Radius, nullptr);
	if (!TestTrue(TEXT("the sweep saw a blocker"), Clearance.bRaised))
	{
		return false;
	}
	const HomeWorldBonk::FArc Arc = HomeWorldBonk::MakeArc(
		From, Target, PadOrigin, PadExtent, Half, Radius, &Clearance);
	TestTrue(TEXT("the raised arc drops after the cruise"), Arc.bDrop);
	TestEqual(TEXT("the endpoint is the pad target"), Arc.Land, Expected, 0.01f);
	TestTrue(TEXT("the path ends on the landing"),
		HomeWorldBonk::PointOnArc(Arc, 1.f).Equals(Expected, 0.1f));
	TestTrue(TEXT("the path starts at the launch"),
		HomeWorldBonk::PointOnArc(Arc, 0.f).Equals(From, 0.1f));
	TestTrue(TEXT("the apex is not below the crest"),
		Arc.Approach.Z >= Arc.Land.Z + HomeWorldBonk::CrestCm - 0.1f
		&& Arc.Drop.Z >= Arc.Land.Z + HomeWorldBonk::CrestCm - 0.1f);
	TestTrue(TEXT("the apex clears the taller block"),
		Arc.Approach.Z >= Kettle.Top + Margin + Half - 1.f);
	TestTrue(TEXT("the cruise holds that apex"),
		FMath::IsNearlyEqual(Arc.Drop.Z, Arc.Approach.Z, 0.1f));

	bool bWallCrossed = false;
	bool bKettleCrossed = false;
	TestTrue(TEXT("the capsule bottom clears the wall"),
		ArcClearsBlock(Arc, Wall, Half, Radius, Margin, bWallCrossed));
	TestTrue(TEXT("the arc crosses the wall"), bWallCrossed);
	TestTrue(TEXT("the capsule bottom clears the kettle"),
		ArcClearsBlock(Arc, Kettle, Half, Radius, Margin, bKettleCrossed));
	TestTrue(TEXT("the arc crosses the kettle"), bKettleCrossed);

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) || !Character->GetCapsuleComponent())
	{
		return false;
	}
	Character->SetActorLocation(From, false, nullptr, ETeleportType::TeleportPhysics);
	Character->BeginBonkReturn(Target, PadOrigin, PadExtent);
	if (!TestTrue(TEXT("the return started"), Character->IsBonkReturning()))
	{
		return false;
	}
	const float BodyHalf = Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
	const float BodyRadius = Character->GetCapsuleComponent()->GetScaledCapsuleRadius();
	TestEqual(TEXT("the flight still lands on the pad target"), Character->BonkArc.Land, Expected, 0.1f);
	TestTrue(TEXT("the flight arc is raised"), Character->BonkArc.bDrop);
	TestTrue(TEXT("the flight apex is not below the crest"),
		Character->BonkArc.Approach.Z >= Character->BonkArc.Land.Z + HomeWorldBonk::CrestCm - 0.1f);

	bool bBodyWall = false;
	bool bBodyKettle = false;
	TestTrue(TEXT("the body clears the wall"),
		ArcClearsBlock(Character->BonkArc, Wall, BodyHalf, BodyRadius, Margin, bBodyWall) && bBodyWall);
	TestTrue(TEXT("the body clears the kettle on the way down"),
		ArcClearsBlock(Character->BonkArc, Kettle, BodyHalf, BodyRadius, Margin, bBodyKettle) && bBodyKettle);

	const float Partial = Character->BonkArc.DurationSec * 0.7f;
	Character->TickBonkReturn(Partial);
	const float T = FMath::Clamp(Partial / FMath::Max(Character->BonkArc.DurationSec, 0.05f), 0.f, 1.f);
	TestEqual(TEXT("the flight follows the clearance arc"),
		Character->GetActorLocation(), HomeWorldBonk::PointOnArc(Character->BonkArc, T), 1.f);
	TestTrue(TEXT("the return is still in the air"), Character->IsBonkReturning());
	return true;
}

#endif
