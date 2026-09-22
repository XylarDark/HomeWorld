// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritNpcTorchCarrier.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "HomeWorldGameMode.h"

AHomeWorldSpiritNpcTorchCarrier::AHomeWorldSpiritNpcTorchCarrier()
{
	PrimaryActorTick.bCanEverTick = true;
	LitSourceKind = EHomeWorldSpiritLitSourceKind::NpcTorch;

	TorchMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TorchMesh"));
	TorchMesh->SetupAttachment(RootComponent);
	TorchMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	if (UStaticMesh* Cylinder = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder")))
	{
		TorchMesh->SetStaticMesh(Cylinder);
	}
	TorchMesh->SetRelativeScale3D(FVector(0.12f, 0.12f, 0.55f));
	TorchMesh->SetRelativeLocation(FVector(0.f, 0.f, 60.f));

	TorchLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("TorchLight"));
	TorchLight->SetupAttachment(TorchMesh);
	TorchLight->SetRelativeLocation(FVector(0.f, 0.f, 55.f));
	TorchLight->SetIntensity(2200.f);
	TorchLight->SetAttenuationRadius(420.f);
	TorchLight->SetLightColor(FLinearColor(1.f, 0.62f, 0.28f));
	TorchLight->SetCastShadows(false);

	LabelText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("LabelText"));
	LabelText->SetupAttachment(RootComponent);
	LabelText->SetHorizontalAlignment(EHTA_Center);
	LabelText->SetVerticalAlignment(EVRTA_TextCenter);
	LabelText->SetWorldSize(24.f);
	LabelText->SetRelativeLocation(FVector(0.f, 0.f, 175.f));
	LabelText->SetText(FText::FromString(TEXT("NPC TORCH")));
	LabelText->SetTextRenderColor(FColor(255, 210, 140));

	Tags.AddUnique(FName(TEXT("SS_NpcTorchCarrier")));
}

void AHomeWorldSpiritNpcTorchCarrier::BeginPlay()
{
	Super::BeginPlay();
	PatrolOrigin = GetActorLocation();
	if (PatrolAxis.IsNearlyZero())
	{
		PatrolAxis = FVector(1.f, 0.f, 0.f);
	}
	PatrolAxis = PatrolAxis.GetSafeNormal();
	UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: NPC torch carrier %s patrol=%d"),
		*GetName(), bPatrolEnabled ? 1 : 0);
}

void AHomeWorldSpiritNpcTorchCarrier::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	if (!bPatrolEnabled || PatrolHalfLength <= KINDA_SMALL_NUMBER)
	{
		return;
	}
	PatrolPhase += DeltaTime * PatrolSpeed;
	const float Offset = FMath::Sin(PatrolPhase) * PatrolHalfLength;
	SetActorLocation(PatrolOrigin + PatrolAxis * Offset, false, nullptr, ETeleportType::TeleportPhysics);
}
