// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Templates/Function.h"

class AActor;
class AHomeWorldCharacter;

/**
 * Hover target pick. Production uses the actor registry. The world scan stays
 * so a host test can prove both paths choose the same actor.
 * Center look is off unless a test turns it on. It does not run in a played game.
 */
namespace HomeWorldOpeningHover
{
	void SetCenterLookForTest(bool bEnable);
	bool UseCenterLookForTest();

	AActor* PickFrom(AHomeWorldCharacter* Character, TFunctionRef<void(TFunctionRef<void(AActor*)>)> ForEach);
	AActor* PickByWorldScan(AHomeWorldCharacter* Character);
	AActor* PickByRegistry(AHomeWorldCharacter* Character);
}
