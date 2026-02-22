// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Abilities/GameplayAbility.h"
#include "HomeWorldGameplayAbility.generated.h"

/**
 * Base C++ class for HomeWorld abilities. Concrete abilities (e.g. 3 survivor skills)
 * can be Blueprint children. Use for replication and shared behavior; data and VFX in Blueprint.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldGameplayAbility : public UGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldGameplayAbility();
};
