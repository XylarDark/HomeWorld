// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldNurtureTarget.generated.h"

class USceneComponent;

/** NP-E V7 — nurture target actor with component in constructor. */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldNurtureTarget : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldNurtureTarget();

	UFUNCTION(BlueprintCallable, Category = "Nurture")
	UHomeWorldNurtureComponent* GetNurtureComponent() const { return NurtureComponent; }

protected:
	UPROPERTY(VisibleAnywhere, Category = "Nurture")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Nurture")
	TObjectPtr<UHomeWorldNurtureComponent> NurtureComponent;
};
