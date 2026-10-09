// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldFallbackGlideComponent.generated.h"

class ACharacter;
class UCharacterMovementComponent;

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnFallbackGlideCompleted);

/**
 * FALLBACK scripted glide: moves the owning pawn along CRUMB_* TargetPoints in locked order.
 * No free-flight, no steering, no flight HUD. See Docs/09_FALLBACK_GLIDE.md and Lib/08_Transit/GLIDE_SPLINE.md.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldFallbackGlideComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldFallbackGlideComponent();

	/** Locked crumb order from Lib/08_Transit/GLIDE_SPLINE.md — do not reorder. */
	static const TArray<FName>& GetLockedCrumbOrder();

	/** Begin scripted glide if crumbs resolve and pawn is eligible (day/body). Returns false if skipped. */
	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK")
	bool StartGlide();

	/**
	 * EJECT_HOME: reverse CRUMB path (Landing -> Depart_Lookout / home).
	 * Reuses same glide machinery as StartGlide -- not a parallel eject service (Arch B).
	 * Distinct from island->planet FALLBACK StartGlide (that alone = closed_fail for MUST #8/#10).
	 * bAllowNightPhase: MUST #10 planetside night boot may pass true; #8 day-camp leaves default false.
	 */
	UFUNCTION(BlueprintCallable, Category = "Transit|EJECT_HOME")
	bool StartGlideHome(bool bAllowNightPhase = false);

	/** Abort glide and restore walk movement. Idempotent. */
	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK")
	void CancelGlide();

	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK")
	bool IsGliding() const { return bIsGliding; }

	/** 1 = the authored glide. Spirit sickness passes 0.85 so the glide hitches with the step. */
	void SetGlideSpeedScale(float Scale);

	/** Fired when CRUMB_Landing is reached and walk is restored. */
	UPROPERTY(BlueprintAssignable, Category = "Transit|FALLBACK")
	FOnFallbackGlideCompleted OnGlideCompleted;

	/** Total traverse duration (seconds). Target 25–40 s readable drop. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transit|FALLBACK", meta = (ClampMin = "25.0", ClampMax = "40.0"))
	float GlideDurationSeconds = 32.0f;

	/** When true, glide only available during day phase (not night). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transit|FALLBACK")
	bool bRequireDayPhase = true;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
	virtual void BeginPlay() override;

	void AdvanceGlide(float DeltaTime);
	void FinishGlide(bool bCompleted);
	void CacheMovementDefaults();
	void ApplyGlideMovementLock();
	void RestoreMovement();

	AActor* FindActorByLabel(UWorld* World, FName Label) const;
	bool ResolveCrumbPath(UWorld* World, TArray<FVector>& OutLocations);

	UPROPERTY()
	TObjectPtr<ACharacter> CachedCharacter;

	UPROPERTY()
	TObjectPtr<UCharacterMovementComponent> CachedMovement;

	TArray<FVector> CrumbLocations;
	int32 CurrentSegmentIndex = 0;
	float SegmentAlpha = 0.0f;
	float SegmentDuration = 0.0f;
	bool bIsGliding = false;
	float GlideSpeedScale = 1.f;
	/** True while traversing reverse crumbs toward home (EJECT_HOME), not FALLBACK down. */
	bool bHomeboundGlide = false;
	bool bSavedOrientRotationToMovement = true;
	bool bSavedUseControllerRotationYaw = false;
	EMovementMode SavedMovementMode = MOVE_Walking;
};
