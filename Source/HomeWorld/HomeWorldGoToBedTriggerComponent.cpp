// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGoToBedTriggerComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "GameFramework/Pawn.h"
#include "Engine/World.h"

UHomeWorldGoToBedTriggerComponent::UHomeWorldGoToBedTriggerComponent(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void UHomeWorldGoToBedTriggerComponent::PostInitProperties()
{
	Super::PostInitProperties();
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
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GoToBedTrigger -- TimeOfDay subsystem not found."));
		return;
	}

	// Night or dusk, still body: sleep grants spirit. Already spirit: wake to dawn.
	// Day: advance the clock to night and stay FORM_BODY.
	AHomeWorldCharacter* HWChar = Cast<AHomeWorldCharacter>(Pawn);
	if (TimeOfDay->GetIsSpiritPhase())
	{
		if (HWChar && !HWChar->GetIsSpiritForm())
		{
			HWChar->TryBedSleepSpirit();
		}
		else
		{
			TimeOfDay->AdvanceToDawn();
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wake (overlap at bed) -- phase set to Dawn. MVP List 56 T3."));
		}
	}
	else
	{
		TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		UE_LOG(LogTemp, Log,
			TEXT("NODE_BED: day bed stays FORM_BODY (overlap; clock to Night; spirit is the night bed; rune latch stays locked)"));
	}

}
