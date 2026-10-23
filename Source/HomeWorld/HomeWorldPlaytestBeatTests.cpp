// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldPlaytestBeats.h"

/**
 * The fast-forward beat table (refactor item 3). The expected values are the ones
 * DebugFastForwardOpening hard-coded on main b5552ae6: the table must carry them,
 * not change them.
 */
namespace HomeWorldPlaytestBeatTestData
{
	using namespace HomeWorldPlaytestBeats;

	struct FExpect
	{
		int32 Id;
		const TCHAR* Word;
		int32 Skip;
		int32 ReadyAfter;
		float Standoff;
		ETarget Target;
		const TCHAR* Tag;
		const TCHAR* AltTag;
		const TCHAR* Name;
		EStand Stand;
	};

	const FExpect GExpect[] = {
		{ 1, TEXT("spirit"), 1, 0, 260.f, ETarget::Reveal, nullptr, nullptr, nullptr, EStand::Bounds },
		{ 2, TEXT("herbs"), 2, 0, 260.f, ETarget::Tagged, TEXT("NODE_GARDEN_EAST"), nullptr, nullptr, EStand::Bounds },
		{ 3, TEXT("backpack"), 3, 0, 260.f, ETarget::Tagged, TEXT("NPC_PARTNER"), nullptr, nullptr, EStand::Bounds },
		{ 4, TEXT("kettle"), 5, 0, 220.f, ETarget::Tagged, TEXT("KettleCounter"), TEXT("NODE_CONSUMABLE_STATION"), nullptr, EStand::Bounds },
		{ 5, TEXT("station"), 6, 0, 220.f, ETarget::Tagged, TEXT("NODE_CONSUMABLE_STATION"), nullptr, nullptr, EStand::Bounds },
		{ 6, TEXT("dog"), 7, 0, 650.f, ETarget::Dog, nullptr, nullptr, nullptr, EStand::Bounds },
		{ 7, TEXT("fish"), 8, 0, 260.f, ETarget::Named, nullptr, nullptr, TEXT("Water_Pond"), EStand::PondEdge },
		{ 8, TEXT("sleep"), 9, 0, 180.f, ETarget::Named, nullptr, nullptr, TEXT("SM_Size_Bed"), EStand::Bounds },
		{ 9, TEXT("night"), 0, 9, 180.f, ETarget::Named, nullptr, nullptr, TEXT("SM_Size_Bed"), EStand::None },
		{ 10, TEXT("collect"), 0, 9, 350.f, ETarget::CopseWisp, nullptr, nullptr, nullptr, EStand::Bounds },
		{ 11, TEXT("heal"), 0, 9, 470.f, ETarget::Named, nullptr, nullptr, TEXT("Water_HotSpring"), EStand::Bounds },
		{ 12, TEXT("glider"), 0, 10, 220.f, ETarget::Tagged, TEXT("NODE_ARMOR_TABLE"), TEXT("ArmorTable"), nullptr, EStand::Bounds },
		{ 13, TEXT("delivery"), 0, 11, 200.f, ETarget::Tagged, TEXT("NODE_OPENING_DELIVERY"), nullptr, nullptr, EStand::Bounds },
		{ 14, TEXT("daycamp"), 0, 12, 320.f, ETarget::Tagged, TEXT("NODE_OPENING_DAY_CAMP"), nullptr, nullptr, EStand::Bounds },
		{ 15, TEXT("dawnglide"), 0, 13, 180.f, ETarget::Tagged, TEXT("GlideStart"), nullptr, nullptr, EStand::Bounds },
		{ 16, TEXT("nightglide"), 0, 14, 180.f, ETarget::Tagged, TEXT("GlideStart"), nullptr, nullptr, EStand::Bounds },
		{ 17, TEXT("stealth"), 0, 15, 260.f, ETarget::Tagged, TEXT("NODE_GUARD"), nullptr, nullptr, EStand::Bounds },
		{ 18, TEXT("ease"), 0, 16, 180.f, ETarget::Tagged, TEXT("NODE_OPENING_EASE"), nullptr, nullptr, EStand::Bounds },
		{ 19, TEXT("shrine"), 0, 17, 180.f, ETarget::Tagged, TEXT("NODE_OPENING_SHRINE"), nullptr, nullptr, EStand::Bounds },
		{ 20, TEXT("stress"), 0, 0, 260.f, ETarget::None, nullptr, nullptr, nullptr, EStand::None },
	};

	FString Str(const TCHAR* Text)
	{
		return Text ? FString(Text) : FString();
	}

	/** The facts the runner's steps publish, step 1..9. Step 3 (partner walk) publishes none. */
	TArray<EHomeWorldOpeningFact> FactsThroughStep(int32 LastStep)
	{
		TArray<EHomeWorldOpeningFact> Out;
		if (LastStep >= 1) Out.Add(EHomeWorldOpeningFact::SpiritClaimed);
		if (LastStep >= 2) { Out.Add(EHomeWorldOpeningFact::HerbFromWest); Out.Add(EHomeWorldOpeningFact::HerbFromEast); }
		if (LastStep >= 4) Out.Add(EHomeWorldOpeningFact::Backpack);
		if (LastStep >= 5) Out.Add(EHomeWorldOpeningFact::KettleBrewed);
		if (LastStep >= 6) Out.Add(EHomeWorldOpeningFact::HasMixedHerb);
		if (LastStep >= 7) Out.Add(EHomeWorldOpeningFact::DogTamed);
		if (LastStep >= 8) Out.Add(EHomeWorldOpeningFact::FishCaught);
		if (LastStep >= 9) Out.Add(EHomeWorldOpeningFact::Slept);
		return Out;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPlaytestBeatTableRowsTest,
	"HomeWorld.Playtest.BeatTable.Rows",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPlaytestBeatTableRowsTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldPlaytestBeats;
	using namespace HomeWorldPlaytestBeatTestData;
	(void)Parameters;
	const TArray<FRow>& Table = Rows();
	if (!TestEqual(TEXT("beat rows"), Table.Num(), static_cast<int32>(UE_ARRAY_COUNT(GExpect))))
	{
		return false;
	}
	for (const FExpect& E : GExpect)
	{
		const FRow* Row = RowFor(E.Id);
		if (!TestNotNull(*FString::Printf(TEXT("row %d"), E.Id), Row))
		{
			continue;
		}
		const FString W = E.Word;
		TestEqual(*FString::Printf(TEXT("%s id"), *W), static_cast<int32>(Row->Beat), E.Id);
		TestEqual(*FString::Printf(TEXT("%s word"), *W), Str(Row->Word), W);
		TestEqual(*FString::Printf(TEXT("%s skip step"), *W), Row->SkipStep, E.Skip);
		TestEqual(*FString::Printf(TEXT("%s ready after step"), *W), Row->ReadyAfterStep, E.ReadyAfter);
		TestEqual(*FString::Printf(TEXT("%s standoff cm"), *W), Row->StandoffCm, E.Standoff);
		TestEqual(*FString::Printf(TEXT("%s target kind"), *W), static_cast<int32>(Row->Target), static_cast<int32>(E.Target));
		TestEqual(*FString::Printf(TEXT("%s tag"), *W), Str(Row->Tag), Str(E.Tag));
		TestEqual(*FString::Printf(TEXT("%s alt tag"), *W), Str(Row->AltTag), Str(E.AltTag));
		TestEqual(*FString::Printf(TEXT("%s name"), *W), Str(Row->Name), Str(E.Name));
		TestEqual(*FString::Printf(TEXT("%s stand"), *W), static_cast<int32>(Row->Stand), static_cast<int32>(E.Stand));
		TestTrue(*FString::Printf(TEXT("%s gaze from bounds"), *W), Row->bGazeFromBounds == (E.Stand == EStand::Bounds));
		TestTrue(*FString::Printf(TEXT("%s night props"), *W), Row->bNightProps == (E.Id == 10 || E.Id == 11));
		TestTrue(*FString::Printf(TEXT("%s carry wisps"), *W), Row->bCarryWisps == (E.Id == 11));
		TestFalse(*FString::Printf(TEXT("%s note set"), *W), E.Id != 20 && Str(Row->Note).IsEmpty());
		// Stress has no runner. Every other beat needs the verbs of the runner steps before its stop.
		const int32 LastRun = E.Id == 20 ? 0 : (E.Skip > 0 ? E.Skip - 1 : 9);
		const TArray<EHomeWorldOpeningFact> Want = FactsThroughStep(LastRun);
		TestEqual(*FString::Printf(TEXT("%s requires count"), *W), Row->Requires.Num(), Want.Num());
		for (int32 Index = 0; Index < Want.Num() && Index < Row->Requires.Num(); ++Index)
		{
			TestEqual(*FString::Printf(TEXT("%s requires %d"), *W, Index),
				static_cast<int32>(Row->Requires[Index]), static_cast<int32>(Want[Index]));
		}
	}
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPlaytestBeatTableWordsTest,
	"HomeWorld.Playtest.BeatTable.Words",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPlaytestBeatTableWordsTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldPlaytestBeats;
	using namespace HomeWorldPlaytestBeatTestData;
	(void)Parameters;
	for (const FExpect& E : GExpect)
	{
		TestEqual(*FString::Printf(TEXT("word '%s' round trip"), E.Word), FromText(E.Word), E.Id);
		TestEqual(*FString::Printf(TEXT("WordFor %d"), E.Id), Str(WordFor(E.Id)), Str(E.Word));
		TestEqual(*FString::Printf(TEXT("StandoffCm %d"), E.Id), StandoffCm(E.Id), E.Standoff);
		TestEqual(*FString::Printf(TEXT("SkipStep %d"), E.Id), SkipStep(E.Id), E.Skip);
		TestEqual(*FString::Printf(TEXT("ReadyAfterStep %d"), E.Id), ReadyAfterStep(E.Id), E.ReadyAfter);
	}
	// The matcher order main has always used: herb collection is herbs, night glide is not night.
	struct FAlias { const TCHAR* Text; int32 Id; };
	const FAlias Aliases[] = {
		{ TEXT(""), 9 },
		{ TEXT("herb collection"), 2 },
		{ TEXT("Garden"), 2 },
		{ TEXT("hot spring"), 11 },
		{ TEXT("partner"), 3 },
		{ TEXT("gift"), 3 },
		{ TEXT("tea"), 4 },
		{ TEXT("counter"), 5 },
		{ TEXT("mix"), 5 },
		{ TEXT("grace"), 6 },
		{ TEXT("pond"), 7 },
		{ TEXT("bed"), 8 },
		{ TEXT("wisp"), 10 },
		{ TEXT("night glide"), 16 },
		{ TEXT("night_glide"), 16 },
		{ TEXT("day camp"), 14 },
		{ TEXT("dawn glide"), 15 },
		{ TEXT("bogus"), 0 },
	};
	for (const FAlias& A : Aliases)
	{
		TestEqual(*FString::Printf(TEXT("FromText('%s')"), A.Text), FromText(A.Text), A.Id);
	}
	TestEqual(TEXT("WordFor unknown"), Str(WordFor(0)), FString(TEXT("night")));
	TestEqual(TEXT("StandoffCm unknown"), StandoffCm(0), 260.f);
	TestEqual(TEXT("ListText"), ListText(), FString(TEXT(
		"spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect, heal, glider, delivery, daycamp, dawnglide, nightglide, stealth, ease, shrine, stress")));
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
