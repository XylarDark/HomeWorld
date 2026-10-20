// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AIController.h"

class AHomeWorldOpeningWalker;
class APawn;

#include "HomeWorldAIController.generated.h"

/**
 * Base AI controller for family/NPCs (Week 2+).
 * The party leash lives here and does not possess the walker. No Behavior Tree and no State Tree.
 * Docs/41_COMPANION_PARTY_DESIGN.md.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldAIController : public AAIController
{
	GENERATED_BODY()

public:
	AHomeWorldAIController(const FObjectInitializer& ObjectInitializer);

	/** Opening follow gap. One body-length behind the player. */
	static constexpr float FollowGapCm = 160.f;

	/** Point one body-length behind the player. */
	static FVector FollowGoal(const APawn* Player);

	/**
	 * Walk an unpossessed opening walker onto the follow goal when that person is out,
	 * the rescue is done, and it is day in the body. Does not possess and does not draw a stroke.
	 * Pass Player to aim at that pawn; null uses the world's first player pawn.
	 */
	static void DriveUnpossessedFollow(AHomeWorldOpeningWalker* Walker, APawn* Player = nullptr);
};
