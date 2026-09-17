// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInteractAbility.h"
#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"

UHomeWorldInteractAbility::UHomeWorldInteractAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldInteractAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
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

	bool bHandled = Character->TryStartFallbackGlide();
	if (!bHandled)
	{
		bHandled = Character->TryShrinePortalInteract();
	}
	if (!bHandled)
	{
		bHandled = Character->TryTameBeastInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryHealSpiritInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryNurtureInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryHarvestInFront();
	}
	EndAbility(Handle, ActorInfo, ActivationInfo, false, !bHandled);
}
