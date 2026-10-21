// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldOpeningDayCamp.generated.h"

class AHomeWorldCharacter;
class USphereComponent;

/**
 * Walking into this clearing takes the partner and sends the player home.
 * The reach is the opening interact distance. The clearing itself is not placed here.
 */
UCLASS()
class HOMEWORLD_API AHomeWorldOpeningDayCamp : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldOpeningDayCamp();

	/** The opening interact reach. Inside it, arrival can eject. Outside it, nothing happens. */
	static constexpr float ArrivalRadiusCm = 280.f;

	bool TryArrive(AHomeWorldCharacter* Character);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "Opening|DayCamp")
	TObjectPtr<USphereComponent> ArrivalSphere;

	UFUNCTION()
	void OnArrivalBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
