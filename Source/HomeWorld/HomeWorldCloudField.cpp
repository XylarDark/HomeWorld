// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCloudField.h"

#include "HomeWorldCloud.h"
#include "HomeWorldCloudWisp.h"

AHomeWorldCloudField::AHomeWorldCloudField()
{
	PrimaryActorTick.bCanEverTick = false;
}

void AHomeWorldCloudField::BeginPlay()
{
	Super::BeginPlay();
	BuildClouds();
}

void AHomeWorldCloudField::BuildClouds()
{
	if (bBuilt)
	{
		return;
	}

	if (LayerHeightsCm.Num() < 2)
	{
		UE_LOG(LogTemp, Warning, TEXT("CLOUD_FIELD: needs at least 2 layer heights; field not built"));
		return;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	const double Diameter = FMath::Clamp(DiameterCm, 600.0, 2400.0);
	const double Radius = Diameter * 0.5;
	const double GroundZ = GetActorLocation().Z;
	const double BandMinCenterZ = GroundZ + 2500.0 + Radius; // lowest cloud bottom sits on the 25 m line
	const double BandMaxCenterZ = GroundZ + 7500.0 - Radius; // top of highest cloud inside the 75 m line

	// Layer indices ordered high to low: highest is top, lowest is bottom,
	// everything between is middle (route fact 2 spacing bands).
	TArray<int32> Order;
	Order.Reserve(LayerHeightsCm.Num());
	for (int32 Index = 0; Index < LayerHeightsCm.Num(); ++Index)
	{
		Order.Add(Index);
	}
	Order.Sort([this](int32 A, int32 B)
	{
		return LayerHeightsCm[A] > LayerHeightsCm[B];
	});

	const double ClampedTopFactor = FMath::Clamp(TopSpacingFactor, 3.0, 4.0);
	const double ClampedMiddleFactor = FMath::Clamp(MiddleSpacingFactor, 1.5, 2.5);
	const double ClampedBottomFactor = FMath::Clamp(BottomSpacingFactor, 4.0, 6.0);

	const int32 WispBudget = FMath::Max(0, WispCloudCount);
	int32 WispsPlaced = 0;

	for (int32 Rank = 0; Rank < Order.Num(); ++Rank)
	{
		const double Height = LayerHeightsCm[Order[Rank]];
		// The 25 m pin owns the lowest layer's Z; its LayerHeightsCm entry is ignored.
		const double CenterZ = (Rank == Order.Num() - 1)
			? BandMinCenterZ
			: FMath::Clamp(GroundZ + Height, BandMinCenterZ, BandMaxCenterZ);

		const double Factor = (Order.Num() == 1)
			? ClampedBottomFactor
			: (Rank == 0 ? ClampedTopFactor : (Rank == Order.Num() - 1 ? ClampedBottomFactor : ClampedMiddleFactor));
		const double Spacing = Factor * Diameter;

		int32 CountPerAxis = FMath::Max(1, FMath::RoundToInt(HorizontalExtentCm / Spacing));
		CountPerAxis = FMath::Clamp(CountPerAxis, 1, MaxCloudsPerAxis);

		for (int32 X = 0; X <= CountPerAxis; ++X)
		{
			for (int32 Y = 0; Y <= CountPerAxis; ++Y)
			{
				const FVector Location(
					GetActorLocation().X + (X - CountPerAxis * 0.5) * Spacing,
					GetActorLocation().Y + (Y - CountPerAxis * 0.5) * Spacing,
					CenterZ);

				FActorSpawnParameters Params;
				Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
				AHomeWorldCloud* Cloud = World->SpawnActor<AHomeWorldCloud>(Location, FRotator::ZeroRotator, Params);
				if (!Cloud)
				{
					continue;
				}
				Cloud->DiameterCm = Diameter;
				Cloud->bCarriesWisp = WispsPlaced < WispBudget;
				Cloud->SetOwner(this);
				Cloud->BuildVisuals();
				Cloud->EnsureSurfaceWisp();
				SpawnedClouds.Add(Cloud);
				if (Cloud->GetSurfaceWisp())
				{
					++WispsPlaced;
				}
			}
		}
	}

	bBuilt = true;
	UE_LOG(LogTemp, Log, TEXT("CLOUD_FIELD: built %d clouds on %d layers, %d surface wisps, extent=%.0f cm"),
		SpawnedClouds.Num(), LayerHeightsCm.Num(), WispsPlaced, HorizontalExtentCm);
}
