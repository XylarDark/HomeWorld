// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "HomeWorldVirtueTypes.h"
#include "HomeWorldVirtueSpawnTable.generated.h"

/** Two spawn rows. Chances are the odds of the 1st through 7th pole. Docs/VIRTUE_ATTRIBUTE_BIBLE.md. */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldVirtueSpawnTable : public UDataAsset
{
	GENERATED_BODY()

public:
	UHomeWorldVirtueSpawnTable();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Virtue")
	TArray<float> CharacterChances;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Virtue")
	TArray<float> CollectibleChances;

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool AreChancesNonIncreasing() const;
};
