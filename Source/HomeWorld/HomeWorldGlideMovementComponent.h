// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "HomeWorldGlideMovementComponent.generated.h"

/** Custom movement mode used by UHomeWorldGlideMovementComponent. UE has no engine glide mode. */
enum EHomeWorldCustomMovementMode : uint8
{
	CMOVE_HW_Glide = 0,
};

/**
 * Character movement for the active cloud descent: a trimmed glider, not free flight.
 *
 * Steering is unrestricted (no rail, corridor, or artificial bound) per
 * Docs/context/HOMEWORLD_ROUTE.md and Docs/01_GDD_MVP.md section 9. The path is
 * produced by forward drive plus a fixed sink rate, so altitude is spent, never held.
 *
 * This is a SUBCLASS of the single engine CMC that ACharacter already owns. It
 * replaces that CMC rather than adding a second one (Lib/ MOVEMENT_BIBLE: one CMC).
 * Every non-glide mode is inherited untouched, so walking, swimming and the
 * traversal boosts behave exactly as before.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldGlideMovementComponent : public UCharacterMovementComponent
{
	GENERATED_BODY()

public:
	UHomeWorldGlideMovementComponent();

	/** Forward airspeed target while gliding. Developer decision 2026-10-05: uniform 5 m/s. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transit|CloudDescent", meta = (ClampMin = "0.0"))
	float GlideForwardSpeed = 500.0f;

	/** Descent sink rate. Developer decision 2026-10-05: uniform 5 m/s, matching GlideForwardSpeed. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transit|CloudDescent", meta = (ClampMin = "0.0"))
	float GlideSinkRate = 500.0f;

	/**
	 * How quickly velocity converges on the glide target. This is a time constant:
	 * the target is reached in roughly 1/GlideSteeringResponsiveness seconds.
	 * Higher = more immediate steering. 8.0 settles in about 0.125 s.
	 */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Transit|CloudDescent", meta = (ClampMin = "0.0"))
	float GlideSteeringResponsiveness = 8.0f;

	/** Enter the glide. Returns false if already gliding or the mode was rejected. */
	UFUNCTION(BlueprintCallable, Category = "Transit|CloudDescent")
	bool StartGlide();

	/** Leave the glide and resume normal falling. */
	UFUNCTION(BlueprintCallable, Category = "Transit|CloudDescent")
	void StopGlide();

	UFUNCTION(BlueprintPure, Category = "Transit|CloudDescent")
	bool IsGliding() const;

	/** The velocity a trimmed glide at the current inputs should be converging on. */
	FVector ComputeGlideTargetVelocity() const;

protected:
	virtual void PhysCustom(float DeltaTime, int32 Iterations) override;
};