// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritShieldAbility.h"
#include "AbilitySystemComponent.h"
#include "GameplayAbilitySpec.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Engine/World.h"
#include "GameFramework/Controller.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"

UHomeWorldSpiritShieldAbility::UHomeWorldSpiritShieldAbility()
{
	InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

void UHomeWorldSpiritShieldAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
	const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData)
{
	UWorld* World = ActorInfo && ActorInfo->AvatarActor.IsValid() ? ActorInfo->AvatarActor->GetWorld() : nullptr;
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr;

	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield [%s] only active at night (Phase 2). Set hw.TimeOfDay.Phase 2 first."), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	const float Now = World ? World->GetTimeSeconds() : 0.0f;
	if (Now < CooldownEndWorldTime)
	{
		const float Remaining = CooldownEndWorldTime - Now;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield on cooldown — %.1fs remaining"), Remaining);
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	if (SpiritPowerCost > 0)
	{
		APawn* AvatarPawn = ActorInfo && ActorInfo->AvatarActor.IsValid() ? Cast<APawn>(ActorInfo->AvatarActor.Get()) : nullptr;
		AController* Ctrl = AvatarPawn ? AvatarPawn->GetController() : nullptr;
		AHomeWorldPlayerState* PS = Ctrl ? Ctrl->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
		if (!PS)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield [%s] requires a HomeWorld PlayerState."), *GetName());
			EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
			return;
		}
		if (PS->GetSpiritualPowerCollected() < SpiritPowerCost)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield [%s] blocked — insufficient spiritual power (need %d, have %d)."), *GetName(), SpiritPowerCost, PS->GetSpiritualPowerCollected());
			PS->SetSpiritBurstBlockMessage(FString::Printf(TEXT("Shield: need %d power"), SpiritPowerCost), Now);
			EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
			return;
		}
	}

	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield ability activated [%s]"), *GetName());

	if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritShield [%s] failed CommitAbility"), *GetName());
		EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
		return;
	}

	if (SpiritPowerCost > 0)
	{
		APawn* AvatarPawn = ActorInfo && ActorInfo->AvatarActor.IsValid() ? Cast<APawn>(ActorInfo->AvatarActor.Get()) : nullptr;
		AController* Ctrl = AvatarPawn ? AvatarPawn->GetController() : nullptr;
		AHomeWorldPlayerState* PS = Ctrl ? Ctrl->GetPlayerState<AHomeWorldPlayerState>() : nullptr;
		if (PS && PS->SpendSpiritualPower(SpiritPowerCost))
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield [%s] spent %d spiritual power; remaining: %d"), *GetName(), SpiritPowerCost, PS->GetSpiritualPowerCollected());
		}
	}

	CooldownEndWorldTime = Now + CooldownSeconds;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield [%s] committed (night-only stub, cooldown %.1fs)"), *GetName(), CooldownSeconds);

	AActor* Avatar = ActorInfo && ActorInfo->AvatarActor.IsValid() ? ActorInfo->AvatarActor.Get() : nullptr;
	if (World && Avatar && ActivationSound)
	{
		UGameplayStatics::PlaySoundAtLocation(this, ActivationSound, Avatar->GetActorLocation());
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield played ActivationSound at avatar location."));
	}
	else if (Avatar)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SpiritShield fired (assign ActivationSound in GA_SpiritShield for audio feedback)."));
	}

	EndAbility(Handle, ActorInfo, ActivationInfo, false, false);
}

float UHomeWorldSpiritShieldAbility::GetSpiritShieldCooldownRemaining(UAbilitySystemComponent* ASC, UWorld* World)
{
	if (!ASC || !World) return 0.f;
	FGameplayAbilitySpec* Spec = ASC->FindAbilitySpecFromClass(UHomeWorldSpiritShieldAbility::StaticClass());
	if (!Spec || !Spec->Ability) return 0.f;
	UHomeWorldSpiritShieldAbility* Instance = Cast<UHomeWorldSpiritShieldAbility>(Spec->Ability);
	if (!Instance) return 0.f;
	const float Now = World->GetTimeSeconds();
	const float Remaining = Instance->CooldownEndWorldTime - Now;
	return FMath::Max(0.f, Remaining);
}
