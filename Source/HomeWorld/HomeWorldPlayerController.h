// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "HomeWorldPlayerController.generated.h"

class AHomeWorldHUD;
class UUserWidget;
class UHomeWorldGameInstance;

/**
 * Player controller that uses AHomeWorldHUD to show Physical and Spiritual counts (T5).
 * On MainMenu map, shows main menu widget and sets input mode to UI.
 */
UCLASS()
class HOMEWORLD_API AHomeWorldPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	AHomeWorldPlayerController();

	virtual void BeginPlay() override;
	virtual void SpawnDefaultHUD() override;

	/** Main menu widget shown when on MainMenu map. Removed when transitioning to game. */
	UPROPERTY(BlueprintReadOnly, Category = "Menu")
	TObjectPtr<UUserWidget> MainMenuWidget;

private:
	void ShowMainMenuIfNeeded();
	void RemoveMainMenuWidget();
};
