// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldQuestLog.generated.h"

/** One line on the tracker. Future steps stay off the list until the one before them is done. */
USTRUCT()
struct FHomeWorldQuestStep
{
	GENERATED_BODY()

	UPROPERTY()
	FName Id;

	UPROPERTY()
	FString Text;

	UPROPERTY()
	bool bDone = false;
};

/** Facts the opening tracker reads. The player still owns the verbs. */
struct FHomeWorldOpeningQuestFacts
{
	bool bSpiritClaimed = false;
	int32 HerbsGathered = 0;
	bool bHerbFromWest = false;
	bool bHerbFromEast = false;
	bool bKettleBrewed = false;
	bool bDogSlow = false;
	bool bDogInSootheRange = false;
	bool bTracingDove = false;
	bool bWrathEased = false;
	bool bHasMixedHerb = false;
	bool bDogTamed = false;
	bool bBackpack = false;
	bool bFishCaught = false;
	bool bSlept = false;
};

/** Both beds, and twenty chunks between them. A miss adds nothing. */
inline constexpr int32 HomeWorldOpeningHerbQuota = 20;

/** Facts for the sibling home_loop chain. It does not replace Opening. */
struct FHomeWorldHomeLoopQuestFacts
{
	bool bKettleCooked = false;
	bool bWispAssigned = false;
	bool bSurfaceCleared = false;
	bool bSeedPlanted = false;
};

/** One chain. Several can be stored. The screen shows only the most recently changed one. */
USTRUCT()
struct FHomeWorldQuestChain
{
	GENERATED_BODY()

	UPROPERTY()
	FName Id;

	UPROPERTY()
	int32 Rank = 0;

	UPROPERTY()
	TArray<FHomeWorldQuestStep> Steps;
};

/**
 * The stand-in quest tracker. The HUD draws the most recent chain at the top left
 * until dialogue bubbles and audio carry the same steps.
 */
UCLASS()
class HOMEWORLD_API UHomeWorldQuestLog : public UActorComponent
{
	GENERATED_BODY()

public:
	/** Store a chain. An unchanged rewrite does not become the most recent. */
	void SetChain(FName Id, const TArray<FHomeWorldQuestStep>& InSteps);

	const TArray<FHomeWorldQuestStep>& GetDisplayedSteps() const;

	static TArray<FHomeWorldQuestStep> BuildOpeningSteps(const FHomeWorldOpeningQuestFacts& Facts);

	/** Copy one stored chain. False when that id has not been set. */
	bool GetChainSteps(FName Id, TArray<FHomeWorldQuestStep>& OutSteps) const;

	static TArray<FHomeWorldQuestStep> BuildHomeLoopSteps(const FHomeWorldHomeLoopQuestFacts& Facts);

private:
	static bool SameSteps(const TArray<FHomeWorldQuestStep>& A, const TArray<FHomeWorldQuestStep>& B);

	UPROPERTY()
	TArray<FHomeWorldQuestChain> Chains;

	int32 NextRank = 1;
};
