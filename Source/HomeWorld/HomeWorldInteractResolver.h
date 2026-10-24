// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

class AActor;
class AHomeWorldCharacter;

/**
 * Beat-prop tags. A prop is admitted by the tag it carries.
 * The interact gate and the verbs read this table, not lists of their own.
 */
namespace HomeWorldT0BeatNodes
{
	enum class ENode : uint8
	{
		Kettle,
		PlantSlot,
		Backpack,
		FieldGather,
		DayCamp,
		Bed,
		Garden,
		ConsumableStation,
		ArmorTable,
	};

	const TArray<TArray<FName>>& TagsPerNode();
	const TArray<FName>& TagsFor(ENode Node);
	bool ActorCarriesTagFor(const AActor* Actor, ENode Node);
}

/**
 * One press. Each verb is a row: priority, which chain it belongs to, and the
 * reach / look / wall / hover contract. Resolve walks the rows in priority order
 * and runs the verb. A new prop is a row, not a branch in the ability.
 */
namespace HomeWorldInteract
{
	enum class EVerb : uint8
	{
		PartyInvite,
		OpeningSpirit,
		PartnerLead,
		CloudDescent,
		ShrinePortal,
		Garden,
		Kettle,
		OpeningStation,
		OpeningDog,
		OpeningFish,
		OpeningNightSet,
		OpeningHotSpring,
		OpeningDelivery,
		OpeningBed,
		OpeningZipline,
		OpeningShrine,
		Dung,
		Fertilizer,
		Wound,
		Bull,
		Barn,
		EaseGuard,
		FreeCaptive,
		Backpack,
		FieldGather,
		DayCamp,
		PlantSlot,
		Tame,
		HealSpirit,
		Nurture,
		Store,
		Minigame,
		BossSeal,
		Craft,
		Harvest,
		Count
	};

	enum class EChain : uint8
	{
		SizeTest,
		World,
		Both
	};

	struct FSpec
	{
		EVerb Verb = EVerb::Count;
		HomeWorldT0BeatNodes::ENode Node = HomeWorldT0BeatNodes::ENode::Kettle;
		int32 Priority = 0;
		float ReachCm = 280.f;
		bool bLook = true;
		bool bWall = true;
		bool bHover = true;
		bool bBeatNode = false;
		EChain Chain = EChain::Both;
	};

	/** Beat-node tags only. The gate uses this to admit a prop. */
	bool TrySpecFor(const AActor* Actor, FSpec& Out);

	/**
	 * Herbs, the bed, night wisps, and delivery enter the hover scan by name or tag.
	 * Hidden herbs, wisps, and delivery nodes stay out. A hidden bed stays in.
	 */
	bool IsProximityExtra(const AActor* Actor);

	const FSpec* SpecFor(EVerb Verb);
	float ReachCm(EVerb Verb);

	/**
	 * Flat reach and optional wall from the verb row. Look runs only when the caller says
	 * this path uses look (the bed fallback passes false even though the row has bLook).
	 */
	bool Admits(AHomeWorldCharacter* Character, EVerb Verb, const AActor* Target, bool bPathUsesLook);

	/** Run the chain for this level. The first verb that handles the press wins. */
	bool Resolve(AHomeWorldCharacter* Character);

	void GetChainOrder(bool bSizeTest, TArray<EVerb>& Out);

	/** Tests arm one verb. A tagged actor then counts as that verb handling the press. */
	void ArmProbe(EVerb Verb);
	void ClearProbe();
	EVerb ResolvedVerb();
	FName ProbeTag(EVerb Verb);
	const TCHAR* VerbName(EVerb Verb);
}
