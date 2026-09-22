// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritStealthTypes.h"

namespace HomeWorldSpiritStealth
{
	bool RevealsSpiritInVolume(EHomeWorldSpiritLitSourceKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldSpiritLitSourceKind::Campfire:
		case EHomeWorldSpiritLitSourceKind::NpcTorch:
		case EHomeWorldSpiritLitSourceKind::SpiritTorch:
			return true;
		case EHomeWorldSpiritLitSourceKind::BodyMundaneTorch:
		default:
			return false;
		}
	}

	const TCHAR* GetLitSourceLogName(EHomeWorldSpiritLitSourceKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldSpiritLitSourceKind::Campfire: return TEXT("Campfire");
		case EHomeWorldSpiritLitSourceKind::NpcTorch: return TEXT("NpcTorch");
		case EHomeWorldSpiritLitSourceKind::SpiritTorch: return TEXT("SpiritTorch");
		case EHomeWorldSpiritLitSourceKind::BodyMundaneTorch: return TEXT("BodyMundaneTorch");
		default: return TEXT("Unknown");
		}
	}
}
