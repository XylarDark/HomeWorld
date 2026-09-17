// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldSpiritWisp.generated.h"

class UHomeWorldSpiritHealComponent;
class USceneComponent;

/** NP-E V6 — spirit wisp actor with heal component in constructor. */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldSpiritWisp : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldSpiritWisp();

	UFUNCTION(BlueprintCallable, Category = "Heal")
	UHomeWorldSpiritHealComponent* GetHealComponent() const { return HealComponent; }

protected:
	UPROPERTY(VisibleAnywhere, Category = "Heal")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Heal")
	TObjectPtr<UHomeWorldSpiritHealComponent> HealComponent;
};
