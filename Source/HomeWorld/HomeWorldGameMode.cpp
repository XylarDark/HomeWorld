// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameMode.h"
#include "HomeWorldCharacter.h"

AHomeWorldGameMode::AHomeWorldGameMode()
{
	DefaultPawnClass = AHomeWorldCharacter::StaticClass();
}
