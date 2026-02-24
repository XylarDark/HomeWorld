// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "BuildPlacementSupport.generated.h"

class APlayerController;

/**
 * Minimal contract for build/placement: trace from player camera to world.
 * Building Blueprints (Week 1+) call GetPlacementHit or GetPlacementTransform for placement or preview.
 * No snap or UI logic here; only the trace query and placement pose.
 */
UCLASS(Abstract, MinimalAPI, meta = (DisplayName = "Build Placement Support"))
class UBuildPlacementSupport : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/** Trace from the local player's camera forward; returns true if something was hit. */
	UFUNCTION(BlueprintCallable, Category = "Build|Placement", meta = (WorldContext = "WorldContextObject"))
	static bool GetPlacementHit(UObject* WorldContextObject, float MaxDistance, FHitResult& OutHit);

	/**
	 * Same trace as GetPlacementHit; also writes a placement transform (location = impact, rotation = surface normal).
	 * Use for snap or preview; single stable API for placement pose.
	 */
	UFUNCTION(BlueprintCallable, Category = "Build|Placement", meta = (WorldContext = "WorldContextObject"))
	static bool GetPlacementTransform(UObject* WorldContextObject, float MaxDistance, FHitResult& OutHit, FTransform& OutTransform);
};
