// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldCombatDreamTypes.generated.h"

/** CD-A minigame stub families (COMBAT_DREAM_BIBLE). Planet-only; log tags MINIGAME:*. */
UENUM(BlueprintType)
enum class EHomeWorldMinigameKind : uint8
{
	Heal UMETA(DisplayName = "Heal"),
	Nurture UMETA(DisplayName = "Nurture"),
	Grow UMETA(DisplayName = "Grow"),
	Possess UMETA(DisplayName = "Possess"),
};

namespace HomeWorldCombatDream
{
	HOMEWORLD_API const TCHAR* GetMinigameLogTag(EHomeWorldMinigameKind Kind);
	HOMEWORLD_API bool IsPolishFirstMinigame(EHomeWorldMinigameKind Kind);
}
