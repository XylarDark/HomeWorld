// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGcPlaceholderTypes.generated.h"

/** GC-C foreshadow volumes — logs only (GATHER_CRAFT_BIBLE C1). */
UENUM(BlueprintType)
enum class EHomeWorldGcPlaceholderKind : uint8
{
	Woodshop UMETA(DisplayName = "Woodshop"),
	TextileShop UMETA(DisplayName = "Textile shop"),
	ResearchShop UMETA(DisplayName = "Research shop"),
	CottageKitchen UMETA(DisplayName = "Cottage kitchen"),
	CottageBedroom UMETA(DisplayName = "Cottage bedroom"),
	CottageLivingCauldron UMETA(DisplayName = "Cottage living / cauldron"),
};

namespace HomeWorldGcPlaceholder
{
	HOMEWORLD_API const TCHAR* GetEnterLogLine(EHomeWorldGcPlaceholderKind Kind);
	/** True when enter requires PROGRESS:COTTAGE_UNLOCK / craft subsystem flag. */
	HOMEWORLD_API bool RequiresCottageUnlock(EHomeWorldGcPlaceholderKind Kind);
}
