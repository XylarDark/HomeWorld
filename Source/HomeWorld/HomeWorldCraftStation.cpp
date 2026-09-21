// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCraftStation.h"
#include "Components/BoxComponent.h"
#include "Components/SceneComponent.h"

AHomeWorldCraftStation::AHomeWorldCraftStation()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	InteractVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("InteractVolume"));
	InteractVolume->SetupAttachment(Root);
	InteractVolume->SetBoxExtent(FVector(80.f, 80.f, 60.f));
	InteractVolume->SetCollisionProfileName(TEXT("OverlapAllDynamic"));
	InteractVolume->SetGenerateOverlapEvents(false);

	Tags.AddUnique(FName(TEXT("CraftStation")));
}
