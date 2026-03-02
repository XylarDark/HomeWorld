// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldPlaceAbility.generated.h"

/**
 * Place ability: trace from camera via GetPlacementTransform and spawn PlaceActorClass at hit.
 * GA_Place Blueprint should use this as parent so no graph wiring is required.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldPlaceAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldPlaceAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;
};
