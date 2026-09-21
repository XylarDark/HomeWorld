// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldCombatDreamTypes.h"
#include "HomeWorldMinigameInteractComponent.generated.h"

class AHomeWorldCharacter;

/**
 * CD-A: planet minigame interact stub — one-shot log per use (COMBAT_DREAM_BIBLE).
 * Possess = polish-first (extra feedback); others log only.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldMinigameInteractComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldMinigameInteractComponent();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CD|Minigame")
	EHomeWorldMinigameKind MinigameKind = EHomeWorldMinigameKind::Heal;

	UFUNCTION(BlueprintCallable, Category = "CD|Minigame")
	EHomeWorldMinigameKind GetMinigameKind() const { return MinigameKind; }

	UFUNCTION(BlueprintCallable, Category = "CD|Minigame")
	bool TryMinigameInteract(AHomeWorldCharacter* Character);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(Transient)
	bool bUsedThisSession = false;
};
