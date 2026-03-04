// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "Kismet/GameplayStatics.h"

const TCHAR* UHomeWorldSaveGameSubsystem::DefaultSlotName = TEXT("HomeWorldSave");

bool UHomeWorldSaveGameSubsystem::SaveGameToSlot(const FString& SlotName, int32 UserIndex)
{
	const FString Slot = SlotName.IsEmpty() ? DefaultSlotName : SlotName;
	UGameInstance* GI = GetGameInstance();
	if (!GI)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Save failed - no GameInstance"));
		return false;
	}

	UHomeWorldSaveGame* SaveGame = Cast<UHomeWorldSaveGame>(UGameplayStatics::CreateSaveGameObject(UHomeWorldSaveGame::StaticClass()));
	if (!SaveGame)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Save failed - could not create SaveGame object"));
		return false;
	}

	if (UHomeWorldFamilySubsystem* Family = GI->GetSubsystem<UHomeWorldFamilySubsystem>())
	{
		Family->SerializeToSaveGame(SaveGame);
	}
	if (UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>())
	{
		Spirits->SerializeToSaveGame(SaveGame);
	}

	bool bSaved = UGameplayStatics::SaveGameToSlot(SaveGame, Slot, UserIndex);
	if (bSaved)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Save completed to slot '%s' (roles=%d, spirits=%d)"),
			*Slot, SaveGame->SavedRoleBySpawnIndex.Num(), SaveGame->SavedSpiritIds.Num());
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SaveGameToSlot failed for '%s'"), *Slot);
	}
	return bSaved;
}

bool UHomeWorldSaveGameSubsystem::LoadGameFromSlot(const FString& SlotName, int32 UserIndex)
{
	const FString Slot = SlotName.IsEmpty() ? DefaultSlotName : SlotName;
	UGameInstance* GI = GetGameInstance();
	if (!GI)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Load failed - no GameInstance"));
		return false;
	}

	USaveGame* Loaded = UGameplayStatics::LoadGameFromSlot(Slot, UserIndex);
	UHomeWorldSaveGame* SaveGame = Cast<UHomeWorldSaveGame>(Loaded);
	if (!SaveGame)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Load failed - no save in slot '%s' or wrong type"), *Slot);
		return false;
	}

	int32 RolesRestored = 0;
	int32 SpiritsRestored = 0;
	if (UHomeWorldFamilySubsystem* Family = GI->GetSubsystem<UHomeWorldFamilySubsystem>())
	{
		Family->DeserializeFromSaveGame(SaveGame);
		RolesRestored = Family->GetMemberCount();
	}
	if (UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>())
	{
		Spirits->DeserializeFromSaveGame(SaveGame);
		SpiritsRestored = Spirits->GetSpiritCount();
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Load completed from slot '%s' (roles=%d, spirits=%d)"),
		*Slot, RolesRestored, SpiritsRestored);
	return true;
}

bool UHomeWorldSaveGameSubsystem::DoesSaveGameExist(const FString& SlotName, int32 UserIndex) const
{
	const FString Slot = SlotName.IsEmpty() ? DefaultSlotName : SlotName;
	return UGameplayStatics::DoesSaveGameExist(Slot, UserIndex);
}
