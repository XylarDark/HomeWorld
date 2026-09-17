// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldSpiritHealComponent.generated.h"

class AHomeWorldCharacter;

UENUM(BlueprintType)
enum class EHomeWorldSpiritHealState : uint8
{
	Hurt,
	Healed
};

/**
 * SYS V6 — one hurt/healed spirit wisp at SM_SpiritWound (Docs/03_SYSTEMS_MVP §6).
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldSpiritHealComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldSpiritHealComponent();

	UFUNCTION(BlueprintCallable, Category = "Heal")
	EHomeWorldSpiritHealState GetHealState() const { return HealState; }

	UFUNCTION(BlueprintCallable, Category = "Heal")
	FName GetSpiritId() const { return SpiritId; }

	UFUNCTION(BlueprintCallable, Category = "Heal")
	bool IsNurturedFlag() const { return HealState == EHomeWorldSpiritHealState::Healed; }

	/** Night/spirit interact: consume RES_HERB (default) or RES_SEED; logs HEAL:. */
	UFUNCTION(BlueprintCallable, Category = "Heal")
	bool TryHeal(AHomeWorldCharacter* Character);

	void ApplyPersistedState(EHomeWorldSpiritHealState NewState);

	/** Placement script: Spirit_A / Spirit_B / Spirit_C. */
	UFUNCTION(BlueprintCallable, Category = "Heal")
	void ConfigureSpirit(FName InSpiritId);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(EditDefaultsOnly, Category = "Heal")
	FName SpiritId = FName(TEXT("Spirit_A"));

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Heal")
	EHomeWorldSpiritHealState HealState = EHomeWorldSpiritHealState::Hurt;

private:
	bool IsNightSpiritInteractionAllowed(AHomeWorldCharacter* Character) const;
	void SetHealState(EHomeWorldSpiritHealState NewState);
};
