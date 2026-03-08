// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMealTriggerComponent.h"
#include "HomeWorldCharacter.h"
#include "GameFramework/Pawn.h"

UHomeWorldMealTriggerComponent::UHomeWorldMealTriggerComponent()
{
	SetBoxExtent(FVector(80.0f, 80.0f, 50.0f));
	SetCollisionProfileName(FName("OverlapAllDynamic"));
	SetGenerateOverlapEvents(true);
}

void UHomeWorldMealTriggerComponent::BeginPlay()
{
	Super::BeginPlay();

	OnComponentBeginOverlap.AddDynamic(this, &UHomeWorldMealTriggerComponent::OnOverlapBegin);
	const TCHAR* MealName = MealType == EMealType::Breakfast ? TEXT("Breakfast") : (MealType == EMealType::Lunch ? TEXT("Lunch") : TEXT("Dinner"));
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: MealTrigger '%s' ready (overlap = %s). List 57."), *GetName(), MealName);
}

void UHomeWorldMealTriggerComponent::OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor) return;

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(OtherActor);
	if (!Character) return;

	const bool bOk = Character->ConsumeMealRestore(MealType);
	const TCHAR* MealName = MealType == EMealType::Breakfast ? TEXT("Breakfast") : (MealType == EMealType::Lunch ? TEXT("Lunch") : TEXT("Dinner"));
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: MealTrigger overlap %s — %s. MVP List 57."), MealName, bOk ? TEXT("consumed") : TEXT("skipped (e.g. night)"));
}
