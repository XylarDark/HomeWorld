// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGatherSiteTypes.h"
#include "HomeWorldInventoryTypes.h"
#include "GameFramework/Actor.h"

namespace HomeWorldGatherSite
{
	namespace
	{
		bool ActorHasTag(const AActor* Actor, const FName Tag)
		{
			return Actor && Actor->ActorHasTag(Tag);
		}

		bool LabelOrNameContains(const AActor* Actor, const TCHAR* Needle)
		{
			if (!Actor || !Needle)
			{
				return false;
			}
#if WITH_EDITOR
			const FString Label = Actor->GetActorLabel();
			if (Label.Contains(Needle, ESearchCase::IgnoreCase))
			{
				return true;
			}
#endif
			return Actor->GetName().Contains(Needle, ESearchCase::IgnoreCase);
		}
	}

	FName ResolveResourceForSite(EHomeWorldGatherSiteKind SiteKind, bool& bInOutFlowerHerbNext)
	{
		switch (SiteKind)
		{
		case EHomeWorldGatherSiteKind::Trees:
			return HomeWorldInventory::RES_WOOD;
		case EHomeWorldGatherSiteKind::Rocks:
			return HomeWorldInventory::RES_STONE;
		case EHomeWorldGatherSiteKind::Flowers:
			if (bInOutFlowerHerbNext)
			{
				bInOutFlowerHerbNext = false;
				return HomeWorldInventory::RES_HERB;
			}
			bInOutFlowerHerbNext = true;
			return HomeWorldInventory::RES_FIBER;
		case EHomeWorldGatherSiteKind::BerryNode:
			return HomeWorldInventory::RES_BERRY;
		case EHomeWorldGatherSiteKind::SeedPod:
			return HomeWorldInventory::RES_SEED;
		default:
			return NAME_None;
		}
	}

	const TCHAR* GetGatherFlavorForResource(const FName NormalizedResId)
	{
		if (NormalizedResId == HomeWorldInventory::RES_STONE)
		{
			return TEXT("flint");
		}
		if (NormalizedResId == HomeWorldInventory::RES_FIBER)
		{
			return TEXT("grass");
		}
		return TEXT("");
	}

	EHomeWorldGatherSiteKind InferSiteKindFromActor(const AActor* Actor)
	{
		if (!Actor)
		{
			return EHomeWorldGatherSiteKind::None;
		}
		if (ActorHasTag(Actor, FName("GC_Site_Trees")))
		{
			return EHomeWorldGatherSiteKind::Trees;
		}
		if (ActorHasTag(Actor, FName("GC_Site_Rocks")))
		{
			return EHomeWorldGatherSiteKind::Rocks;
		}
		if (ActorHasTag(Actor, FName("GC_Site_Flowers")))
		{
			return EHomeWorldGatherSiteKind::Flowers;
		}
		if (ActorHasTag(Actor, FName("GC_Site_Berry")))
		{
			return EHomeWorldGatherSiteKind::BerryNode;
		}
		if (ActorHasTag(Actor, FName("GC_Site_Seed")))
		{
			return EHomeWorldGatherSiteKind::SeedPod;
		}
		if (LabelOrNameContains(Actor, TEXT("Tree")) && !LabelOrNameContains(Actor, TEXT("_Sow")))
		{
			return EHomeWorldGatherSiteKind::Trees;
		}
		if (LabelOrNameContains(Actor, TEXT("Rock")) && !LabelOrNameContains(Actor, TEXT("_Sow")))
		{
			return EHomeWorldGatherSiteKind::Rocks;
		}
		if (LabelOrNameContains(Actor, TEXT("Flower")) && !LabelOrNameContains(Actor, TEXT("_Sow")))
		{
			return EHomeWorldGatherSiteKind::Flowers;
		}
		if (LabelOrNameContains(Actor, TEXT("Berry")))
		{
			return EHomeWorldGatherSiteKind::BerryNode;
		}
		if (LabelOrNameContains(Actor, TEXT("Seed")) || LabelOrNameContains(Actor, TEXT("GP_N1_Crop")))
		{
			return EHomeWorldGatherSiteKind::SeedPod;
		}
		return EHomeWorldGatherSiteKind::None;
	}
}
