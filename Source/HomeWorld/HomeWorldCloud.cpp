// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCloud.h"

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "HomeWorldCloudWisp.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"

AHomeWorldCloud::AHomeWorldCloud()
{
	PrimaryActorTick.bCanEverTick = false;

	VisualMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VisualMesh"));
	SetRootComponent(VisualMesh);

	if (UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere")))
	{
		VisualMesh->SetStaticMesh(Sphere);
	}

	// Pass-through only: query overlap with the pawn, never block, never
	// something to stand on (CLOUDS_WISPS_V1 interview #3, 2A).
	VisualMesh->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	VisualMesh->SetCollisionObjectType(ECC_WorldDynamic);
	VisualMesh->SetCollisionResponseToAllChannels(ECR_Ignore);
	VisualMesh->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	VisualMesh->SetGenerateOverlapEvents(true);
}

void AHomeWorldCloud::BeginPlay()
{
	Super::BeginPlay();
	BuildVisuals();
	EnsureSurfaceWisp();
}

void AHomeWorldCloud::BuildVisuals()
{
	if (!VisualMesh)
	{
		return;
	}

	const double Diameter = GetDiameterCm();
	// Engine sphere primitive is 100 cm across at unit scale.
	VisualMesh->SetRelativeScale3D(FVector(Diameter / 100.0));

	// Runtime dynamic instance of the existing M_SpiritUnlit master; no new
	// material master and no .uasset from Source (packet Source §1).
	UMaterialInterface* Master = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Masters/M_SpiritUnlit.M_SpiritUnlit"));
	if (!Master)
	{
		UE_LOG(LogTemp, Warning, TEXT("CLOUD: M_SpiritUnlit master not loaded; cloud stays unshaded"));
		return;
	}
	UMaterialInstanceDynamic* DynamicMaterial = UMaterialInstanceDynamic::Create(Master, this);
	if (DynamicMaterial)
	{
		VisualMesh->SetMaterial(0, DynamicMaterial);
	}
}

AHomeWorldCloudWisp* AHomeWorldCloud::EnsureSurfaceWisp()
{
	if (!bCarriesWisp || SurfaceWisp || !GetWorld())
	{
		return SurfaceWisp;
	}
	if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = GetWorld()->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
	{
		if (!TimeOfDay->GetIsNight())
		{
			return nullptr;
		}
	}

	const double Radius = GetDiameterCm() * 0.5;
	const FVector SurfaceLocation = GetActorLocation() + FVector(0.0, Radius, 0.0);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	SurfaceWisp = GetWorld()->SpawnActor<AHomeWorldCloudWisp>(SurfaceLocation, GetActorRotation(), Params);
	if (SurfaceWisp)
	{
		SurfaceWisp->SetOwner(this);
		SurfaceWisp->AttachToComponent(GetRootComponent(), FAttachmentTransformRules::KeepWorldTransform);
		UE_LOG(LogTemp, Log, TEXT("CLOUD: surface wisp placed on cloud (diameter=%.0f cm)"), GetDiameterCm());
	}
	return SurfaceWisp;
}
