// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGcPlaceholderVolume.h"
#include "HomeWorldCraftSubsystem.h"
#include "Components/BoxComponent.h"
#include "Engine/GameInstance.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "HomeWorldGameMode.h"

bool AHomeWorldGcPlaceholderVolume::bKitchenRebindHintLogged = false;

AHomeWorldGcPlaceholderVolume::AHomeWorldGcPlaceholderVolume()
{
	PrimaryActorTick.bCanEverTick = false;

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	SetRootComponent(TriggerVolume);
	TriggerVolume->SetBoxExtent(FVector(120.f, 120.f, 100.f));
	TriggerVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	TriggerVolume->SetCollisionResponseToAllChannels(ECR_Ignore);
	TriggerVolume->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	TriggerVolume->SetGenerateOverlapEvents(true);

	Tags.AddUnique(FName(TEXT("GC_PlaceholderVolume")));
}

void AHomeWorldGcPlaceholderVolume::BeginPlay()
{
	Super::BeginPlay();
	TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldGcPlaceholderVolume::OnTriggerBeginOverlap);
	TriggerVolume->OnComponentEndOverlap.AddDynamic(this, &AHomeWorldGcPlaceholderVolume::OnTriggerEndOverlap);
}

void AHomeWorldGcPlaceholderVolume::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor || bLoggedThisOverlap)
	{
		return;
	}

	APlayerController* PC = GetWorld() ? GetWorld()->GetFirstPlayerController() : nullptr;
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor != PlayerPawn)
	{
		return;
	}

	if (HomeWorldGcPlaceholder::RequiresCottageUnlock(PlaceholderKind))
	{
		UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
		UHomeWorldCraftSubsystem* Craft = GI ? GI->GetSubsystem<UHomeWorldCraftSubsystem>() : nullptr;
		if (!Craft || !Craft->IsCottageUnlocked())
		{
			if (PlaceholderKind == EHomeWorldGcPlaceholderKind::CottageKitchen)
			{
				UE_LOG(LogHomeWorld, Log, TEXT("PLACEHOLDER:COTTAGE_KITCHEN locked"));
				bLoggedThisOverlap = true;
			}
			return;
		}

		if (PlaceholderKind == EHomeWorldGcPlaceholderKind::CottageKitchen && !bKitchenRebindHintLogged)
		{
			UE_LOG(LogHomeWorld, Log, TEXT("CRAFT: kitchen rebind TODO"));
			bKitchenRebindHintLogged = true;
		}
	}

	const TCHAR* Line = HomeWorldGcPlaceholder::GetEnterLogLine(PlaceholderKind);
	UE_LOG(LogHomeWorld, Log, TEXT("%s"), Line);
	bLoggedThisOverlap = true;
}

void AHomeWorldGcPlaceholderVolume::OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if (!OtherActor || !GetWorld())
	{
		return;
	}

	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor == PlayerPawn)
	{
		bLoggedThisOverlap = false;
	}
}
