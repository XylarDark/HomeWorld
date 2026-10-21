// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldAIController.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldOpeningWalker.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

namespace
{
	const FName PartyLeashTag(TEXT("PartyLeash"));
}

AHomeWorldAIController::AHomeWorldAIController(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

FVector AHomeWorldAIController::FollowGoal(const APawn* Player)
{
	if (!Player)
	{
		return FVector::ZeroVector;
	}
	return Player->GetActorLocation() - Player->GetActorForwardVector() * FollowGapCm;
}

void AHomeWorldAIController::DriveUnpossessedFollow(AHomeWorldOpeningWalker* Walker, APawn* Player)
{
	if (!Walker)
	{
		return;
	}
	UWorld* World = Walker->GetWorld();
	UGameInstance* GameInstance = World ? World->GetGameInstance() : nullptr;
	UHomeWorldFamilySubsystem* Family = GameInstance ? GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>() : nullptr;
	UCapsuleComponent* Capsule = Walker->GetCapsuleComponent();
	const bool bOut = Family && Family->IsRescueComplete() && Family->IsActorOut(Walker);
	bool bDayBody = bOut;
	if (bDayBody && World)
	{
		if (const UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			const EHomeWorldTimeOfDayPhase Phase = TimeOfDay->GetCurrentPhase();
			bDayBody = Phase != EHomeWorldTimeOfDayPhase::Night && Phase != EHomeWorldTimeOfDayPhase::Dusk;
		}
	}
	APawn* FollowTarget = Player;
	if (!FollowTarget && World)
	{
		if (APlayerController* Controller = World->GetFirstPlayerController())
		{
			FollowTarget = Controller->GetPawn();
		}
	}
	if (bDayBody)
	{
		if (const AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(FollowTarget))
		{
			bDayBody = !Character->GetIsSpiritForm();
		}
	}
	if (!bDayBody || !FollowTarget || FollowTarget == Walker)
	{
		if (Capsule && Walker->ActorHasTag(PartyLeashTag))
		{
			Walker->Tags.Remove(PartyLeashTag);
			Capsule->SetCollisionResponseToChannel(ECC_Pawn, ECR_Block);
		}
		return;
	}
	if (Capsule)
	{
		Walker->Tags.AddUnique(PartyLeashTag);
		Capsule->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	}
	Walker->WalkToward(FollowGoal(FollowTarget), 80.f);
}
