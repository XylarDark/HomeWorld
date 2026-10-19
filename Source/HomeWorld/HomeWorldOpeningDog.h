// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "HomeWorldOpeningDog.generated.h"

class AHomeWorldCharacter;
class APlayerController;
class UHomeWorldBeastTameComponent;
class UHomeWorldRuneShapeComponent;
class UMaterialInstanceDynamic;
class UMaterialInterface;
class USceneComponent;
class UStaticMeshComponent;

/**
 * Beat 4 — the injured dog afflicted by Wrath, on the homestead island.
 *
 * Getting too close, or any closing step faster than the slowest opening-wheel step
 * (150 cm/s), knocks the player back out of reach. At that step the Grace symbol appears
 * and is traced; the eased dog accepts one mixed herb (spent by the character) and the tame
 * records on the existing UHomeWorldBeastTameComponent. The greybox body is a placeholder.
 */
UCLASS()
class HOMEWORLD_API AHomeWorldOpeningDog : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldOpeningDog();

	UFUNCTION(BlueprintCallable, Category = "Opening|Dog")
	bool IsWrathEased() const { return bWrathEased; }

	/** The completed Grace trace. The same call the player's finished trace makes. */
	UFUNCTION(BlueprintCallable, Category = "Opening|Dog")
	void NoteGraceDrawn();

	UFUNCTION(BlueprintCallable, Category = "Opening|Dog")
	bool IsDogTamed() const;

	/** Eased only: records the offering on the tame component. The herb is spent by the caller. */
	bool TryTameWithMixedHerb(AHomeWorldCharacter* Character);

	UHomeWorldBeastTameComponent* GetTameComponent() const { return TameComponent; }
	UHomeWorldRuneShapeComponent* GetRuneShape() const { return RuneShape; }

	/** Shows the Grace outline, camera-facing, for the trace. */
	void ShowGraceRune(APlayerController* Viewer);

	/** Red while Wrath is up, yellow while Grace can be drawn or the herb is still owed, green once tamed. */
	void ApplyGreyboxColor(bool bGraceDrawAvailable);

	/** The Grace draw: the outline of a dove (Luke, 2026-10-18). Unit space (0..1, +Y up). */
	static const TArray<FVector2D>& GraceUnitShape();

	/** Closer than this is too close, at any speed. */
	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float KnockRadiusCm = 140.f;

	/** The Grace trace appears inside this range, at the slow step or standing. */
	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float DrawRadiusCm = 900.f;

	/** A closing approach faster than the slow step is punished inside this range. */
	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float NoticeRadiusCm = 1000.f;

	/** The slowest wheel step (150 cm/s) plus room for numerical slop. */
	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float SlowStepCmS = 175.f;

	/** The shove: back and a small hop, landing well outside KnockRadiusCm. No damage. */
	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float KnockSpeedCmS = 1400.f;

	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float KnockLiftCmS = 250.f;

	UPROPERTY(EditAnywhere, Category = "Opening|Dog")
	float KnockCooldownSeconds = 1.5f;

	/** The traced glyph's size, cm. */
	static constexpr float GraceSizeCm = 110.f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;

	UPROPERTY(VisibleAnywhere, Category = "Opening|Dog")
	TObjectPtr<USceneComponent> Root;

	UPROPERTY(VisibleAnywhere, Category = "Opening|Dog")
	TObjectPtr<UHomeWorldBeastTameComponent> TameComponent;

	UPROPERTY(VisibleAnywhere, Category = "Opening|Dog")
	TObjectPtr<UHomeWorldRuneShapeComponent> RuneShape;

	UPROPERTY()
	TArray<TObjectPtr<UStaticMeshComponent>> GreyboxParts;

	UPROPERTY(Transient)
	TObjectPtr<UMaterialInstanceDynamic> DangerRedDynamic;

	bool bWrathEased = false;

	/** 0 unset, 1 wrath, 2 grace or herb, 3 tamed. */
	uint8 GreyboxColorKey = 0;

	UMaterialInterface* DangerRedMaterial();
};
