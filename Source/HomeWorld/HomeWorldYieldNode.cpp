// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldYieldNode.h"
#include "HomeWorldInventorySubsystem.h"
#include "Components/BoxComponent.h"
#include "TimerManager.h"
#include "Engine/World.h"
#include "Engine/Engine.h"

	AHomeWorldYieldNode::AHomeWorldYieldNode()
{
	PrimaryActorTick.bCanEverTick = false;

	OverlapVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("OverlapVolume"));
	OverlapVolume->SetBoxExtent(FVector(80.0f, 80.0f, 80.0f));
	OverlapVolume->SetCollisionProfileName(FName("OverlapAllDynamic"));
	RootComponent = OverlapVolume;
}

void AHomeWorldYieldNode::SetAssignedSpirit(FName SpiritId)
{
	AssignedSpiritId = SpiritId;
	bIsProducing = !SpiritId.IsNone();
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: YieldNode '%s' assigned spirit '%s', producing=%d"), *GetName(), *SpiritId.ToString(), bIsProducing);
}

void AHomeWorldYieldNode::ClearAssignment()
{
	AssignedSpiritId = FName();
	bIsProducing = false;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: YieldNode '%s' assignment cleared"), *GetName());
}

void AHomeWorldYieldNode::BeginPlay()
{
	Super::BeginPlay();

	// Timer runs always; ProduceYield() gates on bIsProducing so assignment (Day 22) can toggle production at runtime
	if (YieldIntervalSeconds > 0.0f && YieldRate > 0 && ResourceType.IsNone() == false)
	{
		GetWorld()->GetTimerManager().SetTimer(
			YieldTimerHandle,
			this,
			&AHomeWorldYieldNode::ProduceYield,
			YieldIntervalSeconds,
			true,
			YieldIntervalSeconds
		);
		UE_LOG(LogTemp, Verbose, TEXT("HomeWorld: YieldNode '%s' yield timer started (producing=%d)"), *GetName(), bIsProducing);
	}
}

void AHomeWorldYieldNode::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	if (YieldTimerHandle.IsValid())
	{
		if (UWorld* World = GetWorld())
		{
			World->GetTimerManager().ClearTimer(YieldTimerHandle);
		}
	}
	Super::EndPlay(EndPlayReason);
}

void AHomeWorldYieldNode::ProduceYield()
{
	if (!bIsProducing || YieldRate <= 0 || ResourceType.IsNone()) return;

	UWorld* World = GetWorld();
	if (!World) return;

	UGameInstance* GI = World->GetGameInstance();
	if (!GI) return;

	UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
	if (!Inv) return;

	Inv->AddResource(ResourceType, YieldRate);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: YieldNode '%s' produced %s +%d"), *GetName(), *ResourceType.ToString(), YieldRate);
}
