// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldShrinePortalTrigger.h"
#include "HomeWorldShrinePortalComponent.h"

AHomeWorldShrinePortalTrigger::AHomeWorldShrinePortalTrigger()
{
	PrimaryActorTick.bCanEverTick = false;
	PortalComponent = CreateDefaultSubobject<UHomeWorldShrinePortalComponent>(TEXT("PortalComponent"));
	SetRootComponent(PortalComponent);
}
