// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

/**
 * Height, standoff, and tag names from Content/Python/placement_constants.json.
 * The cabin shell and the placer read the same file.
 */
namespace HomeWorldPlacement
{
	struct FConstants
	{
		float CounterHeightCm = 100.f;
		float CounterDepthCm = 70.f;
		float CounterLengthCm = 520.f;
		float RevealCounterX = 910.f;
		float RevealCounterY = 80.f;
		float PartnerStandoffCm = 180.f;
		float PondStandoffCm = 100.f;
		FString TagKettle = TEXT("NODE_KETTLE");
		FString TagKettleCounter = TEXT("KettleCounter");
		FString TagConsumableStation = TEXT("NODE_CONSUMABLE_STATION");
		FString TagArmorTable = TEXT("NODE_ARMOR_TABLE");
		FString TagPartner = TEXT("NPC_PARTNER");
		FString TagOpeningDog = TEXT("NODE_OPENING_DOG");
		bool bLoaded = false;
	};

	const FConstants& Get();
}
