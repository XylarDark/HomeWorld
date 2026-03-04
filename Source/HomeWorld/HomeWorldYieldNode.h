// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldYieldNode.generated.h"

class UBoxComponent;

/**
 * Base actor for cultivation/mining nodes that yield resources over time.
 * Spirits can be assigned in Day 22; until then, stub yields to player inventory on a timer.
 * Use tags CultivationNode or MiningNode for placement and spirit assignment.
 */
UCLASS(Blueprintable, Abstract)
class HOMEWORLD_API AHomeWorldYieldNode : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldYieldNode();

	/** Resource type yielded (e.g. "Wood", "Food", "Ore", "Stone"). */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Yield")
	FName ResourceType;

	/** Amount added per yield interval. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Yield", meta = (ClampMin = "1"))
	int32 YieldRate = 5;

	/** Seconds between yield ticks. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Yield", meta = (ClampMin = "0.5"))
	float YieldIntervalSeconds = 10.0f;

	/** When true, node produces and adds to inventory (Day 22: set when spirit assigned). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Yield")
	bool bIsProducing = true;

	/** Spirit ID currently assigned to this node (empty if none). Day 22 assignment. */
	UPROPERTY(BlueprintReadOnly, Category = "Yield")
	FName AssignedSpiritId;

	/** Assign a spirit to this node; starts producing. Call from assignment subsystem. */
	UFUNCTION(BlueprintCallable, Category = "Yield")
	void SetAssignedSpirit(FName SpiritId);

	/** Clear assignment; stops producing. */
	UFUNCTION(BlueprintCallable, Category = "Yield")
	void ClearAssignment();

	/** Currently assigned spirit ID (none if not set). */
	UFUNCTION(BlueprintPure, Category = "Yield")
	FName GetAssignedSpirit() const { return AssignedSpiritId; }

	virtual void BeginPlay() override;
	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

protected:
	/** Called every YieldIntervalSeconds while bIsProducing; adds YieldRate to game inventory. */
	UFUNCTION(BlueprintCallable, Category = "Yield")
	void ProduceYield();

	/** Overlap volume for placement and future spirit/worker detection. */
	UPROPERTY(VisibleAnywhere, Category = "Yield")
	TObjectPtr<UBoxComponent> OverlapVolume;

private:
	FTimerHandle YieldTimerHandle;
};
