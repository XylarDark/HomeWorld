// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldSoftBoundsComponent.generated.h"

class ACharacter;

/**
 * V1 soft walk bounds: cylindrical pushback when the pawn leaves the hero island plateau.
 * No navmesh required — uses a configurable center/radius from VS_MVP graybox (Lib/00_Core/GRAYBOX_LAYOUT.md).
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldSoftBoundsComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldSoftBoundsComponent();

	/** World-space center of the walkable island (cm). Default: cabin/path hub from MVP anchors. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds")
	FVector BoundsCenter = FVector(-400.f, -50.f, 100.f);

	/** Horizontal radius (cm) before soft pushback applies. ~10.5 m half-width of 21 m island. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds", meta = (ClampMin = "500.0", ClampMax = "10000.0"))
	float BoundsRadiusXY = 1050.f;

	/** Minimum Z (cm) — cliff drop guard. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds")
	float MinZ = -400.f;

	/** Maximum Z (cm) — low aerial cap (no free-flight). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds")
	float MaxZ = 600.f;

	/** Push strength applied toward bounds center when outside (cm/s equivalent via AddMovementInput). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds", meta = (ClampMin = "0.1", ClampMax = "5.0"))
	float PushbackStrength = 1.2f;

	/** When false, component is inert (e.g. during FALLBACK glide). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Walk|Bounds")
	bool bBoundsEnabled = true;

	UFUNCTION(BlueprintCallable, Category = "Walk|Bounds")
	bool IsInsideBounds(const FVector& Location) const;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
	virtual void BeginPlay() override;

	void ApplySoftPushback(float DeltaTime);

	UPROPERTY()
	TObjectPtr<ACharacter> CachedCharacter;

	float LastPushbackLogTime = -1000.f;
};
