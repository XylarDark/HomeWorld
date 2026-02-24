// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "Commandlets/Commandlet.h"
#include "CreateMECCommandlet.generated.h"

/**
 * Commandlet that creates or updates a Mass Entity Config asset (e.g. MEC_FamilyGatherer).
 * Run: UnrealEditor.exe HomeWorld.uproject -run=HomeWorldEditor.CreateMEC [Path=/Game/HomeWorld/Mass/MEC_FamilyGatherer]
 */
UCLASS()
class UCreateMECCommandlet : public UCommandlet
{
	GENERATED_BODY()

public:
	virtual int32 Main(const FString& Params) override;
};
