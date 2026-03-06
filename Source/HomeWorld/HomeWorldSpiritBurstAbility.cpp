// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritBurstAbility.h"
#include "AbilitySystemComponent.h"
#include "GameplayAbilitySpec.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Engine/World.h"
#include "GameFramework/Controller.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

UHomeWorldSpiritBurstAbility::UHomeWorldSpiritBurstAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldSpiritBurstAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	UWorld* World = ActorInfo && ActorInfo->AvatarActor.IsValid() ? ActorInfo->AvatarActor->GetWorld() : nullptr;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;

	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritBurst [%s] only active at night (Phase 2). Set hw.TimeOfDay.Phase 2 first."), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	const float Now = World ? World->GetTimeSeconds() : 0.0f;
	if (Now < CooldownEndWorldTime)
	{
		const float Remaining = CooldownEndWorldTime - Now;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst on cooldown — %.1fs remaining"), Remaining);
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	// Spiritual power cost: only at night; block activation if insufficient.
	if (SpiritPowerCost > 0)
	{
		APawn* AvatarPawn = ActorInfo && ActorInfo->AvatarActor.IsValid() ? Cast<APawn>(ActorInfo->AvatarActor.Get()) : nullptr;
		AController* Ctrl = AvatarPawn ? AvatarPawn->GetController() : nullptr;
		AHomeWorldPlayerState* PS = Ctrl ? Ctrl->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
		if (!PS)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritBurst [%s] requires a HomeWorld PlayerState (no PS on avatar)."), *GetName());
			EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
			return;
		}
		if (PS->GetSpiritualPowerCollected() < SpiritPowerCost)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritBurst [%s] blocked — insufficient spiritual power (need %d, have %d)."), *GetName(), SpiritPowerCost, PS->GetSpiritualPowerCollected());
			PS->SetSpiritBurstBlockMessage(TEXT("Not enough spiritual power"), Now);
			EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
			return;
		}
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst ability activated [%s]"), *GetName());

	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritBurst [%s] failed CommitAbility"), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	// Deduct spiritual power after successful commit (night-only ability).
	if (SpiritPowerCost > 0)
	{
		APawn* AvatarPawn = ActorInfo && ActorInfo->AvatarActor.IsValid() ? Cast<APawn>(ActorInfo->AvatarActor.Get()) : nullptr;
		AController* Ctrl = AvatarPawn ? AvatarPawn->GetController() : nullptr;
		AHomeWorldPlayerState* PS = Ctrl ? Ctrl->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
		if (PS && PS->SpendSpiritualPower(SpiritPowerCost))
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst [%s] spent %d spiritual power; remaining: %d"), *GetName(), SpiritPowerCost, PS->GetSpiritualPowerCollected());
		}
	}

	CooldownEndWorldTime = Now + CooldownSeconds;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst [%s] committed successfully (night-only stub, cooldown %.1fs)"), *GetName(), CooldownSeconds);

	// T4: VFX/sound stub — play optional activation sound at avatar location for feedback when ability fires at night.
	AActor* Avatar = ActorInfo && ActorInfo->AvatarActor.IsValid() ? ActorInfo->AvatarActor.Get() : nullptr;
	if (World && Avatar && ActivationSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ActivationSound, Avatar->GetActorLocation());
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst played ActivationSound at avatar location."));
	}
	else if (Avatar)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritBurst fired (assign ActivationSound in GA_SpiritBurst for audio feedback)."));
	}

	EndAbility(Handle, ActorInfo, ActivationInfo, false, false);
}

float UHomeWorldSpiritBurstAbility::GetSpiritBurstCooldownRemaining(UAbilitySystemComponent* ASC, UWorld* World)
{
	if (!ASC || !World) return 0.f;
	FGameplayAbilitySpec* Spec = ASC->FindAbilitySpecFromClass(UHomeWorldSpiritBurstAbility::StaticClass());
	if (!Spec || !Spec->Ability) return 0.f;
	UHomeWorldSpiritBurstAbility* Instance = Cast<UHomeWorldSpiritBurstAbility>(Spec->Ability);
	if (!Instance) return 0.f;
	const float Now = World->GetTimeSeconds();
	const float Remaining = Instance->CooldownEndWorldTime - Now;
	return FMath::Max(0.f, Remaining);
}
