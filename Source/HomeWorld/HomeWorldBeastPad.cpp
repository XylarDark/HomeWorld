// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBeastPad.h"
#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldBeastEncounterComponent.h"
#include "Components/SceneComponent.h"

AHomeWorldBeastPad::AHomeWorldBeastPad()
{
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	TameComponent = CreateDefaultSubobject<UHomeWorldBeastTameComponent>(TEXT("BeastTame"));

	// Lead 2026-10-07 charge-and-boot threat rules (route): threat meter, herb
	// suppression, tame window, inverse turn authority. See
	// HomeWorldBeastEncounterComponent.h.
	CreateDefaultSubobject<UHomeWorldBeastEncounterComponent>(TEXT("BeastEncounter"));

	Tags.AddUnique(FName(TEXT("BeastPad")));
	Tags.AddUnique(FName(TEXT("SM_BeastPad_01")));
}
