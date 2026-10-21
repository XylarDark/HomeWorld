// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "HomeWorldHomeLoopTypes.h"

class AHomeWorldCharacter;

#include "HomeWorldHomeLoopSubsystem.generated.h"

/**
 * Cooking, cleaning, and the garden. Docs/42_HOME_LOOP_DESIGN.md.
 * Stations, dust, plots, and the armed buff live here, beside the character's tea gate.
 */
UCLASS()
class HOMEWORLD_API UHomeWorldHomeLoopSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	/** The six stations, in design order. No timers. */
	void GetStationIds(TArray<EHomeWorldHomeStation>& OutIds) const;

	/** Logs `home_loop: station <Id>` and returns that same line. */
	FString LogStation(EHomeWorldHomeStation Station) const;

	/** Bite 1 has no clock. Stays 0 until a later bite starts one. */
	float GetHomeClockSeconds() const { return HomeClockSeconds; }

	/** Recipe row. RECIPE_KETTLE is the first food id. */
	bool GetRecipe(FName RecipeId, FHomeWorldRecipe& OutRecipe) const;

	/**
	 * Opening-day kettle. Calls TryBrewNodeKettleTea and does not write the armed slot.
	 * After the first sleep, a later bite serves through the station timers instead.
	 */
	bool TryOpeningKettleBrew(AHomeWorldCharacter* Character);

	/** True until a post-tutorial serve writes the slot. */
	bool IsArmedBuffSlotEmpty() const { return !bArmedBuffOccupied; }

private:
	float HomeClockSeconds = 0.f;
	bool bArmedBuffOccupied = false;
};
