// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldResourcePile.h"
#include "Components/BoxComponent.h"

AHomeWorldResourcePile::AHomeWorldResourcePile()
{
	PrimaryActorTick.bCanEverTick = false;

	OverlapVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("OverlapVolume"));
	OverlapVolume->SetBoxExtent(FVector(50.0f, 50.0f, 50.0f));
	OverlapVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	RootComponent = OverlapVolume;

	Tags.Add(FName("ResourcePile"));
}
