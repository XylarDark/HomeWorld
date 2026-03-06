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

	/**
	 * Complete this build order (e.g. when SO_WallBuilder OnActivated or agent BUILD branch finishes).
	 * Callable from Blueprint or C++; logs and sets bBuildCompleted for hologram swap/hide in Blueprint.
	 * Console: hw.CompleteBuildOrder targets nearest build order to player (PIE).
	 */
	UFUNCTION(BlueprintCallable, Category = "Build Order")
	void CompleteBuildOrder();

	/** True after CompleteBuildOrder(); Blueprint can bind to hide hologram / show final mesh. */
	UPROPERTY(BlueprintReadOnly, Category = "Build Order")
	bool bBuildCompleted = false;

protected:
	/** Overlap volume so agents/EQS can detect this build order. */
	UPROPERTY(VisibleAnywhere, Category = "Build Order")
	TObjectPtr<UBoxComponent> OverlapVolume;
};
