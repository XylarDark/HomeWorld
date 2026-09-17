// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlayWorld.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"

UWorld* HomeWorldPlayWorld::Resolve(UWorld* PreferredWorld)
{
	if (PreferredWorld && PreferredWorld->IsGameWorld())
	{
		return PreferredWorld;
	}

	if (GEngine)
	{
		if (UWorld* PlayWorld = GEngine->GetCurrentPlayWorld())
		{
			return PlayWorld;
		}

		for (const FWorldContext& Context : GEngine->GetWorldContexts())
		{
			UWorld* ContextWorld = Context.World();
			if (!ContextWorld)
			{
				continue;
			}
			if (Context.WorldType == EWorldType::PIE || Context.WorldType == EWorldType::Game)
			{
				return ContextWorld;
			}
		}
	}

	return PreferredWorld;
}

UWorld* HomeWorldPlayWorld::ResolveFromGameInstance(UGameInstance* GI)
{
	if (GI)
	{
		if (UWorld* World = GI->GetWorld())
		{
			if (UWorld* Resolved = Resolve(World))
			{
				return Resolved;
			}
		}
	}

	return Resolve(nullptr);
}
