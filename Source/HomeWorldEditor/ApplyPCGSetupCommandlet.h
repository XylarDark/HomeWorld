// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "Commandlets/Commandlet.h"
#include "ApplyPCGSetupCommandlet.generated.h"

/**
 * Commandlet that finds the level's PCG Volume, assigns the ForestIsland_PCG graph to it,
 * and optionally triggers generate. Use when Python set_graph() is not available or fails.
 * Run with a level loaded in the Editor, or: UnrealEditor.exe HomeWorld.uproject <MapPath> -run=HomeWorldEditor.ApplyPCGSetup [GraphPath=...] [Tag=PCG_Landscape] [MeshList=/Game/Path1,/Game/Path2]
 * Graph assignment is applied; Tag and MeshList are accepted and logged. Setting them on graph nodes requires one-time manual setup or Editor + auto-clicker (pcg_apply_manual_steps.py).
 */
UCLASS()
class UApplyPCGSetupCommandlet : public UCommandlet
{
	GENERATED_BODY()

public:
	virtual int32 Main(const FString& Params) override;
};
