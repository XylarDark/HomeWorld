// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldZoneGenerator.h"

#include "Dom/JsonObject.h"
#include "Misc/Crc.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Math/NumericLimits.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace
{
	bool IsPineForestEdge(const FString& Type)
	{
		return Type.Equals(TEXT("pine_forest"), ESearchCase::IgnoreCase);
	}

	bool TextIsCamp(const FString& Text)
	{
		return Text.Contains(TEXT("camp"), ESearchCase::IgnoreCase);
	}

	const TSharedPtr<FJsonObject>* ObjectField(const TSharedPtr<FJsonObject>& Root, const TCHAR* Name)
	{
		if (!Root.IsValid())
		{
			return nullptr;
		}
		const TSharedPtr<FJsonObject>* Out = nullptr;
		if (!Root->TryGetObjectField(Name, Out) || Out == nullptr || !Out->IsValid())
		{
			return nullptr;
		}
		return Out;
	}

	float NumberOr(const TSharedPtr<FJsonObject>& Obj, const TCHAR* Name, float Fallback)
	{
		if (!Obj.IsValid() || !Obj->HasField(Name))
		{
			return Fallback;
		}
		const TSharedPtr<FJsonValue> Value = Obj->TryGetField(Name);
		if (!Value.IsValid() || Value->Type != EJson::Number)
		{
			return Fallback;
		}
		return static_cast<float>(Value->AsNumber());
	}

	bool ReadVector(const TSharedPtr<FJsonObject>& Obj, const TCHAR* Field, FVector& Out)
	{
		const TArray<TSharedPtr<FJsonValue>>* Values = nullptr;
		if (!Obj.IsValid() || !Obj->TryGetArrayField(Field, Values) || Values == nullptr || Values->Num() < 2)
		{
			return false;
		}
		Out.X = static_cast<float>((*Values)[0]->AsNumber());
		Out.Y = static_cast<float>((*Values)[1]->AsNumber());
		Out.Z = Values->Num() >= 3 ? static_cast<float>((*Values)[2]->AsNumber()) : 0.f;
		return true;
	}

	void ReadOffsetParts(const TSharedPtr<FJsonObject>& Root, const TCHAR* ArrayName, TArray<FHomeWorldZonePartSpec>& OutParts)
	{
		const TArray<TSharedPtr<FJsonValue>>* Values = nullptr;
		if (!Root.IsValid() || !Root->TryGetArrayField(ArrayName, Values) || Values == nullptr)
		{
			return;
		}
		for (const TSharedPtr<FJsonValue>& Value : *Values)
		{
			const TSharedPtr<FJsonObject>* PartObj = nullptr;
			if (!Value.IsValid() || !Value->TryGetObject(PartObj) || PartObj == nullptr || !PartObj->IsValid())
			{
				continue;
			}
			FVector Offset = FVector::ZeroVector;
			if (!ReadVector(*PartObj, TEXT("at_offset"), Offset))
			{
				continue;
			}
			FHomeWorldZonePartSpec Part;
			(*PartObj)->TryGetStringField(TEXT("name"), Part.Id);
			Part.OffsetM = Offset;
			if (!Part.Id.IsEmpty())
			{
				OutParts.Add(Part);
			}
		}
	}

	bool ReadTemplate(const FString& TemplatePath, FHomeWorldZoneSlotSpec& Slot, FString& OutError)
	{
		const FString AbsolutePath = FPaths::ConvertRelativePathToFull(FPaths::ProjectDir() / TemplatePath);
		FString Json;
		if (!FFileHelper::LoadFileToString(Json, *AbsolutePath))
		{
			OutError = FString::Printf(TEXT("Could not read slot template: %s"), *AbsolutePath);
			return false;
		}
		TSharedPtr<FJsonObject> Root;
		const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Json);
		if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
		{
			OutError = FString::Printf(TEXT("Slot template is not JSON: %s"), *AbsolutePath);
			return false;
		}
		const TSharedPtr<FJsonObject>* Size = ObjectField(Root, TEXT("size_m"));
		if (Size && Size->IsValid())
		{
			Slot.ClearingSizeM.X = NumberOr(*Size, TEXT("x"), 0.f);
			Slot.ClearingSizeM.Y = NumberOr(*Size, TEXT("y"), 0.f);
		}
		ReadOffsetParts(Root, TEXT("modules"), Slot.Parts);
		ReadOffsetParts(Root, TEXT("triggers"), Slot.Parts);
		return true;
	}

	bool ReadSlots(const TSharedPtr<FJsonObject>& Root, TArray<FHomeWorldZoneSlotSpec>& OutSlots, FString& OutError)
	{
		const TArray<TSharedPtr<FJsonValue>>* SlotValues = nullptr;
		if (!Root->TryGetArrayField(TEXT("slots"), SlotValues) || SlotValues == nullptr)
		{
			return true;
		}
		for (const TSharedPtr<FJsonValue>& Value : *SlotValues)
		{
			const TSharedPtr<FJsonObject>* SlotObj = nullptr;
			if (!Value.IsValid() || !Value->TryGetObject(SlotObj) || SlotObj == nullptr || !SlotObj->IsValid())
			{
				continue;
			}
			FHomeWorldZoneSlotSpec Slot;
			(*SlotObj)->TryGetStringField(TEXT("id"), Slot.Id);
			(*SlotObj)->TryGetStringField(TEXT("piece"), Slot.Piece);
			Slot.bHasOffset = ReadVector(*SlotObj, TEXT("at"), Slot.OffsetM);
			FString TemplatePath;
			if ((*SlotObj)->TryGetStringField(TEXT("template_path"), TemplatePath) && !TemplatePath.IsEmpty())
			{
				if (!ReadTemplate(TemplatePath, Slot, OutError))
				{
					return false;
				}
			}
			OutSlots.Add(Slot);
		}
		return true;
	}

	void ReadEdges(const TSharedPtr<FJsonObject>& Root, TArray<FHomeWorldZoneEdgeSpec>& OutEdges)
	{
		const TArray<TSharedPtr<FJsonValue>>* EdgeValues = nullptr;
		if (!Root->TryGetArrayField(TEXT("edges"), EdgeValues) || EdgeValues == nullptr)
		{
			return;
		}
		for (const TSharedPtr<FJsonValue>& Value : *EdgeValues)
		{
			const TSharedPtr<FJsonObject>* EdgeObj = nullptr;
			if (!Value.IsValid() || !Value->TryGetObject(EdgeObj) || EdgeObj == nullptr || !EdgeObj->IsValid())
			{
				continue;
			}
			FHomeWorldZoneEdgeSpec Edge;
			(*EdgeObj)->TryGetStringField(TEXT("id"), Edge.Id);
			(*EdgeObj)->TryGetStringField(TEXT("type"), Edge.Type);
			(*EdgeObj)->TryGetStringField(TEXT("side"), Edge.Side);
			if (Edge.Side.IsEmpty())
			{
				FString At;
				if ((*EdgeObj)->TryGetStringField(TEXT("at"), At))
				{
					int32 Comma = INDEX_NONE;
					Edge.Side = At.FindChar(TEXT(','), Comma) ? At.Left(Comma) : At;
					Edge.Side.TrimStartAndEndInline();
				}
			}
			Edge.Side.ToLowerInline();
			if (!Edge.Id.IsEmpty())
			{
				OutEdges.Add(Edge);
			}
		}
	}

	void ReadModuleNames(const TSharedPtr<FJsonObject>& Root, TArray<FString>& OutNames)
	{
		const TArray<TSharedPtr<FJsonValue>>* Modules = nullptr;
		if (!Root->TryGetArrayField(TEXT("modules"), Modules) || Modules == nullptr)
		{
			return;
		}
		for (const TSharedPtr<FJsonValue>& Value : *Modules)
		{
			const TSharedPtr<FJsonObject>* ModuleObj = nullptr;
			if (!Value.IsValid() || !Value->TryGetObject(ModuleObj) || ModuleObj == nullptr || !ModuleObj->IsValid())
			{
				continue;
			}
			FString Name;
			if ((*ModuleObj)->TryGetStringField(TEXT("name"), Name) && !Name.IsEmpty())
			{
				OutNames.Add(Name);
			}
		}
	}

	int32 EstimatePineCount(float WidthM, float DepthM, const FHomeWorldZoneSpec& Spec, float ReservedAreaM2)
	{
		if (Spec.PineInstanceCap <= 0 || WidthM <= 0.f || DepthM <= 0.f || Spec.PineClumpSpacingM <= 0.f)
		{
			return 0;
		}
		const float Area = FMath::Max(0.f, WidthM * DepthM - FMath::Max(0.f, ReservedAreaM2));
		const float Cell = Spec.PineClumpSpacingM * Spec.PineClumpSpacingM;
		const float Raw = Area / Cell * FMath::Max(0.f, Spec.PineClumpMeanCount);
		return FMath::Min(FMath::FloorToInt(Raw), Spec.PineInstanceCap);
	}

	void PinSlots(const FHomeWorldZoneSpec& Spec, FHomeWorldGeneratedZone& Out, float& OutReservedAreaM2)
	{
		OutReservedAreaM2 = 0.f;
		for (const FHomeWorldZoneSlotSpec& Slot : Spec.Slots)
		{
			if (!Slot.bHasOffset)
			{
				continue;
			}
			FHomeWorldZoneSlotSpec Pinned = Slot;
			Pinned.Parts.Reset();
			Out.PlacedSlots.Add(Pinned);
			OutReservedAreaM2 += FMath::Max(0.f, Slot.ClearingSizeM.X) * FMath::Max(0.f, Slot.ClearingSizeM.Y);
			for (const FHomeWorldZonePartSpec& Part : Slot.Parts)
			{
				FHomeWorldZonePartSpec Placed = Part;
				Placed.OffsetM += Slot.OffsetM;
				Out.PlacedParts.Add(Placed);
			}
		}
	}
}

bool FHomeWorldZoneGenerator::LoadSpec(const FString& AbsolutePath, FHomeWorldZoneSpec& OutSpec, FString& OutError)
{
	OutSpec = FHomeWorldZoneSpec();
	FString Json;
	if (!FFileHelper::LoadFileToString(Json, *AbsolutePath))
	{
		OutError = FString::Printf(TEXT("Could not read zone spec: %s"), *AbsolutePath);
		return false;
	}

	TSharedPtr<FJsonObject> Root;
	const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Json);
	if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
	{
		OutError = FString::Printf(TEXT("Zone spec is not JSON: %s"), *AbsolutePath);
		return false;
	}

	if (!Root->TryGetStringField(TEXT("id"), OutSpec.Id) || OutSpec.Id.IsEmpty())
	{
		OutError = FString::Printf(TEXT("Zone spec has no id: %s"), *AbsolutePath);
		return false;
	}

	const TSharedPtr<FJsonObject>* Generation = ObjectField(Root, TEXT("generation"));
	const TSharedPtr<FJsonObject>* Shape = Generation ? ObjectField(*Generation, TEXT("shape")) : nullptr;
	const TSharedPtr<FJsonObject>* Entry = Generation ? ObjectField(*Generation, TEXT("entry")) : nullptr;
	const TSharedPtr<FJsonObject>* Budget = ObjectField(Root, TEXT("budget"));
	const TSharedPtr<FJsonObject>* Bounds = ObjectField(Root, TEXT("world_bounds_m"));

	if (Shape && Shape->IsValid())
	{
		OutSpec.WidthM = NumberOr(*Shape, TEXT("width_m"), OutSpec.WidthM);
		OutSpec.DepthM = NumberOr(*Shape, TEXT("depth_m"), OutSpec.DepthM);
		OutSpec.ExtentJitterFraction = NumberOr(*Shape, TEXT("extent_jitter_fraction"), OutSpec.ExtentJitterFraction);
		OutSpec.EdgeBandDriftM = NumberOr(*Shape, TEXT("edge_band_drift_m"), OutSpec.EdgeBandDriftM);
	}
	else if (Bounds && Bounds->IsValid())
	{
		OutSpec.WidthM = NumberOr(*Bounds, TEXT("x"), OutSpec.WidthM);
		OutSpec.DepthM = NumberOr(*Bounds, TEXT("y"), OutSpec.DepthM);
	}

	if (Entry && Entry->IsValid())
	{
		OutSpec.EntryBandWidthM = NumberOr(*Entry, TEXT("band_width_m"), OutSpec.EntryBandWidthM);
	}
	if (Generation && Generation->IsValid())
	{
		OutSpec.EntryLightDepthM = NumberOr(*Generation, TEXT("entry_light_depth_m"), OutSpec.EntryLightDepthM);
	}
	if (Budget && Budget->IsValid())
	{
		OutSpec.HerbMinSpacingM = NumberOr(*Budget, TEXT("herb_min_spacing_m"), OutSpec.HerbMinSpacingM);
		OutSpec.PineInstanceCap = FMath::FloorToInt(NumberOr(*Budget, TEXT("pine_instance_cap"), static_cast<float>(OutSpec.PineInstanceCap)));
		OutSpec.PineClumpSpacingM = NumberOr(*Budget, TEXT("pine_clump_spacing_m"), OutSpec.PineClumpSpacingM);
		OutSpec.PineClumpMeanCount = NumberOr(*Budget, TEXT("pine_clump_mean_count"), OutSpec.PineClumpMeanCount);
	}

	if (!ReadSlots(Root, OutSpec.Slots, OutError))
	{
		return false;
	}
	ReadEdges(Root, OutSpec.Edges);
	ReadModuleNames(Root, OutSpec.ModuleNames);
	return true;
}

FHomeWorldGeneratedZone FHomeWorldZoneGenerator::Generate(const FHomeWorldZoneSpec& Spec, int32 Seed, bool bPinSlots)
{
	FHomeWorldGeneratedZone Out;
	Out.Seed = Seed;
	Out.EntryBandWidthM = Spec.EntryBandWidthM;

	FRandomStream Stream(Seed);
	const float Jitter = FMath::Clamp(Spec.ExtentJitterFraction, 0.f, 1.f);
	Out.WidthM = FMath::Max(0.f, Spec.WidthM) * Stream.FRandRange(1.f - Jitter, 1.f + Jitter);
	Out.DepthM = FMath::Max(0.f, Spec.DepthM) * Stream.FRandRange(1.f - Jitter, 1.f + Jitter);

	bool bHasForestEdge = false;
	for (const FHomeWorldZoneEdgeSpec& Edge : Spec.Edges)
	{
		if (IsPineForestEdge(Edge.Type))
		{
			bHasForestEdge = true;
			break;
		}
	}
	const float DriftCap = FMath::Max(0.f, Spec.EdgeBandDriftM);
	const float SharedForestDrift = bHasForestEdge ? Stream.FRandRange(-DriftCap, DriftCap) : 0.f;
	for (const FHomeWorldZoneEdgeSpec& Edge : Spec.Edges)
	{
		FHomeWorldZoneEdgeDrift Drift;
		Drift.Id = Edge.Id;
		Drift.DriftM = IsPineForestEdge(Edge.Type) ? SharedForestDrift : Stream.FRandRange(-DriftCap, DriftCap);
		Out.EdgeDrifts.Add(Drift);
	}

	if (Spec.HerbMinSpacingM > 0.f && Out.WidthM > 0.f && Out.DepthM > 0.f)
	{
		const float Spacing = Spec.HerbMinSpacingM;
		const int32 Target = FMath::Clamp(
			FMath::FloorToInt((Out.WidthM * Out.DepthM) / (Spacing * Spacing)),
			0,
			400);
		const int32 MaxAttempts = Target * 40;
		for (int32 Attempt = 0; Attempt < MaxAttempts && Out.HerbPointsM.Num() < Target; ++Attempt)
		{
			const FVector2D Candidate(
				Stream.FRandRange(-Out.WidthM * 0.5f, Out.WidthM * 0.5f),
				Stream.FRandRange(-Out.DepthM * 0.5f, Out.DepthM * 0.5f));
			bool bClear = true;
			for (const FVector2D& Existing : Out.HerbPointsM)
			{
				if (FVector2D::Distance(Candidate, Existing) < Spacing)
				{
					bClear = false;
					break;
				}
			}
			if (bClear)
			{
				Out.HerbPointsM.Add(Candidate);
			}
		}
	}

	float ReservedAreaM2 = 0.f;
	if (bPinSlots)
	{
		PinSlots(Spec, Out, ReservedAreaM2);
	}
	Out.PineInstanceCount = EstimatePineCount(Out.WidthM, Out.DepthM, Spec, ReservedAreaM2);
	return Out;
}

int32 FHomeWorldZoneGenerator::SeedForEdge(int32 FieldSeed, const FString& EdgeId)
{
	const uint32 EdgeCrc = FCrc::StrCrc32(*EdgeId);
	uint32 Mixed = FCrc::MemCrc32(&FieldSeed, sizeof(FieldSeed), EdgeCrc);
	return static_cast<int32>(Mixed);
}

namespace
{
void PlaceEdgeAssets(
	const FHomeWorldZoneSpec& Spec,
	const FHomeWorldGeneratedZone& Zone,
	TArray<FHomeWorldPlacedEdgeAsset>& OutAssets,
	TArray<FHomeWorldDiscoveryBoundary>& OutBoundaries)
{
	const float Spacing = FMath::Max(Spec.HerbMinSpacingM, 1.f);
	const float HalfW = Zone.WidthM * 0.5f;
	const float HalfD = Zone.DepthM * 0.5f;
	const float ForestRadius = FMath::Max(HalfW, HalfD);
	const float ForestSpan = ForestRadius * 2.f;
	const int32 ForestCount = FMath::Max(2, FMath::FloorToInt(ForestSpan / Spacing) + 1);
	const float Pad = Spacing * 0.5f;

	for (const FHomeWorldZoneEdgeSpec& Edge : Spec.Edges)
	{
		if (Edge.Side.IsEmpty())
		{
			continue;
		}
		float Drift = 0.f;
		for (const FHomeWorldZoneEdgeDrift& EdgeDrift : Zone.EdgeDrifts)
		{
			if (EdgeDrift.Id == Edge.Id)
			{
				Drift = EdgeDrift.DriftM;
				break;
			}
		}
		const bool bForest = IsPineForestEdge(Edge.Type);
		const bool bNorthSouth = Edge.Side == TEXT("north") || Edge.Side == TEXT("south");
		const float Radius = bForest ? ForestRadius : (bNorthSouth ? HalfD : HalfW);
		const float Span = bForest ? ForestSpan : (bNorthSouth ? Zone.WidthM : Zone.DepthM);
		const int32 Count = bForest ? ForestCount : FMath::Max(2, FMath::FloorToInt(Span / Spacing) + 1);
		float Fixed = 0.f;
		if (Edge.Side == TEXT("north") || Edge.Side == TEXT("east"))
		{
			Fixed = Radius + Drift;
		}
		else if (Edge.Side == TEXT("south") || Edge.Side == TEXT("west"))
		{
			Fixed = -Radius + Drift;
		}
		else
		{
			continue;
		}

		FHomeWorldDiscoveryBoundary Boundary;
		Boundary.EdgeId = Edge.Id;
		Boundary.NeighborKind = Edge.Type;
		Boundary.MinM = FVector2D(TNumericLimits<float>::Max(), TNumericLimits<float>::Max());
		Boundary.MaxM = FVector2D(TNumericLimits<float>::Lowest(), TNumericLimits<float>::Lowest());
		const float Step = Count <= 1 ? 0.f : Span / static_cast<float>(Count - 1);
		const float Start = -Span * 0.5f;
		for (int32 Index = 0; Index < Count; ++Index)
		{
			const float Along = Start + Step * static_cast<float>(Index);
			const FVector2D Position = bNorthSouth ? FVector2D(Along, Fixed) : FVector2D(Fixed, Along);
			FHomeWorldPlacedEdgeAsset Asset;
			Asset.EdgeId = Edge.Id;
			Asset.PositionM = Position;
			OutAssets.Add(Asset);
			Boundary.MinM.X = FMath::Min(Boundary.MinM.X, Position.X);
			Boundary.MinM.Y = FMath::Min(Boundary.MinM.Y, Position.Y);
			Boundary.MaxM.X = FMath::Max(Boundary.MaxM.X, Position.X);
			Boundary.MaxM.Y = FMath::Max(Boundary.MaxM.Y, Position.Y);
		}
		Boundary.MinM -= FVector2D(Pad, Pad);
		Boundary.MaxM += FVector2D(Pad, Pad);
		OutBoundaries.Add(Boundary);
	}
}
}

void FHomeWorldZoneCrossing::Reset(int32 InFieldSeed)
{
	FieldSeed = InFieldSeed;
	ActiveEdgeId.Reset();
	ChosenEdgeId.Reset();
	SpecialEdgeId.Reset();
	bHasForest = false;
	bFieldReady = false;
	bFieldStreaming = false;
	bGliderUnlocked = false;
	bBoatUnlocked = false;
	bNightSpirit = false;
	Presence = EHomeWorldStreamPresence::Homestead;
	Field = FHomeWorldGeneratedZone();
	Forest = FHomeWorldGeneratedZone();
	EdgeAssets.Reset();
	Boundaries.Reset();
	StreamingEdgeIds.Reset();
	StreamedZones.Reset();
}

void FHomeWorldZoneCrossing::EnsureField(const FHomeWorldZoneSpec& FieldSpec)
{
	if (bFieldReady)
	{
		return;
	}
	Field = FHomeWorldZoneGenerator::Generate(FieldSpec, FieldSeed);
	PlaceEdgeAssets(FieldSpec, Field, EdgeAssets, Boundaries);
	bFieldReady = true;
}

const FHomeWorldDiscoveryBoundary* FHomeWorldZoneCrossing::FindBoundary(const FString& EdgeId) const
{
	for (const FHomeWorldDiscoveryBoundary& Boundary : Boundaries)
	{
		if (Boundary.EdgeId == EdgeId)
		{
			return &Boundary;
		}
	}
	return nullptr;
}

const FHomeWorldDiscoveryBoundary* FHomeWorldZoneCrossing::FindContaining(const FVector2D& PositionM) const
{
	const FHomeWorldDiscoveryBoundary* Best = nullptr;
	float BestDistance = TNumericLimits<float>::Max();
	for (const FHomeWorldDiscoveryBoundary& Boundary : Boundaries)
	{
		if (!Boundary.Contains(PositionM))
		{
			continue;
		}
		const float Distance = FVector2D::Distance(PositionM, Boundary.Center());
		if (Distance < BestDistance)
		{
			Best = &Boundary;
			BestDistance = Distance;
		}
	}
	return Best;
}

EHomeWorldEdgeCrossResult FHomeWorldZoneCrossing::DiscoverAt(
	const FHomeWorldZoneSpec& FieldSpec,
	const FHomeWorldZoneSpec& ForestSpec,
	const FVector2D& PositionM)
{
	EnsureField(FieldSpec);
	const FHomeWorldDiscoveryBoundary* Hit = FindContaining(PositionM);
	if (Hit == nullptr)
	{
		return EHomeWorldEdgeCrossResult::Outside;
	}
	if (!IsPineForestEdge(Hit->NeighborKind))
	{
		return EHomeWorldEdgeCrossResult::NoNeighbor;
	}
	if (bHasForest)
	{
		return ActiveEdgeId == Hit->EdgeId
			? EHomeWorldEdgeCrossResult::Reactivated
			: EHomeWorldEdgeCrossResult::LeftDormant;
	}

	const int32 ZoneSeed = FHomeWorldZoneGenerator::SeedForEdge(FieldSeed, Hit->EdgeId);
	Forest = FHomeWorldZoneGenerator::Generate(ForestSpec, ZoneSeed, true);
	StreamedZones.Add(Hit->EdgeId, Forest);
	StreamingEdgeIds.AddUnique(Hit->EdgeId);
	ActiveEdgeId = Hit->EdgeId;
	ChosenEdgeId = Hit->EdgeId;
	bHasForest = true;
	return EHomeWorldEdgeCrossResult::Instantiated;
}

EHomeWorldEdgeCrossResult FHomeWorldZoneCrossing::Cross(
	const FHomeWorldZoneSpec& FieldSpec,
	const FHomeWorldZoneSpec& ForestSpec,
	const FString& EdgeId)
{
	EnsureField(FieldSpec);
	const FHomeWorldDiscoveryBoundary* Boundary = FindBoundary(EdgeId);
	if (Boundary == nullptr)
	{
		bool bKnown = false;
		for (const FHomeWorldZoneEdgeSpec& Edge : FieldSpec.Edges)
		{
			if (Edge.Id == EdgeId)
			{
				bKnown = true;
				break;
			}
		}
		return bKnown ? EHomeWorldEdgeCrossResult::NoNeighbor : EHomeWorldEdgeCrossResult::UnknownEdge;
	}
	return DiscoverAt(FieldSpec, ForestSpec, Boundary->Center());
}

bool FHomeWorldZoneCrossing::HasCamp() const
{
	if (!bHasForest)
	{
		return false;
	}
	FHomeWorldZoneSpec Placed;
	Placed.Slots = Forest.PlacedSlots;
	return FHomeWorldZoneGenerator::HasCampContent(Placed);
}

EHomeWorldEdgeTraversal FHomeWorldZoneCrossing::TraversalForType(const FString& Type)
{
	if (Type.Equals(TEXT("pine_forest"), ESearchCase::IgnoreCase))
	{
		return EHomeWorldEdgeTraversal::Ground;
	}
	if (Type.Equals(TEXT("cliff"), ESearchCase::IgnoreCase))
	{
		return EHomeWorldEdgeTraversal::Glider;
	}
	if (Type.Equals(TEXT("river"), ESearchCase::IgnoreCase))
	{
		return EHomeWorldEdgeTraversal::Boat;
	}
	return EHomeWorldEdgeTraversal::None;
}

void FHomeWorldZoneCrossing::SetTraversalUnlocks(bool bInGliderUnlocked, bool bInBoatUnlocked)
{
	bGliderUnlocked = bInGliderUnlocked;
	bBoatUnlocked = bInBoatUnlocked;
}

void FHomeWorldZoneCrossing::SetNightSpirit(bool bInNightSpirit)
{
	bNightSpirit = bInNightSpirit;
	if (!bNightSpirit || SpecialEdgeId.IsEmpty())
	{
		return;
	}
	StreamingEdgeIds.Remove(SpecialEdgeId);
	SpecialEdgeId.Reset();
}

bool FHomeWorldZoneCrossing::IsZoneStreaming(const FString& EdgeId) const
{
	return StreamingEdgeIds.Contains(EdgeId);
}

const FHomeWorldGeneratedZone* FHomeWorldZoneCrossing::GetStreamedZone(const FString& EdgeId) const
{
	return StreamedZones.Find(EdgeId);
}

void FHomeWorldZoneCrossing::SetPresence(
	const FHomeWorldZoneSpec& FieldSpec,
	const FHomeWorldZoneSpec& ForestSpec,
	EHomeWorldStreamPresence InPresence)
{
	Presence = InPresence;
	bFieldStreaming = true;
	StreamingEdgeIds.Reset();
	StreamedZones.Reset();
	bHasForest = false;
	Forest = FHomeWorldGeneratedZone();
	if (Presence != EHomeWorldStreamPresence::Field)
	{
		SpecialEdgeId.Reset();
		return;
	}

	EnsureField(FieldSpec);
	for (const FHomeWorldZoneEdgeSpec& Edge : FieldSpec.Edges)
	{
		if (TraversalForType(Edge.Type) != EHomeWorldEdgeTraversal::Ground)
		{
			continue;
		}
		const bool bPinsCamp = Edge.Id == ChosenEdgeId;
		const FHomeWorldGeneratedZone Zone = FHomeWorldZoneGenerator::Generate(
			ForestSpec, FHomeWorldZoneGenerator::SeedForEdge(FieldSeed, Edge.Id), bPinsCamp);
		StreamedZones.Add(Edge.Id, Zone);
		StreamingEdgeIds.Add(Edge.Id);
		if (bPinsCamp)
		{
			Forest = Zone;
			ActiveEdgeId = Edge.Id;
			bHasForest = true;
		}
	}
	if (!bNightSpirit && !SpecialEdgeId.IsEmpty())
	{
		StreamingEdgeIds.AddUnique(SpecialEdgeId);
	}
}

EHomeWorldEdgeCrossResult FHomeWorldZoneCrossing::BeginTraversal(
	const FHomeWorldZoneSpec& FieldSpec,
	const FString& EdgeId)
{
	EnsureField(FieldSpec);
	const FHomeWorldZoneEdgeSpec* Edge = nullptr;
	for (const FHomeWorldZoneEdgeSpec& Candidate : FieldSpec.Edges)
	{
		if (Candidate.Id == EdgeId)
		{
			Edge = &Candidate;
			break;
		}
	}
	if (Edge == nullptr)
	{
		return EHomeWorldEdgeCrossResult::UnknownEdge;
	}
	const EHomeWorldEdgeTraversal Traversal = TraversalForType(Edge->Type);
	if (Traversal == EHomeWorldEdgeTraversal::Ground || Traversal == EHomeWorldEdgeTraversal::None)
	{
		return EHomeWorldEdgeCrossResult::NoNeighbor;
	}
	if (Presence != EHomeWorldStreamPresence::Field)
	{
		return EHomeWorldEdgeCrossResult::NoNeighbor;
	}
	if (bNightSpirit)
	{
		return EHomeWorldEdgeCrossResult::ClosedAtNight;
	}
	const bool bUnlocked = Traversal == EHomeWorldEdgeTraversal::Glider ? bGliderUnlocked : bBoatUnlocked;
	if (!bUnlocked)
	{
		return EHomeWorldEdgeCrossResult::Locked;
	}
	const bool bAlready = StreamingEdgeIds.Contains(EdgeId);
	SpecialEdgeId = EdgeId;
	StreamingEdgeIds.AddUnique(EdgeId);
	return bAlready ? EHomeWorldEdgeCrossResult::Reactivated : EHomeWorldEdgeCrossResult::Instantiated;
}

bool FHomeWorldZoneCrossing::IsForestEdgeDormant(const FHomeWorldZoneSpec& FieldSpec, const FString& EdgeId) const
{
	for (const FHomeWorldZoneEdgeSpec& Edge : FieldSpec.Edges)
	{
		if (Edge.Id == EdgeId && IsPineForestEdge(Edge.Type))
		{
			return !bHasForest || ActiveEdgeId != EdgeId;
		}
	}
	return false;
}

bool FHomeWorldZoneGenerator::HasCampContent(const FHomeWorldZoneSpec& Spec)
{
	for (const FHomeWorldZoneSlotSpec& Slot : Spec.Slots)
	{
		if (TextIsCamp(Slot.Id) || TextIsCamp(Slot.Piece))
		{
			return true;
		}
	}
	for (const FString& Name : Spec.ModuleNames)
	{
		if (TextIsCamp(Name))
		{
			return true;
		}
	}
	return false;
}
