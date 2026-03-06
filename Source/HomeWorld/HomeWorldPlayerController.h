// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "HomeWorldPlayerController.generated.h"

class AHomeWorldHUD;

/**
 * Player controller that uses AHomeWorldHUD to show Physical and Spiritual counts (T5).
 */
UCLASS()
class HOMEWORLD_API AHomeWorldPlayerController : public APlayerController
{
	GENERATED_BODY()

public:
	AHomeWorldPlayerController();

	virtual void SpawnDefaultHUD() override;
};
