// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "HomeWorldCharacterCustomizeWidget.generated.h"

/**
 * Base class for character creation/customization widget (WBP_CharacterCreate).
 * Placeholder for Upload/Scan, face sliders; backend (image->character, morphs) in Phase C/E.
 */
UCLASS(Abstract)
class HOMEWORLD_API UHomeWorldCharacterCustomizeWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	/** Called when Confirm is clicked. Save customization and close or return to menu. */
	UFUNCTION(BlueprintCallable, Category = "Character Customize")
	void OnConfirmClicked();

	/** Called when Back is clicked. Remove this widget and return to main menu. */
	UFUNCTION(BlueprintCallable, Category = "Character Customize")
	void OnBackClicked();
};
