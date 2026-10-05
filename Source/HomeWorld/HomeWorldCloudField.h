// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldCloudField.generated.h"

class AHomeWorldCloud;
class AHomeWorldCloudWisp;

/**
 * One placed actor that lays out a spirit-blue cloud field from settings
 * (CLOUDS_WISPS_V1 Source §3).
 *
 * Canon invariants, enforced in BuildClouds:
 *  - at least 2 layers, no fixed number (route fact 6): the layer count is
 *    the size of LayerHeightsCm, which is editable;
 *  - every layer sits entirely inside the 50 m band, between 25 m and 75 m
 *    above the field ground, and the 25 m gap below stays clear
 *    (interview #3, 1A);
 *  - spacing uses the position band per route fact 2: top 3-4x, middle
 *    1.5-2.5x, bottom 4-6x diameter;
 *  - the lowest cloud bottom sits on the 25 m line (route fact 4);
 *  - no rails, corridors, or bounds (route fact 10).
 *
 * Layer heights are a tunable setting, not fixed numbers (packet Source §3).
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCloudField : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldCloudField();

	/** Per-layer cloud centre heights above the field ground, in cm. Size is the layer count (min 2). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	TArray<double> LayerHeightsCm = { 6800.0, 3100.0 }; // Lead taste-pass placeholder, not a route fact; the lowest entry is ignored for placement because the 25 m pin owns that layer's Z.

	/** Diameter applied to the field's clouds, in cm; clamped to 6-24 m. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	double DiameterCm = 1200.0;

	/** Half-extent (cm) covered, out from GP_GlideStart along the descent path. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	double HorizontalExtentCm = 8000.0;

	/** Spacing factors per layer position, multiples of the diameter (route fact 2 bands: top 3-4, middle 1.5-2.5, bottom 4-6). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	double TopSpacingFactor = 3.5;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	double MiddleSpacingFactor = 2.0;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	double BottomSpacingFactor = 5.0;

	/** How many of the spawned clouds carry a surface wisp (no fixed count, route fact 9). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CloudField")
	int32 WispCloudCount = 1;

	/** Build (or rebuild) the clouds from the current settings. Idempotent. */
	void BuildClouds();

	const TArray<AHomeWorldCloud*>& GetSpawnedClouds() const { return SpawnedClouds; }

	int32 GetLayerCount() const
	{
		return LayerHeightsCm.Num();
	}

protected:
	virtual void BeginPlay() override;

	static constexpr int32 MaxCloudsPerAxis = 8;

	UPROPERTY(Transient)
	TArray<TObjectPtr<AHomeWorldCloud>> SpawnedClouds;

	bool bBuilt = false;
};
