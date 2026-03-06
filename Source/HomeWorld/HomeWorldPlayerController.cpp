// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlayerController.h"
#include "HomeWorldHUD.h"
#include "Engine/World.h"

AHomeWorldPlayerController::AHomeWorldPlayerController()
{
}

void AHomeWorldPlayerController::SpawnDefaultHUD()
{
	UWorld* World = GetWorld();
	if (!World) return;

	FActorSpawnParameters Params;
	Params.Owner = this;
	AHUD* HUD = World->SpawnActor<AHomeWorldHUD>(AHomeWorldHUD::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, Params);
	if (HUD)
	{
		MyHUD = HUD;
	}
}
