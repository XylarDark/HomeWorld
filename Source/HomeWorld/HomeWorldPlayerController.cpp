// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlayerController.h"
#include "HomeWorldHUD.h"
#include "HomeWorldGameInstance.h"
#include "Blueprint/UserWidget.h"
#include "Engine/World.h"

AHomeWorldPlayerController::AHomeWorldPlayerController()
{
}

void AHomeWorldPlayerController::BeginPlay()
{
	Super::BeginPlay();
	ShowMainMenuIfNeeded();
}

void AHomeWorldPlayerController::ShowMainMenuIfNeeded()
{
	UHomeWorldGameInstance* GI = GetWorld() ? Cast<UHomeWorldGameInstance>(GetWorld()->GetGameInstance()) : nullptr;
	if (!GI || !GI->IsMainMenuMap() || !GI->MainMenuWidgetClass)
	{
		return;
	}

	MainMenuWidget = CreateWidget<UUserWidget>(this, GI->MainMenuWidgetClass);
	if (MainMenuWidget)
	{
		MainMenuWidget->AddToViewport(0);
		SetInputMode(FInputModeUIOnly());
		bShowMouseCursor = true;
	}
}

void AHomeWorldPlayerController::RemoveMainMenuWidget()
{
	if (MainMenuWidget)
	{
		MainMenuWidget->RemoveFromParent();
		MainMenuWidget = nullptr;
	}
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
