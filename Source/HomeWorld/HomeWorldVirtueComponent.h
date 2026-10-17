// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldVirtueTypes.h"
#include "HomeWorldVirtueComponent.generated.h"

class UHomeWorldVirtueSpawnTable;

/**
 * Poles on a character or a collectible. A hand set skips the roll.
 * Docs/VIRTUE_ATTRIBUTE_BIBLE.md.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldVirtueComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	const TArray<EHomeWorldVirtuePole>& GetPoles() const { return Poles; }

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool HasPole(EHomeWorldVirtuePole Pole) const;

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool HasAxis(EHomeWorldVirtuePole Pole) const;

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool HasParadox(EHomeWorldVirtuePole PoleOnAxis) const;

	const TArray<int32>& GetParadoxAxes() const { return ParadoxAxes; }

	const TArray<EHomeWorldVirtuePole>& GetDrawnPoles() const { return DrawnPoles; }

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool HasDrawnPole(EHomeWorldVirtuePole Pole) const;

	/** Remember a pole the player has drawn. The spawn roll does not write this. */
	UFUNCTION(BlueprintCallable, Category = "Virtue")
	void RecordDrawnPole(EHomeWorldVirtuePole Pole);

	/** Occupies the pole's axis. Fails when that axis already has a pole or a paradox. */
	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool TrySetParadox(EHomeWorldVirtuePole PoleOnAxis);

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	void ClearPoles();

	/** Adds the pole when its axis is empty. */
	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool TryGivePole(EHomeWorldVirtuePole Pole);

	/** Removes the pole when it is present. */
	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool TryTakePole(EHomeWorldVirtuePole Pole);

	/** Flips whichever pole of this axis is present. */
	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool TrySwapAxis(EHomeWorldVirtuePole Pole);

	UFUNCTION(BlueprintCallable, Category = "Virtue")
	bool TrySetHandPoles(const TArray<EHomeWorldVirtuePole>& Hand, FString& OutError);

	void Roll(const TArray<float>& Chances, FRandomStream& Stream);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditAnywhere, Category = "Virtue")
	bool bHandAuthored = false;

	UPROPERTY(EditAnywhere, Category = "Virtue", meta = (EditCondition = "bHandAuthored"))
	TArray<EHomeWorldVirtuePole> HandPoles;

	UPROPERTY(EditAnywhere, Category = "Virtue")
	bool bCollectible = false;

	UPROPERTY(EditAnywhere, Category = "Virtue")
	TObjectPtr<UHomeWorldVirtueSpawnTable> SpawnTable;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Virtue")
	TArray<EHomeWorldVirtuePole> Poles;

	/** Axis indexes held as a paradox instead of a pole. The spawn roll never writes these. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Virtue")
	TArray<int32> ParadoxAxes;

	/** Poles the player has drawn. Not a spawn result. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Virtue")
	TArray<EHomeWorldVirtuePole> DrawnPoles;
};
