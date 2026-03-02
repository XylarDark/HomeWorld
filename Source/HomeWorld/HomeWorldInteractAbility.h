// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldInteractAbility.generated.h"

/**
 * Interact ability: trace forward, harvest resource pile (AHomeWorldResourcePile) into inventory.
 * GA_Interact Blueprint should use this as parent so no graph wiring is required.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldInteractAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldInteractAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;
};
