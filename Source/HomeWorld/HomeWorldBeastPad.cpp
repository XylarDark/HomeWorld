// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBeastPad.h"
#include "HomeWorldBeastTameComponent.h"
#include "Components/SceneComponent.h"

AHomeWorldBeastPad::AHomeWorldBeastPad()
{
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	TameComponent = CreateDefaultSubobject<UHomeWorldBeastTameComponent>(TEXT("BeastTame"));

	Tags.AddUnique(FName(TEXT("BeastPad")));
	Tags.AddUnique(FName(TEXT("SM_BeastPad_01")));
}
