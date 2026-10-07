// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldBeastEncounterComponent.h"
#include "UObject/StrongObjectPtr.h"

namespace
{
	FHomeWorldBeastEncounterFrame BeastFrame(float Dt, float Speed, float Dist, bool bOffer = false, bool bTamed = false)
	{
		FHomeWorldBeastEncounterFrame Frame;
		Frame.DeltaSeconds = Dt;
		Frame.PlayerSpeedCm = Speed;
		Frame.DistanceCm = Dist;
		Frame.bCarriesOfferFood = bOffer;
		Frame.bBeastTamed = bTamed;
		return Frame;
	}
}

// Lead 2026-10-07 bull rules (Docs/context/HOMEWORLD_ROUTE.md):
// sudden movement builds threat, standing still bleeds it off.

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeastEncounterMovementFillsThreatTest,
	"HomeWorld.T0.BeastEncounter.MovementFillsThreatStillDecays",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeastEncounterMovementFillsThreatTest::RunTest(const FString& Parameters)
{
	TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
		NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
	if (!TestNotNull(TEXT("encounter component"), Encounter.Get()))
	{
		return false;
	}

	TestEqual(TEXT("running inside the area raises threat"),
		Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
		EHomeWorldBeastEncounterOutcome::ThreatRising);
	TestEqual(TEXT("threat after 1 s of running"), Encounter->GetThreat(), 0.25f, 0.001f);

	TestEqual(TEXT("second running frame keeps rising"),
		Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
		EHomeWorldBeastEncounterOutcome::ThreatRising);
	TestEqual(TEXT("threat after 2 s of running"), Encounter->GetThreat(), 0.5f, 0.001f);

	// Standing still is the calm state: the meter bleeds off, it does not fill.
	TestEqual(TEXT("standing still decays threat"),
		Encounter->AdvanceThreat(BeastFrame(1.f, 0.f, 600.f)),
		EHomeWorldBeastEncounterOutcome::ThreatDecaying);
	TestEqual(TEXT("threat after 1 s still"), Encounter->GetThreat(), 0.0f, 0.001f);

	TestEqual(TEXT("calm and still reports Idle"),
		Encounter->AdvanceThreat(BeastFrame(1.f, 0.f, 600.f)),
		EHomeWorldBeastEncounterOutcome::Idle);
	return true;
}

// Charge-and-boot is the fail state; an offering suppresses it (route: "walking
// toward it carrying an herb suppresses the boot"; berry counts too -- V4 offer).

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeastEncounterChargeAndBootTest,
	"HomeWorld.T0.BeastEncounter.ChargeAndBootWithHerbSuppression",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeastEncounterChargeAndBootTest::RunTest(const FString& Parameters)
{
	// Meter fills to full in 4 s of running (ThreatFillPerSecond 0.25) -> boot.
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		TestEqual(TEXT("frame 1"), Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
			EHomeWorldBeastEncounterOutcome::ThreatRising);
		TestEqual(TEXT("frame 2"), Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
			EHomeWorldBeastEncounterOutcome::ThreatRising);
		TestEqual(TEXT("frame 3"), Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
			EHomeWorldBeastEncounterOutcome::ThreatRising);
		TestEqual(TEXT("full meter boots"), Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
			EHomeWorldBeastEncounterOutcome::BootCharged);
		// Meter resets on delivery: spacing instead of a session latch, so the
		// next frame cannot re-fire the boot.
		TestEqual(TEXT("frame after boot must refill, not refire"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f)),
			EHomeWorldBeastEncounterOutcome::ThreatRising);
		TestEqual(TEXT("threat reset after boot"), Encounter->GetThreat(), 0.25f, 0.001f);
	}

	// Same run, offering held: the meter still fills but the boot cannot fire.
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		for (int32 FrameIdx = 0; FrameIdx < 3; ++FrameIdx)
		{
			Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f, /*bOffer=*/true));
		}
		TestEqual(TEXT("full meter with offering is suppressed, not a boot"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f, /*bOffer=*/true)),
			EHomeWorldBeastEncounterOutcome::OfferSuppressedBoot);
		TestEqual(TEXT("suppressed meter holds at full"), Encounter->GetThreat(), 1.f, 0.001f);
		// Drop the offering while the meter is full: the next moving frame boots.
		TestEqual(TEXT("dropping the offering at full meter boots"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 600.f, /*bOffer=*/false)),
			EHomeWorldBeastEncounterOutcome::BootCharged);
	}

	// "If you get too close": instant charge, even while standing still.
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		TestEqual(TEXT("too close without offering boots immediately"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 0.f, 300.f)),
			EHomeWorldBeastEncounterOutcome::BootCharged);
	}
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		// Too close WITH an offering and standing still = the tame window:
		// it approaches and eats rather than charging.
		TestEqual(TEXT("too close with offering while still is the tame window"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 0.f, 300.f, /*bOffer=*/true)),
			EHomeWorldBeastEncounterOutcome::TameWindow);
		TestEqual(TEXT("standing still with offering decays threat"),
			Encounter->GetThreat(), 0.f, 0.001f);
	}
	return true;
}

// Tamed beasts never charge; outside the area nothing ever fills.

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeastEncounterTamedAndRangeTest,
	"HomeWorld.T0.BeastEncounter.TamedAndRangeGates",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeastEncounterTamedAndRangeTest::RunTest(const FString& Parameters)
{
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		TestEqual(TEXT("tamed beast at point-blank never boots"),
			Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 300.f, /*bOffer=*/false, /*bTamed=*/true)),
			EHomeWorldBeastEncounterOutcome::Idle);
		TestEqual(TEXT("tamed clears threat"), Encounter->GetThreat(), 0.f, 0.001f);
	}
	{
		TStrongObjectPtr<UHomeWorldBeastEncounterComponent> Encounter(
			NewObject<UHomeWorldBeastEncounterComponent>(GetTransientPackage()));
		for (int32 FrameIdx = 0; FrameIdx < 3; ++FrameIdx)
		{
			TestEqual(TEXT("outside the area running never fills"),
				Encounter->AdvanceThreat(BeastFrame(1.f, 500.f, 5000.f)),
				EHomeWorldBeastEncounterOutcome::Idle);
		}
		TestEqual(TEXT("threat stays zero outside the area"), Encounter->GetThreat(), 0.f, 0.001f);
	}
	return true;
}

// Real-animal handling (route, Lead 2026-10-07): turn authority inversely
// related to travel speed -- near-zero at 3x sprint, full at walk/stop.

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FBeastEncounterTurnAuthorityTest,
	"HomeWorld.T0.BeastEncounter.TurnAuthorityInvertsWithSpeed",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FBeastEncounterTurnAuthorityTest::RunTest(const FString& Parameters)
{
	const float BullMaxSpeedCm = 1755.f; // 3x player sprint (SprintWalkSpeed 585), route.

	TestEqual(TEXT("full authority at a standstill"),
		UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(0.f, BullMaxSpeedCm), 1.f, 0.001f);
	TestEqual(TEXT("half authority at half speed"),
		UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(877.5f, BullMaxSpeedCm), 0.5f, 0.001f);
	TestEqual(TEXT("zero authority at max speed"),
		UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(BullMaxSpeedCm, BullMaxSpeedCm), 0.f, 0.001f);
	TestEqual(TEXT("clamped beyond max speed"),
		UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(3000.f, BullMaxSpeedCm), 0.f, 0.001f);
	TestEqual(TEXT("no travel possible means full authority"),
		UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(500.f, 0.f), 1.f, 0.001f);
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
