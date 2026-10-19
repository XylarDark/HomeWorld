// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldRuneShapeComponent.generated.h"

class APlayerController;
class USplineMeshComponent;
class UStaticMeshComponent;

/** How the player completes the rune. */
UENUM(BlueprintType)
enum class EHomeWorldRuneDrawMode : uint8
{
	Points,
	Trace
};

/** Fixed like a mark on a wall, or kept parallel to the camera. */
UENUM(BlueprintType)
enum class EHomeWorldRuneOrientation : uint8
{
	Static,
	CameraParallel
};

/** The rune outline on a collectible. Any actor can carry one. */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldRuneShapeComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldRuneShapeComponent();

	void ShowHeart(EHomeWorldRuneDrawMode Draw, EHomeWorldRuneOrientation Orientation, APlayerController* Viewer);

	/**
	 * A rune from unit-space points (0..1, +Y up), centered and scaled to SizeCm.
	 * The opening dog's Grace draw uses this; the heart keeps ShowHeart.
	 */
	void ShowShape(const TArray<FVector2D>& UnitPoints, float SizeCm, bool bCloseLoop,
		EHomeWorldRuneDrawMode Draw, EHomeWorldRuneOrientation Orientation, APlayerController* Viewer);

	void HideShape();
	void AlignToViewer(APlayerController* Viewer);
	void SetCursor(const FVector& WorldCursor);

	/** Points mode. True when the click landed on the next point. */
	bool TryClick();

	/** Trace mode. True when the cursor is still on the ribbon. */
	bool AdvanceTrace();

	bool IsComplete() const;
	int32 GetScore() const;
	void GetPlane(FVector& Origin, FVector& Right, FVector& Up) const;
	bool IsPointsMode() const { return DrawMode == EHomeWorldRuneDrawMode::Points; }
	int32 GetReward() const { return DrawMode == EHomeWorldRuneDrawMode::Trace ? 2 : 1; }
	FVector GetStartPoint() const;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	void EnsureRibbon(int32 SegmentCount);
	void Rebuild(const FVector& Right, const FVector& Up, const FVector& Center);
	void ApplyRibbon();
	void ApplyProgress();
	void PickClickPoints();

	EHomeWorldRuneDrawMode DrawMode = EHomeWorldRuneDrawMode::Points;
	EHomeWorldRuneOrientation Orientation = EHomeWorldRuneOrientation::Static;
	bool bShown = false;
	bool bBasisLocked = false;
	FVector LockedRight = FVector::RightVector;
	FVector LockedUp = FVector::UpVector;
	FVector LockedOffset = FVector::ZeroVector;
	bool bInSection = false;
	int32 Progress = 0;
	int32 SectionsEarned = 0;
	FVector Cursor = FVector::ZeroVector;
	FVector PlaneOrigin = FVector::ZeroVector;
	FVector PlaneRight = FVector::RightVector;
	FVector PlaneUp = FVector::UpVector;
	TArray<FVector2D> HeartLocalPoints;
	TArray<int32> ClickOrder;
	TArray<FVector> Outline;
	TArray<float> Arc;
	TArray<FVector> Goals;
	bool bCustomShape = false;
	bool bOutlineClosed = true;
	TArray<FVector2D> UnitShapePoints;
	float CustomSizeCm = 200.f;

	UPROPERTY()
	TArray<TObjectPtr<USplineMeshComponent>> Segments;

	UPROPERTY()
	TArray<TObjectPtr<UStaticMeshComponent>> ClickMarks;

	TWeakObjectPtr<APlayerController> Viewer;
};
