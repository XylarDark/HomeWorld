// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldHealAbility.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldSpiritHealComponent.h"
#include "AbilitySystemComponent.h"
#include "Engine/World.h"
#include "GameFramework/Character.h"
#include "Components/CapsuleComponent.h"

UHomeWorldHealAbility::UHomeWorldHealAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldHealAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
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
		UE_LOG(LogTemp, Warning, TEXT("HEAL: ability commit failed"));
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	const bool bHealed = Character->TryHealSpiritInFront();
	UE_LOG(LogTemp, Log, TEXT("HEAL: ability %s"), bHealed ? TEXT("handled target") : TEXT("no target or soft fail"));
	EndAbility(Handle, ActorInfo, ActivationInfo, false, !bHealed);
}
