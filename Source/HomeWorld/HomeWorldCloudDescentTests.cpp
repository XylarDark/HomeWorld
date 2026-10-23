// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/CollisionProfile.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldCloud.h"
#include "HomeWorldCloudField.h"
#include "HomeWorldCloudWisp.h"
#include "HomeWorldGlideMovementComponent.h"
#include "HomeWorldTestWorld.h"
#include "HomeWorldTimeOfDaySubsystem.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentSteeringAndWispTest,
	"HomeWorld.Transit.CloudDescent.UnrestrictedSteeringAndWispCarry",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentSteeringAndWispTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	FActorSpawnParameters MarkerParams;
	MarkerParams.Name = FName(TEXT("GP_GlideStart"));
	MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AActor* Marker = Scope.World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, MarkerParams);
	if (!TestNotNull(TEXT("glider start marker"), Marker))
	{
		return false;
	}

	Character->GrantOpeningGliderForTest();
	TestTrue(TEXT("day/body launch starts active descent"), Character->TryStartCloudDescent());
	TestTrue(TEXT("descent is active"), Character->IsCloudDescentActive());

	// The descent is a glider, not a fall. Assert the real movement mode and class
	// rather than AirControl, which was the old free-fall stand-in.
	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}
	TestTrue(TEXT("launch enters the glide custom movement mode"), Glide->IsGliding());
	TestEqual(TEXT("custom movement mode is the glide mode"),
		Glide->CustomMovementMode, static_cast<uint8>(CMOVE_HW_Glide));
	// MOVEMENT_BIBLE: one CMC. The glide subclass must REPLACE the default, not join it.
	int32 MovementComponentCount = 0;
	for (const UActorComponent* Component : Character->GetComponents())
	{
		if (Component && Component->IsA<UCharacterMovementComponent>())
		{
			++MovementComponentCount;
		}
	}
	TestEqual(TEXT("still exactly one movement component"), MovementComponentCount, 1);

	// Developer decision 2026-10-05: uniform forward and sink across the descent;
	// 6× world-scale pass (Lead 2026-10-07) scales both speeds by ×6.
	TestEqual(TEXT("glide forward speed is 30 m/s"), Glide->GlideForwardSpeed, 3000.0f);
	// 30 s descent over the recorded 450 m drop.
	TestEqual(TEXT("glide sink rate is 15 m/s for a 30 s descent"), Glide->GlideSinkRate, 1500.0f);

	// A glide cannot hold altitude: no input grants vertical authority.
	const FVector Target = Glide->ComputeGlideTargetVelocity();
	TestEqual(TEXT("target descends at the sink rate"), Target.Z, -static_cast<double>(Glide->GlideSinkRate), 0.01);
	const double HorizontalMagnitude = FMath::Sqrt(Target.X * Target.X + Target.Y * Target.Y);
	TestTrue(TEXT("target keeps forward drive"), HorizontalMagnitude > 1.0);

	AHomeWorldCloudWisp* Wisp = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	if (!TestNotNull(TEXT("cloud wisp"), Wisp))
	{
		return false;
	}
	TestFalse(TEXT("day descent collects nothing"), Character->CollectCloudWisp(Wisp));
	TestEqual(TEXT("day descent carries no wisp"), Character->GetCarriedCloudWisps(), 0);
	TestTrue(TEXT("day descent sign is camp smoke"), Character->HasDayGlideSmokeSign());

	return true;
}

/**
 * The glide-to-walk handoff.
 *
 * The test world created by FScopedWorld is not physics-ticked, so this does NOT
 * simulate a drop. It covers the deterministic contract instead: the descent
 * hands control back through the engine's landing path, and the character clears
 * its descent state. Whether the glide actually reaches the ground from 450 m and
 * touches down on a real floor surface is a PIE question, not an automation one.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentLandingHandsBackControlTest,
	"HomeWorld.Transit.CloudDescent.LandingReturnsWalkControl",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentLandingHandsBackControlTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent landing"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	FActorSpawnParameters MarkerParams;
	MarkerParams.Name = FName(TEXT("GP_GlideStart"));
	MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	if (!TestNotNull(TEXT("glider start marker"),
		Scope.World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, MarkerParams)))
	{
		return false;
	}

	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}

	Character->GrantOpeningGliderForTest();
	if (!TestTrue(TEXT("day/body launch starts active descent"), Character->TryStartCloudDescent()))
	{
		return false;
	}
	TestTrue(TEXT("descent is gliding before landing"), Character->IsCloudDescentActive());
	TestTrue(TEXT("glide mode is active before landing"), Glide->IsGliding());

	// A glide must not leave horizontal authority behind in the CMC's falling state:
	// StopGlide is the escape hatch and must return to normal falling physics.
	Glide->StopGlide();
	TestFalse(TEXT("stopping the glide leaves glide mode"), Glide->IsGliding());
	TestEqual(TEXT("stopping the glide returns normal falling physics"),
		Glide->MovementMode, MOVE_Falling);

	// Landed() is the engine-side landing callback the glide CMC reaches via
	// ProcessLanded. Assert the character releases its descent state.
	Character->Landed(FHitResult());
	TestFalse(TEXT("landing clears the descent flag"), Character->IsCloudDescentActive());
	TestFalse(TEXT("landing leaves no active glide mode"), Glide->IsGliding());

	return true;
}

/**
 * Descent duration measured from the glide law, deterministically.
 *
 * HOMEWORLD_ROUTE.md records a 450 m drop and a 150 m bottom gap "that is a
 * placeholder until human testing" (6× world-scale pass, Lead 2026-10-07).
 * This advances the glide in fixed steps and
 * reports the time to reach ground so the developer has a number to compare a
 * playtest against.
 *
 * This measures the glide law (altitude over sink rate), NOT engine collision
 * response. It cannot catch a failed touchdown, so it does not replace flying
 * it. It is here to make the recorded placeholder falsifiable rather than to
 * stand in for the playtest.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentDurationMeasurementTest,
	"HomeWorld.Transit.CloudDescent.DurationMeasurement",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentDurationMeasurementTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent duration"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	FActorSpawnParameters MarkerParams;
	MarkerParams.Name = FName(TEXT("GP_GlideStart"));
	MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	if (!TestNotNull(TEXT("glider start marker"),
		Scope.World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, MarkerParams)))
	{
		return false;
	}

	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}

	Character->GrantOpeningGliderForTest();
	if (!TestTrue(TEXT("day/body launch starts active descent"), Character->TryStartCloudDescent()))
	{
		return false;
	}

	// Recorded route geometry: 450 m drop, of which 300 m is cloud layer and 150 m gap
	// (×6 world-scale pass, Lead 2026-10-07).
	const double DropCm = 45000.0;
	const double CloudLayerCm = 30000.0;
	const double GapCm = DropCm - CloudLayerCm;

	const float StepSeconds = 1.0f / 60.0f;
	const double SinkCmPerSecond = Glide->GlideSinkRate;

	// Advance the glide law until the drop is spent. Velocity convergence is
	// included so the first moments at reduced speed are counted honestly.
	FVector Velocity = Glide->Velocity;
	double Elapsed = 0.0;
	double Altitude = DropCm;
	double TimeToCloudBase = -1.0;

	while (Altitude > 0.0 && Elapsed < 600.0)
	{
		const FVector Target = Glide->ComputeGlideTargetVelocity();
		// Must mirror PhysCustom's interpolation exactly, or the measurement would
		// describe a glide the component does not actually fly.
		Velocity = FMath::VInterpTo(Velocity, Target, StepSeconds, Glide->GlideSteeringResponsiveness);
		Altitude += Velocity.Z * StepSeconds;
		Elapsed += StepSeconds;

		if (TimeToCloudBase < 0.0 && Altitude <= GapCm)
		{
			TimeToCloudBase = Elapsed;
		}
	}

	AddInfo(FString::Printf(
		TEXT("CLOUD_DESCENT duration: total=%.2f s, cloud layer=%.2f s, bottom gap=%.2f s")
		TEXT(" (450 m drop, %.0f cm/s sink, %.0f cm/s forward)"),
		Elapsed, TimeToCloudBase, Elapsed - TimeToCloudBase, SinkCmPerSecond, Glide->GlideForwardSpeed));

	// The glide must consume the drop rather than hang or climb. Guard the loop
	// rather than assert a duration: duration is the developer's to measure.
	TestTrue(TEXT("glide consumes the 450 m drop in a plausible time"), Elapsed > 1.0 && Elapsed < 120.0);
	TestTrue(TEXT("glide reaches ground (does not hang)"), Altitude <= 0.0);

	// The developer's 30 s decision, over the recorded 450 m drop. Asserted as a band
	// rather than an equality: velocity convergence adds a fixed startup offset that
	// is real behaviour, not error.
	TestTrue(TEXT("measured descent matches the developer's 30 s decision"),
		Elapsed > 29.0 && Elapsed < 32.0);

	// Sanity on the partition, which is pure arithmetic on recorded figures.
	TestTrue(TEXT("cloud layer accounts for most of the drop"), TimeToCloudBase > 0.0);
	TestTrue(TEXT("bottom gap time is positive"), (Elapsed - TimeToCloudBase) > 0.0);

	return true;
}

/**
 * CLOUDS_WISPS_V1 Source §5 / automation gate: the field builds 2+ layers
 * and 2+ clouds, every diameter is within 36-144 m, spacing sits in its
 * position band, the lowest cloud bottom is 150 m above ground, every cloud
 * sits entirely between 150 m and 450 m above ground, at least one wisp sits
 * on a cloud, and no cloud blocks the player pawn (overlap only).
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudFieldAutomationTest,
	"HomeWorld.Transit.CloudDescent.CloudField",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudFieldAutomationTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud field"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	const FVector SpawnLocation(750.0, 450.0, -7350.0);
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldCloudField* Field = Scope.World->SpawnActor<AHomeWorldCloudField>(SpawnLocation, FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("cloud field"), Field))
	{
		return false;
	}

	Field->BuildClouds();

	TestTrue(TEXT("field keeps placed transform"), Field->GetActorLocation().Equals(SpawnLocation, 1.0));
	TestTrue(TEXT("field builds at least 2 layers"), Field->GetLayerCount() >= 2);
	const TArray<AHomeWorldCloud*>& Clouds = Field->GetSpawnedClouds();
	TestTrue(TEXT("field builds at least 2 clouds"), Clouds.Num() >= 2);

	const double GroundZ = Field->GetActorLocation().Z;
	double LowestBottom = TNumericLimits<double>::Max();
	bool bAllDiametersInBand = true;
	bool bAllCloudsInsideBand = true;
	bool bNoneBlock = true;
	int32 WispCount = 0;

	for (AHomeWorldCloud* Cloud : Clouds)
	{
		const double Diameter = Cloud->GetDiameterCm();
		if (Diameter < 3600.0 || Diameter > 14400.0)
		{
			bAllDiametersInBand = false;
		}
		const double CenterZ = Cloud->GetActorLocation().Z;
		const double Bottom = CenterZ - Diameter * 0.5;
		const double Top = CenterZ + Diameter * 0.5;
		LowestBottom = FMath::Min(LowestBottom, Bottom - GroundZ);
		if (Bottom < GroundZ + 15000.0 - 1.0 || Top > GroundZ + 45000.0 + 1.0)
		{
			bAllCloudsInsideBand = false;
		}
		if (Cloud->GetSurfaceWisp())
		{
			++WispCount;
		}
		UStaticMeshComponent* Mesh = Cloud->GetVisualMesh();
		if (!Mesh
			|| Mesh->GetCollisionEnabled() != ECollisionEnabled::QueryOnly
			|| Mesh->GetCollisionResponseToChannel(ECC_Pawn) != ECR_Overlap)
		{
			bNoneBlock = false;
		}
	}

	TestTrue(TEXT("every diameter is within 36-144 m"), bAllDiametersInBand);
	TestTrue(TEXT("every cloud sits entirely between 150 m and 450 m above ground"), bAllCloudsInsideBand);
	TestTrue(TEXT("lowest cloud bottom is 150 m above ground"), FMath::Abs(LowestBottom - 15000.0) < 1.0);
	TestTrue(TEXT("lowest cloud bottom sits 15000 cm above the field's placed Z"),
		FMath::Abs((Field->GetActorLocation().Z + LowestBottom) - (SpawnLocation.Z + 15000.0)) < 1.0);
	TestTrue(TEXT("at least one wisp sits on a cloud"), WispCount >= 1);
	TestTrue(TEXT("no cloud blocks the player pawn (overlap only)"), bNoneBlock);

	// Spacing per position band (fact 2): top 3-4x, middle 1.5-2.5x, bottom 4-6x diameter.
	// Layers sorted by height, highest first; same row = same Y within the grid.
	TArray<const AHomeWorldCloud*> Sorted;
	Sorted.Reserve(Clouds.Num());
	for (AHomeWorldCloud* Cloud : Clouds)
	{
		Sorted.Add(Cloud);
	}
	Sorted.Sort([](const AHomeWorldCloud& A, const AHomeWorldCloud& B)
	{
		return A.GetActorLocation().Z > B.GetActorLocation().Z;
	});

	TMap<double, TArray<const AHomeWorldCloud*>> LayersByZ;
	for (const AHomeWorldCloud* Cloud : Sorted)
	{
		LayersByZ.FindOrAdd(FMath::RoundToDouble(Cloud->GetActorLocation().Z)).Add(Cloud);
	}
	TArray<double> Zs;
	LayersByZ.GetKeys(Zs);
	Zs.Sort([](double A, double B) { return A > B; });

	int32 SpacingPairsChecked = 0;
	bool bSpacingInBand = true;

	for (int32 LayerRank = 0; LayerRank < Zs.Num(); ++LayerRank)
	{
		const TArray<const AHomeWorldCloud*>& Layer = LayersByZ[Zs[LayerRank]];
		double BandMin = 4.0, BandMax = 6.0; // bottom by default
		if (LayerRank == 0)
		{
			BandMin = 3.0; BandMax = 4.0; // top
		}
		else if (LayerRank < Zs.Num() - 1)
		{
			BandMin = 1.5; BandMax = 2.5; // middle
		}

		TMap<double, TArray<const AHomeWorldCloud*>> Rows;
		for (const AHomeWorldCloud* Cloud : Layer)
		{
			Rows.FindOrAdd(FMath::RoundToDouble(Cloud->GetActorLocation().Y)).Add(Cloud);
		}
		for (auto& RowPair : Rows)
		{
			TArray<const AHomeWorldCloud*>& Row = RowPair.Value;
			Row.Sort([](const AHomeWorldCloud& A, const AHomeWorldCloud& B)
			{
				return A.GetActorLocation().X < B.GetActorLocation().X;
			});
			for (int32 Index = 1; Index < Row.Num(); ++Index)
			{
				const double Gap = FMath::Abs(Row[Index]->GetActorLocation().X - Row[Index - 1]->GetActorLocation().X);
				const double Diameter = Row[Index]->GetDiameterCm();
				const double FactorMultiple = Gap / Diameter;
				++SpacingPairsChecked;
				if (FactorMultiple < BandMin - 0.01 || FactorMultiple > BandMax + 0.01)
				{
					bSpacingInBand = false;
				}
			}
		}
	}

	TestTrue(TEXT("spacing measured on at least one cloud pair"), SpacingPairsChecked > 0);
	TestTrue(TEXT("spacing is within its position band"), bSpacingInBand);

	return true;
}

namespace HomeWorldGlideProbe
{
	extern int32 GCalls;
	extern int32 GDepth;
	extern int32 GMaxDepth;
}

/**
 * A glide that touches walkable ground inside one tick.
 *
 * PIE 2026-10-22 crashed with STACK_OVERFLOW: PhysCustom -> ProcessLanded ->
 * StartNewPhysics -> PhysCustom, forever (HomeWorldGlideMovementComponent.cpp:93).
 * ProcessLanded only switches to walking from MOVE_Falling, so from the custom glide
 * mode it restarted the glide with the whole tick. The move also passed Velocity
 * (one second of travel) instead of Velocity * DeltaTime.
 *
 * Part 1 ticks the glide once in open air and checks the move is one tick long.
 * Part 2 drops the body 10 cm above a floor and ticks once: it must land, walk,
 * and PhysCustom must never be on the stack twice. Part 2 is only run when part 1
 * passes, because the unscaled move overflows the stack and would take the editor
 * down with it.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FCloudDescentSameFrameLandingTest,
	"HomeWorld.Transit.CloudDescent.SameFrameLandingNoReentry",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FCloudDescentSameFrameLandingTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("cloud descent same-frame landing"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	FActorSpawnParameters MarkerParams;
	MarkerParams.Name = FName(TEXT("GP_GlideStart"));
	MarkerParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	if (!TestNotNull(TEXT("glider start marker"),
		Scope.World->SpawnActor<AActor>(FVector(0.f, 0.f, -100000.f), FRotator::ZeroRotator, MarkerParams)))
	{
		return false;
	}

	UHomeWorldGlideMovementComponent* Glide =
		Cast<UHomeWorldGlideMovementComponent>(Character->GetCharacterMovement());
	if (!TestNotNull(TEXT("character owns the glide CMC subclass"), Glide))
	{
		return false;
	}

	Character->GrantOpeningGliderForTest();
	if (!TestTrue(TEXT("launch starts the glide"), Character->TryStartCloudDescent())
		|| !TestTrue(TEXT("glide mode is active"), Glide->IsGliding()))
	{
		return false;
	}

	const float Step = 1.f / 60.f;

	// Part 1: one tick in open air.
	Character->SetActorLocation(FVector(0.f, 0.f, 20000.f), false, nullptr, ETeleportType::TeleportPhysics);
	Glide->Velocity = Glide->ComputeGlideTargetVelocity();
	const FVector AirStart = Character->GetActorLocation();
	HomeWorldGlideProbe::GCalls = 0;
	HomeWorldGlideProbe::GMaxDepth = 0;
	Glide->StartNewPhysics(Step, 0);
	const double AirMoved = FVector::Dist(AirStart, Character->GetActorLocation());
	const double OneTick = Glide->Velocity.Size() * Step;
	AddInfo(FString::Printf(TEXT("GLIDE_AIR_TICK moved=%.1f cm one_tick=%.1f cm speed=%.0f cm/s dt=%.4f s calls=%d max_depth=%d"),
		AirMoved, OneTick, Glide->Velocity.Size(), Step, HomeWorldGlideProbe::GCalls, HomeWorldGlideProbe::GMaxDepth));
	const bool bScaled = TestTrue(TEXT("a glide tick moves velocity times delta time"), AirMoved <= OneTick * 1.5 + 1.0);
	TestTrue(TEXT("the air tick keeps gliding"), Glide->IsGliding());
	if (!bScaled)
	{
		AddError(TEXT("same-frame landing not run: an unscaled glide move re-enters PhysCustom through ProcessLanded until the stack overflows"));
		return false;
	}

	// Part 2: walkable floor 10 cm under the capsule; one tick sinks 25 cm.
	FActorSpawnParameters FloorParams;
	FloorParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AStaticMeshActor* Floor = Scope.World->SpawnActor<AStaticMeshActor>(FVector::ZeroVector, FRotator::ZeroRotator, FloorParams);
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!TestNotNull(TEXT("floor"), Floor) || !TestNotNull(TEXT("cube mesh"), Cube))
	{
		return false;
	}
	UStaticMeshComponent* FloorMesh = Floor->GetStaticMeshComponent();
	FloorMesh->SetMobility(EComponentMobility::Movable);
	FloorMesh->SetStaticMesh(Cube);
	FloorMesh->SetCollisionProfileName(UCollisionProfile::BlockAll_ProfileName);
	Floor->SetActorScale3D(FVector(40.f, 40.f, 1.f));
	const float FloorTop = 50.f;
	const float Half = Character->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
	Character->SetActorLocation(FVector(0.f, 0.f, FloorTop + Half + 10.f), false, nullptr, ETeleportType::TeleportPhysics);
	Glide->Velocity = Glide->ComputeGlideTargetVelocity();
	HomeWorldGlideProbe::GCalls = 0;
	HomeWorldGlideProbe::GMaxDepth = 0;
	Glide->StartNewPhysics(Step, 0);
	const FVector Landed = Character->GetActorLocation();
	AddInfo(FString::Printf(TEXT("GLIDE_LAND_TICK calls=%d max_depth=%d mode=%d gliding=%d z=%.1f floor_stand_z=%.1f descent=%d"),
		HomeWorldGlideProbe::GCalls, HomeWorldGlideProbe::GMaxDepth, static_cast<int32>(Glide->MovementMode.GetValue()),
		Glide->IsGliding() ? 1 : 0, Landed.Z, FloorTop + Half, Character->IsCloudDescentActive() ? 1 : 0));
	TestEqual(TEXT("PhysCustom is never on the stack twice"), HomeWorldGlideProbe::GMaxDepth, 1);
	TestEqual(TEXT("PhysCustom runs once for the landing tick"), HomeWorldGlideProbe::GCalls, 1);
	TestFalse(TEXT("the landing leaves glide mode"), Glide->IsGliding());
	TestEqual(TEXT("the landing hands back walking"),
		static_cast<int32>(Glide->MovementMode.GetValue()), static_cast<int32>(MOVE_Walking));
	TestFalse(TEXT("the landing clears the descent"), Character->IsCloudDescentActive());
	TestTrue(TEXT("the body ends standing on the floor"), FMath::Abs(Landed.Z - (FloorTop + Half)) < 5.0);
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
