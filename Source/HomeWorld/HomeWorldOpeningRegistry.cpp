// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningRegistry.h"

#include "Engine/World.h"
#include "EngineUtils.h"

namespace HomeWorldOpeningRegistry
{
	struct FStore
	{
		TWeakObjectPtr<UWorld> World;
		TArray<TWeakObjectPtr<AActor>> Actors;
		FDelegateHandle Spawned;
		FDelegateHandle Destroyed;
		bool bBound = false;
	};

	static TArray<FStore> GStores;

	static FStore* FindStore(UWorld* World)
	{
		for (FStore& Store : GStores)
		{
			if (Store.World.Get() == World)
			{
				return &Store;
			}
		}
		return nullptr;
	}

	static void AddActor(FStore& Store, AActor* Actor)
	{
		if (!Actor)
		{
			return;
		}
		for (const TWeakObjectPtr<AActor>& Existing : Store.Actors)
		{
			if (Existing.Get() == Actor)
			{
				return;
			}
		}
		Store.Actors.Add(Actor);
	}

	static void RemoveActor(FStore& Store, AActor* Actor)
	{
		Store.Actors.RemoveAll([Actor](const TWeakObjectPtr<AActor>& Existing)
		{
			AActor* Live = Existing.Get();
			return Live == nullptr || Live == Actor;
		});
	}

	void Bind(UWorld* World)
	{
		if (!World)
		{
			return;
		}
		GStores.RemoveAll([](const FStore& Store)
		{
			return !Store.World.IsValid();
		});
		if (FindStore(World))
		{
			return;
		}
		FStore& Store = GStores.AddDefaulted_GetRef();
		Store.World = World;
		Store.bBound = true;
		Store.Spawned = World->AddOnActorSpawnedHandler(
			FOnActorSpawned::FDelegate::CreateLambda([World](AActor* Actor)
			{
				if (FStore* Live = FindStore(World))
				{
					AddActor(*Live, Actor);
				}
			}));
		Store.Destroyed = World->AddOnActorDestroyedHandler(
			FOnActorDestroyed::FDelegate::CreateLambda([World](AActor* Actor)
			{
				if (FStore* Live = FindStore(World))
				{
					RemoveActor(*Live, Actor);
				}
			}));
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			AddActor(Store, *It);
		}
	}

	static FStore& Ensure(UWorld* World)
	{
		Bind(World);
		return *FindStore(World);
	}

	AActor* FindNamed(UWorld* World, const TCHAR* Name, bool bExact)
	{
		if (!World || !Name)
		{
			return nullptr;
		}
		const FStore& Store = Ensure(World);
		for (const TWeakObjectPtr<AActor>& Weak : Store.Actors)
		{
			AActor* Actor = Weak.Get();
			if (!Actor)
			{
				continue;
			}
			const FString Label = Actor->GetActorNameOrLabel();
			if (bExact ? Label.Equals(Name) : Label.Contains(Name))
			{
				return Actor;
			}
		}
		return nullptr;
	}

	AActor* FindTagged(UWorld* World, const TCHAR* Tag, const TCHAR* AltTag)
	{
		if (!World || !Tag)
		{
			return nullptr;
		}
		const FName Primary(Tag);
		const FName Alternate = AltTag ? FName(AltTag) : NAME_None;
		const FStore& Store = Ensure(World);
		for (const TWeakObjectPtr<AActor>& Weak : Store.Actors)
		{
			AActor* Actor = Weak.Get();
			if (!Actor)
			{
				continue;
			}
			if (Actor->ActorHasTag(Primary) || (!Alternate.IsNone() && Actor->ActorHasTag(Alternate)))
			{
				return Actor;
			}
		}
		return nullptr;
	}
}
