// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldHomeLoopTypes.generated.h"

/** Station ids from Docs/42_HOME_LOOP_DESIGN.md. Order is the query order. */
UENUM()
enum class EHomeWorldHomeStation : uint8
{
	Sink,
	Board,
	Pot,
	Stove,
	Oven,
	Garbage
};
