// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldStressComponent.h"

#include "Engine/Engine.h"
#include "HomeWorldVirtueComponent.h"

void UHomeWorldStressComponent::SetPoints(int32 NewPoints)
{
	Points = FMath::Clamp(NewPoints, 0, Cap);
	UE_LOG(LogTemp, Log, TEXT("STRESS: %d"), Points);
}

void UHomeWorldStressComponent::Add(int32 Amount)
{
	SetPoints(Points + Amount);
}

void UHomeWorldStressComponent::NotifyHit()
{
	Add(HitAmount);
}

void UHomeWorldStressComponent::NotifyBonk()
{
	Add(BonkAmount);
}

void UHomeWorldStressComponent::NotifyMissedHomeTend()
{
	Add(MissedTendAmount);
}

void UHomeWorldStressComponent::NotifyGraceMossMeal()
{
	Add(-MealAmount);
}

void UHomeWorldStressComponent::NotifyBedSleep()
{
	Add(-SleepAmount);
}

bool UHomeWorldStressComponent::TryCapSwap(UHomeWorldVirtueComponent* Virtue)
{
	if (Points < Cap || !Virtue || !Virtue->HasPole(EHomeWorldVirtuePole::Grace))
	{
		return false;
	}
	if (!Virtue->TrySwapAxis(EHomeWorldVirtuePole::Grace))
	{
		return false;
	}
	bRuneVisible = true;
	InteractionName = TEXT("Wrath");
	SetPoints(SwapReset);
	return true;
}
