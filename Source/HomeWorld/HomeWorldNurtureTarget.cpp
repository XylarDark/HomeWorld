// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldNurtureTarget.h"
#include "Components/SceneComponent.h"

AHomeWorldNurtureTarget::AHomeWorldNurtureTarget()
{
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	NurtureComponent = CreateDefaultSubobject<UHomeWorldNurtureComponent>(TEXT("Nurture"));
	NurtureComponent->SetupAttachment(Root);

	Tags.AddUnique(FName(TEXT("NurtureTarget")));
}
