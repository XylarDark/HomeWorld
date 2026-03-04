// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritAssignmentSubsystem.h"
#include "HomeWorldYieldNode.h"

void UHomeWorldSpiritAssignmentSubsystem::AssignSpiritToNode(FName SpiritId, AHomeWorldYieldNode* Node)
{
	if (SpiritId.IsNone()) return;
	if (!Node) return;

	// If spirit was assigned elsewhere, clear that node first
	if (TWeakObjectPtr<AHomeWorldYieldNode>* Existing = SpiritToNode.Find(SpiritId))
	{
		if (AHomeWorldYieldNode* OldNode = Existing->Get())
		{
			if (OldNode != Node)
			{
				OldNode->ClearAssignment();
			}
		}
		SpiritToNode.Remove(SpiritId);
	}

	Node->SetAssignedSpirit(SpiritId);
	SpiritToNode.Add(SpiritId, Node);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spirit '%s' assigned to node '%s'"), *SpiritId.ToString(), *Node->GetName());
}

void UHomeWorldSpiritAssignmentSubsystem::UnassignSpirit(FName SpiritId)
{
	if (TWeakObjectPtr<AHomeWorldYieldNode>* Ptr = SpiritToNode.Find(SpiritId))
	{
		if (AHomeWorldYieldNode* Node = Ptr->Get())
		{
			Node->ClearAssignment();
		}
		SpiritToNode.Remove(SpiritId);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spirit '%s' unassigned"), *SpiritId.ToString());
	}
}

AHomeWorldYieldNode* UHomeWorldSpiritAssignmentSubsystem::GetNodeForSpirit(FName SpiritId) const
{
	const TWeakObjectPtr<AHomeWorldYieldNode>* Ptr = SpiritToNode.Find(SpiritId);
	return Ptr ? Ptr->Get() : nullptr;
}
