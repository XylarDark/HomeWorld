// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldStrokeCheck.h"
#include "HomeWorldEasePad.generated.h"

	/**
	 * One ease pad, off L_SizeTest. Offers Grace, then Wrath, then Paradox, then one extra point.
	 * The wind-up clock repeats. The open half is WindowMin to WindowMax. The closed half is as long.
	 */
UCLASS()
class HOMEWORLD_API AHomeWorldEasePad : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldEasePad();

	EHomeWorldStrokeStep GetOfferedStep() const;

	/** A match of the offered step advances. A skip, a paradox-first jump, or a fifth step fails. */
	bool NoteMatch(EHomeWorldStrokeStep Played);

	int32 GetCompletedSteps() const { return CompletedSteps; }

	bool IsLadderComplete() const { return CompletedSteps >= 4; }

	/** One pad, one guard. A negative ordinal is unbound and cannot sleep anyone. */
	void BindGuard(int32 Ordinal);

	int32 GetGuardOrdinal() const { return GuardOrdinal; }

	bool IsBoundToGuard() const { return GuardOrdinal >= 0; }

	bool HasSleptItsGuard() const { return bGuardSlept; }

	void MarkGuardSlept();

	FVector GetFocusPoint() const;

	float GetWindowMin() const { return WindowMin; }

	float GetWindowMax() const { return WindowMax; }

	/** Seconds on the repeating wind-up. A start inside the window is on time. */
	float WindUpTimeAt(float WorldSeconds) const;

	FVector2D GetExtraPoint() const { return ExtraPoint; }

	UPROPERTY(VisibleAnywhere, Category = "Stroke")
	TObjectPtr<USceneComponent> Focus;

protected:
	UPROPERTY(VisibleAnywhere, Category = "Stroke")
	int32 CompletedSteps = 0;

	UPROPERTY(VisibleAnywhere, Category = "Stroke")
	int32 GuardOrdinal = INDEX_NONE;

	UPROPERTY(VisibleAnywhere, Category = "Stroke")
	bool bGuardSlept = false;

	UPROPERTY(EditAnywhere, Category = "Stroke")
	float WindowMin = 0.f;

	UPROPERTY(EditAnywhere, Category = "Stroke")
	float WindowMax = 1.f;

	UPROPERTY(EditAnywhere, Category = "Stroke")
	FVector2D ExtraPoint = FVector2D(0.5f, 0.5f);
};
