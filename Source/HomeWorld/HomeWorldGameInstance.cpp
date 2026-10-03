// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameInstance.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/SoftObjectPtr.h"
#include "Misc/PackageName.h"

void UHomeWorldGameInstance::Init()
{
	Super::Init();

	// Defaults if not set in Blueprint/config
	if (GameMapPath.IsNull())
	{
		// L_VS_MVP_Markers is the only level holding the homestead, the CRUMB_*
		// glide path, and the field below the island. The previous default,
		// DemoMap, has never existed in Content, so Play opened nothing.
		GameMapPath = FSoftObjectPath(TEXT("/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.L_VS_MVP_Markers"));
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: GameMapPath defaulted to %s"), *GameMapPath.ToString());
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

	// Strip asset name suffix for travel (e.g. /Game/.../L_VS_MVP_Markers.L_VS_MVP_Markers
	// -> L_VS_MVP_Markers). The trailing "." form is what GameDefaultMap in
	// DefaultEngine.ini uses; GetAssetName gives us the bare name for both.
	//
	// Resolve first and complain loudly if the target is not in the asset
	// registry. OpenLevel to a missing map is a silent no-op in a packaged
	// build and a confusing one in-editor -- which is exactly how DemoMap
	// survived as the default for so long.
	const FString MapName = GameMapPath.GetAssetName();
	const FString ObjectPath = GameMapPath.ToString();

	if (!FPackageName::DoesPackageExist(ObjectPath))
	{
		UE_LOG(LogTemp, Error,
			TEXT("HomeWorld: OpenGameMap target does not exist: %s")
			TEXT(" -- Play will go nowhere. Set GameMapPath on BP_GameInstance ")
			TEXT("or [/Script/HomeWorld.HomeWorldGameInstance] in DefaultGame.ini."),
			*ObjectPath);
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: OpenGameMap -> %s"), *ObjectPath);
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
