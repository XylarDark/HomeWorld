// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldZoneGenerator.h"
#include "Misc/Paths.h"

namespace
{
	bool ZonesMatch(const FHomeWorldGeneratedZone& A, const FHomeWorldGeneratedZone& B)
	{
		if (A.Seed != B.Seed || A.PineInstanceCount != B.PineInstanceCount
			|| A.HerbPointsM.Num() != B.HerbPointsM.Num()
			|| A.EdgeDrifts.Num() != B.EdgeDrifts.Num()
			|| A.PlacedSlots.Num() != B.PlacedSlots.Num()
			|| A.PlacedParts.Num() != B.PlacedParts.Num()
			|| !FMath::IsNearlyEqual(A.WidthM, B.WidthM)
			|| !FMath::IsNearlyEqual(A.DepthM, B.DepthM)
			|| !FMath::IsNearlyEqual(A.EntryBandWidthM, B.EntryBandWidthM))
		{
			return false;
		}
		for (int32 Index = 0; Index < A.HerbPointsM.Num(); ++Index)
		{
			if (!A.HerbPointsM[Index].Equals(B.HerbPointsM[Index]))
			{
				return false;
			}
		}
		for (int32 Index = 0; Index < A.EdgeDrifts.Num(); ++Index)
		{
			if (A.EdgeDrifts[Index].Id != B.EdgeDrifts[Index].Id
				|| !FMath::IsNearlyEqual(A.EdgeDrifts[Index].DriftM, B.EdgeDrifts[Index].DriftM))
			{
				return false;
			}
		}
		return true;
	}

	bool HerbsRespectSpacing(const TArray<FVector2D>& Points, float Spacing)
	{
		for (int32 I = 0; I < Points.Num(); ++I)
		{
			for (int32 J = I + 1; J < Points.Num(); ++J)
			{
				if (FVector2D::Distance(Points[I], Points[J]) < Spacing - 0.01f)
				{
					return false;
				}
			}
		}
		return true;
	}

	const FHomeWorldZoneSlotSpec* FindSlot(const TArray<FHomeWorldZoneSlotSpec>& Slots, const TCHAR* Id)
	{
		for (const FHomeWorldZoneSlotSpec& Slot : Slots)
		{
			if (Slot.Id == Id)
			{
				return &Slot;
			}
		}
		return nullptr;
	}

	const FHomeWorldZonePartSpec* FindPart(const TArray<FHomeWorldZonePartSpec>& Parts, const TCHAR* Id)
	{
		for (const FHomeWorldZonePartSpec& Part : Parts)
		{
			if (Part.Id == Id)
			{
				return &Part;
			}
		}
		return nullptr;
	}

	const FHomeWorldZoneEdgeDrift* FindDrift(const FHomeWorldGeneratedZone& Zone, const TCHAR* Id)
	{
		for (const FHomeWorldZoneEdgeDrift& Drift : Zone.EdgeDrifts)
		{
			if (Drift.Id == Id)
			{
				return &Drift;
			}
		}
		return nullptr;
	}

	FString ZoneSpecPath(const TCHAR* Relative)
	{
		return FPaths::ConvertRelativePathToFull(FPaths::ProjectDir() / Relative);
	}

	FHomeWorldZoneSpec MeadowSpec()
	{
		FHomeWorldZoneSpec Spec;
		Spec.Id = TEXT("FIELD");
		Spec.WidthM = 420.f;
		Spec.DepthM = 420.f;
		Spec.ExtentJitterFraction = 0.15f;
		Spec.EdgeBandDriftM = 25.f;
		Spec.HerbMinSpacingM = 30.f;
		Spec.PineInstanceCap = 0;
		Spec.Edges = {
			{TEXT("EDGE_CLIFF"), TEXT("cliff"), TEXT("north")},
			{TEXT("EDGE_RIVER"), TEXT("river"), TEXT("east")},
			{TEXT("EDGE_FOREST_A"), TEXT("pine_forest"), TEXT("south")},
			{TEXT("EDGE_FOREST_B"), TEXT("pine_forest"), TEXT("west")},
		};
		return Spec;
	}

	FHomeWorldZoneSpec ForestTemplate()
	{
		FHomeWorldZoneSpec Spec;
		Spec.Id = TEXT("FOREST");
		Spec.WidthM = 420.f;
		Spec.DepthM = 300.f;
		Spec.EntryBandWidthM = 60.f;
		Spec.HerbMinSpacingM = 30.f;
		Spec.PineInstanceCap = 3500;
		FHomeWorldZoneSlotSpec Camp;
		Camp.Id = TEXT("SLOT_CAMP");
		Camp.Piece = TEXT("CAMP assembly");
		Camp.bHasOffset = true;
		Camp.OffsetM = FVector(20.f, 30.f, 0.f);
		Spec.Slots.Add(Camp);
		return Spec;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorSameSeedMatchesTest,
	"HomeWorld.T0.ZoneGenerator.SameSeedMatches",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorSameSeedMatchesTest::RunTest(const FString& Parameters)
{
	const FHomeWorldZoneSpec Spec = MeadowSpec();
	const FHomeWorldGeneratedZone First = FHomeWorldZoneGenerator::Generate(Spec, 18421);
	const FHomeWorldGeneratedZone Second = FHomeWorldZoneGenerator::Generate(Spec, 18421);
	TestTrue(TEXT("same seed regenerates the same skeleton"), ZonesMatch(First, Second));
	TestFalse(TEXT("a different seed changes the skeleton"),
		ZonesMatch(First, FHomeWorldZoneGenerator::Generate(Spec, 18422)));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorJitterStaysInsideSpecTest,
	"HomeWorld.T0.ZoneGenerator.JitterStaysInsideSpec",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorJitterStaysInsideSpecTest::RunTest(const FString& Parameters)
{
	const FHomeWorldZoneSpec Spec = MeadowSpec();
	bool bCliffDiverged = false;
	for (int32 Seed = 1; Seed <= 32; ++Seed)
	{
		const FHomeWorldGeneratedZone Zone = FHomeWorldZoneGenerator::Generate(Spec, Seed);
		TestTrue(TEXT("width stays inside ±15%"),
			Zone.WidthM >= Spec.WidthM * 0.85f - 0.01f && Zone.WidthM <= Spec.WidthM * 1.15f + 0.01f);
		TestTrue(TEXT("depth stays inside ±15%"),
			Zone.DepthM >= Spec.DepthM * 0.85f - 0.01f && Zone.DepthM <= Spec.DepthM * 1.15f + 0.01f);
		const FHomeWorldZoneEdgeDrift* ForestA = FindDrift(Zone, TEXT("EDGE_FOREST_A"));
		const FHomeWorldZoneEdgeDrift* ForestB = FindDrift(Zone, TEXT("EDGE_FOREST_B"));
		const FHomeWorldZoneEdgeDrift* Cliff = FindDrift(Zone, TEXT("EDGE_CLIFF"));
		if (!TestNotNull(TEXT("forest A drift"), ForestA) || !TestNotNull(TEXT("forest B drift"), ForestB)
			|| !TestNotNull(TEXT("cliff drift"), Cliff))
		{
			return false;
		}
		TestTrue(TEXT("both pine edges share one drift"), FMath::IsNearlyEqual(ForestA->DriftM, ForestB->DriftM));
		TestTrue(TEXT("forest drift stays inside ±25 m"), FMath::Abs(ForestA->DriftM) <= Spec.EdgeBandDriftM + 0.01f);
		TestTrue(TEXT("cliff drift stays inside ±25 m"), FMath::Abs(Cliff->DriftM) <= Spec.EdgeBandDriftM + 0.01f);
		if (!FMath::IsNearlyEqual(Cliff->DriftM, ForestA->DriftM))
		{
			bCliffDiverged = true;
		}
	}
	TestTrue(TEXT("non-forest edges are not locked to the forest drift"), bCliffDiverged);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorHerbSpacingAndPineCapTest,
	"HomeWorld.T0.ZoneGenerator.HerbSpacingAndPineCap",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorHerbSpacingAndPineCapTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Spec = MeadowSpec();
	const FHomeWorldGeneratedZone Meadow = FHomeWorldZoneGenerator::Generate(Spec, 9);
	TestTrue(TEXT("meadow herbs respect 30 m spacing"), HerbsRespectSpacing(Meadow.HerbPointsM, Spec.HerbMinSpacingM));
	TestTrue(TEXT("meadow places herbs"), Meadow.HerbPointsM.Num() > 0);
	TestEqual(TEXT("meadow pine cap is zero"), Meadow.PineInstanceCount, 0);

	Spec.PineInstanceCap = 10;
	Spec.WidthM = 10000.f;
	Spec.DepthM = 10000.f;
	const FHomeWorldGeneratedZone Capped = FHomeWorldZoneGenerator::Generate(Spec, 9);
	TestEqual(TEXT("pine estimate clamps to the cap"), Capped.PineInstanceCount, 10);

	Spec.PineInstanceCap = 3500;
	Spec.WidthM = 420.f;
	Spec.DepthM = 300.f;
	const FHomeWorldGeneratedZone Forest = FHomeWorldZoneGenerator::Generate(Spec, 9);
	TestTrue(TEXT("forest pine count stays under the cap"), Forest.PineInstanceCount <= 3500);
	TestTrue(TEXT("forest pine count is a real estimate"), Forest.PineInstanceCount > 0);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorEntryBandIgnoresSeedTest,
	"HomeWorld.T0.ZoneGenerator.EntryBandIgnoresSeed",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorEntryBandIgnoresSeedTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Spec = MeadowSpec();
	Spec.EntryBandWidthM = 60.f;
	const int32 SeedA = FHomeWorldZoneGenerator::SeedForEdge(100, TEXT("EDGE_FOREST_A"));
	const int32 SeedB = FHomeWorldZoneGenerator::SeedForEdge(100, TEXT("EDGE_FOREST_B"));
	TestNotEqual(TEXT("the two forest edges hash to different seeds"), SeedA, SeedB);
	TestEqual(TEXT("the same edge hashes stable"),
		FHomeWorldZoneGenerator::SeedForEdge(100, TEXT("EDGE_FOREST_A")), SeedA);

	const FHomeWorldGeneratedZone FromA = FHomeWorldZoneGenerator::Generate(Spec, SeedA);
	const FHomeWorldGeneratedZone FromB = FHomeWorldZoneGenerator::Generate(Spec, SeedB);
	TestEqual(TEXT("entry band width is the template, not the seed"), FromA.EntryBandWidthM, 60.f, 0.001f);
	TestEqual(TEXT("the other edge keeps the same entry band"), FromB.EntryBandWidthM, 60.f, 0.001f);
	TestFalse(TEXT("interiors differ after the edge seed"), ZonesMatch(FromA, FromB));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorFieldHasZeroCampSlotsTest,
	"HomeWorld.T0.ZoneGenerator.FieldHasZeroCampSlots",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorFieldHasZeroCampSlotsTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Field;
	FString Error;
	if (!TestTrue(TEXT("FIELD.json loads"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/gather/FIELD.json")), Field, Error)))
	{
		AddError(Error);
		return false;
	}
	TestEqual(TEXT("FIELD id"), Field.Id, FString(TEXT("FIELD")));
	TestEqual(TEXT("FIELD template has no slots"), Field.Slots.Num(), 0);
	TestFalse(TEXT("FIELD template has no camp content"), FHomeWorldZoneGenerator::HasCampContent(Field));

	const FHomeWorldGeneratedZone Generated = FHomeWorldZoneGenerator::Generate(Field, 3);
	TestEqual(TEXT("generation does not invent camp slots"), Generated.PlacedSlots.Num(), 0);
	const FHomeWorldZoneEdgeDrift* ForestA = FindDrift(Generated, TEXT("EDGE_FOREST_A"));
	const FHomeWorldZoneEdgeDrift* ForestB = FindDrift(Generated, TEXT("EDGE_FOREST_B"));
	if (!TestNotNull(TEXT("loaded forest A"), ForestA) || !TestNotNull(TEXT("loaded forest B"), ForestB))
	{
		return false;
	}
	TestTrue(TEXT("loaded field keeps the two forest edges identical"),
		FMath::IsNearlyEqual(ForestA->DriftM, ForestB->DriftM));

	FHomeWorldZoneSpec Forest;
	if (!TestTrue(TEXT("FOREST.json loads"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/combat/FOREST.json")), Forest, Error)))
	{
		AddError(Error);
		return false;
	}
	TestTrue(TEXT("FOREST template carries the camp slot"), FHomeWorldZoneGenerator::HasCampContent(Forest));
	const FHomeWorldGeneratedZone ForestZone = FHomeWorldZoneGenerator::Generate(
		Forest, FHomeWorldZoneGenerator::SeedForEdge(3, TEXT("EDGE_FOREST_A")));
	bool bPlacedCamp = false;
	for (const FHomeWorldZoneSlotSpec& Slot : ForestZone.PlacedSlots)
	{
		if (Slot.Id.Contains(TEXT("CAMP")))
		{
			bPlacedCamp = true;
		}
	}
	TestTrue(TEXT("the forest instance keeps the camp slot"), bPlacedCamp);
	TestEqual(TEXT("forest entry band is the spec value"), ForestZone.EntryBandWidthM, 60.f, 0.001f);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorRejectsMissingSpecTest,
	"HomeWorld.T0.ZoneGenerator.RejectsMissingSpec",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorRejectsMissingSpecTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Spec;
	FString Error;
	TestFalse(TEXT("a missing spec file fails"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/gather/NO_SUCH_ZONE.json")), Spec, Error));
	TestFalse(TEXT("the error names the failure"), Error.IsEmpty());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorEdgeCrossCommitsOneForestTest,
	"HomeWorld.T0.ZoneGenerator.EdgeCrossCommitsOneForest",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorEdgeCrossCommitsOneForestTest::RunTest(const FString& Parameters)
{
	const FHomeWorldZoneSpec Field = MeadowSpec();
	const FHomeWorldZoneSpec ForestSpec = ForestTemplate();
	FHomeWorldZoneCrossing Crossing;
	Crossing.Reset(100);

	TestTrue(TEXT("forest A starts dormant"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_A")));
	TestTrue(TEXT("forest B starts dormant"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_B")));
	TestFalse(TEXT("the cliff is not a dormant forest"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_CLIFF")));
	TestFalse(TEXT("nothing is instantiated yet"), Crossing.HasForest());

	TestTrue(TEXT("the cliff opens no neighbor"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_CLIFF")) == EHomeWorldEdgeCrossResult::NoNeighbor);
	TestTrue(TEXT("the river opens no neighbor in T0"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_RIVER")) == EHomeWorldEdgeCrossResult::NoNeighbor);
	TestTrue(TEXT("an unknown edge is refused"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_NOPE")) == EHomeWorldEdgeCrossResult::UnknownEdge);
	TestFalse(TEXT("dead edges do not create a forest"), Crossing.HasForest());

	TestTrue(TEXT("crossing forest A instantiates it"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_A")) == EHomeWorldEdgeCrossResult::Instantiated);
	const int32 SeedA = FHomeWorldZoneGenerator::SeedForEdge(100, TEXT("EDGE_FOREST_A"));
	TestEqual(TEXT("the instance seed is hash(field seed, edge)"), Crossing.GetForest().Seed, SeedA);
	TestEqual(TEXT("the active edge is A"), Crossing.GetActiveEdgeId(), FString(TEXT("EDGE_FOREST_A")));
	TestFalse(TEXT("A is no longer dormant"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_A")));
	TestTrue(TEXT("B stays dormant"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_B")));
	TestTrue(TEXT("the forest instance carries the camp"), FHomeWorldZoneGenerator::HasCampContent(
		[&Crossing]()
		{
			FHomeWorldZoneSpec Placed;
			Placed.Slots = Crossing.GetForest().PlacedSlots;
			return Placed;
		}()));
	TestFalse(TEXT("the field template still has no camp"), FHomeWorldZoneGenerator::HasCampContent(Field));

	const float Width = Crossing.GetForest().WidthM;
	const int32 Herbs = Crossing.GetForest().HerbPointsM.Num();
	TestTrue(TEXT("crossing A again reactivates the same instance"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_A")) == EHomeWorldEdgeCrossResult::Reactivated);
	TestEqual(TEXT("reactivation keeps the seed"), Crossing.GetForest().Seed, SeedA);
	TestEqual(TEXT("reactivation keeps the rolled width"), Crossing.GetForest().WidthM, Width, 0.001f);
	TestEqual(TEXT("reactivation keeps the herb scatter"), Crossing.GetForest().HerbPointsM.Num(), Herbs);

	TestTrue(TEXT("crossing B after the commitment leaves it dormant"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_B")) == EHomeWorldEdgeCrossResult::LeftDormant);
	TestEqual(TEXT("the active edge is still A"), Crossing.GetActiveEdgeId(), FString(TEXT("EDGE_FOREST_A")));
	TestEqual(TEXT("B did not replace the seed"), Crossing.GetForest().Seed, SeedA);
	TestTrue(TEXT("B is still dormant"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_B")));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorEdgeCrossOtherEdgeFirstTest,
	"HomeWorld.T0.ZoneGenerator.EdgeCrossOtherEdgeFirst",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorEdgeCrossOtherEdgeFirstTest::RunTest(const FString& Parameters)
{
	const FHomeWorldZoneSpec Field = MeadowSpec();
	const FHomeWorldZoneSpec ForestSpec = ForestTemplate();
	FHomeWorldZoneCrossing Crossing;
	Crossing.Reset(100);

	TestTrue(TEXT("crossing forest B first instantiates B"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_B")) == EHomeWorldEdgeCrossResult::Instantiated);
	TestEqual(TEXT("B uses its own edge seed"),
		Crossing.GetForest().Seed, FHomeWorldZoneGenerator::SeedForEdge(100, TEXT("EDGE_FOREST_B")));
	TestTrue(TEXT("A stays dormant when B was chosen"), Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_A")));
	TestTrue(TEXT("A cannot open a second forest"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_A")) == EHomeWorldEdgeCrossResult::LeftDormant);
	TestEqual(TEXT("the active edge is still B"), Crossing.GetActiveEdgeId(), FString(TEXT("EDGE_FOREST_B")));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorEdgeCrossLoadsFieldContractTest,
	"HomeWorld.T0.ZoneGenerator.EdgeCrossLoadsFieldContract",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorEdgeCrossLoadsFieldContractTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Field;
	FHomeWorldZoneSpec ForestSpec;
	FString Error;
	if (!TestTrue(TEXT("FIELD.json loads"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/gather/FIELD.json")), Field, Error)))
	{
		AddError(Error);
		return false;
	}
	if (!TestTrue(TEXT("FOREST.json loads"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/combat/FOREST.json")), ForestSpec, Error)))
	{
		AddError(Error);
		return false;
	}

	FHomeWorldZoneCrossing Crossing;
	Crossing.Reset(3);
	TestTrue(TEXT("the loaded field edge instantiates FOREST"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_A")) == EHomeWorldEdgeCrossResult::Instantiated);
	TestFalse(TEXT("the loaded field still has no camp"), FHomeWorldZoneGenerator::HasCampContent(Field));
	TestEqual(TEXT("entry band stays the forest template"), Crossing.GetForest().EntryBandWidthM, 60.f, 0.001f);
	TestTrue(TEXT("the other loaded forest edge stays dormant"),
		Crossing.IsForestEdgeDormant(Field, TEXT("EDGE_FOREST_B")));
	TestTrue(TEXT("the other loaded edge stays dormant after the commitment"),
		Crossing.Cross(Field, ForestSpec, TEXT("EDGE_FOREST_B")) == EHomeWorldEdgeCrossResult::LeftDormant);

	bool bPlacedCamp = false;
	for (const FHomeWorldZoneSlotSpec& Slot : Crossing.GetForest().PlacedSlots)
	{
		if (Slot.Id.Contains(TEXT("CAMP")))
		{
			bPlacedCamp = true;
		}
	}
	TestTrue(TEXT("camp stayed on the chosen forest"), bPlacedCamp);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorSlotPinsStayAuthoredTest,
	"HomeWorld.T0.ZoneGenerator.SlotPinsStayAuthored",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorSlotPinsStayAuthoredTest::RunTest(const FString& Parameters)
{
	FHomeWorldZoneSpec Forest;
	FString Error;
	if (!TestTrue(TEXT("FOREST.json loads"),
		FHomeWorldZoneGenerator::LoadSpec(ZoneSpecPath(TEXT("Lib/02_Zones/combat/FOREST.json")), Forest, Error)))
	{
		AddError(Error);
		return false;
	}
	TestEqual(TEXT("entry light is the authored 40 m band"), Forest.EntryLightDepthM, 40.f, 0.001f);

	const FHomeWorldGeneratedZone First = FHomeWorldZoneGenerator::Generate(Forest, 11);
	const FHomeWorldGeneratedZone Second = FHomeWorldZoneGenerator::Generate(Forest, 99);
	const FHomeWorldZoneSlotSpec* Shrine = FindSlot(First.PlacedSlots, TEXT("SLOT_SHRINE_RETURN"));
	const FHomeWorldZoneSlotSpec* Camp = FindSlot(First.PlacedSlots, TEXT("SLOT_CAMP"));
	const FHomeWorldZoneSlotSpec* Wound = FindSlot(First.PlacedSlots, TEXT("SLOT_SPIRIT_WOUND"));
	const FHomeWorldZoneSlotSpec* Future = FindSlot(First.PlacedSlots, TEXT("SLOT_FUTURE"));
	if (!TestNotNull(TEXT("shrine pin"), Shrine) || !TestNotNull(TEXT("camp pin"), Camp) || !TestNotNull(TEXT("wound pin"), Wound))
	{
		return false;
	}
	TestNull(TEXT("a slot with no offset is not pinned"), Future);
	TestTrue(TEXT("shrine stays at its authored offset"), Shrine->OffsetM.Equals(FVector(6.f, 25.f, 0.f)));
	TestTrue(TEXT("camp stays at its authored offset"), Camp->OffsetM.Equals(FVector(20.f, 30.f, 0.f)));
	TestTrue(TEXT("wound stays at its authored offset"), Wound->OffsetM.Equals(FVector(-10.f, 180.f, 0.f)));
	TestTrue(TEXT("the wound sits deeper than the entry light"), Wound->OffsetM.Y > Forest.EntryLightDepthM);

	const FHomeWorldZoneSlotSpec* ShrineAgain = FindSlot(Second.PlacedSlots, TEXT("SLOT_SHRINE_RETURN"));
	const FHomeWorldZoneSlotSpec* WoundAgain = FindSlot(Second.PlacedSlots, TEXT("SLOT_SPIRIT_WOUND"));
	if (!TestNotNull(TEXT("shrine on the other seed"), ShrineAgain) || !TestNotNull(TEXT("wound on the other seed"), WoundAgain))
	{
		return false;
	}
	TestTrue(TEXT("a new seed does not move the shrine"), ShrineAgain->OffsetM.Equals(Shrine->OffsetM));
	TestTrue(TEXT("a new seed does not move the wound"), WoundAgain->OffsetM.Equals(Wound->OffsetM));

	const FHomeWorldZonePartSpec* Bedroll = FindPart(First.PlacedParts, TEXT("SM_Camp_Bedroll_A"));
	const FHomeWorldZonePartSpec* Guard = FindPart(First.PlacedParts, TEXT("EJECT_TRIGGER_GUARD_WAKES"));
	const FHomeWorldZonePartSpec* Captive = FindPart(First.PlacedParts, TEXT("FREEDOM_GATED_ON_ALL_THREE_CALM"));
	const FHomeWorldZonePartSpec* Portal = FindPart(First.PlacedParts, TEXT("NODE_PORTAL_CAMP_ARRIVAL"));
	const FHomeWorldZonePartSpec* Fire = FindPart(First.PlacedParts, TEXT("SM_Camp_Fire"));
	if (!TestNotNull(TEXT("bedroll A"), Bedroll) || !TestNotNull(TEXT("guard post"), Guard)
		|| !TestNotNull(TEXT("captive"), Captive) || !TestNotNull(TEXT("portal"), Portal))
	{
		return false;
	}
	TestNull(TEXT("the fire has no authored offset, so it is not placed"), Fire);
	TestTrue(TEXT("bedroll A is the camp origin plus its own offset"),
		Bedroll->OffsetM.Equals(FVector(17.5f, 32.f, 0.f)));
	TestTrue(TEXT("the guard post is the camp origin plus its trigger offset"),
		Guard->OffsetM.Equals(FVector(23.f, 28.f, 1.8f)));
	TestTrue(TEXT("the captive is the camp origin plus its trigger offset"),
		Captive->OffsetM.Equals(FVector(20.f, 34.f, 0.f)));
	TestTrue(TEXT("the portal sits on the camp origin"),
		Portal->OffsetM.Equals(FVector(20.f, 30.f, 0.f)));

	FHomeWorldZoneSpec NoClearing = Forest;
	for (FHomeWorldZoneSlotSpec& Slot : NoClearing.Slots)
	{
		Slot.ClearingSizeM = FVector2D::ZeroVector;
	}
	const FHomeWorldGeneratedZone Punched = FHomeWorldZoneGenerator::Generate(NoClearing, 11);
	TestTrue(TEXT("the camp clearing cuts the pine budget"), First.PineInstanceCount < Punched.PineInstanceCount);
	TestTrue(TEXT("pines remain under the cap after the punch"), First.PineInstanceCount <= Forest.PineInstanceCap);
	TestTrue(TEXT("the punch does not zero the forest"), First.PineInstanceCount > 0);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FZoneGeneratorDiscoveryBoundaryPlacesCampTest,
	"HomeWorld.T0.ZoneGenerator.DiscoveryBoundaryPlacesCamp",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FZoneGeneratorDiscoveryBoundaryPlacesCampTest::RunTest(const FString& Parameters)
{
	const FHomeWorldZoneSpec Field = MeadowSpec();
	const FHomeWorldZoneSpec ForestSpec = ForestTemplate();
	FHomeWorldZoneCrossing Crossing;
	Crossing.Reset(100);

	TestTrue(TEXT("the meadow centre does not place the camp"),
		Crossing.DiscoverAt(Field, ForestSpec, FVector2D::ZeroVector) == EHomeWorldEdgeCrossResult::Outside);
	TestFalse(TEXT("no forest exists before discovery"), Crossing.HasForest());
	TestFalse(TEXT("no camp exists before discovery"), Crossing.HasCamp());
	TestTrue(TEXT("the field itself generated"), Crossing.GetField().HerbPointsM.Num() > 0);
	TestFalse(TEXT("the field template still has no camp"), FHomeWorldZoneGenerator::HasCampContent(Field));

	int32 ForestAAssets = 0;
	int32 ForestBAssets = 0;
	for (const FHomeWorldPlacedEdgeAsset& Asset : Crossing.GetEdgeAssets())
	{
		if (Asset.EdgeId == TEXT("EDGE_FOREST_A"))
		{
			++ForestAAssets;
		}
		else if (Asset.EdgeId == TEXT("EDGE_FOREST_B"))
		{
			++ForestBAssets;
		}
	}
	TestTrue(TEXT("both forest edges received assets"), ForestAAssets > 1 && ForestBAssets > 1);
	TestEqual(TEXT("the two forest edges place the same number of assets"), ForestAAssets, ForestBAssets);

	const FHomeWorldDiscoveryBoundary* ForestA = nullptr;
	const FHomeWorldDiscoveryBoundary* Cliff = nullptr;
	for (const FHomeWorldDiscoveryBoundary& Boundary : Crossing.GetBoundaries())
	{
		if (Boundary.EdgeId == TEXT("EDGE_FOREST_A"))
		{
			ForestA = &Boundary;
		}
		else if (Boundary.EdgeId == TEXT("EDGE_CLIFF"))
		{
			Cliff = &Boundary;
		}
	}
	if (!TestNotNull(TEXT("forest A boundary"), ForestA) || !TestNotNull(TEXT("cliff boundary"), Cliff))
	{
		return false;
	}
	TestEqual(TEXT("forest A boundary records the neighbor kind"), ForestA->NeighborKind, FString(TEXT("pine_forest")));
	TestTrue(TEXT("the cliff boundary does not place the camp"),
		Crossing.DiscoverAt(Field, ForestSpec, Cliff->Center()) == EHomeWorldEdgeCrossResult::NoNeighbor);
	TestFalse(TEXT("the cliff left the camp unplaced"), Crossing.HasCamp());

	TestTrue(TEXT("standing in the forest assets places the camp"),
		Crossing.DiscoverAt(Field, ForestSpec, ForestA->Center()) == EHomeWorldEdgeCrossResult::Instantiated);
	TestTrue(TEXT("discovery placed the camp"), Crossing.HasCamp());
	const FHomeWorldZoneSlotSpec* Camp = FindSlot(Crossing.GetForest().PlacedSlots, TEXT("SLOT_CAMP"));
	if (!TestNotNull(TEXT("camp pin after discovery"), Camp))
	{
		return false;
	}
	TestTrue(TEXT("the camp uses the authored forest offset"), Camp->OffsetM.Equals(FVector(20.f, 30.f, 0.f)));
	TestTrue(TEXT("the same boundary reactivates that camp"),
		Crossing.DiscoverAt(Field, ForestSpec, ForestA->Center()) == EHomeWorldEdgeCrossResult::Reactivated);
	TestEqual(TEXT("the active edge is still forest A"), Crossing.GetActiveEdgeId(), FString(TEXT("EDGE_FOREST_A")));
	return true;
}

#endif
