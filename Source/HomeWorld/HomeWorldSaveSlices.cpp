// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSaveSlices.h"
#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldSpiritHealComponent.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "EngineUtils.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "Serialization/MemoryReader.h"
#include "Serialization/MemoryWriter.h"

namespace HomeWorldSaveSlices
{
	const TArray<FName>& GetKeys()
	{
		static const TArray<FName> Keys = {
			FName(Key::Family), FName(Key::SpiritRoster), FName(Key::TimeOfDay), FName(Key::PlayerState),
			FName(Key::Inventory), FName(Key::Tame), FName(Key::Heal), FName(Key::Nurture)};
		return Keys;
	}

	const TArray<FFieldToKey>& GetFieldToKeyTable()
	{
		static const TArray<FFieldToKey> Table = {
			{FName(TEXT("SavedRoleBySpawnIndex")), FName(Key::Family)},
			{FName(TEXT("bSavedPartnerOut")), FName(Key::Family)},
			{FName(TEXT("bSavedChildOut")), FName(Key::Family)},
			{FName(TEXT("SavedSpiritIds")), FName(Key::SpiritRoster)},
			{FName(TEXT("SavedTimeOfDayPhase")), FName(Key::TimeOfDay)},
			{FName(TEXT("SavedSpiritualPowerCollected")), FName(Key::PlayerState)},
			{FName(TEXT("bSavedHasDayRestorationBuff")), FName(Key::PlayerState)},
			{FName(TEXT("SavedLoveLevel")), FName(Key::PlayerState)},
			{FName(TEXT("SavedInventorySlots")), FName(Key::Inventory)},
			{FName(TEXT("SavedBeastTameState")), FName(Key::Tame)},
			{FName(TEXT("SavedSpiritHealIds")), FName(Key::Heal)},
			{FName(TEXT("SavedSpiritHealStates")), FName(Key::Heal)},
			{FName(TEXT("bSavedN1Nurtured")), FName(Key::Nurture)},
			{FName(TEXT("bSavedN2Nurtured")), FName(Key::Nurture)},
		};
		return Table;
	}

	bool HasSlice(const UHomeWorldSaveGame* Save, FName InKey)
	{
		return Save && Save->Slices.Contains(InKey);
	}

	static AHomeWorldPlayerState* FindPlayerState(UWorld* World)
	{
		APlayerController* PC = World ? World->GetFirstPlayerController() : nullptr;
		return PC ? PC->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
	}

	/** The old-save fallback: the pre-slice apply, unchanged. */
	static void ApplyFlat(const UHomeWorldSaveGame* SaveGame, UGameInstance* GI, UWorld* World)
	{
		if (!SaveGame)
		{
			return;
		}
		if (UHomeWorldFamilySubsystem* Family = GI ? GI->GetSubsystem<UHomeWorldFamilySubsystem>() : nullptr)
		{
			Family->DeserializeFromSaveGame(SaveGame);
		}
		if (UHomeWorldSpiritRosterSubsystem* Spirits = GI ? GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>() : nullptr)
		{
			Spirits->DeserializeFromSaveGame(SaveGame);
		}
		if (!World)
		{
			return;
		}
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			const EHomeWorldTimeOfDayPhase Phase = static_cast<EHomeWorldTimeOfDayPhase>(SaveGame->SavedTimeOfDayPhase);
			TimeOfDay->SetPhase(Phase);
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: TimeOfDay phase restored to %d"), static_cast<int32>(Phase));
		}
		if (AHomeWorldPlayerState* PS = FindPlayerState(World))
		{
			PS->SetSpiritualPowerCollected(SaveGame->SavedSpiritualPowerCollected);
			PS->SetDayRestorationBuff(SaveGame->bSavedHasDayRestorationBuff);
			PS->SetLoveLevel(SaveGame->SavedLoveLevel);
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual power=%d, day buff=%d, loveLevel=%d restored"),
				SaveGame->SavedSpiritualPowerCollected, SaveGame->bSavedHasDayRestorationBuff ? 1 : 0, SaveGame->SavedLoveLevel);
		}
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
				const int32 Idx = SaveGame->SavedSpiritHealIds.IndexOfByKey(Heal->GetSpiritId());
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

	void SerializeName(FArchive& Ar, FName& Name)
	{
		FString Text = Name.ToString();
		Ar << Text;
		if (Ar.IsLoading())
		{
			Name = FName(*Text);
		}
	}

	void SerializeNames(FArchive& Ar, TArray<FName>& Names)
	{
		int32 Num = Names.Num();
		Ar << Num;
		if (Ar.IsLoading())
		{
			Names.Reset();
			if (Num < 0 || Ar.IsError())
			{
				Ar.SetError();
				return;
			}
		}
		for (int32 Index = 0; Index < Num && !Ar.IsError(); ++Index)
		{
			FName Name = Ar.IsLoading() ? NAME_None : Names[Index];
			SerializeName(Ar, Name);
			if (Ar.IsLoading())
			{
				Names.Add(Name);
			}
		}
	}

	// ---- One writer and one reader per key. Each touches only its own system. ----

	static void WriteTimeOfDay(UWorld* World, TArray<uint8>& Out)
	{
		const UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
		if (!TimeOfDay)
		{
			return;
		}
		FMemoryWriter Ar(Out);
		uint8 Phase = static_cast<uint8>(TimeOfDay->GetCurrentPhase());
		Ar << Phase;
	}

	static bool ReadPhase(const TArray<uint8>& In, uint8& OutPhase)
	{
		FMemoryReader Ar(In);
		Ar << OutPhase;
		return !Ar.IsError();
	}

	static void ReadTimeOfDay(UWorld* World, const TArray<uint8>& In)
	{
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
		uint8 Phase = 0;
		if (TimeOfDay && ReadPhase(In, Phase))
		{
			TimeOfDay->SetPhase(static_cast<EHomeWorldTimeOfDayPhase>(Phase));
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: TimeOfDay phase restored to %d"), static_cast<int32>(Phase));
		}
	}

	static void WritePlayerState(UWorld* World, TArray<uint8>& Out)
	{
		const AHomeWorldPlayerState* PS = FindPlayerState(World);
		if (!PS)
		{
			return;
		}
		FMemoryWriter Ar(Out);
		int32 Power = PS->GetSpiritualPowerCollected();
		bool bDayBuff = PS->GetHasDayRestorationBuff();
		int32 Love = PS->GetLoveLevel();
		Ar << Power << bDayBuff << Love;
	}

	static void ReadPlayerState(UWorld* World, const TArray<uint8>& In)
	{
		AHomeWorldPlayerState* PS = FindPlayerState(World);
		if (!PS)
		{
			return;
		}
		FMemoryReader Ar(In);
		int32 Power = 0;
		bool bDayBuff = false;
		int32 Love = 0;
		Ar << Power << bDayBuff << Love;
		if (Ar.IsError())
		{
			return;
		}
		PS->SetSpiritualPowerCollected(Power);
		PS->SetDayRestorationBuff(bDayBuff);
		PS->SetLoveLevel(Love);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual power=%d, day buff=%d, loveLevel=%d restored"), Power, bDayBuff ? 1 : 0, Love);
	}

	static void WriteInventory(UGameInstance* GI, TArray<uint8>& Out)
	{
		const UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
		if (!Inv)
		{
			return;
		}
		TArray<FHomeWorldInventorySlot> Slots;
		Inv->CopySlotsTo(Slots);
		FMemoryWriter Ar(Out);
		int32 Num = Slots.Num();
		Ar << Num;
		for (FHomeWorldInventorySlot& Slot : Slots)
		{
			SerializeName(Ar, Slot.ResId);
			Ar << Slot.Count;
		}
	}

	static void ReadInventory(UGameInstance* GI, const TArray<uint8>& In)
	{
		UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
		if (!Inv)
		{
			return;
		}
		FMemoryReader Ar(In);
		int32 Num = 0;
		Ar << Num;
		if (Ar.IsError() || Num != HomeWorldInventory::SlotCount)
		{
			return;
		}
		TArray<FHomeWorldInventorySlot> Slots;
		Slots.SetNum(Num);
		for (FHomeWorldInventorySlot& Slot : Slots)
		{
			SerializeName(Ar, Slot.ResId);
			Ar << Slot.Count;
		}
		if (!Ar.IsError())
		{
			Inv->RestoreSlotsFrom(Slots);
		}
	}

	static void WriteTame(UWorld* World, TArray<uint8>& Out)
	{
		uint8 State = 0;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (const UHomeWorldBeastTameComponent* Tame = *It ? It->FindComponentByClass<UHomeWorldBeastTameComponent>() : nullptr)
			{
				State = static_cast<uint8>(Tame->GetTameState());
			}
		}
		FMemoryWriter Ar(Out);
		Ar << State;
	}

	static void ReadTame(UWorld* World, const TArray<uint8>& In)
	{
		FMemoryReader Ar(In);
		uint8 State = 0;
		Ar << State;
		if (Ar.IsError())
		{
			return;
		}
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (UHomeWorldBeastTameComponent* Tame = *It ? It->FindComponentByClass<UHomeWorldBeastTameComponent>() : nullptr)
			{
				Tame->ApplyPersistedState(static_cast<EHomeWorldBeastTameState>(State));
			}
		}
	}

	static void WriteHeal(UWorld* World, TArray<uint8>& Out)
	{
		TArray<FName> Ids;
		TArray<uint8> States;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (const UHomeWorldSpiritHealComponent* Heal = *It ? It->FindComponentByClass<UHomeWorldSpiritHealComponent>() : nullptr)
			{
				Ids.Add(Heal->GetSpiritId());
				States.Add(static_cast<uint8>(Heal->GetHealState()));
			}
		}
		FMemoryWriter Ar(Out);
		SerializeNames(Ar, Ids);
		Ar << States;
	}

	static void ReadHeal(UWorld* World, const TArray<uint8>& In)
	{
		FMemoryReader Ar(In);
		TArray<FName> Ids;
		TArray<uint8> States;
		SerializeNames(Ar, Ids);
		Ar << States;
		if (Ar.IsError())
		{
			return;
		}
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (UHomeWorldSpiritHealComponent* Heal = *It ? It->FindComponentByClass<UHomeWorldSpiritHealComponent>() : nullptr)
			{
				const int32 Idx = Ids.IndexOfByKey(Heal->GetSpiritId());
				if (States.IsValidIndex(Idx))
				{
					Heal->ApplyPersistedState(static_cast<EHomeWorldSpiritHealState>(States[Idx]));
				}
			}
		}
	}

	static void WriteNurture(UWorld* World, TArray<uint8>& Out)
	{
		bool bN1 = false;
		bool bN2 = false;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (const UHomeWorldNurtureComponent* Nurture = *It ? It->FindComponentByClass<UHomeWorldNurtureComponent>() : nullptr)
			{
				if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
				{
					bN1 = Nurture->GetIsNurtured();
				}
				else if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N2_Stored)
				{
					bN2 = Nurture->GetIsNurtured();
				}
			}
		}
		FMemoryWriter Ar(Out);
		Ar << bN1 << bN2;
	}

	static void ReadNurture(UWorld* World, const TArray<uint8>& In)
	{
		FMemoryReader Ar(In);
		bool bN1 = false;
		bool bN2 = false;
		Ar << bN1 << bN2;
		if (Ar.IsError())
		{
			return;
		}
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (UHomeWorldNurtureComponent* Nurture = *It ? It->FindComponentByClass<UHomeWorldNurtureComponent>() : nullptr)
			{
				if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N1_Crop)
				{
					Nurture->ApplyPersistedNurtured(bN1);
				}
				else if (Nurture->GetTargetId() == EHomeWorldNurtureTargetId::N2_Stored)
				{
					Nurture->ApplyPersistedNurtured(bN2);
				}
			}
		}
	}

	/** Store Bytes under Key unless the writer had nothing to write (its system is absent). */
	static void Put(UHomeWorldSaveGame* Save, const TCHAR* InKey, TArray<uint8>&& Bytes)
	{
		if (Bytes.Num() > 0)
		{
			Save->Slices.FindOrAdd(FName(InKey)).Bytes = MoveTemp(Bytes);
		}
	}

	void CaptureToSave(UHomeWorldSaveGame* Save, UGameInstance* GI, UWorld* World)
	{
		if (!Save)
		{
			return;
		}
		Save->Slices.Reset();
		TArray<uint8> Bytes;
		if (const UHomeWorldFamilySubsystem* Family = GI ? GI->GetSubsystem<UHomeWorldFamilySubsystem>() : nullptr)
		{
			Family->WriteSaveSlice(Bytes);
			Put(Save, Key::Family, MoveTemp(Bytes));
		}
		Bytes.Reset();
		if (const UHomeWorldSpiritRosterSubsystem* Spirits = GI ? GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>() : nullptr)
		{
			Spirits->WriteSaveSlice(Bytes);
			Put(Save, Key::SpiritRoster, MoveTemp(Bytes));
		}
		Bytes.Reset();
		WriteInventory(GI, Bytes);
		Put(Save, Key::Inventory, MoveTemp(Bytes));
		if (!World)
		{
			return;
		}
		Bytes.Reset();
		WriteTimeOfDay(World, Bytes);
		Put(Save, Key::TimeOfDay, MoveTemp(Bytes));
		Bytes.Reset();
		WritePlayerState(World, Bytes);
		Put(Save, Key::PlayerState, MoveTemp(Bytes));
		Bytes.Reset();
		WriteTame(World, Bytes);
		Put(Save, Key::Tame, MoveTemp(Bytes));
		Bytes.Reset();
		WriteHeal(World, Bytes);
		Put(Save, Key::Heal, MoveTemp(Bytes));
		Bytes.Reset();
		WriteNurture(World, Bytes);
		Put(Save, Key::Nurture, MoveTemp(Bytes));
	}

	void ApplyFromSave(const UHomeWorldSaveGame* Save, UGameInstance* GI, UWorld* World)
	{
		if (!Save)
		{
			return;
		}
		if (Save->Slices.Num() == 0)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: save has no slices - reading the flat fields once (old save)"));
			ApplyFlat(Save, GI, World);
			return;
		}

		auto Find = [Save](const TCHAR* InKey) -> const TArray<uint8>*
		{
			const FHomeWorldSaveSlice* Slice = Save->Slices.Find(FName(InKey));
			return Slice ? &Slice->Bytes : nullptr;
		};

		if (const TArray<uint8>* Bytes = Find(Key::Family))
		{
			if (UHomeWorldFamilySubsystem* Family = GI ? GI->GetSubsystem<UHomeWorldFamilySubsystem>() : nullptr)
			{
				Family->ReadSaveSlice(*Bytes);
			}
		}
		if (const TArray<uint8>* Bytes = Find(Key::SpiritRoster))
		{
			if (UHomeWorldSpiritRosterSubsystem* Spirits = GI ? GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>() : nullptr)
			{
				Spirits->ReadSaveSlice(*Bytes);
			}
		}
		if (!World)
		{
			if (const TArray<uint8>* Bytes = Find(Key::Inventory))
			{
				ReadInventory(GI, *Bytes);
			}
			return;
		}
		// Same order as before slices: phase, player state, inventory, then the world's actors.
		if (const TArray<uint8>* Bytes = Find(Key::TimeOfDay))
		{
			ReadTimeOfDay(World, *Bytes);
		}
		if (const TArray<uint8>* Bytes = Find(Key::PlayerState))
		{
			ReadPlayerState(World, *Bytes);
		}
		if (const TArray<uint8>* Bytes = Find(Key::Inventory))
		{
			ReadInventory(GI, *Bytes);
		}
		if (const TArray<uint8>* Bytes = Find(Key::Tame))
		{
			ReadTame(World, *Bytes);
		}
		if (const TArray<uint8>* Bytes = Find(Key::Heal))
		{
			ReadHeal(World, *Bytes);
		}
		if (const TArray<uint8>* Bytes = Find(Key::Nurture))
		{
			ReadNurture(World, *Bytes);
		}
	}

	uint8 GetSavedPhase(const UHomeWorldSaveGame* Save)
	{
		if (!Save)
		{
			return 0;
		}
		if (Save->Slices.Num() == 0)
		{
			return Save->SavedTimeOfDayPhase;
		}
		const FHomeWorldSaveSlice* Slice = Save->Slices.Find(FName(Key::TimeOfDay));
		uint8 Phase = 0;
		return (Slice && ReadPhase(Slice->Bytes, Phase)) ? Phase : 0;
	}
}
