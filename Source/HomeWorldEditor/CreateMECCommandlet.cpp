// Copyright HomeWorld. All Rights Reserved.

#include "CreateMECCommandlet.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Misc/PackageName.h"
#include "Modules/ModuleManager.h"
#include "UObject/SavePackage.h"
#include "MassEntityConfigAsset.h"
#include "MassEntityTraitBase.h"

DEFINE_LOG_CATEGORY_STATIC(LogCreateMEC, Log, All);

static const TCHAR* DefaultMECPath = TEXT("/Game/HomeWorld/Mass/MEC_FamilyGatherer");

// Trait class paths to add (Script/Module.Class). Adjust module/class names for your UE 5.7 build if not found.
static const TCHAR* TraitClassPaths[] = {
	TEXT("/Script/MassSpawner.MassAgentTrait"),
	TEXT("/Script/MassMovement.MassMovementTrait"),
	TEXT("/Script/MassRepresentation.MassRepresentationFragmentTrait"),
	TEXT("/Script/MassStateTree.MassStateTreeTrait"),
};
static const int32 NumTraitPaths = UE_ARRAY_COUNT(TraitClassPaths);

int32 UCreateMECCommandlet::Main(const FString& Params)
{
	FString RequestedPath;
	FParse::Value(*Params, TEXT("Path="), RequestedPath);
	if (RequestedPath.IsEmpty())
	{
		RequestedPath = DefaultMECPath;
	}

	// Normalize: ensure we have a full asset path (package path + asset name).
	FString PackagePath, AssetName;
	if (RequestedPath.Contains(TEXT("/")))
	{
		int32 LastSlash;
		if (RequestedPath.FindLastChar(TEXT('/'), LastSlash))
		{
			PackagePath = RequestedPath.Left(LastSlash);
			AssetName = RequestedPath.RightChop(LastSlash + 1);
		}
	}
	if (AssetName.IsEmpty())
	{
		AssetName = TEXT("MEC_FamilyGatherer");
	}
	if (PackagePath.IsEmpty())
	{
		PackagePath = TEXT("/Game/HomeWorld/Mass");
	}

	const FString LongPackageName = PackagePath + TEXT("/") + AssetName;

	// Try to load existing asset first (idempotent).
	UMassEntityConfigAsset* MEC = LoadObject<UMassEntityConfigAsset>(nullptr, *(LongPackageName + TEXT(".") + AssetName));
	if (!MEC)
	{
		UPackage* Package = CreatePackage(*LongPackageName);
		if (!Package)
		{
			UE_LOG(LogCreateMEC, Error, TEXT("Failed to create package: %s"), *LongPackageName);
			return 1;
		}
		Package->FullyLoad();

		MEC = NewObject<UMassEntityConfigAsset>(Package, FName(*AssetName), RF_Public | RF_Standalone);
		if (!MEC)
		{
			UE_LOG(LogCreateMEC, Error, TEXT("Failed to create UMassEntityConfigAsset in %s"), *LongPackageName);
			return 1;
		}

		FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get().AssetCreated(MEC);
		UE_LOG(LogCreateMEC, Log, TEXT("Created MEC asset: %s"), *LongPackageName);
	}
	else
	{
		UE_LOG(LogCreateMEC, Log, TEXT("Using existing MEC asset: %s"), *LongPackageName);
	}

	// Add standard traits by class (skip if class not found).
	for (int32 i = 0; i < NumTraitPaths; ++i)
	{
		UClass* TraitClass = StaticLoadClass(UMassEntityTraitBase::StaticClass(), nullptr, TraitClassPaths[i]);
		if (TraitClass)
		{
			MEC->AddTrait(TraitClass);
			UE_LOG(LogCreateMEC, Log, TEXT("Added trait: %s"), TraitClassPaths[i]);
		}
		else
		{
			UE_LOG(LogCreateMEC, Warning, TEXT("Trait class not found (skipped): %s"), TraitClassPaths[i]);
		}
	}

	// Save the package.
	UPackage* Package = MEC->GetPackage();
	Package->MarkPackageDirty();

	FString Filename;
	if (!FPackageName::TryConvertLongPackageNameToFilename(Package->GetName(), Filename, FPackageName::GetAssetPackageExtension()))
	{
		UE_LOG(LogCreateMEC, Error, TEXT("Could not resolve filename for package: %s"), *Package->GetName());
		return 1;
	}

	FSavePackageArgs SaveArgs;
	SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
	SaveArgs.SaveFlags = SAVE_NoError;

	FSavePackageResultStruct SaveResult = UPackage::Save(Package, MEC, *Filename, SaveArgs);
	if (SaveResult.Result != ESavePackageResult::Success)
	{
		UE_LOG(LogCreateMEC, Error, TEXT("SavePackage failed for %s"), *Filename);
		return 1;
	}

	UE_LOG(LogCreateMEC, Log, TEXT("Saved: %s"), *Filename);
	return 0;
}
