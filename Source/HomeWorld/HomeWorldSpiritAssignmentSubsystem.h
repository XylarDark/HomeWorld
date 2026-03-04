// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldSpiritAssignmentSubsystem.generated.h"

class AHomeWorldYieldNode;

/**
 * Game instance subsystem for assigning spirits to yield nodes (Day 22).
 * Tracks which spirit is assigned to which node; unassign clears the node and frees the spirit.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldSpiritAssignmentSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Assign a spirit to a yield node. If the spirit was already assigned elsewhere, that node is cleared first. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Assign Spirit To Node"))
	void AssignSpiritToNode(FName SpiritId, AHomeWorldYieldNode* Node);

	/** Unassign a spirit from its current node (if any). Node stops producing; spirit is idle for reassignment. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Unassign Spirit"))
	void UnassignSpirit(FName SpiritId);

	/** Get the node a spirit is currently assigned to, or null. */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Get Node For Spirit"))
	AHomeWorldYieldNode* GetNodeForSpirit(FName SpiritId) const;

private:
	UPROPERTY()
	TMap<FName, TWeakObjectPtr<AHomeWorldYieldNode>> SpiritToNode;
};
