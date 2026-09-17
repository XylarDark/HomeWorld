// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldBeastPad.generated.h"

class UHomeWorldBeastTameComponent;
class USceneComponent;

/**
 * NP-D/NP-E — beast pad actor with tame component created in C++ constructor.
 * Prefer spawning this over Editor-Python add_component_by_class on TargetPoint.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldBeastPad : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldBeastPad();

	UFUNCTION(BlueprintCallable, Category = "Tame")
	UHomeWorldBeastTameComponent* GetTameComponent() const { return TameComponent; }

protected:
	UPROPERTY(VisibleAnywhere, Category = "Tame")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Tame")
	TObjectPtr<UHomeWorldBeastTameComponent> TameComponent;
};
