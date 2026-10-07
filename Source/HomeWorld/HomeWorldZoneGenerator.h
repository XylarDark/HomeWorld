// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"

/**
 * Seeded zone skeleton for FIELD and FOREST.
 *
 * The zone specs in Lib/02_Zones are the contract (docs/39_ZONE_GENERATION_RESEARCH.md).
 * This type jitters the preset shape and scatters herbs from those numbers. It does
 * not spawn actors. Shape-variance amounts stay agent-proposed (docs/39 section 7 Q2)
 * and are read from the spec, not chosen here.
 *
 * Stream order inside Generate is part of the determinism contract: width, depth,
 * one shared pine_forest edge drift, then each non-forest edge in spec order, then
 * herb rejection sampling. EntryBandWidthM is copied from the spec and never rolled,
 * so the field-facing treeline read does not change with the seed.
 *
 * Authored slots are pinned after that scatter and do not consume the stream.
 * Their offsets are entry-relative (y = 0 on the entry band) and do not jitter.
 * Herb points stay zone-centred. A slot template contributes only parts that
 * already have an at_offset; missing offsets are left unplaced.
 */

/** A template piece that already had an at_offset. Offset is local until pin time. */
struct FHomeWorldZonePartSpec
{
	FString Id;
	FVector OffsetM = FVector::ZeroVector;
};

struct FHomeWorldZoneSlotSpec
{
	FString Id;
	FString Piece;
	bool bHasOffset = false;
	/** Entry-relative meters. */
	FVector OffsetM = FVector::ZeroVector;
	/** Full clearing envelope in meters. Zero means this slot does not punch the pine budget. */
	FVector2D ClearingSizeM = FVector2D::ZeroVector;
	/** Template parts that already had an at_offset. Local to this slot until pinned. */
	TArray<FHomeWorldZonePartSpec> Parts;
};

struct FHomeWorldZoneEdgeSpec
{
	FString Id;
	FString Type;
	/** north, south, east, or west. Parsed from the spec's "at" when "side" is absent. */
	FString Side;
};

struct FHomeWorldZoneSpec
{
	FString Id;
	float WidthM = 0.f;
	float DepthM = 0.f;
	/** Fraction of extent. 0.15 means the rolled size stays inside ±15%. */
	float ExtentJitterFraction = 0.15f;
	float EdgeBandDriftM = 25.f;
	float EntryBandWidthM = 0.f;
	/** Depth of the entry-light band. The wound must sit deeper than this. */
	float EntryLightDepthM = 0.f;
	float HerbMinSpacingM = 30.f;
	int32 PineInstanceCap = 0;
	float PineClumpSpacingM = 18.f;
	float PineClumpMeanCount = 5.5f;
	TArray<FHomeWorldZoneSlotSpec> Slots;
	TArray<FString> ModuleNames;
	TArray<FHomeWorldZoneEdgeSpec> Edges;
};

struct FHomeWorldZoneEdgeDrift
{
	FString Id;
	float DriftM = 0.f;
};

struct FHomeWorldGeneratedZone
{
	int32 Seed = 0;
	float WidthM = 0.f;
	float DepthM = 0.f;
	float EntryBandWidthM = 0.f;
	TArray<FHomeWorldZoneEdgeDrift> EdgeDrifts;
	/** Zone-local meters. Origin is the zone centre. */
	TArray<FVector2D> HerbPointsM;
	int32 PineInstanceCount = 0;
	/** Anchors with an authored offset. Slots with no offset (SLOT_FUTURE) are not pinned. */
	TArray<FHomeWorldZoneSlotSpec> PlacedSlots;
	/** Template parts in entry-relative meters: slot origin + the part's own at_offset. */
	TArray<FHomeWorldZonePartSpec> PlacedParts;
};

class FHomeWorldZoneGenerator
{
public:
	static bool LoadSpec(const FString& AbsolutePath, FHomeWorldZoneSpec& OutSpec, FString& OutError);

	/** bPinSlots false builds the biome skeleton only. The camp pins on discovery. */
	static FHomeWorldGeneratedZone Generate(const FHomeWorldZoneSpec& Spec, int32 Seed, bool bPinSlots = true);

	/** hash(field seed, edge id). Same pair always returns the same forest seed. */
	static int32 SeedForEdge(int32 FieldSeed, const FString& EdgeId);

	/** True when a slot or module name is camp content. The field template must stay false. */
	static bool HasCampContent(const FHomeWorldZoneSpec& Spec);
};

/** One marker placed on a decided field edge. The camp trigger is the bounds of these, not the meadow. */
struct FHomeWorldPlacedEdgeAsset
{
	FString EdgeId;
	FVector2D PositionM = FVector2D::ZeroVector;
};

/** Axis-aligned bounds of one edge's placed assets, padded so the line has a thickness. */
struct FHomeWorldDiscoveryBoundary
{
	FString EdgeId;
	FString NeighborKind;
	FVector2D MinM = FVector2D::ZeroVector;
	FVector2D MaxM = FVector2D::ZeroVector;

	bool Contains(const FVector2D& Point) const
	{
		return Point.X >= MinM.X && Point.X <= MaxM.X && Point.Y >= MinM.Y && Point.Y <= MaxM.Y;
	}

	FVector2D Center() const
	{
		return (MinM + MaxM) * 0.5f;
	}
};

/**
 * What a discovery query did. The field generates first. Camp placement happens
 * only when a point is inside a pine_forest edge's asset bounds. Cliff and river
 * bounds open no camp. The other pine edge stays dormant after the commitment.
 */
enum class EHomeWorldEdgeCrossResult : uint8
{
	UnknownEdge,
	NoNeighbor,
	Instantiated,
	Reactivated,
	LeftDormant,
	/** The point is not inside any edge-asset boundary. */
	Outside,
	/** Glider or boat traversal was started without the upgrade. */
	Locked,
	/** Cliff or river was asked for while night spirit is the traversal. */
	ClosedAtNight
};

/** How a field edge is entered. Ground edges stream with the field. The others wait for their upgrade. */
enum class EHomeWorldEdgeTraversal : uint8
{
	None,
	Ground,
	Glider,
	Boat
};

/** Where the player is. This chooses what streams, without a loading screen. */
enum class EHomeWorldStreamPresence : uint8
{
	Homestead,
	Field
};

class FHomeWorldZoneCrossing
{
public:
	void Reset(int32 InFieldSeed);

	/**
	 * Generate the field if needed, then treat the player as standing at the
	 * centre of that edge's placed assets.
	 */
	EHomeWorldEdgeCrossResult Cross(
		const FHomeWorldZoneSpec& FieldSpec,
		const FHomeWorldZoneSpec& ForestSpec,
		const FString& EdgeId);

	/** The real trigger: a point inside the bounds of the placed edge assets. */
	EHomeWorldEdgeCrossResult DiscoverAt(
		const FHomeWorldZoneSpec& FieldSpec,
		const FHomeWorldZoneSpec& ForestSpec,
		const FVector2D& PositionM);

	/** A pine_forest edge with no instance. Cliff and river are not dormant neighbors. */
	bool IsForestEdgeDormant(const FHomeWorldZoneSpec& FieldSpec, const FString& EdgeId) const;

	bool HasForest() const { return bHasForest; }
	bool HasCamp() const;

	/**
	 * Homestead streams the field and nothing beyond it.
	 * The field streams ground-traversable edges (the forests). Cliff and river wait.
	 * Night spirit keeps the forests and closes the cliff and the river.
	 */
	void SetPresence(
		const FHomeWorldZoneSpec& FieldSpec,
		const FHomeWorldZoneSpec& ForestSpec,
		EHomeWorldStreamPresence Presence);

	void SetTraversalUnlocks(bool bGliderUnlocked, bool bBoatUnlocked);

	/**
	 * Interview #17 3A, coded interview #20. Night spirit crosses pine_forest
	 * edges only. Cliff and river stay closed even when the glider and boat are unlocked.
	 */
	void SetNightSpirit(bool bInNightSpirit);
	bool IsNightSpirit() const { return bNightSpirit; }

	/** Start the cliff glider or the river boat. Ground edges are not started this way. */
	EHomeWorldEdgeCrossResult BeginTraversal(const FHomeWorldZoneSpec& FieldSpec, const FString& EdgeId);

	bool IsFieldStreaming() const { return bFieldStreaming; }
	bool IsZoneStreaming(const FString& EdgeId) const;
	const FHomeWorldGeneratedZone* GetStreamedZone(const FString& EdgeId) const;
	static EHomeWorldEdgeTraversal TraversalForType(const FString& Type);
	const FString& GetActiveEdgeId() const { return ActiveEdgeId; }
	const FHomeWorldGeneratedZone& GetForest() const { return Forest; }
	const FHomeWorldGeneratedZone& GetField() const { return Field; }
	const TArray<FHomeWorldPlacedEdgeAsset>& GetEdgeAssets() const { return EdgeAssets; }
	const TArray<FHomeWorldDiscoveryBoundary>& GetBoundaries() const { return Boundaries; }
	int32 GetFieldSeed() const { return FieldSeed; }

private:
	void EnsureField(const FHomeWorldZoneSpec& FieldSpec);
	const FHomeWorldDiscoveryBoundary* FindBoundary(const FString& EdgeId) const;
	const FHomeWorldDiscoveryBoundary* FindContaining(const FVector2D& PositionM) const;

	int32 FieldSeed = 0;
	FString ActiveEdgeId;
	bool bHasForest = false;
	bool bFieldReady = false;
	bool bFieldStreaming = false;
	bool bGliderUnlocked = false;
	bool bBoatUnlocked = false;
	bool bNightSpirit = false;
	EHomeWorldStreamPresence Presence = EHomeWorldStreamPresence::Homestead;
	FString ChosenEdgeId;
	FString SpecialEdgeId;
	FHomeWorldGeneratedZone Field;
	FHomeWorldGeneratedZone Forest;
	TArray<FHomeWorldPlacedEdgeAsset> EdgeAssets;
	TArray<FHomeWorldDiscoveryBoundary> Boundaries;
	TArray<FString> StreamingEdgeIds;
	TMap<FString, FHomeWorldGeneratedZone> StreamedZones;
};
