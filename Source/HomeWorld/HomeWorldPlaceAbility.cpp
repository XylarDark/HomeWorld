// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlaceAbility.h"
#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"

UHomeWorldPlaceAbility::UHomeWorldPlaceAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldPlaceAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	if (!ActorInfo || !ActorInfo->AvatarActor.IsValid())
	{
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(ActorInfo->AvatarActor.Get());
	if (!Character)
	{
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	const bool bPlaced = Character->TryPlaceAtCursor();
	EndAbility(Handle, ActorInfo, ActivationInfo, false, !bPlaced);
}
