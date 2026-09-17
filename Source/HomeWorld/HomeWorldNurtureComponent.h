// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldNurtureComponent.generated.h"

class AHomeWorldCharacter;

UENUM(BlueprintType)
enum class EHomeWorldNurtureTargetId : uint8
{
	N1_Crop,
	N2_Stored
};

/**
 * SYS V7 — homestead nurture target (Docs/03_SYSTEMS_MVP §7).
 * Success sets bNurtured (M_Nurtured flag contract); logs NURTURE:.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldNurtureComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldNurtureComponent();

	UFUNCTION(BlueprintCallable, Category = "Nurture")
	bool GetIsNurtured() const { return bNurtured; }

	UFUNCTION(BlueprintCallable, Category = "Nurture")
	EHomeWorldNurtureTargetId GetTargetId() const { return TargetId; }

	UFUNCTION(BlueprintCallable, Category = "Nurture")
	FName GetRequiredResourceId() const { return RequiredResourceId; }

	/** Night/spirit interact on homestead target. */
	UFUNCTION(BlueprintCallable, Category = "Nurture")
	bool TryNurture(AHomeWorldCharacter* Character);

	void ApplyPersistedNurtured(bool bInNurtured);

	/** Placement script: N1 crop vs N2 stored + required RES_*. */
	UFUNCTION(BlueprintCallable, Category = "Nurture")
	void ConfigureTarget(EHomeWorldNurtureTargetId InTarget, FName InRequiredResource);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditDefaultsOnly, Category = "Nurture")
	EHomeWorldNurtureTargetId TargetId = EHomeWorldNurtureTargetId::N1_Crop;

	/** RES_SEED for N1; RES_WOOD default for N2. */
	UPROPERTY(EditDefaultsOnly, Category = "Nurture")
	FName RequiredResourceId = HomeWorldInventory::RES_SEED;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Nurture")
	bool bNurtured = false;

private:
	bool IsNightSpiritHomesteadAllowed(AHomeWorldCharacter* Character) const;
	FName TargetLabel() const;
	void ApplyNurturedVisual();
};
