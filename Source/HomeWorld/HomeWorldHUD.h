// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "HomeWorldHUD.generated.h"

/**
 * Simple HUD that draws TimeOfDay phase (Day/Night), Physical/Spiritual/Love counts, and at night Astral HP, SpiritBurst and SpiritShield cooldowns.
 * At night also shows Wave N and Converted: N (ConvertedFoesThisNight from GameMode). Love: N is shown day or night (PlayerState GetLoveLevel); Phase label with hw.TimeOfDay.Phase 0|1|2|3.
 */
UCLASS()
class HOMEWORLD_API AHomeWorldHUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void DrawHUD() override;

protected:
	/** Vertical offset from top for first line (pixels). */
	UPROPERTY(EditDefaultsOnly, Category = "HUD")
	float TextOffsetY = 24.f;

	/** Horizontal offset from left (pixels). */
	UPROPERTY(EditDefaultsOnly, Category = "HUD")
	float TextOffsetX = 24.f;

	/** Vertical spacing between lines (pixels). */
	UPROPERTY(EditDefaultsOnly, Category = "HUD")
	float LineSpacing = 22.f;

	/** Scale for debug text. */
	UPROPERTY(EditDefaultsOnly, Category = "HUD")
	float TextScale = 1.2f;
};
