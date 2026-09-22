// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCraftStation.h"
#include "Components/BoxComponent.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"

namespace
{
	UStaticMesh* LoadBasicShape(const TCHAR* Path)
	{
		return LoadObject<UStaticMesh>(nullptr, Path);
	}

	const TCHAR* GetLabelForKind(EHomeWorldCraftStationKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldCraftStationKind::HubBootstrap:
			return TEXT("CRAFT HUB");
		case EHomeWorldCraftStationKind::Campfire:
			return TEXT("CAMPFIRE");
		case EHomeWorldCraftStationKind::TentPlaceable:
			return TEXT("TENT");
		case EHomeWorldCraftStationKind::Kitchen:
			return TEXT("KITCHEN");
		default:
			return TEXT("CRAFT");
		}
	}

	void ConfigureMeshForKind(UStaticMeshComponent* Mesh, EHomeWorldCraftStationKind Kind)
	{
		if (!Mesh)
		{
			return;
		}
		Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		switch (Kind)
		{
		case EHomeWorldCraftStationKind::HubBootstrap:
			Mesh->SetStaticMesh(LoadBasicShape(TEXT("/Engine/BasicShapes/Cylinder.Cylinder")));
			Mesh->SetRelativeScale3D(FVector(0.45f, 0.45f, 0.35f));
			break;
		case EHomeWorldCraftStationKind::Campfire:
			Mesh->SetStaticMesh(LoadBasicShape(TEXT("/Engine/BasicShapes/Cone.Cone")));
			Mesh->SetRelativeScale3D(FVector(0.55f, 0.55f, 0.7f));
			Mesh->SetRelativeLocation(FVector(0.f, 0.f, 35.f));
			break;
		case EHomeWorldCraftStationKind::TentPlaceable:
			Mesh->SetStaticMesh(LoadBasicShape(TEXT("/Engine/BasicShapes/Cube.Cube")));
			Mesh->SetRelativeScale3D(FVector(1.4f, 1.0f, 0.75f));
			Mesh->SetRelativeLocation(FVector(0.f, 0.f, 40.f));
			break;
		case EHomeWorldCraftStationKind::Kitchen:
			Mesh->SetStaticMesh(LoadBasicShape(TEXT("/Engine/BasicShapes/Cube.Cube")));
			Mesh->SetRelativeScale3D(FVector(0.6f, 0.6f, 0.5f));
			break;
		default:
			Mesh->SetStaticMesh(LoadBasicShape(TEXT("/Engine/BasicShapes/Sphere.Sphere")));
			Mesh->SetRelativeScale3D(FVector(0.35f));
			break;
		}
	}
}

AHomeWorldCraftStation::AHomeWorldCraftStation()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	VisualMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VisualMesh"));
	VisualMesh->SetupAttachment(Root);

	InteractVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("InteractVolume"));
	InteractVolume->SetupAttachment(Root);
	InteractVolume->SetBoxExtent(FVector(80.f, 80.f, 60.f));
	InteractVolume->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
	InteractVolume->SetGenerateOverlapEvents(false);

	LabelText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("LabelText"));
	LabelText->SetupAttachment(Root);
	LabelText->SetHorizontalAlignment(EHTA_Center);
	LabelText->SetVerticalAlignment(EVRTA_TextCenter);
	LabelText->SetWorldSize(22.f);
	LabelText->SetRelativeLocation(FVector(0.f, 0.f, 140.f));

	Tags.AddUnique(FName(TEXT("CraftStation")));
}

void AHomeWorldCraftStation::BeginPlay()
{
	Super::BeginPlay();
	RefreshDemoSpineVisuals();
}

void AHomeWorldCraftStation::RefreshDemoSpineVisuals()
{
	ConfigureMeshForKind(VisualMesh, StationKind);
	if (LabelText)
	{
		LabelText->SetText(FText::FromString(GetLabelForKind(StationKind)));
	}
}
