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

	// FPackageName::DoesPackageExist() is documented against a PACKAGE NAME
	// (/Game/Path/Map), while a SoftObjectPath stringifies to an OBJECT PATH
	// (/Game/Path/Map.Map). Whether the engine tolerates the object-path form is
	// not something to bet the Play button on -- if it does not, this guard
	// rejects a perfectly valid map and OpenGameMap never travels, which is the
	// same class of bug as the missing DemoMap default it replaced.
	//
	// So test both forms and accept either. A map exists if EITHER resolves;
	// a map is missing only when both fail, which cannot happen for a real map.
	const FString PackagePath = GameMapPath.GetAssetPathString();
	const bool bExists =
		FPackageName::DoesPackageExist(PackagePath) ||
		FPackageName::DoesPackageExist(ObjectPath);

	if (!bExists)
	{
		UE_LOG(LogTemp, Error,
			TEXT("HomeWorld: OpenGameMap target does not exist: %s")
			TEXT(" (package form tried: %s)")
			TEXT(" -- Play will go nowhere. Set GameMapPath on BP_GameInstance ")
			TEXT("or [/Script/HomeWorld.HomeWorldGameInstance] in DefaultGame.ini."),
			*ObjectPath, *PackagePath);
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: OpenGameMap -> %s"), *ObjectPath);
	UGameplayStatics::OpenLevel(this, FName(*MapName), true);
}

void UHomeWorldGameInstance::OpenCharacterScreen()
{
	APlayerController* PC = GetWorld() ? UGameplayStatics::GetPlayerController(GetWorld(), 0) : nullptr;
	if (!CharacterScreenWidgetClass)
	{
		// DefaultGame.ini still points CharacterScreenWidgetClassPath at
		// /Game/HomeWorld/UI/WBP_CharacterCreate, which does not exist in
		// Content (only WBP_MainMenu does). ResolveClass returns null, so this
		// button used to do nothing at all with nothing logged.
		UE_LOG(LogTemp, Warning,
			TEXT("HomeWorld: OpenCharacterScreen - no widget class resolved from '%s' ")
			TEXT("-- the Character button will do nothing. Either build ")
			TEXT("WBP_CharacterCreate or clear CharacterScreenWidgetClassPath in ")
			TEXT("DefaultGame.ini."),
			*CharacterScreenWidgetClassPath.ToString());
		return;
	}
	if (!PC)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: OpenCharacterScreen - no PlayerController"));
		return;
	}

	UUserWidget* Widget = CreateWidget<UUserWidget>(PC, CharacterScreenWidgetClass);
	if (Widget)
	{
		Widget->AddToViewport(1);
	}
}
