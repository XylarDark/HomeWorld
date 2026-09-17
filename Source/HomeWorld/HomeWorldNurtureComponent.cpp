// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldNurtureComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

namespace
{
	const TCHAR* NurtureTargetLabel(EHomeWorldNurtureTargetId Id)
	{
		switch (Id)
		{
		case EHomeWorldNurtureTargetId::N1_Crop: return TEXT("N1_Crop");
		case EHomeWorldNurtureTargetId::N2_Stored: return TEXT("N2_Stored");
		default: return TEXT("Nurture");
		}
	}
}

UHomeWorldNurtureComponent::UHomeWorldNurtureComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UHomeWorldNurtureComponent::BeginPlay()
{
	Super::BeginPlay();

	if (TargetId == EHomeWorldNurtureTargetId::N2_Stored && RequiredResourceId.IsNone())
	{
		RequiredResourceId = HomeWorldInventory::RES_WOOD;
	}
	if (TargetId == EHomeWorldNurtureTargetId::N1_Crop && RequiredResourceId.IsNone())
	{
		RequiredResourceId = HomeWorldInventory::RES_SEED;
	}

	if (AActor* Owner = GetOwner())
	{
		Owner->Tags.AddUnique(FName(TEXT("NurtureTarget")));
		Owner->Tags.AddUnique(FName(TargetLabel()));
	}

	UE_LOG(LogTemp, Log, TEXT("NURTURE: component ready target=%s nurtured=%d requires=%s"),
		*TargetLabel().ToString(), bNurtured ? 1 : 0, *RequiredResourceId.ToString());
}

FName UHomeWorldNurtureComponent::TargetLabel() const
{
	return FName(NurtureTargetLabel(TargetId));
}

void UHomeWorldNurtureComponent::ConfigureTarget(EHomeWorldNurtureTargetId InTarget, FName InRequiredResource)
{
	TargetId = InTarget;
	if (!InRequiredResource.IsNone())
	{
		RequiredResourceId = InRequiredResource;
	}
	else if (TargetId == EHomeWorldNurtureTargetId::N2_Stored)
	{
		RequiredResourceId = HomeWorldInventory::RES_WOOD;
	}
	else
	{
		RequiredResourceId = HomeWorldInventory::RES_SEED;
	}
}

void UHomeWorldNurtureComponent::ApplyPersistedNurtured(bool bInNurtured)
{
	if (bNurtured == bInNurtured)
	{
		return;
	}
	bNurtured = bInNurtured;
	UE_LOG(LogTemp, Log, TEXT("NURTURE: %s M_Nurtured=%d (restored)"), *TargetLabel().ToString(), bNurtured ? 1 : 0);
}

bool UHomeWorldNurtureComponent::IsNightSpiritHomesteadAllowed(AHomeWorldCharacter* Character) const
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

bool UHomeWorldNurtureComponent::TryNurture(AHomeWorldCharacter* Character)
{
	if (!Character || !GetOwner())
	{
		return false;
	}

	if (!IsNightSpiritHomesteadAllowed(Character))
	{
		UE_LOG(LogTemp, Log, TEXT("NURTURE: soft fail %s — day or body form"), *TargetLabel().ToString());
		return false;
	}

	if (bNurtured)
	{
		UE_LOG(LogTemp, Log, TEXT("NURTURE: soft success %s — already nurtured (M_Nurtured on)"), *TargetLabel().ToString());
		return true;
	}

	UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		return false;
	}

	if (Inv->GetResource(RequiredResourceId) < 1)
	{
		UE_LOG(LogTemp, Log, TEXT("NURTURE: soft fail %s — no %s in inventory"),
			*TargetLabel().ToString(), *RequiredResourceId.ToString());
		return false;
	}

	if (!Inv->SpendResource(RequiredResourceId, 1))
	{
		UE_LOG(LogTemp, Log, TEXT("NURTURE: soft fail %s — spend failed"), *TargetLabel().ToString());
		return false;
	}

	bNurtured = true;
	UE_LOG(LogTemp, Log, TEXT("NURTURE: success %s M_Nurtured=1 consumed 1x %s"),
		*TargetLabel().ToString(), *RequiredResourceId.ToString());
	return true;
}
