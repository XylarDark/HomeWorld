// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldInteractResolver.h"

#include "HomeWorldCharacter.h"
#include "Engine/World.h"
#include "EngineUtils.h"

namespace HomeWorldT0BeatNodes
{
	const TArray<TArray<FName>>& TagsPerNode()
	{
		static const TArray<TArray<FName>> PerNode = {
			{ FName(TEXT("NODE_KETTLE")), FName(TEXT("Kettle")) },
			{ FName(TEXT("NODE_PLANT_SLOT")), FName(TEXT("PlantSlot")) },
			{ FName(TEXT("NODE_BACKPACK")), FName(TEXT("Backpack")) },
			{ FName(TEXT("NODE_FIELD_GATHER")), FName(TEXT("FieldGather")) },
			{ FName(TEXT("NODE_DAY_CAMP")), FName(TEXT("DayCamp")) },
			{ FName(TEXT("NODE_BED")), FName(TEXT("Bed")) },
			{ FName(TEXT("NODE_GARDEN")), FName(TEXT("Garden")) },
			{ FName(TEXT("NODE_CONSUMABLE_STATION")), FName(TEXT("ConsumableStation")) },
			{ FName(TEXT("NODE_ARMOR_TABLE")), FName(TEXT("ArmorTable")) },
		};
		return PerNode;
	}

	const TArray<FName>& TagsFor(ENode Node)
	{
		return TagsPerNode()[static_cast<uint8>(Node)];
	}

	bool ActorCarriesTagFor(const AActor* Actor, ENode Node)
	{
		if (!Actor)
		{
			return false;
		}
		for (const FName& Tag : TagsFor(Node))
		{
			if (Actor->ActorHasTag(Tag))
			{
				return true;
			}
		}
		return false;
	}
}

namespace HomeWorldInteract
{
	struct FVerbEntry
	{
		EVerb Verb;
		int32 Priority;
		EChain Chain;
		float ReachCm;
		bool bLook;
		bool bWall;
		bool bHover;
		bool (AHomeWorldCharacter::*Try)();
	};

	struct FProximityExtra
	{
		FName Tag;
		const TCHAR* NameContains;
		bool bRequireVisible;
	};

	static const FVerbEntry GVerbs[] = {
		{ EVerb::PartyInvite, 10, EChain::Both, 280.f, true, true, true, &AHomeWorldCharacter::TryPartyInviteInFront },
		{ EVerb::OpeningSpirit, 20, EChain::Both, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningSpiritInFront },
		{ EVerb::PartnerLead, 30, EChain::Both, 280.f, true, true, true, &AHomeWorldCharacter::TryPartnerLeadInside },
		{ EVerb::CloudDescent, 40, EChain::World, 0.f, false, false, false, &AHomeWorldCharacter::TryStartCloudDescent },
		{ EVerb::ShrinePortal, 50, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryShrinePortalInteract },
		{ EVerb::Garden, 60, EChain::Both, 280.f, true, true, true, &AHomeWorldCharacter::TryGardenInteractInFront },
		{ EVerb::Kettle, 70, EChain::Both, 280.f, true, true, true, &AHomeWorldCharacter::TryNodeKettleInteractInFront },
		{ EVerb::OpeningStation, 80, EChain::SizeTest, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningStationInFront },
		{ EVerb::OpeningDog, 90, EChain::SizeTest, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningDogInFront },
		{ EVerb::OpeningFish, 100, EChain::SizeTest, 200.f, false, true, false, &AHomeWorldCharacter::TryOpeningFish },
		{ EVerb::OpeningNightSet, 110, EChain::SizeTest, 400.f, true, true, true, &AHomeWorldCharacter::TryOpeningNightSetInFront },
		{ EVerb::OpeningHotSpring, 120, EChain::SizeTest, 600.f, false, true, false, &AHomeWorldCharacter::TryOpeningHotSpringHealInFront },
		{ EVerb::OpeningDelivery, 130, EChain::SizeTest, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningDeliveryInFront },
		{ EVerb::OpeningBed, 140, EChain::SizeTest, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningBedInFront },
		{ EVerb::OpeningZipline, 150, EChain::SizeTest, 280.f, true, true, true, &AHomeWorldCharacter::TryOpeningZiplineInFront },
		{ EVerb::OpeningShrine, 160, EChain::SizeTest, 280.f, false, false, false, &AHomeWorldCharacter::TryOpeningShrineInFront },
		{ EVerb::Dung, 200, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryDungInteractInFront },
		{ EVerb::Fertilizer, 210, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryMixFertilizerInteractInFront },
		{ EVerb::Wound, 220, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryWoundInteractInFront },
		{ EVerb::Bull, 230, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryBullInteractInFront },
		{ EVerb::Barn, 240, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryBarnInteractInFront },
		{ EVerb::EaseGuard, 250, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryEaseGuardInFront },
		{ EVerb::FreeCaptive, 260, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryFreeCaptiveInFront },
		{ EVerb::Backpack, 270, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryNodeBackpackInteractInFront },
		{ EVerb::FieldGather, 280, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryNodeFieldGatherInteractInFront },
		{ EVerb::DayCamp, 290, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryNodeDayCampInteractInFront },
		{ EVerb::PlantSlot, 300, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryNodePlantSlotInteractInFront },
		{ EVerb::Tame, 310, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryTameBeastInFront },
		{ EVerb::HealSpirit, 320, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryHealSpiritInFront },
		{ EVerb::Nurture, 330, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryNurtureInFront },
		{ EVerb::Store, 340, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryStoreTransferInFront },
		{ EVerb::Minigame, 350, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryMinigameInFront },
		{ EVerb::BossSeal, 360, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryBossSealInFront },
		{ EVerb::Craft, 370, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryCraftInFront },
		{ EVerb::Harvest, 380, EChain::World, 280.f, false, true, false, &AHomeWorldCharacter::TryHarvestInFront },
	};

	static const FProximityExtra GExtras[] = {
		{ NAME_None, TEXT("Lupine"), true },
		{ NAME_None, TEXT("Bed"), false },
		{ FName(TEXT("NODE_OPENING_WISP")), nullptr, true },
		{ FName(TEXT("NODE_OPENING_DELIVERY")), nullptr, true },
	};

	static EVerb GProbe = EVerb::Count;
	static EVerb GResolved = EVerb::Count;

	static bool Allows(const FVerbEntry& Entry, bool bSizeTest)
	{
		if (bSizeTest)
		{
			return Entry.Chain != EChain::World;
		}
		return Entry.Chain != EChain::SizeTest;
	}

	static const FVerbEntry* EntryFor(EVerb Verb)
	{
		for (const FVerbEntry& Entry : GVerbs)
		{
			if (Entry.Verb == Verb)
			{
				return &Entry;
			}
		}
		return nullptr;
	}

	static FSpec ToSpec(const FVerbEntry& Entry)
	{
		FSpec Spec;
		Spec.Verb = Entry.Verb;
		Spec.Priority = Entry.Priority;
		Spec.Chain = Entry.Chain;
		Spec.ReachCm = Entry.ReachCm;
		Spec.bLook = Entry.bLook;
		Spec.bWall = Entry.bWall;
		Spec.bHover = Entry.bHover;
		return Spec;
	}

	static EVerb VerbForNode(HomeWorldT0BeatNodes::ENode Node)
	{
		using HomeWorldT0BeatNodes::ENode;
		switch (Node)
		{
		case ENode::Kettle: return EVerb::Kettle;
		case ENode::PlantSlot: return EVerb::PlantSlot;
		case ENode::Backpack: return EVerb::Backpack;
		case ENode::FieldGather: return EVerb::FieldGather;
		case ENode::DayCamp: return EVerb::DayCamp;
		case ENode::Bed: return EVerb::OpeningBed;
		case ENode::Garden: return EVerb::Garden;
		case ENode::ConsumableStation: return EVerb::OpeningStation;
		case ENode::ArmorTable: return EVerb::OpeningStation;
		default: return EVerb::Count;
		}
	}

	static bool WorldHasTag(UWorld* World, FName Tag)
	{
		if (!World || Tag.IsNone())
		{
			return false;
		}
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (It->ActorHasTag(Tag))
			{
				return true;
			}
		}
		return false;
	}

	bool TrySpecFor(const AActor* Actor, FSpec& Out)
	{
		if (!Actor)
		{
			return false;
		}
		const TArray<TArray<FName>>& PerNode = HomeWorldT0BeatNodes::TagsPerNode();
		for (int32 Index = 0; Index < PerNode.Num(); ++Index)
		{
			const HomeWorldT0BeatNodes::ENode Node = static_cast<HomeWorldT0BeatNodes::ENode>(Index);
			if (!HomeWorldT0BeatNodes::ActorCarriesTagFor(Actor, Node))
			{
				continue;
			}
			const EVerb Verb = VerbForNode(Node);
			if (const FVerbEntry* Entry = EntryFor(Verb))
			{
				Out = ToSpec(*Entry);
			}
			else
			{
				Out = FSpec();
			}
			Out.Node = Node;
			Out.Verb = Verb;
			Out.bBeatNode = true;
			return true;
		}
		return false;
	}

	bool IsProximityExtra(const AActor* Actor)
	{
		if (!Actor)
		{
			return false;
		}
		for (const FProximityExtra& Extra : GExtras)
		{
			if (Extra.bRequireVisible && Actor->IsHidden())
			{
				continue;
			}
			if (!Extra.Tag.IsNone() && Actor->ActorHasTag(Extra.Tag))
			{
				return true;
			}
			if (Extra.NameContains && Actor->GetActorNameOrLabel().Contains(Extra.NameContains))
			{
				return true;
			}
		}
		return false;
	}

	const FSpec* SpecFor(EVerb Verb)
	{
		static FSpec Cache[static_cast<int32>(EVerb::Count)];
		static bool bReady = false;
		if (!bReady)
		{
			for (const FVerbEntry& Entry : GVerbs)
			{
				Cache[static_cast<int32>(Entry.Verb)] = ToSpec(Entry);
			}
			bReady = true;
		}
		const int32 Index = static_cast<int32>(Verb);
		if (Index < 0 || Index >= static_cast<int32>(EVerb::Count))
		{
			return nullptr;
		}
		if (Cache[Index].Verb != Verb)
		{
			return nullptr;
		}
		return &Cache[Index];
	}

	float ReachCm(EVerb Verb)
	{
		if (const FSpec* Spec = SpecFor(Verb))
		{
			return Spec->ReachCm;
		}
		return 280.f;
	}

	bool Admits(AHomeWorldCharacter* Character, EVerb Verb, const AActor* Target, bool bPathUsesLook)
	{
		if (!Character || !Target)
		{
			return false;
		}
		const FSpec* Spec = SpecFor(Verb);
		if (!Spec)
		{
			return false;
		}
		if (FVector::Dist2D(Character->GetActorLocation(), Target->GetActorLocation()) > Spec->ReachCm)
		{
			return false;
		}
		if (Spec->bWall && !Character->HasOpeningLineOfSight(Target))
		{
			return false;
		}
		if (bPathUsesLook && Spec->bLook)
		{
			float LookSq = 0.f;
			if (!Character->OpeningLookDistSq(Target, LookSq))
			{
				return false;
			}
		}
		return true;
	}

	bool Resolve(AHomeWorldCharacter* Character)
	{
		GResolved = EVerb::Count;
		if (!Character)
		{
			return false;
		}
		const bool bSizeTest = Character->UsesSizeTestInteractChain();
		TArray<const FVerbEntry*> Ordered;
		for (const FVerbEntry& Entry : GVerbs)
		{
			if (Allows(Entry, bSizeTest))
			{
				Ordered.Add(&Entry);
			}
		}
		Ordered.Sort([](const FVerbEntry& A, const FVerbEntry& B)
		{
			return A.Priority < B.Priority;
		});
		for (const FVerbEntry* Entry : Ordered)
		{
			if ((Character->*(Entry->Try))())
			{
				GResolved = Entry->Verb;
				return true;
			}
			if (GProbe == Entry->Verb && WorldHasTag(Character->GetWorld(), ProbeTag(Entry->Verb)))
			{
				GResolved = Entry->Verb;
				return true;
			}
		}
		return false;
	}

	void GetChainOrder(bool bSizeTest, TArray<EVerb>& Out)
	{
		TArray<FVerbEntry> Ordered;
		for (const FVerbEntry& Entry : GVerbs)
		{
			if (Allows(Entry, bSizeTest))
			{
				Ordered.Add(Entry);
			}
		}
		Ordered.Sort([](const FVerbEntry& A, const FVerbEntry& B)
		{
			return A.Priority < B.Priority;
		});
		Out.Reset();
		for (const FVerbEntry& Entry : Ordered)
		{
			Out.Add(Entry.Verb);
		}
	}

	void ArmProbe(EVerb Verb)
	{
		GProbe = Verb;
		GResolved = EVerb::Count;
	}

	void ClearProbe()
	{
		GProbe = EVerb::Count;
	}

	EVerb ResolvedVerb()
	{
		return GResolved;
	}

	const TCHAR* VerbName(EVerb Verb)
	{
		switch (Verb)
		{
		case EVerb::PartyInvite: return TEXT("PartyInvite");
		case EVerb::OpeningSpirit: return TEXT("OpeningSpirit");
		case EVerb::PartnerLead: return TEXT("PartnerLead");
		case EVerb::CloudDescent: return TEXT("CloudDescent");
		case EVerb::ShrinePortal: return TEXT("ShrinePortal");
		case EVerb::Garden: return TEXT("Garden");
		case EVerb::Kettle: return TEXT("Kettle");
		case EVerb::OpeningStation: return TEXT("OpeningStation");
		case EVerb::OpeningDog: return TEXT("OpeningDog");
		case EVerb::OpeningFish: return TEXT("OpeningFish");
		case EVerb::OpeningNightSet: return TEXT("OpeningNightSet");
		case EVerb::OpeningHotSpring: return TEXT("OpeningHotSpring");
		case EVerb::OpeningDelivery: return TEXT("OpeningDelivery");
		case EVerb::OpeningBed: return TEXT("OpeningBed");
		case EVerb::OpeningZipline: return TEXT("OpeningZipline");
		case EVerb::OpeningShrine: return TEXT("OpeningShrine");
		case EVerb::Dung: return TEXT("Dung");
		case EVerb::Fertilizer: return TEXT("Fertilizer");
		case EVerb::Wound: return TEXT("Wound");
		case EVerb::Bull: return TEXT("Bull");
		case EVerb::Barn: return TEXT("Barn");
		case EVerb::EaseGuard: return TEXT("EaseGuard");
		case EVerb::FreeCaptive: return TEXT("FreeCaptive");
		case EVerb::Backpack: return TEXT("Backpack");
		case EVerb::FieldGather: return TEXT("FieldGather");
		case EVerb::DayCamp: return TEXT("DayCamp");
		case EVerb::PlantSlot: return TEXT("PlantSlot");
		case EVerb::Tame: return TEXT("Tame");
		case EVerb::HealSpirit: return TEXT("HealSpirit");
		case EVerb::Nurture: return TEXT("Nurture");
		case EVerb::Store: return TEXT("Store");
		case EVerb::Minigame: return TEXT("Minigame");
		case EVerb::BossSeal: return TEXT("BossSeal");
		case EVerb::Craft: return TEXT("Craft");
		case EVerb::Harvest: return TEXT("Harvest");
		default: return TEXT("Count");
		}
	}

	FName ProbeTag(EVerb Verb)
	{
		return FName(*FString::Printf(TEXT("INTERACT_%s"), VerbName(Verb)));
	}
}
