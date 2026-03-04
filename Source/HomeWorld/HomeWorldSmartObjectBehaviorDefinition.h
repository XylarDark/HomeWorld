// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "SmartObjectDefinition.h"
#include "HomeWorldSmartObjectBehaviorDefinition.generated.h"

/**
 * Minimal Smart Object behavior definition for use as default on SO_WallBuilder (and other SOs).
 * Satisfies content validation without the experimental Gameplay Behavior Smart Objects plugin.
 * For full build behavior (e.g. play montage, spawn wall), extend in Blueprint or add logic later.
 */
UCLASS(BlueprintType, NotBlueprintable)
class HOMEWORLD_API UHomeWorldSmartObjectBehaviorDefinition : public USmartObjectBehaviorDefinition
{
	GENERATED_BODY()

public:
	UHomeWorldSmartObjectBehaviorDefinition(const FObjectInitializer& ObjectInitializer = FObjectInitializer::Get())
		: Super(ObjectInitializer)
	{}
};
