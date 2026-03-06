// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldSpiritualCollectible.generated.h"

class UBoxComponent;

/**
 * Night-only collectible: overlap grants spiritual power when TimeOfDay is Night (Phase 2).
 * Per VISION: "We collect spiritual artefacts and power at night."
 * Stub for T2; test in PIE: set hw.TimeOfDay.Phase 2, overlap this actor, check hw.SpiritualPower.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldSpiritualCollectible : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldSpiritualCollectible();

	/** Overlap volume: player overlapping at night collects spiritual power. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spiritual")
	TObjectPtr<UBoxComponent> CollectVolume;

protected:
	virtual void BeginPlay() override;

	UFUNCTION()
	void OnCollectVolumeOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
