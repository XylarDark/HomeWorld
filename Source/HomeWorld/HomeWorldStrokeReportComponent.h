// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldStrokeCheck.h"
#include "HomeWorldStrokeReportComponent.generated.h"

class UHomeWorldFallbackGlideComponent;
class UHomeWorldVirtueComponent;

/** What the last stroke check asked the existing glide to do. */
UENUM(BlueprintType)
enum class EHomeWorldStrokeReport : uint8
{
	None,
	WeakHit,
	Bonk,
	Matched
};

/** The two ease commits. Spend finishes inside the wind-up. Wait keeps what you are holding. */
UENUM(BlueprintType)
enum class EHomeWorldEaseCommit : uint8
{
	SpendInside,
	Wait
};

/** Which marked-herb verb a stroke match may spend. A miss spends none. */
UENUM(BlueprintType)
enum class EHomeWorldHerbVerb : uint8
{
	None,
	Give,
	Take,
	Swap
};

/**
 * Reports a stroke. A quiet miss steps away from a focus when one is given.
 * A late paradox calls the existing glide home. A wrong shape does not.
 * It does not ease the camp.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldStrokeReportComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = "Stroke")
	void BeginStrokeHold();

	/** Reads the player cursor while a stroke is held. No cursor leaves the stroke unchanged. */
	UFUNCTION(BlueprintCallable, Category = "Stroke")
	void SampleCursor(float Time);

	UFUNCTION(BlueprintCallable, Category = "Stroke")
	void AppendCursorSample(FVector2D ScreenPoint, float Time);

	UFUNCTION(BlueprintCallable, Category = "Stroke")
	EHomeWorldStrokeReport EndStrokeHold(
		EHomeWorldStrokeStep Step,
		float WindowMin,
		float WindowMax,
		FVector2D ExtraPoint,
		UHomeWorldVirtueComponent* VirtueOverride = nullptr,
		UHomeWorldFallbackGlideComponent* GlideOverride = nullptr,
		bool bHasFocus = false,
		FVector FocusPoint = FVector::ZeroVector,
		EHomeWorldEaseCommit Commit = EHomeWorldEaseCommit::SpendInside,
		bool bSpendBonkTry = false);

	UFUNCTION(BlueprintCallable, Category = "Stroke")
	EHomeWorldStrokeReport ReportStroke(
		EHomeWorldStrokeStep Step,
		const TArray<FHomeWorldStrokeSample>& Stroke,
		float WindowMin,
		float WindowMax,
		FVector2D ExtraPoint,
		UHomeWorldVirtueComponent* VirtueOverride = nullptr,
		UHomeWorldFallbackGlideComponent* GlideOverride = nullptr,
		bool bHasFocus = false,
		FVector FocusPoint = FVector::ZeroVector,
		EHomeWorldEaseCommit Commit = EHomeWorldEaseCommit::SpendInside,
		bool bSpendBonkTry = false);

	UFUNCTION(BlueprintCallable, Category = "Stroke")
	EHomeWorldStrokeReport GetLastReport() const { return LastReport; }

	bool IsStrokeHeld() const { return bStrokeHeld; }

	const TArray<FHomeWorldStrokeSample>& GetHeldStroke() const { return HeldStroke; }

	bool WasGlideHomeInvoked() const { return bGlideHomeInvoked; }

	bool WasWeakHitMoved() const { return bWeakHitMoved; }

	FVector GetLastWeakHitOffset() const { return LastWeakHitOffset; }

	bool HasCarriedPoint() const { return bHasCarriedPoint; }

	FVector2D GetCarriedPoint() const { return CarriedPoint; }

	UFUNCTION(BlueprintCallable, Category = "Stroke")
	void SetBonkTries(int32 Tries);

	int32 GetBonkTries() const { return BonkTries; }

protected:
	void RecordDrawnPoles(EHomeWorldStrokeStep Step, UHomeWorldVirtueComponent* Virtue) const;

	void ApplyWeakHit(const FVector& FocusPoint);

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stroke")
	EHomeWorldStrokeReport LastReport = EHomeWorldStrokeReport::None;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stroke")
	TArray<FHomeWorldStrokeSample> HeldStroke;

	bool bStrokeHeld = false;

	bool bGlideHomeInvoked = false;

	bool bWeakHitMoved = false;

	FVector LastWeakHitOffset = FVector::ZeroVector;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stroke")
	bool bHasCarriedPoint = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stroke")
	FVector2D CarriedPoint = FVector2D::ZeroVector;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Stroke")
	int32 BonkTries = 0;
};
