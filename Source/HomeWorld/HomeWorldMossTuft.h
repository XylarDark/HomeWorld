// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldMossTuft.generated.h"

/** Greybox green tuft. A Grace wisp gathers it from a tree or a rock. */
UCLASS()
class HOMEWORLD_API AHomeWorldMossTuft : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldMossTuft();

	void SetSource(FName NewSource);
	bool IsForestSource() const;
	void MarkGathered();
	bool WasGathered() const { return bGathered; }

private:
	FName Source = TEXT("tree");
	bool bGathered = false;
};
