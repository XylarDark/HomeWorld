// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMainMenuWidget.h"
#include "HomeWorldGameInstance.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/PlayerController.h"

void UHomeWorldMainMenuWidget::NativeConstruct()
{
	Super::NativeConstruct();
}

void UHomeWorldMainMenuWidget::OnPlayClicked()
{
	UHomeWorldGameInstance* GI = GetHomeWorldGameInstance();
	if (GI)
	{
		GI->OpenGameMap();
	}
}

void UHomeWorldMainMenuWidget::OnCharacterClicked()
{
	UHomeWorldGameInstance* GI = GetHomeWorldGameInstance();
	if (GI)
	{
		GI->OpenCharacterScreen();
	}
}

void UHomeWorldMainMenuWidget::OnOptionsClicked()
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Main menu Options clicked (stub; override in Blueprint for options panel)."));
}

void UHomeWorldMainMenuWidget::OnQuitClicked()
{
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		PC->ConsoleCommand(TEXT("quit"));
	}
}

UHomeWorldGameInstance* UHomeWorldMainMenuWidget::GetHomeWorldGameInstance() const
{
	UWorld* World = GetWorld();
	if (!World) return nullptr;

	return Cast<UHomeWorldGameInstance>(World->GetGameInstance());
}
