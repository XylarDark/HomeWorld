// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Sound/SoundBase.h"
#include "HomeWorldGameplayAbility.h"
#include "HomeWorldSpiritShieldAbility.generated.h"

class UAbilitySystemComponent;
class UWorld;

/**
 * Second spirit/night ability stub (shield). Active only when TimeOfDay is night (Phase 2).
 * GA_SpiritShield Blueprint should use this as parent. Trigger via key (e.g. R) or hw.SpiritShield in PIE.
 * Cooldown and optional spiritual power cost; HUD shows "SpiritShield: ready" or "N.Xs" at night.
 * See VISION.md (spirit abilities at night), DAY12_ROLE_PROTECTOR.md.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API UHomeWorldSpiritShieldAbility : public UHomeWorldGameplayAbility
{
	GENERATED_BODY()

public:
	UHomeWorldSpiritShieldAbility();

	virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle, const FGameplayAbilityActorInfo* ActorInfo,
		const FGameplayAbilityActivationInfo ActivationInfo, const FGameplayEventData* TriggerEventData) override;

	/** Spiritual power cost per activation (only at night). If player has less, activation is blocked. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritShield", meta = (ClampMin = "0"))
	int32 SpiritPowerCost = 2;

	/** Cooldown duration in seconds. Editable in Blueprint for tuning. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritShield", meta = (ClampMin = "0.1", ClampMax = "300.0"))
	float CooldownSeconds = 8.0f;

	/** Optional sound played when the ability activates. Assign in GA_SpiritShield Blueprint or leave null. */
	UPROPERTY(EditDefaultsOnly, Category = "SpiritShield")
	TObjectPtr<USoundBase> ActivationSound = nullptr;

	/** World time when cooldown ends (for cooldown display / block). */
	UPROPERTY()
	float CooldownEndWorldTime = 0.0f;

	/** Returns seconds remaining on SpiritShield cooldown, or 0 if ready. For HUD/UI. */
	UFUNCTION(BlueprintCallable, Category = "SpiritShield")
	static float GetSpiritShieldCooldownRemaining(UAbilitySystemComponent* ASC, UWorld* World);
};
