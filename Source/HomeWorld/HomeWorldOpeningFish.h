// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class AActor;
class UWorld;

/**
 * The pond the fish verb uses. FindPond reads the actor registry.
 * FindPondByWorldScan is the previous walk, kept for the parity test.
 */
namespace HomeWorldOpeningFish
{
	AActor* FindPond(UWorld* World);
	AActor* FindPondByWorldScan(UWorld* World);
}
