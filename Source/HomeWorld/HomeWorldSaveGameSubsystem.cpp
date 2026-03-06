// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

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

	UWorld* World = GI->GetWorld();
	if (World)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			SaveGame->SavedTimeOfDayPhase = static_cast<uint8>(TimeOfDay->GetCurrentPhase());
		}
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			if (AHomeWorldPlayerState* PS = PC->GetPlayerState<AHomeWorldPlayerState>())
			{
				SaveGame->SavedSpiritualPowerCollected = PS->GetSpiritualPowerCollected();
				SaveGame->bSavedHasDayRestorationBuff = PS->GetHasDayRestorationBuff();
				SaveGame->SavedLoveLevel = PS->GetLoveLevel();
			}
		}
	}

	bool bSaved = UGameplayStatics::SaveGameToSlot(SaveGame, Slot, UserIndex);
	if (bSaved)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Save completed to slot '%s' (roles=%d, spirits=%d, phase=%d, spiritualPower=%d, dayBuff=%d, loveLevel=%d)"),
			*Slot, SaveGame->SavedRoleBySpawnIndex.Num(), SaveGame->SavedSpiritIds.Num(), SaveGame->SavedTimeOfDayPhase, SaveGame->SavedSpiritualPowerCollected, SaveGame->bSavedHasDayRestorationBuff ? 1 : 0, SaveGame->SavedLoveLevel);
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

	UWorld* World = GI->GetWorld();
	if (World)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			const EHomeWorldTimeOfDayPhase Phase = static_cast<EHomeWorldTimeOfDayPhase>(SaveGame->SavedTimeOfDayPhase);
			TimeOfDay->SetPhase(Phase);
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: TimeOfDay phase restored to %d"), static_cast<int32>(Phase));
		}
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			if (AHomeWorldPlayerState* PS = PC->GetPlayerState<AHomeWorldPlayerState>())
			{
				PS->SetSpiritualPowerCollected(SaveGame->SavedSpiritualPowerCollected);
				PS->SetDayRestorationBuff(SaveGame->bSavedHasDayRestorationBuff);
				PS->SetLoveLevel(SaveGame->SavedLoveLevel);
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual power=%d, day buff=%d, loveLevel=%d restored"), SaveGame->SavedSpiritualPowerCollected, SaveGame->bSavedHasDayRestorationBuff ? 1 : 0, SaveGame->SavedLoveLevel);
			}
		}
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Load completed from slot '%s' (roles=%d, spirits=%d, phase=%d, spiritualPower=%d, dayBuff=%d, loveLevel=%d)"),
		*Slot, RolesRestored, SpiritsRestored, SaveGame->SavedTimeOfDayPhase, SaveGame->SavedSpiritualPowerCollected, SaveGame->bSavedHasDayRestorationBuff ? 1 : 0, SaveGame->SavedLoveLevel);
	return true;
}

bool UHomeWorldSaveGameSubsystem::DoesSaveGameExist(const FString& SlotName, int32 UserIndex) const
{
	const FString Slot = SlotName.IsEmpty() ? DefaultSlotName : SlotName;
	return UGameplayStatics::DoesSaveGameExist(Slot, UserIndex);
}
