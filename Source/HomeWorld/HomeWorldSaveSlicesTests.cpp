// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldNurtureComponent.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldQuestLog.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldSaveSlices.h"
#include "HomeWorldSpiritHealComponent.h"
#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldTestWorld.h"
#include "Engine/GameInstance.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "UObject/UnrealType.h"

namespace HomeWorldSaveSlicesTest
{
	/** Every flat field of the save: the UPROPERTYs named Saved* or bSaved*. */
	static TArray<FProperty*> FlatFields()
	{
		TArray<FProperty*> Out;
		for (TFieldIterator<FProperty> It(UHomeWorldSaveGame::StaticClass(), EFieldIteratorFlags::ExcludeSuper); It; ++It)
		{
			const FString Name = It->GetName();
			if (Name.StartsWith(TEXT("Saved")) || Name.StartsWith(TEXT("bSaved")))
			{
				Out.Add(*It);
			}
		}
		return Out;
	}

	/** The quest ids a key must not collide with: the two chain ids and every step id. */
	static TSet<FName> QuestIds()
	{
		TSet<FName> Ids;
		// Chain ids as AHomeWorldCharacter registers them with the quest log.
		Ids.Add(FName(TEXT("Opening")));
		Ids.Add(FName(TEXT("home_loop")));
		for (const FHomeWorldQuestStep& Step : UHomeWorldQuestLog::BuildOpeningSteps(FHomeWorldOpeningQuestFacts()))
		{
			Ids.Add(Step.Id);
		}
		for (const FHomeWorldQuestStep& Step : UHomeWorldQuestLog::BuildHomeLoopSteps(FHomeWorldHomeLoopQuestFacts()))
		{
			Ids.Add(Step.Id);
		}
		return Ids;
	}

	/**
	 * Everything the save touches, in one throwaway world: a game instance (family, spirit
	 * roster, inventory), a player controller holding a HomeWorld player state, one beast,
	 * two spirit wisps and both nurture targets.
	 */
	struct FRig
	{
		HomeWorldTestWorld::FScopedWorld Scoped;
		UGameInstance* GI = nullptr;
		AHomeWorldPlayerState* PS = nullptr;
		APlayerController* FirstPC = nullptr;
		UHomeWorldBeastTameComponent* Tame = nullptr;
		UHomeWorldSpiritHealComponent* HealA = nullptr;
		UHomeWorldSpiritHealComponent* HealB = nullptr;
		UHomeWorldNurtureComponent* N1 = nullptr;
		UHomeWorldNurtureComponent* N2 = nullptr;

		explicit FRig(const TCHAR* What)
			: Scoped(What)
		{
			UWorld* World = Scoped.World;
			if (!World || !GEngine)
			{
				return;
			}
			GI = NewObject<UGameInstance>(GEngine);
			GI->Init();

			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			APlayerController* PC = World->SpawnActor<APlayerController>(Params);
			PS = World->SpawnActor<AHomeWorldPlayerState>(Params);
			if (PC && PS)
			{
				PC->PlayerState = PS;
				// The save reaches the player state through World->GetFirstPlayerController().
				// A controller spawned without a game mode is not always on that list.
				if (World->GetFirstPlayerController() != PC)
				{
					World->AddController(PC);
				}
			}
			FirstPC = PC;

			Tame = AddComponent<UHomeWorldBeastTameComponent>(World);
			HealA = AddComponent<UHomeWorldSpiritHealComponent>(World);
			HealB = AddComponent<UHomeWorldSpiritHealComponent>(World);
			N1 = AddComponent<UHomeWorldNurtureComponent>(World);
			N2 = AddComponent<UHomeWorldNurtureComponent>(World);
			if (HealA && HealB && N1 && N2)
			{
				HealA->ConfigureSpirit(FName(TEXT("Spirit_A")));
				HealB->ConfigureSpirit(FName(TEXT("Spirit_B")));
				N1->ConfigureTarget(EHomeWorldNurtureTargetId::N1_Crop, NAME_None);
				N2->ConfigureTarget(EHomeWorldNurtureTargetId::N2_Stored, NAME_None);
			}
		}

		template <typename T>
		static T* AddComponent(UWorld* World)
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			AActor* Owner = World->SpawnActor<AActor>(AActor::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, Params);
			if (!Owner)
			{
				return nullptr;
			}
			T* Comp = NewObject<T>(Owner);
			Comp->RegisterComponent();
			return Comp;
		}

		bool Ok(FAutomationTestBase* Test) const
		{
			return Scoped.Ok(Test)
				&& Test->TestNotNull(TEXT("game instance"), GI)
				&& Test->TestNotNull(TEXT("player state spawned"), PS)
				&& Test->TestTrue(TEXT("fixture: the first controller holds the player state"),
					FirstPC && Scoped.World->GetFirstPlayerController() == FirstPC && FirstPC->GetPlayerState<AHomeWorldPlayerState>() == PS)
				&& Test->TestTrue(TEXT("beast, wisps and nurture targets spawned"), Tame && HealA && HealB && N1 && N2)
				&& Test->TestNotNull(TEXT("family"), GI->GetSubsystem<UHomeWorldFamilySubsystem>())
				&& Test->TestNotNull(TEXT("spirit roster"), GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>())
				&& Test->TestNotNull(TEXT("inventory"), GI->GetSubsystem<UHomeWorldInventorySubsystem>());
		}
	};

	/** Through the save file format: SaveGameToMemory then LoadGameFromMemory. */
	static UHomeWorldSaveGame* ThroughDisk(UHomeWorldSaveGame* Save)
	{
		TArray<uint8> Bytes;
		if (!Save || !UGameplayStatics::SaveGameToMemory(Save, Bytes))
		{
			return nullptr;
		}
		return Cast<UHomeWorldSaveGame>(UGameplayStatics::LoadGameFromMemory(Bytes));
	}

	static TArray<FHomeWorldInventorySlot> OldInventory()
	{
		TArray<FHomeWorldInventorySlot> Slots;
		Slots.SetNum(HomeWorldInventory::SlotCount);
		Slots[0].ResId = HomeWorldInventory::RES_WOOD;
		Slots[0].Count = 3;
		Slots[1].ResId = HomeWorldInventory::RES_SEED;
		Slots[1].Count = 2;
		return Slots;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSaveSlicesFieldToKeyTest,
	"HomeWorld.Save.Slices.FieldToKeyTable",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSaveSlicesFieldToKeyTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldSaveSlices;

	const TArray<FName> Locked = {
		FName(TEXT("Family")), FName(TEXT("SpiritRoster")), FName(TEXT("TimeOfDay")), FName(TEXT("PlayerState")),
		FName(TEXT("Inventory")), FName(TEXT("Tame")), FName(TEXT("Heal")), FName(TEXT("Nurture"))};
	TestTrue(TEXT("the key list is exactly the locked eight, in order"), GetKeys() == Locked);

	const TArray<FProperty*> Fields = HomeWorldSaveSlicesTest::FlatFields();
	TestTrue(TEXT("the save has flat Saved* fields to map"), Fields.Num() > 0);

	const TArray<FFieldToKey>& Table = GetFieldToKeyTable();
	for (const FProperty* Field : Fields)
	{
		int32 Rows = 0;
		for (const FFieldToKey& Row : Table)
		{
			Rows += (Row.Field == Field->GetFName()) ? 1 : 0;
		}
		TestEqual(*FString::Printf(TEXT("%s maps to exactly one key"), *Field->GetName()), Rows, 1);
	}

	TSet<FName> Owned;
	for (const FFieldToKey& Row : Table)
	{
		const bool bIsField = Fields.ContainsByPredicate([&Row](const FProperty* P) { return P->GetFName() == Row.Field; });
		TestTrue(*FString::Printf(TEXT("table row %s names a flat Saved* field"), *Row.Field.ToString()), bIsField);
		TestTrue(*FString::Printf(TEXT("table row %s uses a listed key (%s)"), *Row.Field.ToString(), *Row.Key.ToString()),
			GetKeys().Contains(Row.Key));
		Owned.Add(Row.Key);
	}
	for (const FName& K : GetKeys())
	{
		TestTrue(*FString::Printf(TEXT("key %s owns at least one field (nothing new in the save)"), *K.ToString()), Owned.Contains(K));
	}

	const TSet<FName> Quests = HomeWorldSaveSlicesTest::QuestIds();
	TestTrue(TEXT("there are quest ids to check against"), Quests.Num() > 2);
	for (const FName& K : GetKeys())
	{
		TestFalse(*FString::Printf(TEXT("key %s is not also a quest id"), *K.ToString()), Quests.Contains(K));
	}
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSaveSlicesOldSaveRoundTripTest,
	"HomeWorld.Save.Slices.OldSaveRoundTrip",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSaveSlicesOldSaveRoundTripTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldSaveSlicesTest;

	// An old save: only the flat fields, every one off its default.
	UHomeWorldSaveGame* Old = NewObject<UHomeWorldSaveGame>();
	Old->SavedRoleBySpawnIndex = {static_cast<uint8>(EHomeWorldFamilyRole::Protector), static_cast<uint8>(EHomeWorldFamilyRole::Child)};
	Old->bSavedPartnerOut = true;
	Old->bSavedChildOut = true;
	Old->SavedSpiritIds = {FName(TEXT("Spirit_Test1")), FName(TEXT("Spirit_Test2"))};
	Old->SavedTimeOfDayPhase = static_cast<uint8>(EHomeWorldTimeOfDayPhase::Dusk);
	Old->SavedSpiritualPowerCollected = 7;
	Old->bSavedHasDayRestorationBuff = true;
	Old->SavedLoveLevel = 3;
	Old->SavedInventorySlots = OldInventory();
	Old->SavedBeastTameState = static_cast<uint8>(EHomeWorldBeastTameState::Cautious);
	Old->SavedSpiritHealIds = {FName(TEXT("Spirit_A")), FName(TEXT("Spirit_B"))};
	Old->SavedSpiritHealStates = {static_cast<uint8>(EHomeWorldSpiritHealState::Healed), static_cast<uint8>(EHomeWorldSpiritHealState::Healed)};
	Old->bSavedN1Nurtured = true;
	Old->bSavedN2Nurtured = true;

	const UHomeWorldSaveGame* Defaults = GetDefault<UHomeWorldSaveGame>();
	for (const FProperty* Field : FlatFields())
	{
		TestFalse(*FString::Printf(TEXT("fixture: old save sets %s off its default"), *Field->GetName()),
			Field->Identical_InContainer(Old, Defaults));
	}
	for (const FName& K : HomeWorldSaveSlices::GetKeys())
	{
		TestFalse(*FString::Printf(TEXT("fixture: old save has no %s slice"), *K.ToString()), HomeWorldSaveSlices::HasSlice(Old, K));
	}

	UHomeWorldSaveGame* OldOnDisk = ThroughDisk(Old);
	if (!TestNotNull(TEXT("old save survives the file format"), OldOnDisk))
	{
		return false;
	}

	// Load it, save it.
	UHomeWorldSaveGame* Resaved = NewObject<UHomeWorldSaveGame>();
	{
		FRig First(TEXT("save slices: first load"));
		if (!First.Ok(this))
		{
			return false;
		}
		HomeWorldSaveSlices::ApplyFromSave(OldOnDisk, First.GI, First.Scoped.World);
		HomeWorldSaveSlices::CaptureToSave(Resaved, First.GI, First.Scoped.World);
	}
	UHomeWorldSaveGame* ResavedOnDisk = ThroughDisk(Resaved);
	if (!TestNotNull(TEXT("re-save survives the file format"), ResavedOnDisk))
	{
		return false;
	}

	for (const FName& K : HomeWorldSaveSlices::GetKeys())
	{
		TestTrue(*FString::Printf(TEXT("re-save carries the %s slice"), *K.ToString()), HomeWorldSaveSlices::HasSlice(ResavedOnDisk, K));
	}
	for (const FProperty* Field : FlatFields())
	{
		TestTrue(*FString::Printf(TEXT("re-save writes only slices: %s stays default"), *Field->GetName()),
			Field->Identical_InContainer(ResavedOnDisk, Defaults));
	}

	// Reload into fresh systems, and read every value back from them.
	FRig Second(TEXT("save slices: reload"));
	if (!Second.Ok(this))
	{
		return false;
	}
	Second.Scoped.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	HomeWorldSaveSlices::ApplyFromSave(ResavedOnDisk, Second.GI, Second.Scoped.World);

	const UHomeWorldFamilySubsystem* Family = Second.GI->GetSubsystem<UHomeWorldFamilySubsystem>();
	TestEqual(TEXT("roles: member count"), Family->GetMemberCount(), 2);
	TestTrue(TEXT("roles: index 0 Protector"), Family->GetRoleForIndex(0) == EHomeWorldFamilyRole::Protector);
	TestTrue(TEXT("roles: index 1 Child"), Family->GetRoleForIndex(1) == EHomeWorldFamilyRole::Child);
	TestTrue(TEXT("partner out"), Family->IsPartnerOut());
	TestTrue(TEXT("child out"), Family->IsChildOut());

	const TArray<FName> Spirits = Second.GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>()->GetSpirits();
	TestTrue(TEXT("spirit roster"), Spirits == Old->SavedSpiritIds);

	TestTrue(TEXT("time of day is Dusk"), Second.Scoped.TimeOfDay->GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Dusk);

	TestEqual(TEXT("spiritual power"), Second.PS->GetSpiritualPowerCollected(), 7);
	TestTrue(TEXT("day restoration buff"), Second.PS->GetHasDayRestorationBuff());
	TestEqual(TEXT("love level"), Second.PS->GetLoveLevel(), 3);

	TArray<FHomeWorldInventorySlot> Slots;
	Second.GI->GetSubsystem<UHomeWorldInventorySubsystem>()->CopySlotsTo(Slots);
	const TArray<FHomeWorldInventorySlot> Expected = OldInventory();
	TestEqual(TEXT("inventory: slot count"), Slots.Num(), Expected.Num());
	for (int32 Index = 0; Index < FMath::Min(Slots.Num(), Expected.Num()); ++Index)
	{
		TestTrue(*FString::Printf(TEXT("inventory: slot %d"), Index),
			Slots[Index].ResId == Expected[Index].ResId && Slots[Index].Count == Expected[Index].Count);
	}

	TestTrue(TEXT("beast is Cautious"), Second.Tame->GetTameState() == EHomeWorldBeastTameState::Cautious);
	TestTrue(TEXT("Spirit_A healed"), Second.HealA->GetHealState() == EHomeWorldSpiritHealState::Healed);
	TestTrue(TEXT("Spirit_B healed"), Second.HealB->GetHealState() == EHomeWorldSpiritHealState::Healed);
	TestTrue(TEXT("N1 nurtured"), Second.N1->GetIsNurtured());
	TestTrue(TEXT("N2 nurtured"), Second.N2->GetIsNurtured());
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
