// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "HomeWorldSessionSubsystem.generated.h"

/** Session state for co-op (Week 2+). Stub; implement with SteamSockets. */
UENUM(BlueprintType)
enum class EHomeWorldSessionState : uint8
{
	None,
	Creating,
	Created,
	Joining,
	Joined,
	Failed
};

/**
 * World subsystem for co-op session (create/join). Game and UI call this API; implement with SteamSockets in Week 2.
 * Stub only; no backend implementation.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldSessionSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	/** Create a session (host). Stub: returns false. Implement with SteamSockets. */
	UFUNCTION(BlueprintCallable, Category = "Session", meta = (DisplayName = "Create Session"))
	virtual bool CreateSession(int32 MaxPlayers);

	/** Join an existing session (client). Stub: returns false. Implement with SteamSockets. */
	UFUNCTION(BlueprintCallable, Category = "Session", meta = (DisplayName = "Join Session"))
	virtual bool JoinSession(const FString& ConnectionString);

	/** Current session state. Stub: returns None. */
	UFUNCTION(BlueprintCallable, Category = "Session", meta = (DisplayName = "Get Session State"))
	virtual EHomeWorldSessionState GetSessionState() const;
};
