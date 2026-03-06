// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritualCollectible.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/BoxComponent.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

AHomeWorldSpiritualCollectible::AHomeWorldSpiritualCollectible()
{
	PrimaryActorTick.bCanEverTick = false;

	CollectVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("CollectVolume"));
	CollectVolume->SetBoxExtent(FVector(80.0f, 80.0f, 80.0f));
	CollectVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	CollectVolume->SetGenerateOverlapEvents(true);
	RootComponent = CollectVolume;
}

void AHomeWorldSpiritualCollectible::BeginPlay()
{
	Super::BeginPlay();

	if (CollectVolume)
	{
		CollectVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldSpiritualCollectible::OnCollectVolumeOverlap);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritualCollectible '%s' ready (collect at night via overlap)"), *GetName());
	}
}

void AHomeWorldSpiritualCollectible::OnCollectVolumeOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
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
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritualCollectible — TimeOfDay subsystem not found."));
		return;
	}

	if (!TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual collectible only available at night (set hw.TimeOfDay.Phase 2)."));
		return;
	}

	// Day buff and love level at night: bonus spiritual power per collectible (DAY_RESTORATION_LOOP, DAY_LOVE_OR_BOND).
	constexpr int32 BasePower = 1;
	const int32 BonusFromDayBuff = PS->GetHasDayRestorationBuff() ? 1 : 0;
	const int32 LoveBonus = FMath::Min(PS->GetLoveLevel(), 5); // Placeholder cap; love scales night bonus (stub).
	const int32 TotalPower = BasePower + BonusFromDayBuff + LoveBonus;

	PS->AddSpiritualPower(TotalPower);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Collected spiritual power (night). Base %d%s%s -> total %d. Power: %d, Artefacts: %d"),
		BasePower,
		BonusFromDayBuff > 0 ? TEXT(" + day buff") : TEXT(""),
		LoveBonus > 0 ? *FString::Printf(TEXT(" + love %d"), LoveBonus) : TEXT(""),
		TotalPower, PS->GetSpiritualPowerCollected(), PS->GetSpiritualArtefactsCollected());
}
