// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldStoreProp.h"
#include "Components/SceneComponent.h"

AHomeWorldStoreProp::AHomeWorldStoreProp()
{
	PrimaryActorTick.bCanEverTick = false;
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);
	StoreComponent = CreateDefaultSubobject<UHomeWorldStoreTransferComponent>(TEXT("StoreTransfer"));
	Tags.Add(FName("StoreProp"));
}
