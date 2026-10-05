// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldCloudWisp.generated.h"

class USphereComponent;
class UPrimitiveComponent;

/** Route collectible for the active cloud descent; can be given a level Blueprint mesh. */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCloudWisp : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldCloudWisp();

protected:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Cloud Wisp")
	TObjectPtr<USphereComponent> Trigger;

	UFUNCTION()
	void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep,
		const FHitResult& SweepResult);
};
