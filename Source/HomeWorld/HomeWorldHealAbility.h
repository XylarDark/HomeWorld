// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldHealAbility.generated.h"

/**
 * SYS V6 heal ability. GA_Heal Blueprint parent — traces spirit wisps and spends RES_HERB/RES_SEED.
 * Interact (E) also routes through AHomeWorldCharacter::TryHealSpiritInFront (same component path).
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
