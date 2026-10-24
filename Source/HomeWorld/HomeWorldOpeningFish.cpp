// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningFish.h"

#include "HomeWorldOpeningRegistry.h"
#include "EngineUtils.h"
#include "GameFramework/Actor.h"

namespace HomeWorldOpeningFish
{
	AActor* FindPond(UWorld* World)
	{
		return HomeWorldOpeningRegistry::FindNamed(World, TEXT("Water_Pond"), true);
	}

	AActor* FindPondByWorldScan(UWorld* World)
	{
		if (!World)
		{
			return nullptr;
		}
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (It->GetActorNameOrLabel() == TEXT("Water_Pond"))
			{
				return *It;
			}
		}
		return nullptr;
	}
}
