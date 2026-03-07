// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameInstance.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/SoftObjectPtr.h"

void UHomeWorldGameInstance::Init()
{
	Super::Init();

	// Defaults if not set in Blueprint/config
	if (GameMapPath.IsNull())
	{
		GameMapPath = FSoftObjectPath(TEXT("/Game/HomeWorld/Maps/DemoMap.DemoMap"));
	}
	if (MainMenuMapName.IsEmpty())
	{
		MainMenuMapName = TEXT("MainMenu");
	}
	// Resolve main menu widget class from config path if not set in Blueprint
	if (!MainMenuWidgetClass && !MainMenuWidgetClassPath.IsNull())
	{
		MainMenuWidgetClass = MainMenuWidgetClassPath.ResolveClass();
	}
	// Resolve character screen widget class from config if not set
	if (!CharacterScreenWidgetClass && !CharacterScreenWidgetClassPath.IsNull())
	{
		CharacterScreenWidgetClass = CharacterScreenWidgetClassPath.ResolveClass();
	}
}

bool UHomeWorldGameInstance::IsMainMenuMap() const
{
	UWorld* World = GetWorld();
	if (!World) return false;

	FString MapName = World->GetMapName();
	return MapName.Contains(MainMenuMapName);
}

void UHomeWorldGameInstance::OpenGameMap()
{
	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: OpenGameMap failed - no World"));
		return;
	}

	FString MapPath = GameMapPath.ToString();
	if (MapPath.IsEmpty())
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: OpenGameMap failed - GameMapPath not set"));
		return;
	}

	// Strip asset name suffix for ServerTravel (e.g. /Game/HomeWorld/Maps/DemoMap.DemoMap -> DemoMap)
	FString MapName = GameMapPath.GetAssetName();
	UGameplayStatics::OpenLevel(this, FName(*MapName), true);
}

void UHomeWorldGameInstance::OpenCharacterScreen()
{
	APlayerController* PC = GetWorld() ? UGameplayStatics::GetPlayerController(GetWorld(), 0) : nullptr;
	if (!PC || !CharacterScreenWidgetClass)
	{
		return;
	}

	UUserWidget* Widget = CreateWidget<UUserWidget>(PC, CharacterScreenWidgetClass);
	if (Widget)
	{
		Widget->AddToViewport(1);
	}
}
