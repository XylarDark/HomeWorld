// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBossSealComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "GameFramework/Actor.h"

UHomeWorldBossSealComponent::UHomeWorldBossSealComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UHomeWorldBossSealComponent::BeginPlay()
{
	Super::BeginPlay();
	if (AActor* Owner = GetOwner())
	{
		Owner->Tags.AddUnique(FName(TEXT("BossSealStub")));
	}
}

bool UHomeWorldBossSealComponent::TrySealStub(AHomeWorldCharacter* Character)
{
	if (!Character || bSealUsed)
	{
		return false;
	}
	UE_LOG(LogHomeWorld, Log, TEXT("BOSS:SEAL"));
	bSealUsed = true;
	return true;
}
