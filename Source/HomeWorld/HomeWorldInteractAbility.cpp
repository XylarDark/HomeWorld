// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInteractAbility.h"
#include "HomeWorldCharacter.h"
#include "AbilitySystemComponent.h"
#include "Kismet/GameplayStatics.h"

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

	if (UGameplayStatics::GetCurrentLevelName(Character).Contains(TEXT("SizeTest")))
	{
		bool bHandled = Character->TryPartyInviteInFront();
		if (!bHandled)
		{
			bHandled = Character->TryOpeningSpiritInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryPartnerLeadInside();
		}
		if (!bHandled)
		{
			bHandled = Character->TryGardenInteractInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryNodeKettleInteractInFront();
		}
		if (!bHandled)
		{
			// Opening stations: the kitchen consumable table and the armory table.
			bHandled = Character->TryOpeningStationInFront();
		}
		if (!bHandled)
		{
			// Beat 4: the opening dog. Eased Wrath takes one mixed herb; otherwise it refuses.
			bHandled = Character->TryOpeningDogInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningFish();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningNightSetInFront();
		}
		if (!bHandled)
		{
			// Night wisps: a damaged wisp in the backpack can be left in the hot springs with one mixed herb.
			bHandled = Character->TryOpeningHotSpringHealInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningDeliveryInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningBedInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningZiplineInFront();
		}
		if (!bHandled)
		{
			bHandled = Character->TryOpeningShrineInFront();
		}
		Character->NoteSizeTestInteract(bHandled);
		EndAbility(Handle, ActorInfo, ActivationInfo, false, !bHandled);
		return;
	}

	bool bHandled = Character->TryPartyInviteInFront();
	if (!bHandled)
	{
		bHandled = Character->TryOpeningSpiritInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryPartnerLeadInside();
	}
	if (!bHandled)
	{
		bHandled = Character->TryStartCloudDescent();
	}
	if (!bHandled)
	{
		bHandled = Character->TryShrinePortalInteract();
	}
	if (!bHandled)
	{
		bHandled = Character->TryGardenInteractInFront();
	}
	if (!bHandled)
	{
		// T0 #2 NODE_KETTLE: herbs->tea before other day interacts (not meal-BP-as-tea).
		bHandled = Character->TryNodeKettleInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryDungInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryMixFertilizerInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryWoundInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryBullInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryBarnInteractInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryEaseGuardInFront();
	}
	if (!bHandled)
	{
		bHandled = Character->TryFreeCaptiveInFront();
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
	Character->NoteSizeTestInteract(bHandled);
	EndAbility(Handle, ActorInfo, ActivationInfo, false, !bHandled);
}
