// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldCharacterCustomizationSubsystem.generated.h"

class USkeletalMeshComponent;

/**
 * Subsystem for character face/body customization: morph target discovery,
 * apply values, and persist to profile. Used by WBP_CharacterCreate and in-game customize.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldCharacterCustomizationSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Set the mesh component to customize (e.g. pawn's GetMesh()). Call when opening character screen. */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize")
	void SetCustomizationTarget(USkeletalMeshComponent* MeshComponent);

	/** Get morph target names from the current target mesh. Returns empty if no target or mesh has no morphs. */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize", meta = (DisplayName = "Get Morph Target Names"))
	TArray<FName> GetMorphTargetNames() const;

	/** Set a morph target value on the current target (0..1). No-op if target not set. */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize", meta = (DisplayName = "Set Morph Target Value"))
	void SetMorphTargetValue(FName MorphName, float Value);

	/** Save current morph values to profile (Saved/CharacterCustomization.json). */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize", meta = (DisplayName = "Save Customization To Profile"))
	void SaveCustomizationToProfile();

	/** Load morph values from profile and apply to current target. Returns true if profile existed and was applied. */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize", meta = (DisplayName = "Load Customization From Profile"))
	bool LoadCustomizationFromProfile();

	/** Apply a set of morph values (e.g. from LoadCustomizationFromProfile) to the current target. */
	UFUNCTION(BlueprintCallable, Category = "Character|Customize")
	void ApplyMorphValues(const TMap<FName, float>& Values);

	/** Current target mesh for customization (preview or pawn). */
	UPROPERTY(BlueprintReadOnly, Category = "Character|Customize")
	TObjectPtr<USkeletalMeshComponent> CustomizationTarget;

private:
	TMap<FName, float> CachedMorphValues;
	static FString GetProfilePath();
};
