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
		// T0 #2 NODE_KETTLE: herbs->tea before other day interacts (not meal-BP-as-tea).
		bHandled = Character->TryNodeKettleInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #4 NODE_BACKPACK: equip -> inventory gate (not inventory-lite alone / not PROXY-as-equip).
		bHandled = Character->TryNodeBackpackInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #6 NODE_FIELD_GATHER: field herb/seed collect near landing (not dress/GP_Store/PROXY/plant; not ungated Gather.Flowers).
		bHandled = Character->TryNodeFieldGatherInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #7 NODE_RUNE: day field-path rune unlock -> SetRuneGateUnlocked (not PROXY / not spirit-on-phase).
		bHandled = Character->TryNodeRuneInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #8 NODE_DAY_CAMP: cartoon EJECT_HOME via StartGlideHome (not FALLBACK/PROXY/script-camp/convert).
		bHandled = Character->TryNodeDayCampInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #3 NODE_PLANT_SLOT: day plant given herb (not TryNurture / not PROXY-as-plant).
		bHandled = Character->TryNodePlantSlotInteractInFront();
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
		bHandled = Character->TryStoreTransferInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryMinigameInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryBossSealInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryCraftInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryHarvestInFront();
	}
	EndAbility(Handle, ActorInfo, ActivationInfo, false, !bHandled);
}
