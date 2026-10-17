// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldParadoxToy.h"

AHomeWorldParadoxToy::AHomeWorldParadoxToy()
{
	PrimaryActorTick.bCanEverTick = false;
}

void AHomeWorldParadoxToy::ArmForDawn()
{
	bArmedForDawn = true;
}
