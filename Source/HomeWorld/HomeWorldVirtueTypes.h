// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldVirtueTypes.generated.h"

/** One pole of a virtue axis. Adjacent values are opposites. Docs/VIRTUE_ATTRIBUTE_BIBLE.md. */
UENUM(BlueprintType)
enum class EHomeWorldVirtuePole : uint8
{
	Greed,
	Generosity,
	Gluttony,
	Abstinence,
	Sloth,
	Productivity,
	Wrath,
	Grace,
	Pride,
	Humility,
	Envy,
	Fulfillment,
	Lust,
	Love
};

namespace HomeWorldVirtue
{
	inline constexpr int32 AxisCount = 7;

	inline int32 AxisIndex(EHomeWorldVirtuePole Pole)
	{
		return static_cast<int32>(Pole) / 2;
	}

	inline EHomeWorldVirtuePole Opposite(EHomeWorldVirtuePole Pole)
	{
		const int32 Value = static_cast<int32>(Pole);
		return static_cast<EHomeWorldVirtuePole>(Value ^ 1);
	}

	HOMEWORLD_API TArray<float> PlaceholderChances();

	HOMEWORLD_API bool ChancesAreNonIncreasing(const TArray<float>& Chances);

	/** Rejects a second pole on an axis and a set larger than seven. */
	HOMEWORLD_API bool TrySetHandPoles(TArray<EHomeWorldVirtuePole>& OutPoles, const TArray<EHomeWorldVirtuePole>& Hand, FString& OutError);

	/** Stops on the first miss. Picks an unused axis, then one of its two poles. Never a paradox. */
	HOMEWORLD_API void RollPoles(TArray<EHomeWorldVirtuePole>& OutPoles, const TArray<float>& Chances, FRandomStream& Stream);

	/** One paradox occupies the axis. Fails if that axis already has a pole or a paradox, or the set is full. */
	HOMEWORLD_API bool TryAddParadoxAxis(
		TArray<int32>& ParadoxAxes,
		const TArray<EHomeWorldVirtuePole>& Poles,
		int32 Axis,
		FString& OutError);

	HOMEWORLD_API bool ParadoxOccupies(const TArray<int32>& ParadoxAxes, int32 Axis);

	HOMEWORLD_API FString FormatPoles(const TArray<EHomeWorldVirtuePole>& Poles);

	HOMEWORLD_API const TCHAR* PoleName(EHomeWorldVirtuePole Pole);
}

/** One herb that carries poles. Not a RES_HERB count. */
USTRUCT(BlueprintType)
struct FHomeWorldMarkedHerb
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly, Category = "Virtue")
	TArray<EHomeWorldVirtuePole> Poles;
};
