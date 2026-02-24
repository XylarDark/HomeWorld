// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "HomeWorldAIController.generated.h"

/**
 * Base AI controller for family/NPCs (Week 2+). Assign Behavior Tree or State Tree in Blueprint.
 * Stub only; no behavior in C++. Use this as the controller class for family member pawns.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldAIController : public AAIController
{
	GENERATED_BODY()

public:
	AHomeWorldAIController(const FObjectInitializer& ObjectInitializer);
};
