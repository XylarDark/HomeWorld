// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/BoxComponent.h"
#include "HomeWorldMealTypes.h"
#include "HomeWorldMealTriggerComponent.generated.h"

/**
 * Optional trigger volume for in-world meal (breakfast/lunch/dinner) on overlap.
 * Add to BP_MealTrigger_Breakfast or any actor. When the player overlaps, calls
 * ConsumeMealRestore(MealType) on the character. Day-only effect (ConsumeMealRestore no-ops at night).
 * List 57 (in-world meal triggers).
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldMealTriggerComponent : public UBoxComponent
{
	GENERATED_BODY()

public:
	UHomeWorldMealTriggerComponent();

	/** Which meal this trigger fires (Breakfast, Lunch, Dinner). Set per Blueprint instance. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Meal")
	EMealType MealType = EMealType::Breakfast;

	virtual void BeginPlay() override;

protected:
	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);
};
