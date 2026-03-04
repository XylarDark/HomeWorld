// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldProtectorAttackAbility.h"
#include "AbilitySystemComponent.h"

UHomeWorldProtectorAttackAbility::UHomeWorldProtectorAttackAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldProtectorAttackAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: ProtectorAttack ability activated [%s]"), *GetName());

	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: ProtectorAttack [%s] failed CommitAbility"), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	// Minimal: commit succeeded. Add montage or damage GE in Blueprint or extend in C++ later.
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: ProtectorAttack [%s] committed successfully"), *GetName());
	EndAbility(Handle, ActorInfo, ActivationInfo, false, false);
}
