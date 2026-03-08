// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlayerState.h"
#include "Engine/World.h"

DEFINE_LOG_CATEGORY_STATIC(LogHomeWorldPlayerState, Log, All);

AHomeWorldPlayerState::AHomeWorldPlayerState()
{
}

void AHomeWorldPlayerState::SetDefendCombatMode(EDefendCombatMode Mode)
{
	if (DefendCombatMode != Mode)
	{
		DefendCombatMode = Mode;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("DefendCombatMode set to %s"),
			Mode == EDefendCombatMode::Ranged ? TEXT("Ranged") : TEXT("GroundAOE"));
	}
}

void AHomeWorldPlayerState::SetPlanetoidCombatStyle(EPlanetoidCombatStyle Style)
{
	if (PlanetoidCombatStyle != Style)
	{
		PlanetoidCombatStyle = Style;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("PlanetoidCombatStyle set to %s"),
			Style == EPlanetoidCombatStyle::Combo ? TEXT("Combo") : TEXT("SingleTarget"));
	}
}

void AHomeWorldPlayerState::AddComboHit()
{
	if (ComboHitCount < INT32_MAX)
	{
		ComboHitCount++;
	}
}

void AHomeWorldPlayerState::ResetComboHitCount()
{
	if (ComboHitCount != 0)
	{
		ComboHitCount = 0;
	}
}

void AHomeWorldPlayerState::SetTutorialComplete(bool bComplete)
{
	if (bTutorialComplete != bComplete)
	{
		bTutorialComplete = bComplete;
		if (bTutorialComplete)
		{
			UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Tutorial complete (family taken — inciting incident)."));
		}
	}
}

void AHomeWorldPlayerState::SetSpiritBurstBlockMessage(const FString& Message, float WorldTime)
{
	LastSpiritBurstBlockMessage = Message;
	LastSpiritBurstBlockWorldTime = WorldTime;
}

FString AHomeWorldPlayerState::GetSpiritBurstBlockMessageForHUD(UWorld* World, float DisplayDurationSeconds) const
{
	if (LastSpiritBurstBlockMessage.IsEmpty() || !World) return FString();
	const float Now = World->GetTimeSeconds();
	if (Now - LastSpiritBurstBlockWorldTime > DisplayDurationSeconds) return FString();
	return LastSpiritBurstBlockMessage;
}

void AHomeWorldPlayerState::AddSpiritualPower(int32 Amount)
{
	if (Amount > 0)
	{
		SpiritualPowerCollected += Amount;
	}
}

void AHomeWorldPlayerState::SetSpiritualPowerCollected(int32 Value)
{
	SpiritualPowerCollected = FMath::Max(0, Value);
}

bool AHomeWorldPlayerState::SpendSpiritualPower(int32 Amount)
{
	if (Amount <= 0 || SpiritualPowerCollected < Amount)
	{
		return false;
	}
	SpiritualPowerCollected -= Amount;
	return true;
}

void AHomeWorldPlayerState::AddSpiritualArtefact(int32 Amount)
{
	if (Amount > 0)
	{
		SpiritualArtefactsCollected += Amount;
	}
}

void AHomeWorldPlayerState::SetDayRestorationBuff(bool bActive)
{
	if (bHasDayRestorationBuff != bActive)
	{
		bHasDayRestorationBuff = bActive;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Day restoration buff %s (visible on HUD as 'Day buff: active' at night)."), bActive ? TEXT("set") : TEXT("cleared"));
	}
}

void AHomeWorldPlayerState::IncrementMealsConsumedToday()
{
	if (MealsConsumedToday < INT32_MAX)
	{
		MealsConsumedToday++;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Restored today: %d (HUD updates; use hw.RestoreMeal to trigger)."), MealsConsumedToday);
	}
}

void AHomeWorldPlayerState::IncrementMealsWithFamilyToday()
{
	if (MealsWithFamilyToday < INT32_MAX)
	{
		MealsWithFamilyToday++;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Meals with family today: %d (HUD shows during day)."), MealsWithFamilyToday);
	}
}

void AHomeWorldPlayerState::SetLastMealTriggered(EMealType Type)
{
	LastMealTriggered = Type;
}

void AHomeWorldPlayerState::SetLoveLevel(int32 Level)
{
	const int32 NewLevel = FMath::Max(0, Level);
	if (LoveLevel != NewLevel)
	{
		LoveLevel = NewLevel;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Love: %d (HUD updates when AddLovePoints/SetLoveLevel or RestoreMeal used)."), LoveLevel);
	}
}

void AHomeWorldPlayerState::AddLovePoints(int32 Points)
{
	if (Points > 0 && LoveLevel < INT32_MAX - Points)
	{
		LoveLevel += Points;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Love: %d (+%d) (HUD updates; scales night bonuses)."), LoveLevel, Points);
	}
}

void AHomeWorldPlayerState::IncrementLoveTasksCompletedToday()
{
	if (LoveTasksCompletedToday < INT32_MAX)
	{
		LoveTasksCompletedToday++;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Love tasks today: %d (one love task done; MVP tutorial List 4 step 3)."), LoveTasksCompletedToday);
	}
}

void AHomeWorldPlayerState::CompleteOneLoveTask()
{
	AddLovePoints(1);
	IncrementLoveTasksCompletedToday();
}

void AHomeWorldPlayerState::IncrementGamesWithChildToday()
{
	if (GamesWithChildToday < INT32_MAX)
	{
		GamesWithChildToday++;
		UE_LOG(LogHomeWorldPlayerState, Log, TEXT("Games with child today: %d (one game with child done; MVP tutorial List 5 step 4)."), GamesWithChildToday);
	}
}

void AHomeWorldPlayerState::CompleteOneGameWithChild()
{
	AddLovePoints(1);
	IncrementGamesWithChildToday();
}
