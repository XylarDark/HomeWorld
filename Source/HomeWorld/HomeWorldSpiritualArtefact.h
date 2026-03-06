// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldSpiritualArtefact.generated.h"

class UBoxComponent;

/**
 * Second night-only collectible type: overlap grants spiritual artefacts when TimeOfDay is Night (Phase 2).
 * Per VISION: "We collect spiritual artefacts and power at night."
 * T2: second type alongside SpiritualCollectible (power); counter visible via hw.Goods and on collect log.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldSpiritualArtefact : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldSpiritualArtefact();

	/** Overlap volume: player overlapping at night collects one spiritual artefact. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Spiritual")
	TObjectPtr<UBoxComponent> CollectVolume;

protected:
	virtual void BeginPlay() override;

	UFUNCTION()
	void OnCollectVolumeOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
