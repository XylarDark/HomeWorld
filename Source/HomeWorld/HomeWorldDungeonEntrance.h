// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldDungeonEntrance.generated.h"

class UBoxComponent;

/**
 * Trigger actor that opens a level when the player overlaps.
 * Use at dungeon (or portal) entrance: set LevelToOpen to the target map name (e.g. "Dungeon_Interior").
 * Day 24 / T5: Dungeon level streaming.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldDungeonEntrance : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldDungeonEntrance();

	/** Level to open when player enters the trigger (e.g. "Dungeon_Interior" for /Game/.../Dungeon_Interior). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dungeon")
	FName LevelToOpen;

	/** If set, only a pawn with this tag will trigger the load (e.g. "Player"). Leave empty to accept any pawn. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Dungeon", meta = (DisplayName = "Require Pawn Tag"))
	FName RequiredPawnTag;

	virtual void BeginPlay() override;

protected:
	UFUNCTION()
	void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UPROPERTY(VisibleAnywhere, Category = "Dungeon")
	TObjectPtr<UBoxComponent> TriggerVolume;
};
