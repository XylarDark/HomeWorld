// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGcPlaceholderTypes.h"

namespace HomeWorldGcPlaceholder
{
	const TCHAR* GetEnterLogLine(EHomeWorldGcPlaceholderKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldGcPlaceholderKind::Woodshop:
			return TEXT("PLACEHOLDER:WOODSHOP enter");
		case EHomeWorldGcPlaceholderKind::TextileShop:
			return TEXT("PLACEHOLDER:TEXTILE enter");
		case EHomeWorldGcPlaceholderKind::ResearchShop:
			return TEXT("PLACEHOLDER:RESEARCH enter");
		case EHomeWorldGcPlaceholderKind::CottageKitchen:
			return TEXT("PLACEHOLDER:COTTAGE_KITCHEN");
		case EHomeWorldGcPlaceholderKind::CottageBedroom:
			return TEXT("PLACEHOLDER:COTTAGE_BEDROOM");
		case EHomeWorldGcPlaceholderKind::CottageLivingCauldron:
			return TEXT("PLACEHOLDER:CAULDRON");
		default:
			return TEXT("PLACEHOLDER:UNKNOWN");
		}
	}

	bool RequiresCottageUnlock(EHomeWorldGcPlaceholderKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldGcPlaceholderKind::CottageKitchen:
		case EHomeWorldGcPlaceholderKind::CottageBedroom:
		case EHomeWorldGcPlaceholderKind::CottageLivingCauldron:
			return true;
		default:
			return false;
		}
	}
}
