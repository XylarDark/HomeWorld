// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class UGameInstance;
class UWorld;

namespace HomeWorldPlayWorld
{
	/** Prefer GEngine play world; fall back to active PIE/Game world (MCP console path). */
	HOMEWORLD_API UWorld* Resolve(UWorld* PreferredWorld = nullptr);

	/** Resolve from GameInstance when GI->GetWorld() is null in PIE (SaveGame / Dawn snapshot). */
	HOMEWORLD_API UWorld* ResolveFromGameInstance(UGameInstance* GI);
}
