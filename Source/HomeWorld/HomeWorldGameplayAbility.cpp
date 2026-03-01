// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameplayAbility.h"
#include "AbilitySystemComponent.h"

UHomeWorldGameplayAbility::UHomeWorldGameplayAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldGameplayAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Ability activated [%s]"), *GetName());
	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Ability [%s] failed CommitAbility"), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}
	// Base implementation: no-op; Blueprint children override to add effects (e.g. apply GE, play montage).
	EndAbility(Handle, ActorInfo, ActivationInfo, false, false);
}
