// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritualArtefact.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/BoxComponent.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

AHomeWorldSpiritualArtefact::AHomeWorldSpiritualArtefact()
{
	PrimaryActorTick.bCanEverTick = false;

	CollectVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("CollectVolume"));
	CollectVolume->SetBoxExtent(FVector(80.0f, 80.0f, 80.0f));
	CollectVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	CollectVolume->SetGenerateOverlapEvents(true);
	RootComponent = CollectVolume;
}

void AHomeWorldSpiritualArtefact::BeginPlay()
{
	Super::BeginPlay();

	if (CollectVolume)
	{
		CollectVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldSpiritualArtefact::OnCollectVolumeOverlap);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritualArtefact '%s' ready (collect at night via overlap)"), *GetName());
	}
}

void AHomeWorldSpiritualArtefact::OnCollectVolumeOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor) return;

	APawn* Pawn = Cast<APawn>(OtherActor);
	if (!Pawn) return;

	APlayerController* PC = Cast<APlayerController>(Pawn->GetController());
	if (!PC) return;

	AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
	if (!PS) return;

	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritualArtefact — TimeOfDay subsystem not found."));
		return;
	}

	if (!TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual artefact only available at night (set hw.TimeOfDay.Phase 2)."));
		return;
	}

	PS->AddSpiritualArtefact(1);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Collected spiritual artefact (night). Power: %d, Artefacts: %d"),
		PS->GetSpiritualPowerCollected(), PS->GetSpiritualArtefactsCollected());
}
