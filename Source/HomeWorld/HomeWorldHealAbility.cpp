// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldHealAbility.h"
#include "AbilitySystemComponent.h"

UHomeWorldHealAbility::UHomeWorldHealAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldHealAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Heal ability activated [%s]"), *GetName());

	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Heal [%s] failed CommitAbility"), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	// Minimal: commit succeeded. Add healing GE or attribute change in Blueprint or extend in C++ later.
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Heal [%s] committed successfully"), *GetName());
	EndAbility(Handle, ActorInfo, ActivationInfo, false, false);
}
