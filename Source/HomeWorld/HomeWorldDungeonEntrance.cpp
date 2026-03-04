// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldDungeonEntrance.h"
#include "Components/BoxComponent.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Pawn.h"
#include "Engine/World.h"

AHomeWorldDungeonEntrance::AHomeWorldDungeonEntrance()
{
	PrimaryActorTick.bCanEverTick = false;

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	TriggerVolume->SetBoxExtent(FVector(100.0f, 100.0f, 100.0f));
	TriggerVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	TriggerVolume->SetGenerateOverlapEvents(true);
	RootComponent = TriggerVolume;
}

void AHomeWorldDungeonEntrance::BeginPlay()
{
	Super::BeginPlay();

	if (TriggerVolume && LevelToOpen.IsNone() == false)
	{
		TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldDungeonEntrance::OnTriggerBeginOverlap);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: DungeonEntrance '%s' will open level '%s' on overlap"), *GetName(), *LevelToOpen.ToString());
	}
	else if (LevelToOpen.IsNone())
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: DungeonEntrance '%s' has no LevelToOpen set"), *GetName());
	}
}

void AHomeWorldDungeonEntrance::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor || LevelToOpen.IsNone())
	{
		return;
	}

	APawn* Pawn = Cast<APawn>(OtherActor);
	if (!Pawn)
	{
		return;
	}

	if (RequiredPawnTag.IsNone() == false)
	{
		if (!OtherActor->ActorHasTag(RequiredPawnTag))
		{
			return;
		}
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: DungeonEntrance opening level '%s' (overlap by %s)"), *LevelToOpen.ToString(), *OtherActor->GetName());
	UGameplayStatics::OpenLevel(this, LevelToOpen);
}
