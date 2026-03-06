// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldNightEncounterPlaceholder.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SphereComponent.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"

AHomeWorldNightEncounterPlaceholder::AHomeWorldNightEncounterPlaceholder()
{
	PrimaryActorTick.bCanEverTick = false;

	OverlapSphere = CreateDefaultSubobject<USphereComponent>(TEXT("OverlapSphere"));
	RootComponent = OverlapSphere;
	OverlapSphere->SetSphereRadius(80.f);
	OverlapSphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	OverlapSphere->SetCollisionResponseToAllChannels(ECR_Overlap);

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
	MeshComponent->SetupAttachment(RootComponent);
	MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void AHomeWorldNightEncounterPlaceholder::BeginPlay()
{
	Super::BeginPlay();
	OverlapSphere->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldNightEncounterPlaceholder::OnOverlapBegin);
}

void AHomeWorldNightEncounterPlaceholder::OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor || !GetWorld()) return;

	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor != PlayerPawn) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = GetWorld()->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsNight()) return;

	AHomeWorldGameMode* HWGM = GetWorld()->GetAuthGameMode<AHomeWorldGameMode>();
	if (HWGM)
	{
		HWGM->ReportFoeConverted(this);
	}
	Destroy();
}
