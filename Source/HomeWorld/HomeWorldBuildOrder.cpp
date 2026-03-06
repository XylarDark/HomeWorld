// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBuildOrder.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Logging/LogMacros.h"

DEFINE_LOG_CATEGORY_STATIC(LogBuildOrder, Log, All);

AHomeWorldBuildOrder::AHomeWorldBuildOrder()
{
	PrimaryActorTick.bCanEverTick = false;

	OverlapVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("OverlapVolume"));
	OverlapVolume->SetBoxExtent(FVector(50.0f, 50.0f, 50.0f));
	OverlapVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	RootComponent = OverlapVolume;

	Tags.Add(FName("BuildOrder"));
}

void AHomeWorldBuildOrder::CompleteBuildOrder()
{
	if (bBuildCompleted)
	{
		UE_LOG(LogBuildOrder, Verbose, TEXT("Build order already completed: %s"), *GetName());
		return;
	}
	bBuildCompleted = true;
	UE_LOG(LogBuildOrder, Log, TEXT("HomeWorld: Build order completed (%s, BuildDefinitionID=%s). Hologram can be hidden / final mesh shown in Blueprint."),
		*GetName(), *BuildDefinitionID.ToString());
}
