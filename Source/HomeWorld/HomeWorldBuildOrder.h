// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldBuildOrder.generated.h"

class UBoxComponent;

/**
 * Base actor for build-order holograms that agents detect and fulfill (EQS, State Tree BUILD).
 * Blueprint BP_BuildOrder_Wall (and future farm/bed) inherit; add Static Mesh and Smart Object in Blueprint.
 */
UCLASS(Blueprintable, Abstract)
class HOMEWORLD_API AHomeWorldBuildOrder : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldBuildOrder();

	/** Identifier for this build type (e.g. "Wall", "Farm"); used by State Tree / EQS to filter. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Build Order")
	FName BuildDefinitionID;

	/** Returns BuildDefinitionID for queries from State Tree or EQS. */
	UFUNCTION(BlueprintCallable, Category = "Build Order")
	FName GetBuildDefinitionID() const { return BuildDefinitionID; }

protected:
	/** Overlap volume so agents/EQS can detect this build order. */
	UPROPERTY(VisibleAnywhere, Category = "Build Order")
	TObjectPtr<UBoxComponent> OverlapVolume;
};
