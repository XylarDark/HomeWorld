// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldCraftTypes.h"
#include "HomeWorldCraftStation.generated.h"

class UBoxComponent;
class USceneComponent;
class UStaticMeshComponent;
class UTextRenderComponent;

/**
 * GC-B craft interact target — hub bootstrap, placed campfire, or cottage kitchen stub.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCraftStation : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldCraftStation();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Craft")
	EHomeWorldCraftStationKind StationKind = EHomeWorldCraftStationKind::HubBootstrap;

	UFUNCTION(BlueprintCallable, Category = "Craft")
	EHomeWorldCraftStationKind GetStationKind() const { return StationKind; }

	/** DS-A: engine primitive + floating label for demo spine readability in PIE. */
	void RefreshDemoSpineVisuals();

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "Craft")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Craft")
	TObjectPtr<UBoxComponent> InteractVolume;

	UPROPERTY(VisibleAnywhere, Category = "Craft|DS")
	TObjectPtr<UStaticMeshComponent> VisualMesh;

	UPROPERTY(VisibleAnywhere, Category = "Craft|DS")
	TObjectPtr<UTextRenderComponent> LabelText;
};
