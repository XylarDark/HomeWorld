// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"

/**
 * Behaviour tests for the six-resource inventory (Docs/03_SYSTEMS_MVP A2-A3).
 *
 * WHY BEHAVIOUR TESTS AND NOT UNIT TESTS ON THE CLASSES
 *
 * Per "Week 1 - Agentic Engineering": unit-level TDD is impractical for most cases
 * when the unit is a class, and BDD is the fit for LLM-assisted engineering. So this
 * asserts the outcomes a designer would check by hand after an agent change - can I
 * gather, does the stack cap hold, does a save round trip - rather than testing
 * FindSlotIndexIndex or EnsureSlotArray in isolation.
 *
 * The first behaviour test in Source/. Before this file, the only automated fact
 * about HomeWorld was that it compiles, and every gate in the repo measured harness
 * tooling rather than the game.
 *
 * The invariants below are CANON, not implementation detail. Exactly six slots and a
 * stack cap of 9 come from Docs/03_SYSTEMS_MVP; a test that lets either drift is
 * letting the design drift silently, which is precisely the failure mode a single
 * developer cannot catch by eye across many agent changes.
 */

namespace HomeWorldInventoryTest
{
	/** A subsystem instance for a test, with its own GameInstance so slots start empty. */
	static UHomeWorldInventorySubsystem* MakeInventory()
	{
		if (!GEngine)
		{
			return nullptr;
		}
		UGameInstance* GameInstance = NewObject<UGameInstance>(GEngine);
		if (!GameInstance)
		{
			return nullptr;
		}
		GameInstance->Init();
		return GameInstance->GetSubsystem<UHomeWorldInventorySubsystem>();
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSixResourceSchemaTest,
	"HomeWorld.Systems.Inventory.SixResourceSchema",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSixResourceSchemaTest::RunTest(const FString& Parameters)
{
	using namespace HomeWorldInventory;

	// CANON: exactly six slots. Not a tuning value - it is the slot schema.
	TestEqual(TEXT("six canonical resource ids"), GetAllResourceIds().Num(), SlotCount);
	TestEqual(TEXT("slot count constant is six"), SlotCount, 6);

	// Every canonical id validates, and nothing else does. An unvalidated id reaching
	// a slot is how a second, parallel inventory grows without anyone deciding to
	// build one - the header explicitly calls that out.
	for (const FName& Id : GetAllResourceIds())
	{
		TestTrue(FString::Printf(TEXT("%s is valid"), *Id.ToString()), IsValidResourceId(Id));
	}
	TestFalse(TEXT("NAME_None is not a resource"), IsValidResourceId(NAME_None));
	TestFalse(TEXT("RES_BACON is not a resource"), IsValidResourceId(FName(TEXT("RES_BACON"))));

	// The evolve stub: legacy pile/tutorial names map onto the six rather than opening
	// a parallel set. Unmapped input must NOT be silently accepted as itself.
	TestEqual(TEXT("legacy WOOD normalizes"), NormalizeResourceId(FName(TEXT("WOOD"))), RES_WOOD);
	TestEqual(TEXT("canonical id is unchanged"), NormalizeResourceId(RES_FIBER), RES_FIBER);
	TestFalse(TEXT("unknown name does not become a valid id"),
		IsValidResourceId(NormalizeResourceId(FName(TEXT("MysteryRock")))));

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FGatherAndStackCapTest,
	"HomeWorld.Systems.Inventory.GatherAndStackCap",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FGatherAndStackCapTest::RunTest(const FString& Parameters)
{
	UHomeWorldInventorySubsystem* Inventory = HomeWorldInventoryTest::MakeInventory();
	if (!TestNotNull(TEXT("inventory subsystem"), Inventory))
	{
		AddError(TEXT("could not create a GameInstance - the test is not measuring the inventory"));
		return false;
	}

	// Gather: +1 to a resource is accepted and reads back.
	TestTrue(TEXT("first gather accepted"), Inventory->TryAddResource(HomeWorldInventory::RES_WOOD, 1));
	TestEqual(TEXT("wood after gather"), Inventory->GetResource(HomeWorldInventory::RES_WOOD), 1);

	// CANON: stack cap is 9. The tenth must be refused, not silently stacked, and the
	// refusal must not destroy what is already carried.
	for (int32 i = 0; i < HomeWorldInventory::StackMax; ++i)
	{
		Inventory->TryAddResource(HomeWorldInventory::RES_WOOD, 1);
	}
	TestEqual(TEXT("stack holds at the cap"), Inventory->GetResource(HomeWorldInventory::RES_WOOD), HomeWorldInventory::StackMax);
	TestFalse(TEXT("gathering past the cap is refused"),
		Inventory->TryAddResource(HomeWorldInventory::RES_WOOD, 1));
	TestEqual(TEXT("a refused gather leaves the stack intact"),
		Inventory->GetResource(HomeWorldInventory::RES_WOOD), HomeWorldInventory::StackMax);

	// Slots are per-resource, so a second resource does not disturb the first.
	Inventory->TryAddResource(HomeWorldInventory::RES_BERRY, 3);
	TestEqual(TEXT("berry stack is independent"), Inventory->GetResource(HomeWorldInventory::RES_BERRY), 3);
	TestEqual(TEXT("wood unaffected by berry gather"),
		Inventory->GetResource(HomeWorldInventory::RES_WOOD), HomeWorldInventory::StackMax);
	TestEqual(TEXT("total counts both"), Inventory->GetTotalPhysicalGoods(),
		HomeWorldInventory::StackMax + 3);

	// Spend: legitimate spend succeeds, over-spend is refused without side effects.
	TestTrue(TEXT("spend within the stack"), Inventory->SpendResource(HomeWorldInventory::RES_WOOD, 4));
	TestEqual(TEXT("wood after spend"), Inventory->GetResource(HomeWorldInventory::RES_WOOD),
		HomeWorldInventory::StackMax - 4);
	TestFalse(TEXT("cannot spend more than carried"),
		Inventory->SpendResource(HomeWorldInventory::RES_WOOD, HomeWorldInventory::StackMax + 1));
	TestEqual(TEXT("a refused spend changes nothing"),
		Inventory->GetResource(HomeWorldInventory::RES_WOOD), HomeWorldInventory::StackMax - 4);

	// Tame and heal are the two documented spend paths, and they pick different
	// resources. HasTameFood is documented as berry OR herb, so spending one berry of
	// three must NOT exhaust tame food - the first version of this assertion claimed
	// otherwise and was wrong about the code, not the code wrong about the spec.
	TestTrue(TEXT("tame food available from berry"), Inventory->HasTameFood());
	TestEqual(TEXT("tame food prefers berry"),
		Inventory->SpendTameFood(), HomeWorldInventory::RES_BERRY);
	TestEqual(TEXT("one berry spent"), Inventory->GetResource(HomeWorldInventory::RES_BERRY), 2);
	TestTrue(TEXT("tame food still available from remaining berry"), Inventory->HasTameFood());

	// Drain the berries, then confirm tame food is genuinely gone once neither berry
	// nor herb remains - that is the state the tame mechanic actually gates on.
	Inventory->SpendTameFood();
	Inventory->SpendTameFood();
	TestFalse(TEXT("tame food gone once berries are drained"), Inventory->HasTameFood());

	// Heal draws on herb or seed and prefers herb, so it is a separate stack.
	TestTrue(TEXT("heal resource available from seed"),
		Inventory->TryAddResource(HomeWorldInventory::RES_SEED, 1) && Inventory->HasHealResource());
	TestEqual(TEXT("heal spends the seed"), Inventory->SpendHealResource(), HomeWorldInventory::RES_SEED);
	TestFalse(TEXT("heal resource spent"), Inventory->HasHealResource());

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FSaveLoadRoundTripTest,
	"HomeWorld.Systems.Inventory.SaveLoadRoundTrip",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FSaveLoadRoundTripTest::RunTest(const FString& Parameters)
{
	UHomeWorldInventorySubsystem* Inventory = HomeWorldInventoryTest::MakeInventory();
	if (!TestNotNull(TEXT("inventory subsystem"), Inventory))
	{
		AddError(TEXT("could not create a GameInstance - the test is not measuring save/load"));
		return false;
	}

	// Put a known, uneven state in: an empty slot, a partial stack, and a full one.
	// Even state would pass a round trip that quietly zeroed everything, which is the
	// bug this test exists to catch.
	Inventory->TryAddResource(HomeWorldInventory::RES_STONE, 4);
	Inventory->TryAddResource(HomeWorldInventory::RES_HERB, HomeWorldInventory::StackMax);

	TArray<FHomeWorldInventorySlot> Saved;
	Inventory->CopySlotsTo(Saved);
	TestEqual(TEXT("saved slot count matches the schema"), Saved.Num(), HomeWorldInventory::SlotCount);
	TestEqual(TEXT("total survives the save"), Inventory->GetTotalPhysicalGoods(),
		4 + HomeWorldInventory::StackMax);

	// A save made by CopySlotsTo is ALWAYS SlotCount long, even when the player carries
	// nothing. So "the player saved an empty inventory" arrives as six empty slots and
	// MUST clear - that is the case the first version of this test got wrong by
	// passing a zero-length array instead.
	TArray<FHomeWorldInventorySlot> EmptySave;
	EmptySave.SetNum(HomeWorldInventory::SlotCount);
	Inventory->RestoreSlotsFrom(EmptySave);
	TestEqual(TEXT("a six-slot empty save clears the inventory"),
		Inventory->GetTotalPhysicalGoods(), 0);

	// A zero-length array is not "an empty save", it is "no save data". RestoreSlotsFrom
	// guards on length precisely so a missing or truncated save cannot silently wipe
	// what the player is carrying, and this pins that guard rather than assuming it.
	Inventory->RestoreSlotsFrom(Saved);
	Inventory->RestoreSlotsFrom(TArray<FHomeWorldInventorySlot>());
	TestEqual(TEXT("a zero-length restore is ignored, not treated as a clear"),
		Inventory->GetTotalPhysicalGoods(), 4 + HomeWorldInventory::StackMax);

	// And the real round trip: a save taken from the subsystem survives a wipe.
	Inventory->RestoreSlotsFrom(EmptySave);
	TestEqual(TEXT("wipe applied"), Inventory->GetTotalPhysicalGoods(), 0);
	Inventory->RestoreSlotsFrom(Saved);
	TestEqual(TEXT("stone round trips"), Inventory->GetResource(HomeWorldInventory::RES_STONE), 4);
	TestEqual(TEXT("herb round trips at the cap"), Inventory->GetResource(HomeWorldInventory::RES_HERB),
		HomeWorldInventory::StackMax);
	TestEqual(TEXT("total round trips"), Inventory->GetTotalPhysicalGoods(),
		4 + HomeWorldInventory::StackMax);
	TestEqual(TEXT("an untouched resource is still empty"),
		Inventory->GetResource(HomeWorldInventory::RES_SEED), 0);

	// Reading an out-of-range slot must not crash an agent-driven reload path.
	TestTrue(TEXT("out-of-range slot read is empty"), Inventory->GetSlot(99).IsEmpty());
	TestEqual(TEXT("slot count reports the schema"), Inventory->GetSlotCount(), HomeWorldInventory::SlotCount);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS