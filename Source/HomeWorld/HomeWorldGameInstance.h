// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/GameInstance.h"
#include "Blueprint/UserWidget.h"
#include "HomeWorldGameInstance.generated.h"

/**
 * Game instance that drives main menu flow: shows main menu on MainMenu map,
 * opens game map when Play is clicked. See docs CHARACTER_GENERATION_AND_CUSTOMIZATION.md.
 */
UCLASS()
class HOMEWORLD_API UHomeWorldGameInstance : public UGameInstance
{
	GENERATED_BODY()

public:
	/**
	 * Map to load when Play is clicked.
	 *
	 * Defaults to L_VS_MVP_Markers, which is the only level that actually
	 * contains the homestead, the glide crumbs, and the field below. The old
	 * default was /Game/HomeWorld/Maps/DemoMap, which does not exist in
	 * Content -- so pressing Play travelled to nothing. Override in a
	 * Blueprint or in DefaultGame.ini; see KNOWN_ERRORS 2026-10-03.
	 */
	UPROPERTY(EditDefaultsOnly, Category = "Menu", meta = (AllowedClasses = "/Script/Engine.World"))
	FSoftObjectPath GameMapPath;

	/** Map name used to detect main menu (e.g. "MainMenu"). If current map contains this, menu is shown. */
	UPROPERTY(EditDefaultsOnly, Category = "Menu")
	FString MainMenuMapName;

	/** Widget class for main menu (WBP_MainMenu). Set in Blueprint or resolved from MainMenuWidgetClassPath in Init. */
	UPROPERTY(EditDefaultsOnly, Category = "Menu")
	TSubclassOf<UUserWidget> MainMenuWidgetClass;

	/** If MainMenuWidgetClass is not set, load from this path (e.g. /Game/HomeWorld/UI/WBP_MainMenu.WBP_MainMenu_C). Config in DefaultGame.ini [/Script/HomeWorld.HomeWorldGameInstance]. */
	UPROPERTY(Config)
	FSoftClassPath MainMenuWidgetClassPath;

	/** Widget class for character create/customize screen (WBP_CharacterCreate). Loaded from config if set. */
	UPROPERTY(EditDefaultsOnly, Category = "Menu")
	TSubclassOf<UUserWidget> CharacterScreenWidgetClass;

	/** Config path for character screen widget. Resolved in Init if CharacterScreenWidgetClass is null. */
	UPROPERTY(Config)
	FSoftClassPath CharacterScreenWidgetClassPath;

	/** Request transition to game map. Called by main menu widget when Play is clicked. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OpenGameMap();

	/** Show character creation/customization screen (WBP_CharacterCreate). Creates widget from CharacterScreenWidgetClassPath and adds to viewport. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OpenCharacterScreen();

	/** Returns true if the current level is the main menu (so UI should be shown). */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	bool IsMainMenuMap() const;

	virtual void Init() override;
};
