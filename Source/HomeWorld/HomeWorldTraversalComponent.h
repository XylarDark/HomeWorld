// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldTraversalComponent.generated.h"

class ACharacter;
class UCharacterMovementComponent;

/**
 * MV-A: parkour-lite + spirit blink + mount speed mode on the owner's single CMC.
 * See Docs/MOVEMENT_BIBLE.md NOW and Docs/24_MOVEMENT_IMPL.md.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldTraversalComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldTraversalComponent();

	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A")
	void SetSprintHeld(bool bHeld);

	/** Attempt mantle (high ledge) or vault (low obstacle). Logs MOVE: MANTLE / MOVE: VAULT. */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A")
	bool TryMantleOrVault();

	/** Spirit-only short blink toward nearest SpiritAnchor / shrine tag. Logs MOVE: SPIRIT_BLINK. */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A")
	bool TrySpiritBlink();

	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A")
	void SetMountBoostActive(bool bActive);

	/** Called from character form sync (body vs spirit walk tuning). */
	void ApplyFormMovementTuning(bool bSpiritForm);

	/** 1 = full walk. Spirit sickness and the late-wake minute pass 0.85. Gather and ease do not call this. */
	void SetMovementSlowScale(float Scale);

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
	virtual void BeginPlay() override;

	void CacheDefaultMovement();
	void UpdateSprintSpeed();
	void UpdateFallSoftReset(float DeltaTime);
	/** True when the pawn is falling with walkable ground within DropCorridorProbeCm below. */
	bool IsOverLandingGround() const;
	bool ResolveMantleTarget(FVector& OutStandLocation, bool& bOutVault) const;
	AActor* FindSpiritBlinkTarget() const;
	bool IsTraversalBlocked() const;

	UPROPERTY()
	TObjectPtr<ACharacter> CachedCharacter;

	UPROPERTY()
	TObjectPtr<UCharacterMovementComponent> CachedMovement;

	/** Multiplies walk, sprint, spirit, and mount speed. Default 1. */
	float MovementSlowScale = 1.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Walk", meta = (ClampMin = "100.0"))
	float BodyWalkSpeed = 450.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Walk", meta = (ClampMin = "100.0"))
	float SprintWalkSpeed = 585.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Walk", meta = (ClampMin = "100.0"))
	float SpiritWalkSpeed = 520.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Walk", meta = (ClampMin = "100.0"))
	float MountBoostWalkSpeed = 720.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Jump", meta = (ClampMin = "100.0"))
	float JumpZVelocity = 420.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Spirit", meta = (ClampMin = "0.1", ClampMax = "1.0"))
	float SpiritGravityScale = 0.82f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Mantle", meta = (ClampMin = "30.0"))
	float MantleForwardTraceCm = 75.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Mantle", meta = (ClampMin = "40.0"))
	float MantleMaxRiseCm = 120.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Mantle", meta = (ClampMin = "20.0"))
	float VaultMaxRiseCm = 65.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Blink", meta = (ClampMin = "200.0"))
	float BlinkMaxRangeCm = 1400.f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Blink", meta = (ClampMin = "0.5"))
	float BlinkCooldownSeconds = 2.5f;

	/**
	 * Soft reset: after this long in the air, put the pawn back on its last
	 * safe ground. This is a STUCK-prevention net for falls off the homestead
	 * edge -- it is NOT a drop budget. Lead owns these numbers for feel; the
	 * polishable fact is that the homestead-to-field drop is ~9500 cm, so any
	 * FallReset*Cm below that fires mid-drop and strands the player in the air.
	 * See IsOverLandingGround and bRespectDropCorridor below.
	 */
	UPROPERTY(EditDefaultsOnly, Category = "Movement|Fall", meta = (ClampMin = "1.0"))
	float FallResetSeconds = 2.75f;

	UPROPERTY(EditDefaultsOnly, Category = "Movement|Fall", meta = (ClampMin = "500.0"))
	float FallResetDropCm = 2200.f;

	/**
	 * When true the soft reset stands down on any frame where the pawn is
	 * falling with walkable ground within DropCorridorProbeCm below it.
	 *
	 * The Lead's stated intent for the homestead: you can jump off the edge
	 * toward the starting zone and "no matter what you do while you are
	 * travelling toward the ground, you will land in the field." With the reset
	 * at 22 m and the field at 95 m, that intent is unreachable, so this
	 * defaults ON.
	 *
	 * This does not weaken stuck-prevention, because it only stands the reset
	 * down where there is somewhere to land. Falling off the rear of the island
	 * into open air still resets, which is what the net is for.
	 *
	 * Set false to restore the old unconditional behaviour.
	 */
	UPROPERTY(EditDefaultsOnly, Category = "Movement|Fall")
	bool bRespectDropCorridor = true;

	/** Trace distance used to decide "is there somewhere to land". */
	UPROPERTY(EditDefaultsOnly, Category = "Movement|Fall", meta = (ClampMin = "1000.0"))
	float DropCorridorProbeCm = 30000.f;

	bool bSprintHeld = false;
	bool bMountBoostActive = false;
	bool bSpiritFormTuning = false;
	float DefaultGravityScale = 1.f;
	float DefaultJumpZ = 420.f;
	FVector LastSafeGroundLocation = FVector::ZeroVector;
	float TimeInFall = 0.f;
	float LastBlinkWorldTime = -1000.f;
};
