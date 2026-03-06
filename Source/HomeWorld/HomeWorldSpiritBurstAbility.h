// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Sound/SoundBase.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldSpiritBurstAbility.generated.h"

class UAbilitySystemComponent;
class UWorld;

/**
 * Spirit/night-combat ability stub. Active only when TimeOfDay is night (Phase 2).
 * GA_SpiritBurst Blueprint should use this as parent. Trigger via hw.SpiritBurst in PIE or input.
 * Cooldown: after use, cannot activate again for CooldownSeconds; attempts log remaining time (cooldown display stub).
 * See VISION.md (spirit abilities at night), DAY12_ROLE_PROTECTOR.md.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldSpiritBurstAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldSpiritBurstAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;

	/** Spiritual power cost per activation (only at night). If player has less, activation is blocked. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritBurst", meta = (ClampMin = "0"))
	int32 SpiritPowerCost = 1;

	/** Cooldown duration in seconds. Editable in Blueprint for tuning. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritBurst", meta = (ClampMin = "0.1", ClampMax = "300.0"))
	float CooldownSeconds = 5.0f;

	/** Optional sound played when the ability activates (stub for VFX/sound feedback). Assign in GA_SpiritBurst Blueprint or leave null for log-only. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritBurst")
	TObjectPtr<USoundBase> ActivationSound = nullptr;

	/** World time when cooldown ends (for cooldown display / block). */
	UPROPERTY()
	float CooldownEndWorldTime = 0.0f;

	/** Returns seconds remaining on SpiritBurst cooldown, or 0 if ready. For HUD/UI. */
	UFUNCTION(BlueprintCallable, Category = "SpiritBurst")
	static float GetSpiritBurstCooldownRemaining(UAbilitySystemComponent* ASC, UWorld* World);
};
