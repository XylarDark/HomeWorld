// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldHomeLoopSubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * Docs/42_HOME_LOOP_DESIGN.md section 15. One shot per bite.
 * Tea, quest, cloud-wisp, fertilizer, and nurture tests stay on their own files.
 */

namespace HomeWorldHomeLoopTest
{
	struct FScopedWorld
	{
		UWorld* World = nullptr;

		FScopedWorld()
		{
			World = UWorld::CreateWorld(EWorldType::Game, false);
		}

		~FScopedWorld()
		{
			if (World)
			{
				World->DestroyWorld(false);
				World = nullptr;
			}
		}
	};
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopStationIdsTest,
	"HomeWorld.HomeLoop.StationIds",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopStationIdsTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("world"), Scope.World) || !TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}

	TArray<EHomeWorldHomeStation> Ids;
	Loop->GetStationIds(Ids);
	TestEqual(TEXT("six stations"), Ids.Num(), 6);

	const EHomeWorldHomeStation Expected[] = {
		EHomeWorldHomeStation::Sink,
		EHomeWorldHomeStation::Board,
		EHomeWorldHomeStation::Pot,
		EHomeWorldHomeStation::Stove,
		EHomeWorldHomeStation::Oven,
		EHomeWorldHomeStation::Garbage
	};
	const TCHAR* Names[] = { TEXT("Sink"), TEXT("Board"), TEXT("Pot"), TEXT("Stove"), TEXT("Oven"), TEXT("Garbage") };
	for (int32 Index = 0; Index < 6; ++Index)
	{
		TestEqual(FString::Printf(TEXT("station %d"), Index), Ids[Index], Expected[Index]);
		TestEqual(
			FString::Printf(TEXT("log %s"), Names[Index]),
			Loop->LogStation(Ids[Index]),
			FString::Printf(TEXT("home_loop: station %s"), Names[Index]));
	}

	TestEqual(TEXT("no clock yet"), Loop->GetHomeClockSeconds(), 0.f);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopKettleStillBrewsTest,
	"HomeWorld.HomeLoop.KettleStillBrews",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopKettleStillBrewsTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("world"), Scope.World) || !TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}

	FHomeWorldRecipe Recipe;
	TestTrue(TEXT("kettle row exists"), Loop->GetRecipe(FName(TEXT("RECIPE_KETTLE")), Recipe));
	TestEqual(TEXT("kettle id"), Recipe.Id, FName(TEXT("RECIPE_KETTLE")));
	TestEqual(TEXT("kettle vessel is the pot"), Recipe.Vessel, EHomeWorldHomeVessel::Pot);
	TestEqual(TEXT("kettle arms stamina"), Recipe.BuffId, EHomeWorldHomeBuff::Stamina);
	if (!TestEqual(TEXT("one ingredient"), Recipe.Ingredients.Num(), 1))
	{
		return false;
	}
	TestEqual(TEXT("herb chest item"), Recipe.Ingredients[0].ChestItemId, FName(TEXT("ITEM_HERB")));
	TestEqual(TEXT("wash at the sink"), Recipe.Ingredients[0].PrepStation, EHomeWorldHomeStation::Sink);
	TestEqual(TEXT("sink prep is 4s"), Recipe.Ingredients[0].PrepSeconds, 4.f);
	TestEqual(TEXT("pot cook is 10s"), Recipe.Ingredients[0].CookSeconds, 10.f);
	TestFalse(TEXT("greens recipe is not in this bite"), Loop->GetRecipe(FName(TEXT("RECIPE_GREENS_HERB")), Recipe));

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = Scope.World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TestNotNull(TEXT("time of day"), TimeOfDay))
	{
		return false;
	}
	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);

	UGameInstance* GameInstance = NewObject<UGameInstance>(Scope.World);
	if (!TestNotNull(TEXT("game instance"), GameInstance))
	{
		return false;
	}
	GameInstance->Init();
	Scope.World->SetGameInstance(GameInstance);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldCharacter* Character = Scope.World->SpawnActor<AHomeWorldCharacter>(Params);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();
	Character->DebugSeedOpeningWispLoop(0, 9);

	TestTrue(TEXT("opening brew still calls the current kettle"), Loop->TryOpeningKettleBrew(Character));
	TestTrue(TEXT("sprint gate is on"), Character->IsTeaSprintGateActive());
	TestTrue(TEXT("quest fact kettle_brewed"), Character->GetPlaytestStateJson().Contains(TEXT("\"kettle_brewed\":true")));
	TestTrue(TEXT("opening brew leaves the armed slot empty"), Loop->IsArmedBuffSlotEmpty());
	return true;
}

namespace HomeWorldHomeLoopTest
{
	static void OpenDawn(UWorld* World, UHomeWorldHomeLoopSubsystem* Loop)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
		}
		Loop->Advance(0.f);
	}

	static bool Nearly(float Actual, float Expected)
	{
		return FMath::IsNearlyEqual(Actual, Expected, 0.01f);
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopKettlePrepCookTest,
	"HomeWorld.HomeLoop.KettlePrepCook",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopKettlePrepCookTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("dawn opens the 90s window"), Loop->IsHomeWindowOpen());
	TestTrue(TEXT("window is 90s"), HomeWorldHomeLoopTest::Nearly(Loop->GetWindowRemaining(), 90.f));

	TestTrue(TEXT("kettle wash starts"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(4.f);
	TestTrue(TEXT("herb is washed"), Loop->IsIngredientPrepped(0));
	TestFalse(TEXT("cook waits until the next moment"), Loop->IsIngredientCooking(0));
	TestFalse(TEXT("not served at prep"), Loop->GetLastServe().bServed);

	Loop->Advance(10.f);
	TestTrue(TEXT("kettle served"), Loop->GetLastServe().bServed);
	TestTrue(TEXT("one ingredient syncs full"), HomeWorldHomeLoopTest::Nearly(Loop->GetLastServe().SyncFactor, 1.f));
	TestEqual(TEXT("spent the herb row"), Loop->GetLastServe().SpentItemIds.Num(), 1);
	TestEqual(TEXT("spent ITEM_HERB"), Loop->GetLastServe().SpentItemIds[0], FName(TEXT("ITEM_HERB")));
	TestFalse(TEXT("a post-tutorial serve arms the slot"), Loop->IsArmedBuffSlotEmpty());
	TestFalse(TEXT("the buff waits for the Day phase"), Loop->GetArmedBuff().bLive);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopMistimeServesTest,
	"HomeWorld.HomeLoop.MistimeServes",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopMistimeServesTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	Loop->Advance(80.f);
	TestTrue(TEXT("late wash still starts"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(4.f);
	TestTrue(TEXT("washed with cook still waiting"), Loop->IsIngredientPrepped(0));
	Loop->Advance(6.f);
	TestTrue(TEXT("window-end cook still serves"), Loop->GetLastServe().bServed);
	TestTrue(TEXT("mistime factor is half"), HomeWorldHomeLoopTest::Nearly(Loop->GetLastServe().SyncFactor, 0.5f));
	TestEqual(TEXT("mistime still spends the herb"), Loop->GetLastServe().SpentItemIds.Num(), 1);
	TestEqual(TEXT("spent item is ITEM_HERB"), Loop->GetLastServe().SpentItemIds[0], FName(TEXT("ITEM_HERB")));
	TestFalse(TEXT("window is closed"), Loop->IsHomeWindowOpen());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopPrepCarriesTest,
	"HomeWorld.HomeLoop.PrepCarries",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopPrepCarriesTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop) || !TestNotNull(TEXT("time of day"), TimeOfDay))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("prep starts"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(2.f);
	TestTrue(TEXT("two seconds of wash remain"), HomeWorldHomeLoopTest::Nearly(Loop->GetPrepRemaining(0), 2.f));

	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Loop->Advance(0.f);
	TestFalse(TEXT("day closes the window"), Loop->IsHomeWindowOpen());
	TestTrue(TEXT("unfinished wash carries"), HomeWorldHomeLoopTest::Nearly(Loop->GetPrepRemaining(0), 2.f));

	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	Loop->Advance(2.f);
	TestTrue(TEXT("carried wash finishes"), Loop->IsIngredientPrepped(0));
	TestFalse(TEXT("a carried wash is not a serve"), Loop->GetLastServe().bServed);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopOpeningSprintUntouchedTest,
	"HomeWorld.HomeLoop.OpeningSprintUntouched",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopOpeningSprintUntouchedTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop) || !TestNotNull(TEXT("time of day"), TimeOfDay))
	{
		return false;
	}
	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	UGameInstance* GameInstance = NewObject<UGameInstance>(Scope.World);
	if (!TestNotNull(TEXT("game instance"), GameInstance))
	{
		return false;
	}
	GameInstance->Init();
	Scope.World->SetGameInstance(GameInstance);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldCharacter* Character = Scope.World->SpawnActor<AHomeWorldCharacter>(Params);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();
	Character->DebugSeedOpeningWispLoop(0, 9);

	TestFalse(TEXT("the opening day has not ended"), Loop->HasOpeningDayEnded());
	TestTrue(TEXT("the world kettle still brews"), Loop->TryKettleFromWorld(Character));
	TestTrue(TEXT("sprint gate stays the opening gate"), Character->IsTeaSprintGateActive());
	TestTrue(TEXT("kettle_brewed still sets"), Character->GetPlaytestStateJson().Contains(TEXT("\"kettle_brewed\":true")));
	TestEqual(TEXT("opening brew starts no station timer"), Loop->GetActiveWorkCount(), 0);
	TestTrue(TEXT("opening brew leaves the slot empty"), Loop->IsArmedBuffSlotEmpty());

	Character->GrantSpiritSleepGate();
	TestTrue(TEXT("the first sleep ends the opening day"), Loop->HasOpeningDayEnded());
	TestTrue(TEXT("the sprint gate is still the tea gate"), Character->IsTeaSprintGateActive());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopTutorialStationsInertTest,
	"HomeWorld.HomeLoop.TutorialStationsInert",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopTutorialStationsInertTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("sink runs on the tutorial island"), Loop->CanRunStation(EHomeWorldHomeStation::Sink));
	TestTrue(TEXT("pot runs on the tutorial island"), Loop->CanRunStation(EHomeWorldHomeStation::Pot));
	TestFalse(TEXT("board stays inert"), Loop->CanRunStation(EHomeWorldHomeStation::Board));
	TestFalse(TEXT("stove stays inert"), Loop->CanRunStation(EHomeWorldHomeStation::Stove));
	TestFalse(TEXT("oven stays inert"), Loop->CanRunStation(EHomeWorldHomeStation::Oven));
	TestFalse(TEXT("garbage stays inert"), Loop->CanRunStation(EHomeWorldHomeStation::Garbage));

	TestTrue(TEXT("sink can wash"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(4.f);
	TestFalse(TEXT("garbage refuses the washed herb"), Loop->DiscardPrepped(0));
	TestTrue(TEXT("the herb is still prepped"), Loop->IsIngredientPrepped(0));

	Loop->SetBodyForm(false);
	TestFalse(TEXT("spirit form refuses the sink"), Loop->CanRunStation(EHomeWorldHomeStation::Sink));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopDiscardSpendsTest,
	"HomeWorld.HomeLoop.DiscardSpends",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopDiscardSpendsTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("wash starts"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(4.f);
	TestTrue(TEXT("discard spends the washed herb"), Loop->DiscardPrepped(0));
	TestTrue(TEXT("discard is not a serve"), Loop->GetLastServe().bDiscarded);
	TestFalse(TEXT("a discarded piece is not a meal"), Loop->GetLastServe().bServed);
	TestEqual(TEXT("one piece spent"), Loop->GetLastServe().SpentItemIds.Num(), 1);
	TestEqual(TEXT("dust stays at zero"), Loop->GetDustTotal(), 0);
	TestEqual(TEXT("no work remains"), Loop->GetActiveWorkCount(), 0);
	return true;
}

namespace HomeWorldHomeLoopTest
{
	static void GoToPhase(UWorld* World, UHomeWorldHomeLoopSubsystem* Loop, EHomeWorldTimeOfDayPhase Phase)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			TimeOfDay->SetPhase(Phase);
		}
		Loop->Advance(0.f);
	}

	static bool CookKettle(UHomeWorldHomeLoopSubsystem* Loop)
	{
		if (!Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0))
		{
			return false;
		}
		Loop->Advance(4.f);
		Loop->Advance(10.f);
		return Loop->GetLastServe().bServed && Nearly(Loop->GetLastServe().SyncFactor, 1.f);
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopArmedBuffDawnTest,
	"HomeWorld.HomeLoop.ArmedBuffDawn",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopArmedBuffDawnTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("dawn kettle serves"), HomeWorldHomeLoopTest::CookKettle(Loop));
	TestFalse(TEXT("the slot holds the meal"), Loop->IsArmedBuffSlotEmpty());
	TestEqual(TEXT("dawn meal covers the coming day"), Loop->GetArmedBuff().CoveredDayId, 1);
	TestTrue(TEXT("bonus waits until Day"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestTrue(TEXT("full clear-house stamina is 60s"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 60.f));

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dusk);
	TestTrue(TEXT("leaving Day clears the slot"), Loop->IsArmedBuffSlotEmpty());
	TestTrue(TEXT("dusk has no leftover bonus"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Night);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dawn);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestTrue(TEXT("the next day is unbuffed"), Loop->IsArmedBuffSlotEmpty());
	TestTrue(TEXT("the next day has no sprint bonus"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopArmedBuffDuskTest,
	"HomeWorld.HomeLoop.ArmedBuffDusk",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopArmedBuffDuskTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dusk);
	TestTrue(TEXT("dusk kettle serves"), HomeWorldHomeLoopTest::CookKettle(Loop));
	TestEqual(TEXT("dusk meal covers the day after the next dawn"), Loop->GetArmedBuff().CoveredDayId, 2);
	TestTrue(TEXT("dusk itself is not the covered day"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Night);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dawn);
	TestTrue(TEXT("the following dawn still waits"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestTrue(TEXT("the next day receives the dusk meal"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 60.f));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopArmedBuffClearsTest,
	"HomeWorld.HomeLoop.ArmedBuffClears",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopArmedBuffClearsTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::OpenDawn(Scope.World, Loop);
	TestTrue(TEXT("serve"), HomeWorldHomeLoopTest::CookKettle(Loop));
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestTrue(TEXT("live on the covered day"), Loop->GetArmedBuff().bLive);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Night);
	TestTrue(TEXT("gone when the day ends"), Loop->IsArmedBuffSlotEmpty());
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dawn);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestFalse(TEXT("absent the following day"), Loop->GetArmedBuff().bLive);
	TestTrue(TEXT("no bonus the following day"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 0.f));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopArmedBuffReplacesTest,
	"HomeWorld.HomeLoop.ArmedBuffReplaces",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopArmedBuffReplacesTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop))
	{
		return false;
	}
	Loop->SetOpeningDayEnded(true);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dusk);
	Loop->Advance(80.f);
	TestTrue(TEXT("late wash"), Loop->BeginPrep(FName(TEXT("RECIPE_KETTLE")), 0));
	Loop->Advance(4.f);
	Loop->Advance(6.f);
	TestTrue(TEXT("dusk mistime armed"), HomeWorldHomeLoopTest::Nearly(Loop->GetArmedBuff().SyncFactor, 0.5f));

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Night);
	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Dawn);
	TestTrue(TEXT("dawn meal replaces the dusk meal"), HomeWorldHomeLoopTest::CookKettle(Loop));
	TestTrue(TEXT("the slot keeps the later sync"), HomeWorldHomeLoopTest::Nearly(Loop->GetArmedBuff().SyncFactor, 1.f));
	TestEqual(TEXT("still the same coming day"), Loop->GetArmedBuff().CoveredDayId, 2);

	HomeWorldHomeLoopTest::GoToPhase(Scope.World, Loop, EHomeWorldTimeOfDayPhase::Day);
	TestTrue(TEXT("the replacement is the one that pays"), HomeWorldHomeLoopTest::Nearly(Loop->GetSprintBonusSeconds(), 60.f));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FHomeLoopOpeningBrewSkipsSlotTest,
	"HomeWorld.HomeLoop.OpeningBrewSkipsSlot",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FHomeLoopOpeningBrewSkipsSlotTest::RunTest(const FString& Parameters)
{
	HomeWorldHomeLoopTest::FScopedWorld Scope;
	UHomeWorldHomeLoopSubsystem* Loop = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldHomeLoopSubsystem>() : nullptr;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = Scope.World
		? Scope.World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;
	if (!TestNotNull(TEXT("home loop"), Loop) || !TestNotNull(TEXT("time of day"), TimeOfDay))
	{
		return false;
	}
	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	UGameInstance* GameInstance = NewObject<UGameInstance>(Scope.World);
	GameInstance->Init();
	Scope.World->SetGameInstance(GameInstance);
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldCharacter* Character = Scope.World->SpawnActor<AHomeWorldCharacter>(Params);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();
	Character->DebugSeedOpeningWispLoop(0, 9);
	TestTrue(TEXT("opening brew"), Loop->TryKettleFromWorld(Character));
	TestTrue(TEXT("opening brew skips the slot"), Loop->IsArmedBuffSlotEmpty());
	return true;
}

#endif
