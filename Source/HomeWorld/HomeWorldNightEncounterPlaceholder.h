// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldNightEncounterPlaceholder.generated.h"

class UStaticMeshComponent;
class USphereComponent;

/**
 * Night encounter placeholder: when the player overlaps this actor at night,
 * we treat it as "defeated" and call ReportFoeConverted then destroy.
 * Used for wave, planetoid pack, and boss placeholders. See CONVERSION_NOT_KILL.md.
 */
UCLASS()
class HOMEWORLD_API AHomeWorldNightEncounterPlaceholder : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldNightEncounterPlaceholder();

	/** For GameMode spawn code: set mesh same as AStaticMeshActor. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld")
	UStaticMeshComponent* GetStaticMeshComponent() const { return MeshComponent; }

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "HomeWorld|NightEncounter")
	TObjectPtr<USphereComponent> OverlapSphere;

	UPROPERTY(VisibleAnywhere, Category = "HomeWorld|NightEncounter")
	TObjectPtr<UStaticMeshComponent> MeshComponent;

	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
