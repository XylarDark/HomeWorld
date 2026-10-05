// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCloudWisp.h"

#include "Components/SphereComponent.h"
#include "HomeWorldCharacter.h"

AHomeWorldCloudWisp::AHomeWorldCloudWisp()
{
	PrimaryActorTick.bCanEverTick = false;
	Trigger = CreateDefaultSubobject<USphereComponent>(TEXT("Trigger"));
	SetRootComponent(Trigger);
	Trigger->InitSphereRadius(90.0f);
	Trigger->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Trigger->SetCollisionObjectType(ECC_WorldDynamic);
	Trigger->SetCollisionResponseToAllChannels(ECR_Ignore);
	Trigger->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	Trigger->SetGenerateOverlapEvents(true);
	Trigger->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldCloudWisp::OnTriggerBeginOverlap);
}

void AHomeWorldCloudWisp::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComponent, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(OtherActor);
	if (Character && Character->CollectCloudWisp(this))
	{
		UE_LOG(LogTemp, Log, TEXT("CLOUD_WISP: collected; carried=%d"), Character->GetCarriedCloudWisps());
		Destroy();
	}
}
