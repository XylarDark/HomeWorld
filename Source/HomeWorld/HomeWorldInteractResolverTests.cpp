// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInteractResolver.h"
#include "HomeWorldPlacementConstants.h"
#include "HomeWorldTestWorld.h"

namespace
{
	bool RunVerb(FAutomationTestBase* Test, HomeWorldInteract::EVerb Verb)
	{
		const HomeWorldInteract::FSpec* Spec = HomeWorldInteract::SpecFor(Verb);
		if (!Test->TestNotNull(TEXT("spec"), Spec))
		{
			return false;
		}
		HomeWorldTestWorld::FScopedWorld Scope(HomeWorldInteract::VerbName(Verb));
		if (!Scope.Ok(Test))
		{
			return false;
		}
		AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
		if (!Test->TestNotNull(TEXT("character"), Character))
		{
			return false;
		}
		const bool bSizeTest = Spec->Chain != HomeWorldInteract::EChain::World;
		Character->SetInteractChainForTest(bSizeTest);
		HomeWorldInteract::ArmProbe(Verb);
		AActor* Prop = HomeWorldTestWorld::SpawnTagged(Scope.World, FVector(120.f, 0.f, 0.f), HomeWorldInteract::ProbeTag(Verb));
		if (!Test->TestNotNull(TEXT("tagged prop"), Prop))
		{
			HomeWorldInteract::ClearProbe();
			return false;
		}
		const bool bResolved = Character->ResolveOpeningTarget();
		const HomeWorldInteract::EVerb Got = HomeWorldInteract::ResolvedVerb();
		HomeWorldInteract::ClearProbe();
		const bool bVerb = Test->TestEqual(TEXT("resolved verb"), static_cast<int32>(Got), static_cast<int32>(Verb));
		const bool bHandled = Test->TestTrue(TEXT("resolver handled the tagged prop"), bResolved);
		return bVerb && bHandled;
	}
}

#define HW_VERB_TEST(Suffix, Verb) \
	IMPLEMENT_SIMPLE_AUTOMATION_TEST( \
		FResolve##Suffix, \
		"HomeWorld.Interact.Resolve." #Suffix, \
		EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter) \
	bool FResolve##Suffix::RunTest(const FString& Parameters) \
	{ \
		(void)Parameters; \
		return RunVerb(this, HomeWorldInteract::EVerb::Verb); \
	}

HW_VERB_TEST(PartyInvite, PartyInvite)
HW_VERB_TEST(OpeningSpirit, OpeningSpirit)
HW_VERB_TEST(PartnerLead, PartnerLead)
HW_VERB_TEST(CloudDescent, CloudDescent)
HW_VERB_TEST(ShrinePortal, ShrinePortal)
HW_VERB_TEST(Garden, Garden)
HW_VERB_TEST(Kettle, Kettle)
HW_VERB_TEST(OpeningStation, OpeningStation)
HW_VERB_TEST(OpeningDog, OpeningDog)
HW_VERB_TEST(OpeningFish, OpeningFish)
HW_VERB_TEST(OpeningNightSet, OpeningNightSet)
HW_VERB_TEST(OpeningHotSpring, OpeningHotSpring)
HW_VERB_TEST(OpeningDelivery, OpeningDelivery)
HW_VERB_TEST(OpeningBed, OpeningBed)
HW_VERB_TEST(OpeningZipline, OpeningZipline)
HW_VERB_TEST(OpeningShrine, OpeningShrine)
HW_VERB_TEST(Dung, Dung)
HW_VERB_TEST(Fertilizer, Fertilizer)
HW_VERB_TEST(Wound, Wound)
HW_VERB_TEST(Bull, Bull)
HW_VERB_TEST(Barn, Barn)
HW_VERB_TEST(EaseGuard, EaseGuard)
HW_VERB_TEST(FreeCaptive, FreeCaptive)
HW_VERB_TEST(Backpack, Backpack)
HW_VERB_TEST(FieldGather, FieldGather)
HW_VERB_TEST(DayCamp, DayCamp)
HW_VERB_TEST(PlantSlot, PlantSlot)
HW_VERB_TEST(Tame, Tame)
HW_VERB_TEST(HealSpirit, HealSpirit)
HW_VERB_TEST(Nurture, Nurture)
HW_VERB_TEST(Store, Store)
HW_VERB_TEST(Minigame, Minigame)
HW_VERB_TEST(BossSeal, BossSeal)
HW_VERB_TEST(Craft, Craft)
HW_VERB_TEST(Harvest, Harvest)

#undef HW_VERB_TEST

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FInteractChainOrderTest,
	"HomeWorld.Interact.ChainOrder",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FInteractChainOrderTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	const HomeWorldInteract::EVerb SizeTest[] = {
		HomeWorldInteract::EVerb::PartyInvite,
		HomeWorldInteract::EVerb::OpeningSpirit,
		HomeWorldInteract::EVerb::PartnerLead,
		HomeWorldInteract::EVerb::Garden,
		HomeWorldInteract::EVerb::Kettle,
		HomeWorldInteract::EVerb::OpeningStation,
		HomeWorldInteract::EVerb::OpeningDog,
		HomeWorldInteract::EVerb::OpeningFish,
		HomeWorldInteract::EVerb::OpeningNightSet,
		HomeWorldInteract::EVerb::OpeningHotSpring,
		HomeWorldInteract::EVerb::OpeningDelivery,
		HomeWorldInteract::EVerb::OpeningBed,
		HomeWorldInteract::EVerb::OpeningZipline,
		HomeWorldInteract::EVerb::OpeningShrine,
	};
	const HomeWorldInteract::EVerb World[] = {
		HomeWorldInteract::EVerb::PartyInvite,
		HomeWorldInteract::EVerb::OpeningSpirit,
		HomeWorldInteract::EVerb::PartnerLead,
		HomeWorldInteract::EVerb::CloudDescent,
		HomeWorldInteract::EVerb::ShrinePortal,
		HomeWorldInteract::EVerb::Garden,
		HomeWorldInteract::EVerb::Kettle,
		HomeWorldInteract::EVerb::Dung,
		HomeWorldInteract::EVerb::Fertilizer,
		HomeWorldInteract::EVerb::Wound,
		HomeWorldInteract::EVerb::Bull,
		HomeWorldInteract::EVerb::Barn,
		HomeWorldInteract::EVerb::EaseGuard,
		HomeWorldInteract::EVerb::FreeCaptive,
		HomeWorldInteract::EVerb::Backpack,
		HomeWorldInteract::EVerb::FieldGather,
		HomeWorldInteract::EVerb::DayCamp,
		HomeWorldInteract::EVerb::PlantSlot,
		HomeWorldInteract::EVerb::Tame,
		HomeWorldInteract::EVerb::HealSpirit,
		HomeWorldInteract::EVerb::Nurture,
		HomeWorldInteract::EVerb::Store,
		HomeWorldInteract::EVerb::Minigame,
		HomeWorldInteract::EVerb::BossSeal,
		HomeWorldInteract::EVerb::Craft,
		HomeWorldInteract::EVerb::Harvest,
	};

	TArray<HomeWorldInteract::EVerb> Got;
	HomeWorldInteract::GetChainOrder(true, Got);
	if (!TestEqual(TEXT("size-test chain length"), Got.Num(), static_cast<int32>(UE_ARRAY_COUNT(SizeTest))))
	{
		return false;
	}
	for (int32 Index = 0; Index < Got.Num(); ++Index)
	{
		TestEqual(HomeWorldInteract::VerbName(SizeTest[Index]), static_cast<int32>(Got[Index]), static_cast<int32>(SizeTest[Index]));
		const HomeWorldInteract::FSpec* Spec = HomeWorldInteract::SpecFor(Got[Index]);
		TestNotNull(TEXT("size-test spec"), Spec);
		if (Index > 0 && Spec)
		{
			const HomeWorldInteract::FSpec* Previous = HomeWorldInteract::SpecFor(Got[Index - 1]);
			TestTrue(TEXT("size-test priority rises"), Previous && Spec->Priority > Previous->Priority);
		}
	}

	HomeWorldInteract::GetChainOrder(false, Got);
	if (!TestEqual(TEXT("world chain length"), Got.Num(), static_cast<int32>(UE_ARRAY_COUNT(World))))
	{
		return false;
	}
	for (int32 Index = 0; Index < Got.Num(); ++Index)
	{
		TestEqual(HomeWorldInteract::VerbName(World[Index]), static_cast<int32>(Got[Index]), static_cast<int32>(World[Index]));
	}
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPlacementConstantsTest,
	"HomeWorld.Interact.PlacementConstants",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPlacementConstantsTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	const HomeWorldPlacement::FConstants& Constants = HomeWorldPlacement::Get();
	TestTrue(TEXT("placement file loaded"), Constants.bLoaded);
	TestTrue(TEXT("counter height"), Constants.CounterHeightCm == 100.f);
	TestTrue(TEXT("pond standoff"), Constants.PondStandoffCm == 100.f);
	TestTrue(TEXT("partner standoff"), Constants.PartnerStandoffCm == 180.f);
	TestEqual(TEXT("kettle tag"), Constants.TagKettle, FString(TEXT("NODE_KETTLE")));
	const HomeWorldInteract::FSpec* Fish = HomeWorldInteract::SpecFor(HomeWorldInteract::EVerb::OpeningFish);
	const HomeWorldInteract::FSpec* Spring = HomeWorldInteract::SpecFor(HomeWorldInteract::EVerb::OpeningHotSpring);
	TestTrue(TEXT("fish margin"), Fish && Fish->ReachCm == 200.f && Fish->bWall && !Fish->bLook);
	TestTrue(TEXT("spring reach"), Spring && Spring->ReachCm == 600.f && Spring->bWall && !Spring->bLook);
	return true;
}

#endif
