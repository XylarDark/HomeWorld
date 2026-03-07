// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "HomeWorldMainMenuWidget.generated.h"

class UHomeWorldGameInstance;

/**
 * Base class for main menu widget (WBP_MainMenu). Buttons call these handlers;
 * Blueprint can bind Play, Character, Options, Quit to OnPlayClicked, etc.
 */
UCLASS(Abstract)
class HOMEWORLD_API UHomeWorldMainMenuWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;

	/** Called when Play button is clicked. Default: open game map. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OnPlayClicked();

	/** Called when Character button is clicked. Default: open character screen (Blueprint or subsystem). */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OnCharacterClicked();

	/** Called when Options button is clicked. Default: no-op; override in Blueprint. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OnOptionsClicked();

	/** Called when Quit button is clicked. Default: request exit. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	void OnQuitClicked();

	/** Get the game instance as UHomeWorldGameInstance. */
	UFUNCTION(BlueprintCallable, Category = "Menu")
	UHomeWorldGameInstance* GetHomeWorldGameInstance() const;
};
