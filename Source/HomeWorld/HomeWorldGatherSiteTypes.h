// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGatherSiteTypes.generated.h"

class AActor;

/** Docs/GATHER_CRAFT_BIBLE + Docs/21 site kind IDs for day gather (GC-A). */
UENUM(BlueprintType)
enum class EHomeWorldGatherSiteKind : uint8
{
	None UMETA(DisplayName = "Unset"),
	Trees UMETA(DisplayName = "trees"),
	Rocks UMETA(DisplayName = "rocks"),
	Flowers UMETA(DisplayName = "flowers"),
	BerryNode UMETA(DisplayName = "berry"),
	SeedPod UMETA(DisplayName = "seed"),
};

namespace HomeWorldGatherSite
{
	/** Map site kind to RES_*; flowers alternate FIBER (grass) / HERB when bInOutFlowerHerbNext is toggled. */
	FName ResolveResourceForSite(EHomeWorldGatherSiteKind SiteKind, bool& bInOutFlowerHerbNext);

	/** Optional log/UI flavor: flint for STONE, grass for FIBER (not a 7th resource). */
	const TCHAR* GetGatherFlavorForResource(FName NormalizedResId);

	/** When GatherSiteKind unset: tags GC_Site_* or GP_RS_* / GP_Gather_* labels. */
	EHomeWorldGatherSiteKind InferSiteKindFromActor(const AActor* Actor);
}
