// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/World.h"
#include "HomeWorldHomeLoopSubsystem.h"

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

#endif
