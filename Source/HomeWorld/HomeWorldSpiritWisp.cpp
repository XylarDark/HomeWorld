// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritWisp.h"
#include "HomeWorldSpiritHealComponent.h"
#include "Components/SceneComponent.h"

AHomeWorldSpiritWisp::AHomeWorldSpiritWisp()
{
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	HealComponent = CreateDefaultSubobject<UHomeWorldSpiritHealComponent>(TEXT("SpiritHeal"));

	Tags.AddUnique(FName(TEXT("SpiritWound")));
	Tags.AddUnique(FName(TEXT("SM_SpiritWound_01")));
}
