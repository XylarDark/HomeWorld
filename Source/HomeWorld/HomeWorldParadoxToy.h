// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldParadoxToy.generated.h"

/** A paradox success arms this toy. The next dawn removes it. A grace match does not. */
UCLASS()
class HOMEWORLD_API AHomeWorldParadoxToy : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldParadoxToy();

	void ArmForDawn();

	bool IsArmedForDawn() const { return bArmedForDawn; }

	bool IsUp() const { return !IsActorBeingDestroyed(); }

private:
	bool bArmedForDawn = false;
};
