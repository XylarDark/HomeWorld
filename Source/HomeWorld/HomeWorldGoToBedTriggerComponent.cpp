// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGoToBedTriggerComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "GameFramework/Pawn.h"
#include "Engine/World.h"

UHomeWorldGoToBedTriggerComponent::UHomeWorldGoToBedTriggerComponent()
{
	SetBoxExtent(FVector(80.0f, 80.0f, 50.0f));
	SetCollisionProfileName(FName("OverlapAllDynamic"));
	SetGenerateOverlapEvents(true);
}

void UHomeWorldGoToBedTriggerComponent::BeginPlay()
{
	Super::BeginPlay();

	OnComponentBeginOverlap.AddDynamic(this, &UHomeWorldGoToBedTriggerComponent::OnOverlapBegin);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: GoToBedTrigger '%s' ready (overlap = go to bed)"), *GetName());
}

void UHomeWorldGoToBedTriggerComponent::OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor) return;

	APawn* Pawn = Cast<APawn>(OtherActor);
	if (!Pawn) return;

	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GoToBedTrigger — TimeOfDay subsystem not found."));
		return;
	}

	// List 56 T3: At night, overlap = wake (AdvanceToDawn); otherwise go to bed (SetPhase(Night)).
	if (TimeOfDay->GetIsNight())
	{
		TimeOfDay->AdvanceToDawn();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wake (overlap at bed) — phase set to Dawn. MVP List 56 T3."));
	}
	else
	{
		TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Go to bed (overlap) — phase set to Night. MVP List 8 / List 56."));
	}
}
