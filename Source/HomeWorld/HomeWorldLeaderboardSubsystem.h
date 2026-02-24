// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldLeaderboardSubsystem.generated.h"

/** One leaderboard row. Stub; implement with Steam API or SteamLead in Weeks 3-4. */
USTRUCT(BlueprintType)
struct FHomeWorldLeaderboardEntry
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	int32 Rank = 0;

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	FString PlayerName;

	UPROPERTY(BlueprintReadOnly, Category = "Leaderboard")
	int32 Score = 0;
};

/**
 * Game instance subsystem for leaderboards. Game code submits scores and reads rankings through this API;
 * implement with Steam API or SteamLead in Weeks 3-4. Stub only.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldLeaderboardSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Submit a score for a category. Stub: no-op, returns false. */
	UFUNCTION(BlueprintCallable, Category = "Leaderboard", meta = (DisplayName = "Submit Score"))
	virtual bool SubmitScore(int32 Score, const FString& Category);

	/** Get top N entries for a category. Stub: clears OutEntries, returns false. */
	UFUNCTION(BlueprintCallable, Category = "Leaderboard", meta = (DisplayName = "Get Ranking"))
	virtual bool GetRanking(const FString& Category, int32 TopN, TArray<FHomeWorldLeaderboardEntry>& OutEntries);
};
