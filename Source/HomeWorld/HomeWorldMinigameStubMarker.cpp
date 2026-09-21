// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMinigameStubMarker.h"
#include "HomeWorldMinigameInteractComponent.h"
#include "Components/SceneComponent.h"

AHomeWorldMinigameStubMarker::AHomeWorldMinigameStubMarker()
{
	PrimaryActorTick.bCanEverTick = false;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	MinigameComponent = CreateDefaultSubobject<UHomeWorldMinigameInteractComponent>(TEXT("MinigameInteract"));
}

void AHomeWorldMinigameStubMarker::BeginPlay()
{
	Super::BeginPlay();
	if (MinigameComponent)
	{
		MinigameComponent->MinigameKind = MinigameKind;
	}
}
