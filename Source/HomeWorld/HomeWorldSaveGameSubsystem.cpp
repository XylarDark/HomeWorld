// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldPlayWorld.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldSaveSlices.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

const TCHAR* UHomeWorldSaveGameSubsystem::DefaultSlotName = TEXT("HomeWorldSave");

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

	HomeWorldSaveSlices::CaptureToSave(SaveGame, GI, GI->GetWorld());

	bool bSaved = UGameplayStatics::SaveGameToSlot(SaveGame, Slot, UserIndex);
	if (bSaved)
	{
		const UHomeWorldFamilySubsystem* Family = GI->GetSubsystem<UHomeWorldFamilySubsystem>();
		const UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Save completed to slot '%s' (roles=%d, spirits=%d, phase=%d)"),
			*Slot, Family ? Family->GetMemberCount() : 0, Spirits ? Spirits->GetSpiritCount() : 0,
			static_cast<int32>(HomeWorldSaveSlices::GetSavedPhase(SaveGame)));
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

	// Read the pawn before anything is restored, as the old order did: the load forces below
	// depend on the rescue and the form the player is in now, not on what the save says.
	UWorld* World = GI->GetWorld();
	bool bRescueDone = false;
	bool bSpirit = false;
	if (World)
	{
		if (APlayerController* PC = World->GetFirstPlayerController())
		{
			if (AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(PC->GetPawn()))
			{
				bSpirit = Character->GetIsSpiritForm();
				if (const UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>())
				{
					bRescueDone = Stealth->IsCaptiveFreed();
				}
			}
		}
	}

	HomeWorldSaveSlices::ApplyFromSave(SaveGame, GI, World);

	const uint8 SavedPhase = HomeWorldSaveSlices::GetSavedPhase(SaveGame);
	int32 RolesRestored = 0;
	int32 SpiritsRestored = 0;
	if (UHomeWorldFamilySubsystem* Family = GI->GetSubsystem<UHomeWorldFamilySubsystem>())
	{
		RolesRestored = Family->GetMemberCount();
		const bool bNight = SavedPhase == static_cast<uint8>(EHomeWorldTimeOfDayPhase::Night);
		Family->ApplyLoadForces(bRescueDone, bNight || bSpirit, World);
	}
	if (const UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>())
	{
		SpiritsRestored = Spirits->GetSpiritCount();
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Load completed from slot '%s' (roles=%d, spirits=%d, phase=%d)"),
		*Slot, RolesRestored, SpiritsRestored, static_cast<int32>(SavedPhase));
	return true;
}

bool UHomeWorldSaveGameSubsystem::DoesSaveGameExist(const FString& SlotName, int32 UserIndex) const
{
	const FString Slot = SlotName.IsEmpty() ? DefaultSlotName : SlotName;
	return UGameplayStatics::DoesSaveGameExist(Slot, UserIndex);
}
