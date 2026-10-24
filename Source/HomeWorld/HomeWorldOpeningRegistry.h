// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Templates/Function.h"

class AActor;
class UWorld;

/**
 * Actors for opening lookup. Built once, then kept by spawn and destroy.
 * Finds read this list. They do not walk the world again.
 */
namespace HomeWorldOpeningRegistry
{
	void Bind(UWorld* World);
	void Visit(UWorld* World, TFunctionRef<void(AActor*)> Fn);
	AActor* FindNamed(UWorld* World, const TCHAR* Name, bool bExact);
	AActor* FindTagged(UWorld* World, const TCHAR* Tag, const TCHAR* AltTag);
}
