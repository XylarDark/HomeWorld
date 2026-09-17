// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldStoreTransferComponent.h"
#include "HomeWorldStoreProp.generated.h"

class USceneComponent;

/** PL-C PA-07 — homestead Stored prop with store-transfer component. */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldStoreProp : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldStoreProp();

	UFUNCTION(BlueprintCallable, Category = "Store")
	UHomeWorldStoreTransferComponent* GetStoreComponent() const { return StoreComponent; }

protected:
	UPROPERTY(VisibleAnywhere, Category = "Store")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Store")
	TObjectPtr<UHomeWorldStoreTransferComponent> StoreComponent;
};
