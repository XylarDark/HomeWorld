// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldQuestLog.h"

bool UHomeWorldQuestLog::SameSteps(const TArray<FHomeWorldQuestStep>& A, const TArray<FHomeWorldQuestStep>& B)
{
	if (A.Num() != B.Num())
	{
		return false;
	}
	for (int32 Index = 0; Index < A.Num(); ++Index)
	{
		if (A[Index].Text != B[Index].Text || A[Index].bDone != B[Index].bDone)
		{
			return false;
		}
	}
	return true;
}

void UHomeWorldQuestLog::SetChain(FName Id, const TArray<FHomeWorldQuestStep>& InSteps)
{
	FHomeWorldQuestChain* Chain = nullptr;
	for (FHomeWorldQuestChain& Existing : Chains)
	{
		if (Existing.Id == Id)
		{
			Chain = &Existing;
			break;
		}
	}
	if (Chain && SameSteps(Chain->Steps, InSteps))
	{
		return;
	}

	FString Previous;
	if (Chain)
	{
		for (const FHomeWorldQuestStep& Step : Chain->Steps)
		{
			if (!Step.bDone)
			{
				Previous = Step.Text;
				break;
			}
		}
	}
	if (!Chain)
	{
		FHomeWorldQuestChain Added;
		Added.Id = Id;
		Chains.Add(Added);
		Chain = &Chains.Last();
	}
	Chain->Steps = InSteps;
	Chain->Rank = NextRank++;
	for (const FHomeWorldQuestStep& Step : Chain->Steps)
	{
		if (!Step.bDone && Step.Text != Previous)
		{
			UE_LOG(LogTemp, Log, TEXT("quest: %s"), *Step.Text);
			break;
		}
	}
}

bool UHomeWorldQuestLog::GetChainSteps(FName Id, TArray<FHomeWorldQuestStep>& OutSteps) const
{
	for (const FHomeWorldQuestChain& Chain : Chains)
	{
		if (Chain.Id == Id)
		{
			OutSteps = Chain.Steps;
			return true;
		}
	}
	OutSteps.Reset();
	return false;
}

void UHomeWorldQuestLog::PublishOpeningFact(EHomeWorldOpeningFact Fact, bool bValue)
{
	switch (Fact)
	{
	case EHomeWorldOpeningFact::SpiritClaimed:
		OpeningFacts.bSpiritClaimed = bValue;
		break;
	case EHomeWorldOpeningFact::HerbFromWest:
		OpeningFacts.bHerbFromWest = bValue;
		break;
	case EHomeWorldOpeningFact::HerbFromEast:
		OpeningFacts.bHerbFromEast = bValue;
		break;
	case EHomeWorldOpeningFact::KettleBrewed:
		OpeningFacts.bKettleBrewed = bValue;
		break;
	case EHomeWorldOpeningFact::DogSlow:
		OpeningFacts.bDogSlow = bValue;
		break;
	case EHomeWorldOpeningFact::DogInSootheRange:
		OpeningFacts.bDogInSootheRange = bValue;
		break;
	case EHomeWorldOpeningFact::TracingDove:
		OpeningFacts.bTracingDove = bValue;
		break;
	case EHomeWorldOpeningFact::WrathEased:
		OpeningFacts.bWrathEased = bValue;
		break;
	case EHomeWorldOpeningFact::HasMixedHerb:
		OpeningFacts.bHasMixedHerb = bValue;
		break;
	case EHomeWorldOpeningFact::DogTamed:
		OpeningFacts.bDogTamed = bValue;
		break;
	case EHomeWorldOpeningFact::Backpack:
		OpeningFacts.bBackpack = bValue;
		break;
	case EHomeWorldOpeningFact::FishCaught:
		OpeningFacts.bFishCaught = bValue;
		break;
	case EHomeWorldOpeningFact::Slept:
		OpeningFacts.bSlept = bValue;
		break;
	default:
		break;
	}
}

void UHomeWorldQuestLog::PublishOpeningHerbsGathered(int32 Count)
{
	OpeningFacts.HerbsGathered = Count;
}

const TArray<FHomeWorldQuestStep>& UHomeWorldQuestLog::GetDisplayedSteps() const
{
	const FHomeWorldQuestChain* Best = nullptr;
	for (const FHomeWorldQuestChain& Chain : Chains)
	{
		if (!Best || Chain.Rank > Best->Rank)
		{
			Best = &Chain;
		}
	}
	if (!Best)
	{
		static const TArray<FHomeWorldQuestStep> Empty;
		return Empty;
	}
	return Best->Steps;
}

static TArray<FHomeWorldQuestStep> BuildOpeningStepsThroughFish(const FHomeWorldOpeningQuestFacts& Facts)
{
	TArray<FHomeWorldQuestStep> Steps;
	auto Add = [&Steps](const TCHAR* Id, const FString& Text, bool bDone)
	{
		FHomeWorldQuestStep Step;
		Step.Id = FName(Id);
		Step.Text = Text;
		Step.bDone = bDone;
		Steps.Add(Step);
	};

	Add(TEXT("Spirit"), TEXT("Pick up the spirit."), Facts.bSpiritClaimed);
	if (!Facts.bSpiritClaimed)
	{
		return Steps;
	}

	const bool bHerbs = Facts.HerbsGathered >= HomeWorldOpeningHerbQuota && Facts.bHerbFromWest && Facts.bHerbFromEast;
	FString HerbText = FString::Printf(
		TEXT("Gather herbs from both beds (%d/%d)."),
		FMath::Min(Facts.HerbsGathered, HomeWorldOpeningHerbQuota),
		HomeWorldOpeningHerbQuota);
	if (Facts.HerbsGathered >= HomeWorldOpeningHerbQuota && !bHerbs)
	{
		HerbText = TEXT("Gather herbs from both beds.");
	}
	Add(TEXT("Herbs"), HerbText, bHerbs);
	if (!bHerbs)
	{
		return Steps;
	}

	Add(TEXT("Backpack"), TEXT("Take the backpack."), Facts.bBackpack);
	if (!Facts.bBackpack)
	{
		return Steps;
	}

	Add(TEXT("Kettle"), TEXT("Brew the kettle."), Facts.bKettleBrewed);
	if (!Facts.bKettleBrewed)
	{
		return Steps;
	}

	FString DogText = TEXT("Approach the dog slowly.");
	if (Facts.bDogTamed)
	{
		DogText = TEXT("Soothe the dog.");
	}
	else if (Facts.bTracingDove)
	{
		DogText = TEXT("Trace the dove.");
	}
	else if (Facts.bWrathEased)
	{
		DogText = Facts.bHasMixedHerb ? TEXT("Press E to feed the dog.") : TEXT("Feed the dog the mixed herb.");
	}
	else if (Facts.bDogSlow && Facts.bDogInSootheRange)
	{
		DogText = TEXT("Press E to soothe.");
	}
	else if (Facts.bDogSlow)
	{
		DogText = TEXT("Approach the dog.");
	}
	Add(TEXT("Dog"), DogText, Facts.bDogTamed);
	if (!Facts.bDogTamed)
	{
		return Steps;
	}

	Add(TEXT("Fish"), TEXT("Press E at the pond."), Facts.bFishCaught);
	return Steps;
}

TArray<FHomeWorldQuestStep> UHomeWorldQuestLog::BuildOpeningSteps(const FHomeWorldOpeningQuestFacts& Facts)
{
	// The bed opens the night pass. Keep it on the tracker at all times so a tester
	// is reminded to walk straight to it, even while the opening steps are unfinished.
	TArray<FHomeWorldQuestStep> Steps = BuildOpeningStepsThroughFish(Facts);
	FHomeWorldQuestStep Sleep;
	Sleep.Id = FName(TEXT("Sleep"));
	Sleep.Text = TEXT("Sleep in the bed.");
	Sleep.bDone = Facts.bSlept;
	Steps.Add(Sleep);
	return Steps;
}

TArray<FHomeWorldQuestStep> UHomeWorldQuestLog::BuildHomeLoopSteps(const FHomeWorldHomeLoopQuestFacts& Facts)
{
	TArray<FHomeWorldQuestStep> Steps;
	auto Add = [&Steps](const TCHAR* Id, const FString& Text, bool bDone)
	{
		FHomeWorldQuestStep Step;
		Step.Id = FName(Id);
		Step.Text = Text;
		Step.bDone = bDone;
		Steps.Add(Step);
	};

	Add(TEXT("Cook"), TEXT("Cook the kettle."), Facts.bKettleCooked);
	if (!Facts.bKettleCooked)
	{
		return Steps;
	}
	Add(TEXT("Assign"), TEXT("Assign a wisp."), Facts.bWispAssigned);
	if (!Facts.bWispAssigned)
	{
		return Steps;
	}
	Add(TEXT("Clean"), TEXT("Clear one surface."), Facts.bSurfaceCleared);
	if (!Facts.bSurfaceCleared)
	{
		return Steps;
	}
	Add(TEXT("Plant"), TEXT("Plant one seed."), Facts.bSeedPlanted);
	return Steps;
}
