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

#endif
