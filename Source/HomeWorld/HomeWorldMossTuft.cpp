// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMossTuft.h"

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"

AHomeWorldMossTuft::AHomeWorldMossTuft()
{
	PrimaryActorTick.bCanEverTick = false;
	UStaticMeshComponent* Tuft = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Tuft"));
	SetRootComponent(Tuft);
	Tuft->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Tuft->SetRelativeScale3D(FVector(0.2f, 0.2f, 0.08f));
	if (UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
	{
		Tuft->SetStaticMesh(Cube);
	}
	if (UMaterialInterface* Olive = LoadObject<UMaterialInterface>(
		nullptr, TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Olive.MI_Greybox_Olive")))
	{
		Tuft->SetMaterial(0, Olive);
	}
}

void AHomeWorldMossTuft::SetSource(FName NewSource)
{
	Source = NewSource;
}

bool AHomeWorldMossTuft::IsForestSource() const
{
	return Source == TEXT("tree") || Source == TEXT("rock");
}

void AHomeWorldMossTuft::MarkGathered()
{
	bGathered = true;
}
