// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

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
	TestTrue(TEXT("wisp collected during active descent"), Character->CollectCloudWisp(Wisp));
	TestEqual(TEXT("wisp remains in carried route state"), Character->GetCarriedCloudWisps(), 1);

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

#endif // WITH_DEV_AUTOMATION_TESTS
