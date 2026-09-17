// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldShrinePortalTrigger.generated.h"

class UHomeWorldShrinePortalComponent;

/**
 * Editor-spawnable shrine portal trigger (FALLBACK V5). Wraps UHomeWorldShrinePortalComponent for level dress / Python placement.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldShrinePortalTrigger : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldShrinePortalTrigger();

	UPROPERTY(VisibleAnywhere, Category = "Portal|FALLBACK")
	TObjectPtr<UHomeWorldShrinePortalComponent> PortalComponent;
};
