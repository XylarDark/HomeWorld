// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "HomeWorldPlayerState.generated.h"

/**
 * Replication anchor for co-op (2-8p). Use for player name, role, score, etc.
 * Keep minimal until Week 2+; add replicated properties as needed.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldPlayerState : public APlayerState
{
	GENERATED_BODY()

public:
	AHomeWorldPlayerState();
};
