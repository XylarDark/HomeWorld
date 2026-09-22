// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritLitVolume.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldSpiritStealthComponent.h"
#include "Components/BoxComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"

AHomeWorldSpiritLitVolume::AHomeWorldSpiritLitVolume()
{
	PrimaryActorTick.bCanEverTick = false;

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	SetRootComponent(TriggerVolume);
	TriggerVolume->SetBoxExtent(FVector(180.f, 180.f, 120.f));
	TriggerVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	TriggerVolume->SetCollisionResponseToAllChannels(ECR_Ignore);
	TriggerVolume->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	TriggerVolume->SetGenerateOverlapEvents(true);

	Tags.AddUnique(FName(TEXT("SS_LitVolume")));
	Tags.AddUnique(FName(TEXT("SS_PlanetOnly")));
}

void AHomeWorldSpiritLitVolume::BeginPlay()
{
	Super::BeginPlay();
	TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldSpiritLitVolume::OnTriggerBeginOverlap);
	TriggerVolume->OnComponentEndOverlap.AddDynamic(this, &AHomeWorldSpiritLitVolume::OnTriggerEndOverlap);
}

void AHomeWorldSpiritLitVolume::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
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

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(OtherActor);
	if (!Character)
	{
		return;
	}

	if (!HomeWorldSpiritStealth::RevealsSpiritInVolume(LitSourceKind))
	{
		// Body mundane torch: no spirit reveal; body darkness kidnap stays on DAYNIGHT owner.
		return;
	}

	if (!Character->GetIsSpiritForm())
	{
		return;
	}

	if (UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>())
	{
		Stealth->NotifyLitVolumeEntered(LitSourceKind, this);
	}
}

void AHomeWorldSpiritLitVolume::OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
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

	if (!HomeWorldSpiritStealth::RevealsSpiritInVolume(LitSourceKind))
	{
		return;
	}

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(OtherActor);
	if (!Character || !Character->GetIsSpiritForm())
	{
		return;
	}

	if (UHomeWorldSpiritStealthComponent* Stealth = Character->FindComponentByClass<UHomeWorldSpiritStealthComponent>())
	{
		Stealth->NotifyLitVolumeExited(this);
	}
}
