// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/BoxComponent.h"
#include "HomeWorldGoToBedTriggerComponent.generated.h"

/**
 * Optional trigger volume for "go to bed" / "wake" on overlap. Add to BP_Bed (or any actor). When the player
 * overlaps: if night -> AdvanceToDawn (wake, List 56 T3); else -> SetPhase(Night) (go to bed, List 56 T2).
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldGoToBedTriggerComponent : public UBoxComponent
{
	GENERATED_BODY()

public:
	UHomeWorldGoToBedTriggerComponent();

	virtual void BeginPlay() override;

protected:
	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
