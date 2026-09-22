// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldSpiritStealthTypes.h"
#include "HomeWorldSpiritLitVolume.generated.h"

class UBoxComponent;

/**
 * SS-A: thin overlap volume — campfire / NPC torch / spirit torch reveal spirits; body mundane torch does not.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldSpiritLitVolume : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldSpiritLitVolume();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stealth|SS-A")
	EHomeWorldSpiritLitSourceKind LitSourceKind = EHomeWorldSpiritLitSourceKind::Campfire;

	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-A")
	EHomeWorldSpiritLitSourceKind GetLitSourceKind() const { return LitSourceKind; }

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-A")
	TObjectPtr<UBoxComponent> TriggerVolume;

	UFUNCTION()
	void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
