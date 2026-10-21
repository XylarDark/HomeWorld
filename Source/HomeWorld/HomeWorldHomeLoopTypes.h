// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldHomeLoopTypes.generated.h"

/** Station ids from Docs/42_HOME_LOOP_DESIGN.md. Order is the query order. */
UENUM()
enum class EHomeWorldHomeStation : uint8
{
	Sink,
	Board,
	Pot,
	Stove,
	Oven,
	Garbage
};

/** Vessels. Pan and Oven stay unused until a later recipe names one. */
UENUM()
enum class EHomeWorldHomeVessel : uint8
{
	Pot,
	Pan,
	Oven
};

/** Meal buffs. Glide and Gather log only; Stamina lengthens the sprint window. */
UENUM()
enum class EHomeWorldHomeBuff : uint8
{
	Stamina,
	Glide,
	Gather
};

/** One ingredient row. Chest item ids are not RES_* ids. */
USTRUCT()
struct FHomeWorldRecipeIngredient
{
	GENERATED_BODY()

	UPROPERTY()
	FName ChestItemId;

	UPROPERTY()
	EHomeWorldHomeStation PrepStation = EHomeWorldHomeStation::Sink;

	UPROPERTY()
	float PrepSeconds = 0.f;

	UPROPERTY()
	float CookSeconds = 0.f;
};

/** One food recipe. RECIPE_KETTLE is the first row. */
USTRUCT()
struct FHomeWorldRecipe
{
	GENERATED_BODY()

	UPROPERTY()
	FName Id;

	UPROPERTY()
	EHomeWorldHomeVessel Vessel = EHomeWorldHomeVessel::Pot;

	UPROPERTY()
	EHomeWorldHomeBuff BuffId = EHomeWorldHomeBuff::Stamina;

	UPROPERTY()
	TArray<FHomeWorldRecipeIngredient> Ingredients;
};

/** What the last serve or discard did. An empty result means nothing has finished. */
struct FHomeWorldServeResult
{
	bool bServed = false;
	float SyncFactor = 0.f;
	FName RecipeId;
	TArray<FName> SpentItemIds;
	bool bDiscarded = false;
};

/** One meal armed for one Day phase. */
struct FHomeWorldArmedBuff
{
	bool bOccupied = false;
	bool bLive = false;
	EHomeWorldHomeBuff BuffId = EHomeWorldHomeBuff::Stamina;
	float SyncFactor = 1.f;
	float CleanFactor = 1.f;
	int32 CoveredDayId = 0;
};

/** One healed task wisp, one target. */
UENUM()
enum class EHomeWorldWispTarget : uint8
{
	None,
	Station,
	Plot,
	Surface
};

struct FHomeWorldWispAssignment
{
	FName WispId;
	EHomeWorldWispTarget Target = EHomeWorldWispTarget::None;
	EHomeWorldHomeStation Station = EHomeWorldHomeStation::Sink;
	int32 PlotIndex = INDEX_NONE;
	FName SurfaceId;
};

/** One dusty surface. Floor is always tracked. Props are capped at six. */
struct FHomeWorldDustSurface
{
	FName SurfaceId;
	int32 Dust = 0;
};

/** One garden plot. A seed is ready after two home windows with a wisp on it. */
struct FHomeWorldPlot
{
	int32 Index = 0;
	bool bPlanted = false;
	bool bReady = false;
	int32 WindowsGrown = 0;
	FName CropItemId;
};
