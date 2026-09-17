// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Components/SphereComponent.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

namespace
{
	const TCHAR* BeastStateLabel(EHomeWorldBeastTameState State)
	{
		switch (State)
		{
		case EHomeWorldBeastTameState::Wild: return TEXT("wild");
		case EHomeWorldBeastTameState::Cautious: return TEXT("cautious");
		case EHomeWorldBeastTameState::Tamed: return TEXT("tamed");
		case EHomeWorldBeastTameState::Helper: return TEXT("helper");
		default: return TEXT("unknown");
		}
	}
}

UHomeWorldBeastTameComponent::UHomeWorldBeastTameComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UHomeWorldBeastTameComponent::BeginPlay()
{
	Super::BeginPlay();

	AActor* Owner = GetOwner();
	if (!Owner)
	{
		return;
	}

	if (!ProximitySphere)
	{
		ProximitySphere = NewObject<USphereComponent>(Owner, TEXT("BeastProximity"));
		if (ProximitySphere)
		{
			ProximitySphere->SetSphereRadius(ProximityRadiusCm);
			ProximitySphere->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
			ProximitySphere->SetCollisionProfileName(FName("OverlapAllDynamic"));
			ProximitySphere->SetupAttachment(Owner->GetRootComponent());
			ProximitySphere->RegisterComponent();
		}
	}

	Owner->Tags.AddUnique(FName(TEXT("BeastPad")));
	UE_LOG(LogTemp, Log, TEXT("TAME: component ready on '%s' state=wild"), *Owner->GetName());
}

void UHomeWorldBeastTameComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}

	AHomeWorldCharacter* NearbyPlayer = nullptr;
	if (APlayerController* PC = World->GetFirstPlayerController())
	{
		NearbyPlayer = Cast<AHomeWorldCharacter>(PC->GetPawn());
	}

	UpdateProximity(NearbyPlayer);

	if (bBondInProgress && bOfferAccepted && TameState == EHomeWorldBeastTameState::Cautious)
	{
		const float Dist = NearbyPlayer && GetOwner()
			? FVector::Dist(NearbyPlayer->GetActorLocation(), GetOwner()->GetActorLocation())
			: ProximityRadiusCm + 1.f;

		if (Dist <= ProximityRadiusCm * 1.25f)
		{
			BondElapsed += DeltaTime;
			if (BondElapsed >= BondWaitSeconds)
			{
				SetTameState(EHomeWorldBeastTameState::Tamed);
				bBondInProgress = false;
				bOfferAccepted = false;
				UE_LOG(LogTemp, Log, TEXT("TAME: bond complete -> tamed"));
			}
		}
		else
		{
			UE_LOG(LogTemp, Log, TEXT("TAME: left calm radius during bond -> cautious (offer retained)"));
			bBondInProgress = false;
			BondElapsed = 0.f;
		}
	}
}

void UHomeWorldBeastTameComponent::SetTameState(EHomeWorldBeastTameState NewState)
{
	if (TameState == NewState)
	{
		return;
	}
	const EHomeWorldBeastTameState Old = TameState;
	TameState = NewState;
	UE_LOG(LogTemp, Log, TEXT("TAME: %s -> %s on '%s'"),
		BeastStateLabel(Old), BeastStateLabel(NewState),
		GetOwner() ? *GetOwner()->GetName() : TEXT("(none)"));
}

void UHomeWorldBeastTameComponent::UpdateProximity(AHomeWorldCharacter* NearbyPlayer)
{
	if (!NearbyPlayer || !GetOwner() || TameState == EHomeWorldBeastTameState::Tamed
		|| TameState == EHomeWorldBeastTameState::Helper)
	{
		return;
	}

	const float Dist = FVector::Dist(NearbyPlayer->GetActorLocation(), GetOwner()->GetActorLocation());
	if (Dist <= ProximityRadiusCm && TameState == EHomeWorldBeastTameState::Wild)
	{
		SetTameState(EHomeWorldBeastTameState::Cautious);
	}
}

bool UHomeWorldBeastTameComponent::IsDayBodyInteractionAllowed(AHomeWorldCharacter* Character) const
{
	if (!Character || Character->GetIsSpiritForm())
	{
		return false;
	}
	if (UWorld* World = GetWorld())
	{
		if (UHomeWorldTimeOfDaySubsystem* TOD = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (TOD->GetIsNight())
			{
				return false;
			}
		}
	}
	return true;
}

void UHomeWorldBeastTameComponent::ResetBondProgress()
{
	bOfferAccepted = false;
	bBondInProgress = false;
	BondElapsed = 0.f;
}

bool UHomeWorldBeastTameComponent::TryOfferFood(AHomeWorldCharacter* Character)
{
	if (!Character || !GetOwner())
	{
		return false;
	}

	if (!IsDayBodyInteractionAllowed(Character))
	{
		UE_LOG(LogTemp, Log, TEXT("TAME: offer blocked — night or spirit form"));
		return false;
	}

	if (TameState == EHomeWorldBeastTameState::Tamed || TameState == EHomeWorldBeastTameState::Helper)
	{
		UE_LOG(LogTemp, Log, TEXT("TAME: offer skipped — already tamed/helper"));
		return false;
	}

	if (TameState == EHomeWorldBeastTameState::Wild)
	{
		SetTameState(EHomeWorldBeastTameState::Cautious);
	}

	UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
	UHomeWorldInventorySubsystem* Inv = GI ? GI->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!Inv)
	{
		return false;
	}

	if (!Inv->HasTameFood(1))
	{
		UE_LOG(LogTemp, Log, TEXT("TAME: soft reject — no RES_BERRY or RES_HERB"));
		return false;
	}

	const FName Spent = Inv->SpendTameFood();
	if (Spent.IsNone())
	{
		UE_LOG(LogTemp, Log, TEXT("TAME: soft reject — spend failed"));
		return false;
	}

	bOfferAccepted = true;
	bBondInProgress = true;
	BondElapsed = 0.f;
	BondPlayer = Character;
	UE_LOG(LogTemp, Log, TEXT("TAME: offer accepted (%s consumed) — bond wait %.1fs"),
		*Spent.ToString(), BondWaitSeconds);
	return true;
}

bool UHomeWorldBeastTameComponent::TryPromoteToHelper(AHomeWorldCharacter* Character)
{
	if (!Character || TameState != EHomeWorldBeastTameState::Tamed)
	{
		return false;
	}
	if (!IsDayBodyInteractionAllowed(Character))
	{
		return false;
	}
	SetTameState(EHomeWorldBeastTameState::Helper);
	return true;
}
