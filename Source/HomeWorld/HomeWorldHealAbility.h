// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldHealAbility.generated.h"

/**
 * Support/Healer role ability. GA_Heal Blueprint should use this as parent.
 * Minimal: commit + log; add healing GE or attribute change in Blueprint or extend in C++.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldHealAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldHealAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;
};
