// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"
#include "HomeWorldQuestLog.h"
#include "HomeWorldTestWorld.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningQuestGrowsInOrder,
	"HomeWorld.Systems.Opening.QuestLog",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningQuestGrowsInOrder::RunTest(const FString& Parameters)
{
	FHomeWorldOpeningQuestFacts Facts;
	TArray<FHomeWorldQuestStep> Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the spirit and the bed"), Steps.Num(), 2);
	TestEqual(TEXT("the spirit line"), Steps[0].Text, FString(TEXT("Pick up the spirit.")));
	TestFalse(TEXT("the spirit is still to do"), Steps[0].bDone);
	TestEqual(TEXT("the bed is always last"), Steps.Last().Text, FString(TEXT("Sleep in the bed.")));
	TestFalse(TEXT("the bed waits before sleep"), Steps.Last().bDone);

	Facts.bSpiritClaimed = true;
	Facts.HerbsGathered = 10;
	Facts.bHerbFromWest = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("herbs follow the spirit"), Steps.Num(), 3);
	TestTrue(TEXT("the spirit stays checked"), Steps[0].bDone);
	TestFalse(TEXT("one bed is not both"), Steps[1].bDone);

	Facts.HerbsGathered = 20;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestFalse(TEXT("twenty from one bed still waits"), Steps[1].bDone);

	Facts.bHerbFromEast = true;
	Facts.bKettleBrewed = false;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the backpack is next"), Steps.Num(), 4);
	TestEqual(TEXT("the backpack line"), Steps[2].Text, FString(TEXT("Take the backpack.")));

	Facts.bBackpack = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the kettle follows the backpack"), Steps.Num(), 5);
	TestEqual(TEXT("brew is the current line"), Steps[3].Text, FString(TEXT("Brew the kettle.")));

	Facts.bKettleBrewed = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the dog line starts slow"), Steps[Steps.Num() - 2].Text, FString(TEXT("Approach the dog slowly.")));

	Facts.bDogSlow = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("a slow walk changes the line"), Steps[Steps.Num() - 2].Text, FString(TEXT("Approach the dog.")));

	Facts.bDogInSootheRange = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("in range the line asks for E"), Steps[Steps.Num() - 2].Text, FString(TEXT("Press E to soothe.")));

	Facts.bTracingDove = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the trace is its own line"), Steps[Steps.Num() - 2].Text, FString(TEXT("Trace the dove.")));

	Facts.bTracingDove = false;
	Facts.bWrathEased = true;
	Facts.bHasMixedHerb = false;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("a finished dove asks for the herb"), Steps[Steps.Num() - 2].Text, FString(TEXT("Feed the dog the mixed herb.")));

	Facts.bHasMixedHerb = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestEqual(TEXT("the herb in hand asks for E"), Steps[Steps.Num() - 2].Text, FString(TEXT("Press E to feed the dog.")));

	Facts.bDogTamed = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestTrue(TEXT("the dog step checks off"), Steps[Steps.Num() - 3].bDone);
	TestEqual(TEXT("the pond is next"), Steps[Steps.Num() - 2].Text, FString(TEXT("Press E at the pond.")));
	TestFalse(TEXT("the fish is still to catch"), Steps[Steps.Num() - 2].bDone);

	Facts.bFishCaught = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestTrue(TEXT("the fish step checks off"), Steps[Steps.Num() - 2].bDone);

	Facts.bSlept = true;
	Steps = UHomeWorldQuestLog::BuildOpeningSteps(Facts);
	TestTrue(TEXT("the bed checks off after sleep"), Steps.Last().bDone);

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

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningQuestFactFromBed,
	"HomeWorld.Systems.Opening.QuestFactFromBed",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningQuestFactFromBed::RunTest(const FString& Parameters)
{
	(void)Parameters;
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening quest bed"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	UHomeWorldQuestLog* Log = Character->FindComponentByClass<UHomeWorldQuestLog>();
	if (!TestNotNull(TEXT("quest log"), Log))
	{
		return false;
	}

	// The SizeTest tick is what formats held facts. This world has no map name, so that tick does not run.
	auto FormatOpening = [](UHomeWorldQuestLog* InLog)
	{
		InLog->SetChain(TEXT("Opening"), UHomeWorldQuestLog::BuildOpeningSteps(InLog->GetOpeningFacts()));
	};
	FormatOpening(Log);
	TArray<FHomeWorldQuestStep> Steps;
	if (!TestTrue(TEXT("opening chain before the bed"), Log->GetChainSteps(TEXT("Opening"), Steps))
		|| !TestEqual(TEXT("the spirit and the bed"), Steps.Num(), 2))
	{
		return false;
	}
	TestFalse(TEXT("the bed is not slept yet"), Steps.Last().bDone);
	TestFalse(TEXT("slept is not held yet"), Log->GetOpeningFacts().bSlept);

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	Params.Name = FName(TEXT("SM_Size_Bed"));
	AStaticMeshActor* Bed = Scope.World->SpawnActor<AStaticMeshActor>(
		FVector(160.f, 0.f, 0.f), FRotator::ZeroRotator, Params);
	if (!TestNotNull(TEXT("bed"), Bed))
	{
		return false;
	}
	if (UStaticMeshComponent* Mesh = Bed->GetStaticMeshComponent())
	{
		if (UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
		{
			Mesh->SetStaticMesh(Cube);
		}
	}
#if WITH_EDITOR
	Bed->SetActorLabel(TEXT("SM_Size_Bed"), false);
#endif

	if (!TestTrue(TEXT("the bed verb"), Character->TryOpeningBedInFront()))
	{
		return false;
	}
	TestTrue(TEXT("the bed published slept"), Log->GetOpeningFacts().bSlept);
	if (!TestTrue(TEXT("the chain waits for the format"), Log->GetChainSteps(TEXT("Opening"), Steps)))
	{
		return false;
	}
	TestFalse(TEXT("the step is not checked until the facts are formatted"), Steps.Last().bDone);

	FormatOpening(Log);
	if (!TestTrue(TEXT("opening chain after the bed"), Log->GetChainSteps(TEXT("Opening"), Steps)))
	{
		return false;
	}
	TestEqual(TEXT("the spirit line is still first"), Steps[0].Text, FString(TEXT("Pick up the spirit.")));
	TestFalse(TEXT("the spirit is still to do"), Steps[0].bDone);
	TestEqual(TEXT("the bed line"), Steps.Last().Text, FString(TEXT("Sleep in the bed.")));
	TestTrue(TEXT("the bed verb checked the step"), Steps.Last().bDone);
	TestEqual(TEXT("still the spirit and the bed"), Steps.Num(), 2);
	return true;
}

#endif
