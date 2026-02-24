// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldResourcePile.generated.h"

class UBoxComponent;

/**
 * Base actor for resource piles (e.g. wood) that agents harvest via Smart Object.
 * Blueprint BP_WoodPile inherits; add Smart Object "HarvestWood" in Blueprint.
 */
UCLASS(Blueprintable, Abstract)
class HOMEWORLD_API AHomeWorldResourcePile : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldResourcePile();

	/** Resource type (e.g. "Wood") for EQS or game logic. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource")
	FName ResourceType;

	/** Amount granted per harvest interaction (e.g. 10 wood). */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource", meta = (ClampMin = "1"))
	int32 AmountPerHarvest = 10;

protected:
	/** Overlap volume for agent/EQS detection. */
	UPROPERTY(VisibleAnywhere, Category = "Resource")
	TObjectPtr<UBoxComponent> OverlapVolume;
};
