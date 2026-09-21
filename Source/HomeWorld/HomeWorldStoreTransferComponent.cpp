// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldStoreTransferComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"

UHomeWorldStoreTransferComponent::UHomeWorldStoreTransferComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UHomeWorldStoreTransferComponent::ConfigureResource(FName InResourceId)
{
	ResourceId = HomeWorldInventory::NormalizeResourceId(InResourceId);
}

void UHomeWorldStoreTransferComponent::SetStoredCountForCraft(const int32 NewCount)
{
	StoredCount = FMath::Clamp(NewCount, 0, MaxStored);
}

UHomeWorldInventorySubsystem* UHomeWorldStoreTransferComponent::GetInventory(AHomeWorldCharacter* Character) const
{
	if (!Character)
	{
		return nullptr;
	}
	UWorld* World = Character->GetWorld();
	if (!World)
	{
		return nullptr;
	}
	UGameInstance* GI = World->GetGameInstance();
	return GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
}

bool UHomeWorldStoreTransferComponent::TryDeposit(UHomeWorldInventorySubsystem* Inv)
{
	const FName Id = HomeWorldInventory::NormalizeResourceId(ResourceId);
	if (!Inv || !HomeWorldInventory::IsValidResourceId(Id))
	{
		return false;
	}
	if (StoredCount >= MaxStored)
	{
		UE_LOG(LogTemp, Log, TEXT("STORE: deposit fail %s — store full (%d/%d)"), *Id.ToString(), StoredCount, MaxStored);
		return false;
	}
	if (!Inv->SpendResource(Id, 1))
	{
		return false;
	}
	StoredCount++;
	UE_LOG(LogTemp, Log, TEXT("STORE: deposit %s inventory->stored count=%d"), *Id.ToString(), StoredCount);
	return true;
}

bool UHomeWorldStoreTransferComponent::TryWithdraw(UHomeWorldInventorySubsystem* Inv)
{
	const FName Id = HomeWorldInventory::NormalizeResourceId(ResourceId);
	if (!Inv || !HomeWorldInventory::IsValidResourceId(Id) || StoredCount <= 0)
	{
		return false;
	}
	if (!Inv->TryAddResource(Id, 1))
	{
		UE_LOG(LogTemp, Log, TEXT("STORE: withdraw fail %s — inventory full"), *Id.ToString());
		return false;
	}
	StoredCount--;
	UE_LOG(LogTemp, Log, TEXT("STORE: withdraw %s stored->inventory count=%d"), *Id.ToString(), StoredCount);
	return true;
}

bool UHomeWorldStoreTransferComponent::TryTransfer(AHomeWorldCharacter* Character)
{
	UHomeWorldInventorySubsystem* Inv = GetInventory(Character);
	if (!Inv)
	{
		UE_LOG(LogTemp, Log, TEXT("STORE: fail — no inventory subsystem"));
		return false;
	}
	if (TryDeposit(Inv))
	{
		return true;
	}
	if (TryWithdraw(Inv))
	{
		return true;
	}
	UE_LOG(LogTemp, Log, TEXT("STORE: soft fail %s — nothing to deposit or withdraw"), *ResourceId.ToString());
	return false;
}
