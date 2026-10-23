// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlaytestBeats.h"

namespace HomeWorldPlaytestBeats
{
	namespace
	{
		using F = EHomeWorldOpeningFact;

		/** The facts runner steps 1..LastStep publish. Step 3 (the partner walk) publishes none. */
		TArray<EHomeWorldOpeningFact> RunnerFactsThrough(int32 LastStep)
		{
			TArray<EHomeWorldOpeningFact> Out;
			if (LastStep >= 1) Out.Add(F::SpiritClaimed);
			if (LastStep >= 2) { Out.Add(F::HerbFromWest); Out.Add(F::HerbFromEast); }
			if (LastStep >= 4) Out.Add(F::Backpack);
			if (LastStep >= 5) Out.Add(F::KettleBrewed);
			if (LastStep >= 6) Out.Add(F::HasMixedHerb);
			if (LastStep >= 7) Out.Add(F::DogTamed);
			if (LastStep >= 8) Out.Add(F::FishCaught);
			if (LastStep >= 9) Out.Add(F::Slept);
			return Out;
		}

		FRow Make(EBeat Beat, const TCHAR* Word, int32 Skip, int32 ReadyAfter, float Standoff,
			ETarget Target, const TCHAR* Tag, const TCHAR* AltTag, const TCHAR* Name, EStand Stand,
			const TCHAR* Note, bool bNightProps = false, bool bCarryWisps = false)
		{
			FRow Row;
			Row.Beat = Beat;
			Row.Word = Word;
			Row.SkipStep = Skip;
			Row.ReadyAfterStep = ReadyAfter;
			Row.StandoffCm = Standoff;
			Row.Target = Target;
			Row.Tag = Tag;
			Row.AltTag = AltTag;
			Row.Name = Name;
			Row.Stand = Stand;
			Row.bGazeFromBounds = Stand == EStand::Bounds;
			Row.bNightProps = bNightProps;
			Row.bCarryWisps = bCarryWisps;
			Row.Note = Note;
			// Stress has no runner. A skip stop needs the steps before it; the rest need all nine.
			const int32 LastRun = Beat == EBeat::Stress ? 0 : (Skip > 0 ? Skip - 1 : 9);
			Row.Requires = RunnerFactsThrough(LastRun);
			return Row;
		}

		struct FKey
		{
			const TCHAR* Key;
			EBeat Beat;
		};

		/** Order matters: "herb collection" carries both herb and collect; "nightglide" carries night. */
		const FKey GKeys[] = {
			{ TEXT("heal"), EBeat::Heal },
			{ TEXT("spring"), EBeat::Heal },
			{ TEXT("herb"), EBeat::Herbs },
			{ TEXT("garden"), EBeat::Herbs },
			{ TEXT("stealth"), EBeat::Stealth },
			{ TEXT("spirit"), EBeat::Spirit },
			{ TEXT("backpack"), EBeat::Backpack },
			{ TEXT("partner"), EBeat::Backpack },
			{ TEXT("gift"), EBeat::Backpack },
			{ TEXT("kettle"), EBeat::Kettle },
			{ TEXT("tea"), EBeat::Kettle },
			{ TEXT("station"), EBeat::Station },
			{ TEXT("counter"), EBeat::Station },
			{ TEXT("mix"), EBeat::Station },
			{ TEXT("dog"), EBeat::Dog },
			{ TEXT("grace"), EBeat::Dog },
			{ TEXT("fish"), EBeat::Fish },
			{ TEXT("pond"), EBeat::Fish },
			{ TEXT("sleep"), EBeat::Sleep },
			{ TEXT("bed"), EBeat::Sleep },
			{ TEXT("wisp"), EBeat::Collect },
			{ TEXT("collect"), EBeat::Collect },
			{ TEXT("nightglide"), EBeat::NightGlide },
			{ TEXT("night"), EBeat::Night },
			{ TEXT("glider"), EBeat::Glider },
			{ TEXT("delivery"), EBeat::Delivery },
			{ TEXT("daycamp"), EBeat::DayCamp },
			{ TEXT("dawnglide"), EBeat::DawnGlide },
			{ TEXT("shrine"), EBeat::Shrine },
			{ TEXT("stress"), EBeat::Stress },
			{ TEXT("ease"), EBeat::Ease },
		};
	}

	const TArray<FRow>& Rows()
	{
		// Standoffs, tags, names and runner steps are the values DebugFastForwardOpening
		// hard-coded on main b5552ae6. Only their home moved.
		static const TArray<FRow> Table = {
			Make(EBeat::Spirit, TEXT("spirit"), 1, 0, 260.f, ETarget::Reveal, nullptr, nullptr, nullptr, EStand::Bounds,
				TEXT("E at the spirit")),
			Make(EBeat::Herbs, TEXT("herbs"), 2, 0, 260.f, ETarget::Tagged, TEXT("NODE_GARDEN_EAST"), nullptr, nullptr, EStand::Bounds,
				TEXT("E at the east bed, draw the trace heart")),
			Make(EBeat::Backpack, TEXT("backpack"), 3, 0, 260.f, ETarget::Tagged, TEXT("NPC_PARTNER"), nullptr, nullptr, EStand::Bounds,
				TEXT("E at the partner: the backpack")),
			Make(EBeat::Kettle, TEXT("kettle"), 5, 0, 220.f, ETarget::Tagged, TEXT("KettleCounter"), TEXT("NODE_CONSUMABLE_STATION"), nullptr, EStand::Bounds,
				TEXT("E at the counter: open, mix, then brew")),
			Make(EBeat::Station, TEXT("station"), 6, 0, 220.f, ETarget::Tagged, TEXT("NODE_CONSUMABLE_STATION"), nullptr, nullptr, EStand::Bounds,
				TEXT("E at the counter: open, then mix")),
			Make(EBeat::Dog, TEXT("dog"), 7, 0, 650.f, ETarget::Dog, nullptr, nullptr, nullptr, EStand::Bounds,
				TEXT("walk up slowly, draw the Grace trace, then E")),
			Make(EBeat::Fish, TEXT("fish"), 8, 0, 260.f, ETarget::Named, nullptr, nullptr, TEXT("Water_Pond"), EStand::PondEdge,
				TEXT("E at the pond bank, one fish")),
			Make(EBeat::Sleep, TEXT("sleep"), 9, 0, 180.f, ETarget::Named, nullptr, nullptr, TEXT("SM_Size_Bed"), EStand::Bounds,
				TEXT("E at the bed: sleep")),
			Make(EBeat::Night, TEXT("night"), 0, 9, 180.f, ETarget::Named, nullptr, nullptr, TEXT("SM_Size_Bed"), EStand::None,
				TEXT("night is on, the bed is behind you")),
			Make(EBeat::Collect, TEXT("collect"), 0, 9, 350.f, ETarget::CopseWisp, nullptr, nullptr, nullptr, EStand::Bounds,
				TEXT("E at the wisp, click the heart"), true, false),
			Make(EBeat::Heal, TEXT("heal"), 0, 9, 470.f, ETarget::Named, nullptr, nullptr, TEXT("Water_HotSpring"), EStand::Bounds,
				TEXT("E at the hot springs, the heal takes 20s"), true, true),
			Make(EBeat::Glider, TEXT("glider"), 0, 10, 220.f, ETarget::Tagged, TEXT("NODE_ARMOR_TABLE"), TEXT("ArmorTable"), nullptr, EStand::Bounds,
				TEXT("E at the armory: craft the glider")),
			Make(EBeat::Delivery, TEXT("delivery"), 0, 11, 200.f, ETarget::Tagged, TEXT("NODE_OPENING_DELIVERY"), nullptr, nullptr, EStand::Bounds,
				TEXT("E at the wood node: set the healed wisp")),
			Make(EBeat::DayCamp, TEXT("daycamp"), 0, 12, 320.f, ETarget::Tagged, TEXT("NODE_OPENING_DAY_CAMP"), nullptr, nullptr, EStand::Bounds,
				TEXT("walk into the clearing")),
			Make(EBeat::DawnGlide, TEXT("dawnglide"), 0, 13, 180.f, ETarget::Tagged, TEXT("GlideStart"), nullptr, nullptr, EStand::Bounds,
				TEXT("the launch is yours")),
			Make(EBeat::NightGlide, TEXT("nightglide"), 0, 14, 180.f, ETarget::Tagged, TEXT("GlideStart"), nullptr, nullptr, EStand::Bounds,
				TEXT("travel only, the launch is yours")),
			Make(EBeat::Stealth, TEXT("stealth"), 0, 15, 260.f, ETarget::Tagged, TEXT("NODE_GUARD"), nullptr, nullptr, EStand::Bounds,
				TEXT("reach the guard")),
			Make(EBeat::Ease, TEXT("ease"), 0, 16, 180.f, ETarget::Tagged, TEXT("NODE_OPENING_EASE"), nullptr, nullptr, EStand::Bounds,
				TEXT("the wind-up is yours")),
			Make(EBeat::Shrine, TEXT("shrine"), 0, 17, 180.f, ETarget::Tagged, TEXT("NODE_OPENING_SHRINE"), nullptr, nullptr, EStand::Bounds,
				TEXT("E at the shrine")),
			Make(EBeat::Stress, TEXT("stress"), 0, 0, 260.f, ETarget::None, nullptr, nullptr, nullptr, EStand::None,
				TEXT("stress 90, cap is 100")),
		};
		return Table;
	}

	const FRow* RowFor(int32 Beat)
	{
		const TArray<FRow>& Table = Rows();
		const int32 Index = Beat - 1;
		return Table.IsValidIndex(Index) ? &Table[Index] : nullptr;
	}

	int32 FromText(const FString& Text)
	{
		FString Key = Text.ToLower();
		Key.ReplaceInline(TEXT("_"), TEXT(""));
		Key.ReplaceInline(TEXT(" "), TEXT(""));
		if (Key.IsEmpty())
		{
			return static_cast<int32>(EBeat::Night);
		}
		for (const FKey& Entry : GKeys)
		{
			if (Key.Contains(Entry.Key))
			{
				return static_cast<int32>(Entry.Beat);
			}
		}
		return 0;
	}

	const TCHAR* WordFor(int32 Beat)
	{
		const FRow* Row = RowFor(Beat);
		return Row ? Row->Word : TEXT("night");
	}

	float StandoffCm(int32 Beat)
	{
		const FRow* Row = RowFor(Beat);
		return Row ? Row->StandoffCm : 260.f;
	}

	int32 SkipStep(int32 Beat)
	{
		const FRow* Row = RowFor(Beat);
		return Row ? Row->SkipStep : 0;
	}

	int32 ReadyAfterStep(int32 Beat)
	{
		const FRow* Row = RowFor(Beat);
		return Row ? Row->ReadyAfterStep : 0;
	}

	FString ListText()
	{
		TArray<FString> Words;
		for (const FRow& Row : Rows())
		{
			Words.Add(Row.Word);
		}
		return FString::Join(Words, TEXT(", "));
	}
}
