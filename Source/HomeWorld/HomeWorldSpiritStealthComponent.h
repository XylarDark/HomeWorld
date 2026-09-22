// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldSpiritStealthTypes.h"
#include "HomeWorldSpiritStealthComponent.generated.h"

class AHomeWorldSpiritLitVolume;

class UPointLightComponent;
class USkeletalMeshComponent;

/**
 * SS-A/SS-B: spirit-form lit / alert (A2 pressure) + readable hidden/revealed feel. Logs STEALTH:* — no kill, no kidnap, no homestead combat.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldSpiritStealthComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldSpiritStealthComponent();

	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-A")
	bool IsSpiritLit() const { return LitOverlapCount > 0 || bForceLitCheat; }

	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-A")
	float GetAlertLevel() const { return AlertLevel; }

	/** SS-B: true when spirit is unlit (hidden fantasy cue active). */
	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-B")
	bool IsSpiritHiddenCueActive() const;

	/** SS-B: true when lit or alert is rising (revealed fantasy cue). */
	UFUNCTION(BlueprintCallable, Category = "Stealth|SS-B")
	bool IsSpiritRevealedCueActive() const;

	void NotifyLitVolumeEntered(EHomeWorldSpiritLitSourceKind SourceKind, AHomeWorldSpiritLitVolume* Volume);
	void NotifyLitVolumeExited(AHomeWorldSpiritLitVolume* Volume);

	/** Optional haste hook — once per lit session while alert is rising. */
	void NotifyInteractWhileLit();

	/** hw.Stealth.ForceLit — debug only. */
	void SetForceLitCheat(bool bForce);

	void LogStatus() const;

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	void UpdateAlert(float DeltaTime);
	void TryLogClear();
	void UpdateFeelVisuals();
	void EnsureFeelLight();
	void ApplyMeshFeelTint(bool bRevealed, float Alert01);

	UPROPERTY(Transient)
	TObjectPtr<UPointLightComponent> FeelLight;

	UPROPERTY(Transient)
	bool bFeelLightSpawned = false;

	UPROPERTY(Transient)
	bool bLastRevealedCue = false;

	UPROPERTY(Transient)
	int32 LitOverlapCount = 0;

	UPROPERTY(Transient)
	float AlertLevel = 0.f;

	UPROPERTY(Transient)
	bool bLoggedAlertThisLitSession = false;

	UPROPERTY(Transient)
	bool bLoggedQuickWindowThisLitSession = false;

	UPROPERTY(Transient)
	bool bWasLitLastFrame = false;

	UPROPERTY(Transient)
	bool bForceLitCheat = false;

	UPROPERTY(Transient)
	EHomeWorldSpiritLitSourceKind LastEnterSourceKind = EHomeWorldSpiritLitSourceKind::Campfire;

	static constexpr float AlertRisePerSecond = 0.35f;
	static constexpr float AlertDecayPerSecond = 0.55f;
	static constexpr float AlertThreshold = 0.72f;
};
