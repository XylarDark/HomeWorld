// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameMode.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldPlayerState.h"

AHomeWorldGameMode::AHomeWorldGameMode()
{
	DefaultPawnClass = AHomeWorldCharacter::StaticClass();
	PlayerStateClass = AHomeWorldPlayerState::StaticClass();
}
