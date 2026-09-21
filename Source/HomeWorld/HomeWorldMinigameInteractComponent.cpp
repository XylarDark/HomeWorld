// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldMinigameInteractComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "GameFramework/Actor.h"

UHomeWorldMinigameInteractComponent::UHomeWorldMinigameInteractComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UHomeWorldMinigameInteractComponent::BeginPlay()
{
	Super::BeginPlay();
	if (AActor* Owner = GetOwner())
	{
		Owner->Tags.AddUnique(FName(TEXT("MinigameStub")));
		Owner->Tags.AddUnique(FName(TEXT("CD_PlanetOnly")));
	}
}

bool UHomeWorldMinigameInteractComponent::TryMinigameInteract(AHomeWorldCharacter* Character)
{
	if (!Character || !GetOwner())
	{
		return false;
	}

	if (GetOwner()->ActorHasTag(FName(TEXT("Homestead"))))
	{
		UE_LOG(LogHomeWorld, Log, TEXT("MINIGAME: blocked — homestead never combat"));
		return false;
	}

	if (bUsedThisSession)
	{
		UE_LOG(LogHomeWorld, Verbose, TEXT("%s already used on '%s'"),
			HomeWorldCombatDream::GetMinigameLogTag(MinigameKind),
			*GetOwner()->GetName());
		return false;
	}

	const TCHAR* Tag = HomeWorldCombatDream::GetMinigameLogTag(MinigameKind);
	UE_LOG(LogHomeWorld, Log, TEXT("%s"), Tag);
	bUsedThisSession = true;

	if (HomeWorldCombatDream::IsPolishFirstMinigame(MinigameKind))
	{
		UE_LOG(LogHomeWorld, Log, TEXT("MOVEMENT:POSSESS stub — dream-object hook (Docs/21 bridge)"));
	}

	return true;
}
