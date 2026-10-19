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

TArray<FHomeWorldQuestStep> UHomeWorldQuestLog::BuildOpeningSteps(const FHomeWorldOpeningQuestFacts& Facts)
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
