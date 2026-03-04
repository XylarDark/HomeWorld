// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldProtectorAttackAbility.generated.h"

/**
 * Protector role combat ability. GA_ProtectorAttack Blueprint should use this as parent.
 * Trigger when in Defend state (State Tree or input). Minimal: commit + log; add montage/effects in Blueprint.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldProtectorAttackAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldProtectorAttackAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;
};
