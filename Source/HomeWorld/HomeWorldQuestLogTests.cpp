// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldQuestLog.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningQuestGrowsInOrder,
	"HomeWorld.Systems.Opening.QuestLog",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningQuestGrowsInOrder::RunTest(const FString& Parameters)
{
	FHomeWorldOpeningQuestFacts Facts;
	TArray<FHomeWorldQuestStep> Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the first line is the spirit"), Steps.Num(), 1);
	TestEqual(TEXT("the spirit line"), Steps[0].Text, FString(TEXT("Pick up the spirit.")));
	TestFalse(TEXT("the spirit is still to do"), Steps[0].bDone);

	Facts.bSpiritClaimed = true;
	Facts.HerbsGathered = 10;
	Facts.bHerbFromWest = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("herbs follow the spirit"), Steps.Num(), 2);
	TestTrue(TEXT("the spirit stays checked"), Steps[0].bDone);
	TestFalse(TEXT("one bed is not both"), Steps[1].bDone);

	Facts.HerbsGathered = 20;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestFalse(TEXT("twenty from one bed still waits"), Steps[1].bDone);

	Facts.bHerbFromEast = true;
	Facts.bKettleBrewed = false;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the backpack is next"), Steps.Num(), 3);
	TestEqual(TEXT("the backpack line"), Steps[2].Text, FString(TEXT("Take the backpack.")));

	Facts.bBackpack = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the kettle follows the backpack"), Steps.Num(), 4);
	TestEqual(TEXT("brew is the current line"), Steps[3].Text, FString(TEXT("Brew the kettle.")));

	Facts.bKettleBrewed = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the dog line starts slow"), Steps.Last().Text, FString(TEXT("Approach the dog slowly.")));

	Facts.bDogSlow = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("a slow walk changes the line"), Steps.Last().Text, FString(TEXT("Approach the dog.")));

	Facts.bDogInSootheRange = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("in range the line asks for E"), Steps.Last().Text, FString(TEXT("Press E to soothe.")));

	Facts.bTracingDove = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the trace is its own line"), Steps.Last().Text, FString(TEXT("Trace the dove.")));

	Facts.bTracingDove = false;
	Facts.bWrathEased = true;
	Facts.bHasMixedHerb = false;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("a finished dove asks for the herb"), Steps.Last().Text, FString(TEXT("Feed the dog the mixed herb.")));

	Facts.bHasMixedHerb = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the herb in hand asks for E"), Steps.Last().Text, FString(TEXT("Press E to feed the dog.")));

	Facts.bDogTamed = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestTrue(TEXT("the dog step checks off"), Steps[Steps.Num() - 2].bDone);
	TestEqual(TEXT("the pond is next"), Steps.Last().Text, FString(TEXT("Press E at the pond.")));
	TestFalse(TEXT("the fish is still to catch"), Steps.Last().bDone);

	Facts.bFishCaught = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestTrue(TEXT("the fish step checks off"), Steps.Last().bDone);

	UHomeWorldQuestLog* Log = NewObject<UHomeWorldQuestLog>();
	TArray<FHomeWorldQuestStep> Older;
	Older.Add(Steps[0]);
	TArray<FHomeWorldQuestStep> Newer;
	Newer.Add(Steps.Last());
	Log->SetChain(TEXT("Opening"), Older);
	Log->SetChain(TEXT("Fish"), Newer);
	TestEqual(TEXT("the newer chain is the one on screen"), Log->GetDisplayedSteps().Num(), 1);
	TestEqual(TEXT("the newer line"), Log->GetDisplayedSteps()[0].Text, Newer[0].Text);
	Log->SetChain(TEXT("Opening"), Older);
	TestEqual(TEXT("an unchanged chain does not take the screen"), Log->GetDisplayedSteps()[0].Text, Newer[0].Text);
	Older[0].bDone = !Older[0].bDone;
	Log->SetChain(TEXT("Opening"), Older);
	TestEqual(TEXT("a changed chain becomes the one on screen"), Log->GetDisplayedSteps()[0].Text, Older[0].Text);
	return true;
}

#endif
