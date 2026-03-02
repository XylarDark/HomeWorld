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

	/** Override so minimal Blueprint children can work without implementing: commits and ends. Override in Blueprint to add cost/effects. */
	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;
};
