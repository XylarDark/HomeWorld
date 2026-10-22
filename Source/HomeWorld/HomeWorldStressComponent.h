// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldVirtueTypes.h"
#include "HomeWorldStressComponent.generated.h"

class UHomeWorldVirtueComponent;

/** Player stress. The cap and the amounts are the locked first slice. */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldStressComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	static constexpr int32 Cap = 100;
	static constexpr int32 HitAmount = 10;
	static constexpr int32 BonkAmount = 5;
	static constexpr int32 MissedTendAmount = 20;
	static constexpr int32 MealAmount = 30;
	static constexpr int32 SleepAmount = 10;
	static constexpr int32 SwapReset = 50;

	int32 GetPoints() const { return Points; }
	void SetPoints(int32 NewPoints);
	void NotifyHit();
	void NotifyBonk();
	void NotifyMissedHomeTend();
	void NotifyGraceMossMeal();
	void NotifyBedSleep();

	/** At the cap, and only with Grace, Swap turns it into Wrath. */
	bool TryCapSwap(UHomeWorldVirtueComponent* Virtue);

	bool IsRuneVisible() const { return bRuneVisible; }
	FName GetInteractionName() const { return InteractionName; }
	int32 GetUntouchedStat() const { return UntouchedStat; }

private:
	void Add(int32 Amount);

	int32 Points = 0;
	bool bRuneVisible = false;
	FName InteractionName = TEXT("Grace");
	int32 UntouchedStat = 7;
};
