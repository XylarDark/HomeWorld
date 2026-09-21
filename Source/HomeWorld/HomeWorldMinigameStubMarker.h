// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldCombatDreamTypes.h"
#include "HomeWorldMinigameStubMarker.generated.h"

class UHomeWorldMinigameInteractComponent;
class USceneComponent;

/** CD-A planet minigame marker — prefer spawn over Python add_component. */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldMinigameStubMarker : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldMinigameStubMarker();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CD|Minigame")
	EHomeWorldMinigameKind MinigameKind = EHomeWorldMinigameKind::Heal;

	UFUNCTION(BlueprintCallable, Category = "CD|Minigame")
	UHomeWorldMinigameInteractComponent* GetMinigameComponent() const { return MinigameComponent; }

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "CD|Minigame")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "CD|Minigame")
	TObjectPtr<UHomeWorldMinigameInteractComponent> MinigameComponent;
};
