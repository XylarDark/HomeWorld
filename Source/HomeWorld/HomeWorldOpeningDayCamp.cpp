// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningDayCamp.h"

#include "Components/SphereComponent.h"
#include "HomeWorldCharacter.h"

AHomeWorldOpeningDayCamp::AHomeWorldOpeningDayCamp()
{
	PrimaryActorTick.bCanEverTick = false;

	ArrivalSphere = CreateDefaultSubobject<USphereComponent>(TEXT("ArrivalSphere"));
	RootComponent = ArrivalSphere;
	ArrivalSphere->SetSphereRadius(ArrivalRadiusCm);
	ArrivalSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	ArrivalSphere->SetCollisionResponseToAllChannels(ECR_Ignore);
	ArrivalSphere->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	ArrivalSphere->SetGenerateOverlapEvents(true);

	Tags.Add(FName(TEXT("NODE_DAY_CAMP")));
	Tags.Add(FName(TEXT("NODE_OPENING_DAY_CAMP")));
	Tags.Add(FName(TEXT("DayCamp")));
}

void AHomeWorldOpeningDayCamp::BeginPlay()
{
	Super::BeginPlay();
	ArrivalSphere->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldOpeningDayCamp::OnArrivalBegin);
}

bool AHomeWorldOpeningDayCamp::TryArrive(AHomeWorldCharacter* Character)
{
	if (!Character)
	{
		return false;
	}
	if (FVector::Dist2D(GetActorLocation(), Character->GetActorLocation()) > ArrivalRadiusCm)
	{
		return false;
	}
	return Character->TryEjectNodeDayCamp();
}

void AHomeWorldOpeningDayCamp::OnArrivalBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	TryArrive(Cast<AHomeWorldCharacter>(OtherActor));
}
