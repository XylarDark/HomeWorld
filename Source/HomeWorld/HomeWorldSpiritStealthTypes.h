// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldSpiritStealthTypes.generated.h"

/** SS-A: reveal sources for spirit lit / alert (overlap volumes only). */
UENUM(BlueprintType)
enum class EHomeWorldSpiritLitSourceKind : uint8
{
	Campfire UMETA(DisplayName = "Campfire"),
	NpcTorch UMETA(DisplayName = "NpcTorch"),
	SpiritTorch UMETA(DisplayName = "SpiritTorch"),
	/** Mundane body torch light — does NOT reveal spirits (body darkness safety only). */
	BodyMundaneTorch UMETA(DisplayName = "BodyMundaneTorch"),
};

namespace HomeWorldSpiritStealth
{
	HOMEWORLD_API bool RevealsSpiritInVolume(EHomeWorldSpiritLitSourceKind Kind);
	HOMEWORLD_API const TCHAR* GetLitSourceLogName(EHomeWorldSpiritLitSourceKind Kind);
}
