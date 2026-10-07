// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldCloud.generated.h"

class AHomeWorldCloudWisp;
class UStaticMeshComponent;

/**
 * One spirit-blue cloud on the descent route.
 *
 * Clouds are pass-through (CLOUDS_WISPS_V1 interview #3, 2A): the visual
 * mesh only registers an overlap with the pawn and can never block or be
 * stood on. Diameter is a setting clamped to the recorded 36-144 m band (×6 world-scale pass 2026-10-07)
 * (route fact 1) and the look is a runtime dynamic instance of the
 * existing M_SpiritUnlit master; no new master, no .uasset.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCloud : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldCloud();

	/** Cloud diameter in cm. Setting; clamped to 6-24 m (route fact 1). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Cloud")
	double DiameterCm = 7200.0;

	/** Whether this cloud carries one surface wisp (route fact 8). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Cloud")
	bool bCarriesWisp = false;

	/** (Re)apply diameter, material and collision from the current settings. */
	void BuildVisuals();

	/** Spawn the surface wisp when bCarriesWisp is set. Idempotent. */
	AHomeWorldCloudWisp* EnsureSurfaceWisp();

	double GetDiameterCm() const
	{
		return FMath::Clamp(DiameterCm, MinDiameterCm, MaxDiameterCm);
	}

	UStaticMeshComponent* GetVisualMesh() const { return VisualMesh; }

	AHomeWorldCloudWisp* GetSurfaceWisp() const { return SurfaceWisp; }

protected:
	virtual void BeginPlay() override;

	static constexpr double MinDiameterCm = 3600.0;
	static constexpr double MaxDiameterCm = 14400.0;

	UPROPERTY(VisibleAnywhere, Category = "Cloud")
	TObjectPtr<UStaticMeshComponent> VisualMesh;

	UPROPERTY(Transient)
	TObjectPtr<AHomeWorldCloudWisp> SurfaceWisp;
};
