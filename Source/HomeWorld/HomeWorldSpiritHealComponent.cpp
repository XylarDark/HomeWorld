// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritHealComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

namespace
{
	const TCHAR* HealStateLabel(EHomeWorldSpiritHealState State)
	{
		switch (State)
		{
		case EHomeWorldSpiritHealState::Hurt: return TEXT("hurt");
		case EHomeWorldSpiritHealState::Healed: return TEXT("healed");
		default: return TEXT("unknown");
		}
	}
}

UHomeWorldSpiritHealComponent::UHomeWorldSpiritHealComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UHomeWorldSpiritHealComponent::BeginPlay()
{
	Super::BeginPlay();

	if (AActor* Owner = GetOwner())
	{
		Owner->Tags.AddUnique(FName(TEXT("SpiritWound")));
		Owner->Tags.AddUnique(FName(TEXT("SpiritHeal")));
	}

	UE_LOG(LogTemp, Log, TEXT("HEAL: component ready id=%s state=%s"),
		*SpiritId.ToString(), HealStateLabel(HealState));
}

void UHomeWorldSpiritHealComponent::SetHealState(EHomeWorldSpiritHealState NewState)
{
	if (HealState == NewState)
	{
		return;
	}
	const EHomeWorldSpiritHealState Old = HealState;
	HealState = NewState;
	UE_LOG(LogTemp, Log, TEXT("HEAL: %s %s -> %s on '%s'"),
		*SpiritId.ToString(), HealStateLabel(Old), HealStateLabel(NewState),
		GetOwner() ? *GetOwner()->GetName() : TEXT("(none)"));
}

void UHomeWorldSpiritHealComponent::ConfigureSpirit(FName InSpiritId)
{
	if (!InSpiritId.IsNone())
	{
		SpiritId = InSpiritId;
	}
}

void UHomeWorldSpiritHealComponent::ApplyPersistedState(EHomeWorldSpiritHealState NewState)
{
	if (HealState != NewState)
	{
		SetHealState(NewState);
	}
}

bool UHomeWorldSpiritHealComponent::IsNightSpiritInteractionAllowed(AHomeWorldCharacter* Character) const
{
	if (!Character || !Character->GetIsSpiritForm())
	{
		return false;
	}
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TOD = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			return TOD->GetIsSpiritPhase();
		}
	}
	return false;
}

bool UHomeWorldSpiritHealComponent::TryHeal(AHomeWorldCharacter* Character)
{
	if (!Character || !GetOwner())
	{
		return false;
	}

	if (!IsNightSpiritInteractionAllowed(Character))
	{
		UE_LOG(LogTemp, Log, TEXT("HEAL: soft fail %s — day or body form"), *SpiritId.ToString());
		return false;
	}

	if (HealState == EHomeWorldSpiritHealState::Healed)
	{
		UE_LOG(LogTemp, Log, TEXT("HEAL: soft fail %s — already healed"), *SpiritId.ToString());
		return false;
	}

	UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		return false;
	}

	if (!Inv->HasHealResource(1))
	{
		UE_LOG(LogTemp, Log, TEXT("HEAL: soft fail %s — no RES_HERB or RES_SEED"), *SpiritId.ToString());
		return false;
	}

	const FName Spent = Inv->SpendHealResource();
	if (Spent.IsNone())
	{
		UE_LOG(LogTemp, Log, TEXT("HEAL: soft fail %s — spend failed"), *SpiritId.ToString());
		return false;
	}

	SetHealState(EHomeWorldSpiritHealState::Healed);
	UE_LOG(LogTemp, Log, TEXT("HEAL: success %s consumed %s"), *SpiritId.ToString(), *Spent.ToString());
	return true;
}
