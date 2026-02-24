// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldLeaderboardSubsystem.h"

bool UHomeWorldLeaderboardSubsystem::SubmitScore(int32 Score, const FString& Category)
{
	// Stub: implement with Steam API or SteamLead in Weeks 3-4.
	return false;
}

bool UHomeWorldLeaderboardSubsystem::GetRanking(const FString& Category, int32 TopN, TArray<FHomeWorldLeaderboardEntry>& OutEntries)
{
	// Stub: implement with Steam API or SteamLead in Weeks 3-4.
	OutEntries.Empty();
	return false;
}
