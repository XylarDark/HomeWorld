// Copyright HomeWorld. All Rights Reserved.

// Own header first (Source/HomeWorld/AGENTS.md).
#include "HomeWorldBeastEncounterComponent.h"

#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "Kismet/GameplayStatics.h"

UHomeWorldBeastEncounterComponent::UHomeWorldBeastEncounterComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

EHomeWorldBeastEncounterOutcome UHomeWorldBeastEncounterComponent::AdvanceThreat(const FHomeWorldBeastEncounterFrame& Frame)
{
	const float Dt = FMath::Max(Frame.DeltaSeconds, 0.f);

	// Tamed/Helper beasts never charge -- the rideable/pet half of the route.
	if (Frame.bBeastTamed)
	{
		Threat = 0.f;
		return EHomeWorldBeastEncounterOutcome::Idle;
	}

	// Outside the beast's area the meter always bleeds off: the boot only exists
	// "without leaving its area" (route, Lead 2026-10-07).
	if (Frame.DistanceCm > AggroRadiusCm)
	{
		const float Before = Threat;
		Threat = FMath::Max(0.f, Threat - ThreatDecayPerSecond * Dt);
		return (Threat < Before || Threat > 0.f)
			? EHomeWorldBeastEncounterOutcome::ThreatDecaying
			: EHomeWorldBeastEncounterOutcome::Idle;
	}

	// Standing still, no offering: it watches and the meter bleeds off.
	// (Route: sudden movement builds threat; standing still is the calm state.)
	const bool bStill = Frame.PlayerSpeedCm <= StillSpeedCm;

	// "If you get too close" without an offering: instant charge-and-boot,
	// regardless of speed. Meter resets so the charge cannot fire per-tick.
	if (Frame.DistanceCm <= TooCloseRadiusCm && !Frame.bCarriesOfferFood)
	{
		Threat = 0.f;
		return EHomeWorldBeastEncounterOutcome::BootCharged;
	}

	// Standing still with an offering: the tame window. The beast approaches,
	// eats, and is tamed (the actual offer/bond stays on the V4 tame flow).
	if (bStill && Frame.bCarriesOfferFood)
	{
		Threat = FMath::Max(0.f, Threat - ThreatDecayPerSecond * Dt);
		return EHomeWorldBeastEncounterOutcome::TameWindow;
	}

	if (bStill)
	{
		const float Before = Threat;
		Threat = FMath::Max(0.f, Threat - ThreatDecayPerSecond * Dt);
		return (Threat < Before || Threat > 0.f)
			? EHomeWorldBeastEncounterOutcome::ThreatDecaying
			: EHomeWorldBeastEncounterOutcome::Idle;
	}

	// Sudden movement inside the area fills the meter.
	Threat = FMath::Min(1.f, Threat + ThreatFillPerSecond * Dt);
	if (Threat >= 1.f)
	{
		// Carrying an offering suppresses the boot (route: "walking toward it
		// carrying an herb suppresses the boot"). The meter holds full, so
		// dropping the offering charges on the next moving frame.
		if (Frame.bCarriesOfferFood)
		{
			return EHomeWorldBeastEncounterOutcome::OfferSuppressedBoot;
		}
		Threat = 0.f;
		return EHomeWorldBeastEncounterOutcome::BootCharged;
	}
	return EHomeWorldBeastEncounterOutcome::ThreatRising;
}

float UHomeWorldBeastEncounterComponent::TurnAuthorityForSpeed(float SpeedCm, float MaxSpeedCm)
{
	if (MaxSpeedCm <= 0.f)
	{
		return 1.f;
	}
	return 1.f - FMath::Clamp(SpeedCm / MaxSpeedCm, 0.f, 1.f);
}

void UHomeWorldBeastEncounterComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	AActor* Owner = GetOwner();
	UWorld* World = GetWorld();
	if (!Owner || !World || DeltaTime <= 0.f)
	{
		return;
	}
	AHomeWorldCharacter* Player = Cast<AHomeWorldCharacter>(UGameplayStatics::GetPlayerCharacter(World, 0));
	if (!Player || Player == Owner)
	{
		return;
	}
	SampleAndAdvance(Player, DeltaTime);
}

void UHomeWorldBeastEncounterComponent::SampleAndAdvance(AHomeWorldCharacter* Player, float DeltaTime)
{
	const float DistanceCm = FVector::Dist(GetOwner()->GetActorLocation(), Player->GetActorLocation());

	FHomeWorldBeastEncounterFrame Frame;
	Frame.DeltaSeconds = DeltaTime;
	Frame.PlayerSpeedCm = Player->GetVelocity().Size();
	Frame.DistanceCm = DistanceCm;

	// Inventory is a GameInstance subsystem and can be absent (created-world
	// fixtures) -- null-guard, no GameInstance assumptions.
	UWorld* World = GetWorld();
	if (UGameInstance* GameInstance = World ? World->GetGameInstance() : nullptr)
	{
		if (const UHomeWorldInventorySubsystem* Inventory = GameInstance->GetSubsystem<UHomeWorldInventorySubsystem>())
		{
			Frame.bCarriesOfferFood =
				(Inventory->GetResource(HomeWorldInventory::RES_HERB) +
				 Inventory->GetResource(HomeWorldInventory::RES_BERRY)) > 0;
		}
	}

	if (const UHomeWorldBeastTameComponent* Tame = GetOwner()->FindComponentByClass<UHomeWorldBeastTameComponent>())
	{
		const EHomeWorldBeastTameState State = Tame->GetTameState();
		Frame.bBeastTamed =
			State == EHomeWorldBeastTameState::Tamed ||
			State == EHomeWorldBeastTameState::Helper;
	}

	const EHomeWorldBeastEncounterOutcome Outcome = AdvanceThreat(Frame);

	// Transition-only logging: a refusal or boot the player cannot see reads as
	// a broken game (same law as spirit touch logging, CAMP.json).
	if (Outcome != LastOutcome)
	{
		switch (Outcome)
		{
		case EHomeWorldBeastEncounterOutcome::BootCharged:
			UE_LOG(LogTemp, Log, TEXT("BEAST_CHARGE: threat full / too close without offering -> charge-and-boot (Lead 2026-10-07; not day-camp #8; not planetside #10)"));
			Player->TryBootBeastChargeHome();
			break;
		case EHomeWorldBeastEncounterOutcome::OfferSuppressedBoot:
			UE_LOG(LogTemp, Log, TEXT("BEAST_CHARGE: meter full but offering held -> boot suppressed (route: herb suppresses the boot)"));
			break;
		case EHomeWorldBeastEncounterOutcome::TameWindow:
			UE_LOG(LogTemp, Log, TEXT("BEAST_CHARGE: standing still with offering -> tame window (it approaches and eats)"));
			break;
		default:
			break;
		}
	}
	LastOutcome = Outcome;
}
