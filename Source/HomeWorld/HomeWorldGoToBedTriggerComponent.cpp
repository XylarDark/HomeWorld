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

	// List 56 T3: At night, overlap = wake (AdvanceToDawn); otherwise go to bed.
	// T0 #11: go-to-bed grants sleep gate; spirit only with NODE_RUNE via CanEnterSpiritForm.
	if (TimeOfDay->GetIsNight())
	{
		TimeOfDay->AdvanceToDawn();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wake (overlap at bed) -- phase set to Dawn. MVP List 56 T3."));
	}
	else if (AHomeWorldCharacter* HWChar = Cast<AHomeWorldCharacter>(Pawn))
	{
		if (HWChar->IsRuneGateUnlocked())
		{
			HWChar->TryBedSleepSpirit();
		}
		else
		{
			TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
			HWChar->GrantSpiritSleepGate();
			UE_LOG(LogTemp, Log,
				TEXT("NODE_BED: sleep gate Night FORM_BODY (overlap; need NODE_RUNE for FORM_SPIRIT TOD_NIGHT_SPIRIT CAM_T0_BED; not phase-alone spirit; #9 w/o bed stay FORM_BODY)"));
		}
	}
	else
	{
		TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Go to bed (overlap) -- phase set to Night (no AHomeWorldCharacter; sleep gate not granted)."));
	}

}
