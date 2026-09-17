// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldBeastTameComponent.generated.h"

class AHomeWorldCharacter;
class UHomeWorldInventorySubsystem;
class USphereComponent;

UENUM(BlueprintType)
enum class EHomeWorldBeastTameState : uint8
{
	Wild,
	Cautious,
	Tamed,
	Helper
};

/**
 * SYS V4 — one beast pad state machine (Docs/03_SYSTEMS_MVP §5).
 * Attach to beast pad / SK_Beast_Small proxy. Logs TAME: on transitions.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldBeastTameComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldBeastTameComponent();

	UFUNCTION(BlueprintCallable, Category = "Tame")
	EHomeWorldBeastTameState GetTameState() const { return TameState; }

	/** Interact offer: day/body only; consumes 1× RES_BERRY or RES_HERB. */
	UFUNCTION(BlueprintCallable, Category = "Tame")
	bool TryOfferFood(AHomeWorldCharacter* Character);

	/** Optional helper step (V4 step 3): day/body while tamed. */
	UFUNCTION(BlueprintCallable, Category = "Tame")
	bool TryPromoteToHelper(AHomeWorldCharacter* Character);

	/** V8 dawn persist — restore tame state without transition log spam. */
	void ApplyPersistedState(EHomeWorldBeastTameState NewState);

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	UPROPERTY(EditDefaultsOnly, Category = "Tame")
	float ProximityRadiusCm = 450.f;

	UPROPERTY(EditDefaultsOnly, Category = "Tame")
	float BondWaitSeconds = 4.f;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Tame")
	EHomeWorldBeastTameState TameState = EHomeWorldBeastTameState::Wild;

	UPROPERTY(VisibleAnywhere, Category = "Tame")
	TObjectPtr<USphereComponent> ProximitySphere;

private:
	bool bOfferAccepted = false;
	bool bBondInProgress = false;
	float BondElapsed = 0.f;
	TWeakObjectPtr<AActor> BondPlayer;

	void SetTameState(EHomeWorldBeastTameState NewState);
	void UpdateProximity(AHomeWorldCharacter* NearbyPlayer);
	bool IsDayBodyInteractionAllowed(AHomeWorldCharacter* Character) const;
	void ResetBondProgress();
};
