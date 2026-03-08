// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldMealTypes.generated.h"

/** In-world meal trigger type for breakfast/lunch/dinner. Used by ConsumeMealRestore and in-world triggers. List 57; see MVP_FULL_SCOPE_10_LISTS.md, DAY_RESTORATION_LOOP.md. */
UENUM(BlueprintType)
enum class EMealType : uint8
{
	Breakfast UMETA(DisplayName = "Breakfast"),
	Lunch     UMETA(DisplayName = "Lunch"),
	Dinner    UMETA(DisplayName = "Dinner")
};
