// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "HomeWorldOpeningWalker.generated.h"

/** Partner and child on the opening pad. They use the player movement component: orient to velocity. */
UCLASS()
class HOMEWORLD_API AHomeWorldOpeningWalker : public ACharacter
{
	GENERATED_BODY()

public:
	AHomeWorldOpeningWalker();

	/** Mesh and tags from the placed skeletal actor. Call before FinishSpawningActor. */
	void CopyAppearance(AActor* Source);

	void SetMoveSpeed(float CentimetersPerSecond);

	/** True when within AcceptCm. Otherwise feeds the movement component toward Goal. */
	bool WalkToward(const FVector& Goal, float AcceptCm);

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;

	bool bWalkPlaying = false;
};
