// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBossPlaceholderVolume.h"
#include "HomeWorldBossSealComponent.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/BoxComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "HomeWorldGameMode.h"

AHomeWorldBossPlaceholderVolume::AHomeWorldBossPlaceholderVolume()
{
	PrimaryActorTick.bCanEverTick = false;

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	SetRootComponent(TriggerVolume);
	TriggerVolume->SetBoxExtent(FVector(400.f, 400.f, 200.f));
	TriggerVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	TriggerVolume->SetCollisionResponseToAllChannels(ECR_Ignore);
	TriggerVolume->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	TriggerVolume->SetGenerateOverlapEvents(true);

	SealComponent = CreateDefaultSubobject<UHomeWorldBossSealComponent>(TEXT("BossSeal"));

	Tags.AddUnique(FName(TEXT("BossPlaceholder")));
	Tags.AddUnique(FName(TEXT("CD_PlanetOnly")));
}

void AHomeWorldBossPlaceholderVolume::BeginPlay()
{
	Super::BeginPlay();
	TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldBossPlaceholderVolume::OnTriggerBeginOverlap);
	TriggerVolume->OnComponentEndOverlap.AddDynamic(this, &AHomeWorldBossPlaceholderVolume::OnTriggerEndOverlap);
}

void AHomeWorldBossPlaceholderVolume::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor || !GetWorld() || bLoggedThisOverlap)
	{
		return;
	}

	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor != PlayerPawn)
	{
		return;
	}

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = GetWorld()->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	const bool bNight = TimeOfDay && TimeOfDay->GetIsNight();

	AHomeWorldPlayerState* PS = PC ? PC->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
	if (PS)
	{
		PS->SetBossPhaseFlags(!bNight, bNight);
	}

	if (bNight)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("BOSS:PHASE_NIGHT"));
	}
	else
	{
		UE_LOG(LogHomeWorld, Log, TEXT("BOSS:PHASE_DAY"));
	}
	bLoggedThisOverlap = true;
}

void AHomeWorldBossPlaceholderVolume::OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if (!OtherActor || !GetWorld())
	{
		return;
	}

	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor != PlayerPawn)
	{
		return;
	}

	bLoggedThisOverlap = false;

	if (AHomeWorldPlayerState* PS = PC ? PC->GetPlayerState<AHomeWorldPlayerState>() : nullptr)
	{
		PS->ClearBossPhaseFlags();
	}
}
