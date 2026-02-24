// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSessionSubsystem.h"

bool UHomeWorldSessionSubsystem::CreateSession(int32 MaxPlayers)
{
	// Stub: implement with SteamSockets in Week 2.
	return false;
}

bool UHomeWorldSessionSubsystem::JoinSession(const FString& ConnectionString)
{
	// Stub: implement with SteamSockets in Week 2.
	return false;
}

EHomeWorldSessionState UHomeWorldSessionSubsystem::GetSessionState() const
{
	return EHomeWorldSessionState::None;
}
