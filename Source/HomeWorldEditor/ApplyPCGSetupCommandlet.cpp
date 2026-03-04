// Copyright HomeWorld. All Rights Reserved.

#include "ApplyPCGSetupCommandlet.h"
#include "PCGComponent.h"
#include "PCGGraph.h"
#include "Editor.h"
#include "EngineUtils.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "Misc/Parse.h"

DEFINE_LOG_CATEGORY_STATIC(LogApplyPCGSetup, Log, All);

static const TCHAR* DefaultGraphPath = TEXT("/Game/HomeWorld/PCG/ForestIsland_PCG");
static const TCHAR* DefaultTag = TEXT("PCG_Landscape");

static void ParseMeshList(const FString& Params, TArray<FString>& OutMeshPaths)
{
	FString MeshListStr;
	if (FParse::Value(*Params, TEXT("MeshList="), MeshListStr) && !MeshListStr.IsEmpty())
	{
		MeshListStr.ParseIntoArray(OutMeshPaths, TEXT(","), true);
		for (FString& Path : OutMeshPaths)
		{
			Path.TrimStartAndEndInline();
		}
	}
}

int32 UApplyPCGSetupCommandlet::Main(const FString& Params)
{
	FString GraphPath;
	FParse::Value(*Params, TEXT("GraphPath="), GraphPath);
	if (GraphPath.IsEmpty())
	{
		GraphPath = DefaultGraphPath;
	}

	FString Tag;
	FParse::Value(*Params, TEXT("Tag="), Tag);
	if (Tag.IsEmpty())
	{
		Tag = DefaultTag;
	}

	TArray<FString> MeshPaths;
	ParseMeshList(Params, MeshPaths);

	if (!GEditor || !GEditor->GetEditorWorldContext().World())
	{
		UE_LOG(LogApplyPCGSetup, Error, TEXT("No editor world loaded. Open a level first or pass a map: UnrealEditor.exe HomeWorld.uproject <MapPath> -run=HomeWorldEditor.ApplyPCGSetup"));
		return 1;
	}

	UWorld* World = GEditor->GetEditorWorldContext().World();
	if (!World)
	{
		UE_LOG(LogApplyPCGSetup, Error, TEXT("World is null."));
		return 1;
	}

	// Find first actor that has a PCGComponent (e.g. PCG Volume)
	UPCGComponent* PCGComp = nullptr;
	AActor* VolumeActor = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		UPCGComponent* Comp = It->FindComponentByClass<UPCGComponent>();
		if (Comp)
		{
			PCGComp = Comp;
			VolumeActor = *It;
			break;
		}
	}

	if (!PCGComp || !VolumeActor)
	{
		UE_LOG(LogApplyPCGSetup, Error, TEXT("No actor with PCGComponent found in the level. Add a PCG Volume first."));
		return 1;
	}

	// Load graph asset (path can be /Game/.../AssetName; LoadObject expects Package.Path or full object path)
	FString GraphObjectPath = GraphPath;
	if (!GraphObjectPath.Contains(TEXT(".")))
	{
		FString AssetName = FPaths::GetBaseFilename(GraphPath);
		GraphObjectPath = GraphPath + TEXT(".") + AssetName;
	}

	UPCGGraph* Graph = LoadObject<UPCGGraph>(nullptr, *GraphObjectPath);
	if (!Graph)
	{
		UE_LOG(LogApplyPCGSetup, Error, TEXT("Failed to load PCG graph: %s"), *GraphObjectPath);
		return 1;
	}

	PCGComp->SetGraph(Graph);
	UE_LOG(LogApplyPCGSetup, Log, TEXT("Assigned graph %s to PCG Volume %s. Use Details > Generate in the Editor to run the graph."), *GraphPath, *VolumeActor->GetName());

	// Optional: apply Tag and MeshList to graph nodes. PCG graph node iteration and settings modification
	// are editor-internal; when the engine exposes a stable API we can set Get Landscape Data (By Tag + Tag)
	// and Static Mesh Spawner mesh entries here. Until then, use one-time manual setup or Editor + auto-clicker
	// (pcg_apply_manual_steps.py with refs). Params are accepted and logged for documentation.
	if (!Tag.IsEmpty())
	{
		UE_LOG(LogApplyPCGSetup, Log, TEXT("Tag=%s (set Get Landscape Data to By Tag + this tag in graph Details if not already)."), *Tag);
	}
	if (MeshPaths.Num() > 0)
	{
		UE_LOG(LogApplyPCGSetup, Log, TEXT("MeshList: %d path(s) (assign these on Static Mesh Spawner node(s) in graph Details if not already)."), MeshPaths.Num());
	}

	return 0;
}
