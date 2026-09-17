// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldPlayWorld.h"
#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldSpiritHealComponent.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

const TCHAR* UHomeWorldSaveGameSubsystem::DefaultSlotName = TEXT("HomeWorldSave");

void UHomeWorldSaveGameSubsystem::CaptureNPSessionState(UHomeWorldSaveGame* SaveGame, UWorld* World)
{
	if (!SaveGame || !World)
	{
		return;
	}

	UGameInstance* GI = World->GetGameInstance();
	if (UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr)
	{
		Inv->CopySlotsTo(SaveGame->SavedInventorySlots);
	}

	SaveGame->SavedBeastTameState = 0;
	SaveGame->SavedSpiritHealIds.Reset();
	SaveGame->SavedSpiritHealStates.Reset();
	SaveGame->bSavedN1Nurtured = false;
	SaveGame->bSavedN2Nurtured = false;

	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		if (UHomeWorldBeastTameComponent* Tame = Actor->FindComponentByClass<UHomeWorldBeastTameComponent>())
		{
			SaveGame->SavedBeastTameState = static_cast<uint8>(Tame->GetTameState());
		}
		if (UHomeWorldSpiritHealComponent* Heal = Actor->FindComponentByClass<UHomeWorldSpiritHealComponent>())
		{
			SaveGame->SavedSpiritHealIds.Add(Heal->GetSpiritId());
			SaveGame->SavedSpiritHealStates.Add(static_cast<uint8>(Heal->GetHealState()));
		}
		if (UHomeWorldNurtureComponent* Nurture = Actor->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
			{
				SaveGame->bSavedN1Nurtured = Nurture->GetIsNurtured();
			}
			else if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N2_Stored)
			{
				SaveGame->bSavedN2Nurtured = Nurture->GetIsNurtured();
			}
		}
	}
}

void UHomeWorldSaveGameSubsystem::ApplyNPSessionState(const UHomeWorldSaveGame* SaveGame, UWorld* World)
{
	if (!SaveGame || !World)
	{
		return;
	}

	UGameInstance* GI = World->GetGameInstance();
	if (UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr)
	{
		if (SaveGame->SavedInventorySlots.Num() == HomeWorldInventory::SlotCount)
		{
			Inv->RestoreSlotsFrom(SaveGame->SavedInventorySlots);
		}
	}

	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		if (UHomeWorldBeastTameComponent* Tame = Actor->FindComponentByClass<UHomeWorldBeastTameComponent>())
		{
			Tame->ApplyPersistedState(static_cast<EHomeWorldBeastTameState>(SaveGame->SavedBeastTameState));
		}
		if (UHomeWorldSpiritHealComponent* Heal = Actor->FindComponentByClass<UHomeWorldSpiritHealComponent>())
		{
			const FName Id = Heal->GetSpiritId();
			const int32 Idx = SaveGame->SavedSpiritHealIds.IndexOfByKey(Id);
			if (SaveGame->SavedSpiritHealStates.IsValidIndex(Idx))
			{
				Heal->ApplyPersistedState(static_cast<EHomeWorldSpiritHealState>(SaveGame->SavedSpiritHealStates[Idx]));
			}
		}
		if (UHomeWorldNurtureComponent* Nurture = Actor->FindComponentByClass<UHomeWorldNurtureComponent>())
		{
			if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
			{
				Nurture->ApplyPersistedNurtured(SaveGame->bSavedN1Nurtured);
			}
			else if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N2_Stored)
			{
				Nurture->ApplyPersistedNurtured(SaveGame->bSavedN2Nurtured);
			}
		}
	}
}

bool UHomeWorldSaveGameSubsystem::PersistDawnSnapshot()
{
	UWorld* World = HomeWorldPlayWorld::ResolveFromGameInstance(GetGameInstance());
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("DAWN: persist skipped — no world"));
		return false;
	}

	const bool bOk = SaveGameToSlot(FString(), 0);
	const UHomeWorldInventorySubsystem* Inv = GetGameInstance()->GetSubsystem<UHomeWorldInventorySubsystem>();
	const int32 Physical = Inv ? Inv->GetTotalPhysicalGoods() : 0;
	UE_LOG(LogTemp, Log, TEXT("DAWN: persisted inventory=%d tame+heal+nurture in slot '%s' (%s)"),
		Physical, DefaultSlotName, bOk ? TEXT("ok") : TEXT("failed"));
	return bOk;
}

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
		CaptureNPSessionState(SaveGame, World);
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
		ApplyNPSessionState(SaveGame, World);
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
