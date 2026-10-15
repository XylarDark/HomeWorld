// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldVirtueComponent.h"
#include "HomeWorldVirtueSpawnTable.h"
#include "HomeWorldVirtueTypes.h"

namespace HomeWorldVirtueTest
{
	static UHomeWorldVirtueComponent* MakeVirtue()
	{
		return NewObject<UHomeWorldVirtueComponent>();
	}

	static UHomeWorldInventorySubsystem* MakeInventory()
	{
		if (!GEngine)
		{
			return nullptr;
		}
		UGameInstance* GameInstance = NewObject<UGameInstance>(GEngine);
		if (!GameInstance)
		{
			return nullptr;
		}
		GameInstance->Init();
		return GameInstance->GetSubsystem<UHomeWorldInventorySubsystem>();
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FVirtueHandRejectsOpposites,
	"HomeWorld.Systems.Virtue.HandRejectsOpposites",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FVirtueHandRejectsOpposites::RunTest(const FString& Parameters)
{
	FString Error;
	TArray<EHomeWorldVirtuePole> Poles;
	const TArray<EHomeWorldVirtuePole> Both = { EHomeWorldVirtuePole::Greed, EHomeWorldVirtuePole::Generosity };
	TestFalse(TEXT("opposite poles are rejected"), HomeWorldVirtue::TrySetHandPoles(Poles, Both, Error));

	TArray<EHomeWorldVirtuePole> Eight;
	for (int32 Index = 0; Index < 8; ++Index)
	{
		Eight.Add(EHomeWorldVirtuePole::Greed);
	}
	TestFalse(TEXT("eight poles are rejected"), HomeWorldVirtue::TrySetHandPoles(Poles, Eight, Error));

	const TArray<EHomeWorldVirtuePole> OneEach = {
		EHomeWorldVirtuePole::Greed, EHomeWorldVirtuePole::Abstinence, EHomeWorldVirtuePole::Productivity,
		EHomeWorldVirtuePole::Grace, EHomeWorldVirtuePole::Humility, EHomeWorldVirtuePole::Fulfillment,
		EHomeWorldVirtuePole::Love };
	TestTrue(TEXT("one pole per axis is kept"), HomeWorldVirtue::TrySetHandPoles(Poles, OneEach, Error));
	TestEqual(TEXT("cap is seven"), Poles.Num(), 7);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FVirtueRollStopsOnMiss,
	"HomeWorld.Systems.Virtue.RollStopsOnMiss",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FVirtueRollStopsOnMiss::RunTest(const FString& Parameters)
{
	TArray<float> Never = { 0.f, 0.f, 0.f, 0.f, 0.f, 0.f, 0.f };
	FRandomStream Stream(1);
	TArray<EHomeWorldVirtuePole> Poles;
	HomeWorldVirtue::RollPoles(Poles, Never, Stream);
	TestEqual(TEXT("a miss before the first pole leaves the set empty"), Poles.Num(), 0);

	TArray<float> Always = { 1.f, 1.f, 1.f, 1.f, 1.f, 1.f, 1.f };
	HomeWorldVirtue::RollPoles(Poles, Always, Stream);
	TestEqual(TEXT("seven certain chances fill seven axes"), Poles.Num(), 7);
	TSet<int32> Axes;
	for (const EHomeWorldVirtuePole Pole : Poles)
	{
		Axes.Add(HomeWorldVirtue::AxisIndex(Pole));
	}
	TestEqual(TEXT("no axis is repeated"), Axes.Num(), 7);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FVirtueChancesComeFromTheAsset,
	"HomeWorld.Systems.Virtue.ChancesComeFromTheAsset",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FVirtueChancesComeFromTheAsset::RunTest(const FString& Parameters)
{
	UHomeWorldVirtueSpawnTable* Table = NewObject<UHomeWorldVirtueSpawnTable>();
	TestTrue(TEXT("placeholder chances do not rise"), Table->AreChancesNonIncreasing());
	TestEqual(TEXT("seven character chances"), Table->CharacterChances.Num(), 7);
	TestTrue(TEXT("first chance is larger than the second"), Table->CharacterChances[0] > Table->CharacterChances[1]);

	UHomeWorldVirtueComponent* Virtue = HomeWorldVirtueTest::MakeVirtue();
	FRandomStream Stream(4);
	Virtue->Roll(Table->CharacterChances, Stream);
	TestTrue(TEXT("a roll from the asset stays within seven"), Virtue->GetPoles().Num() <= 7);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FVirtueHerbVerbs,
	"HomeWorld.Systems.Virtue.HerbVerbs",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FVirtueHerbVerbs::RunTest(const FString& Parameters)
{
	UHomeWorldInventorySubsystem* Inventory = HomeWorldVirtueTest::MakeInventory();
	UHomeWorldVirtueComponent* Virtue = HomeWorldVirtueTest::MakeVirtue();
	if (!TestNotNull(TEXT("inventory"), Inventory) || !TestNotNull(TEXT("virtue"), Virtue))
	{
		return false;
	}

	TestTrue(TEXT("unmarked herb is still a count"), Inventory->TryAddResource(HomeWorldInventory::RES_HERB, 1));
	TestEqual(TEXT("RES_HERB count"), Inventory->GetResource(HomeWorldInventory::RES_HERB), 1);
	TestFalse(TEXT("a herb with no poles is not an instance"), Inventory->AddMarkedHerb({}));
	TestEqual(TEXT("count is unchanged"), Inventory->GetResource(HomeWorldInventory::RES_HERB), 1);

	FString Error;
	TestTrue(TEXT("hand set Greed"), Virtue->TrySetHandPoles({ EHomeWorldVirtuePole::Greed }, Error));
	TestTrue(TEXT("generosity herb is stored"), Inventory->AddMarkedHerb({ EHomeWorldVirtuePole::Generosity }));
	TestFalse(TEXT("give refuses an occupied axis"), Inventory->TryVirtueGive(Virtue));
	TestEqual(TEXT("failed give keeps the herb"), Inventory->GetMarkedHerbCount(), 1);
	TestTrue(TEXT("Greed is still there"), Virtue->HasPole(EHomeWorldVirtuePole::Greed));

	TestTrue(TEXT("swap flips to Generosity"), Inventory->TryVirtueSwap(Virtue));
	TestTrue(TEXT("opposite is now held"), Virtue->HasPole(EHomeWorldVirtuePole::Generosity));
	TestFalse(TEXT("Greed is gone"), Virtue->HasPole(EHomeWorldVirtuePole::Greed));
	TestEqual(TEXT("swap spent the herb"), Inventory->GetMarkedHerbCount(), 0);

	TestTrue(TEXT("take herb"), Inventory->AddMarkedHerb({ EHomeWorldVirtuePole::Generosity }));
	TestTrue(TEXT("take removes Generosity"), Inventory->TryVirtueTake(Virtue));
	TestEqual(TEXT("set is empty after take"), Virtue->GetPoles().Num(), 0);

	TestTrue(TEXT("hand set two poles"), Virtue->TrySetHandPoles(
		{ EHomeWorldVirtuePole::Pride, EHomeWorldVirtuePole::Wrath }, Error));
	TestTrue(TEXT("nullify herb"), Inventory->AddMarkedHerb({ EHomeWorldVirtuePole::Love }));
	TestTrue(TEXT("nullify clears every pole"), Inventory->TryVirtueNullify(Virtue));
	TestEqual(TEXT("nullify leaves none"), Virtue->GetPoles().Num(), 0);
	TestEqual(TEXT("nullify spent the herb"), Inventory->GetMarkedHerbCount(), 0);
	TestEqual(TEXT("RES_HERB count still one"), Inventory->GetResource(HomeWorldInventory::RES_HERB), 1);
	return true;
}
#endif
