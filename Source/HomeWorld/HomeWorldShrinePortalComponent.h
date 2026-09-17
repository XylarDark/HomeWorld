// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/BoxComponent.h"
#include "HomeWorldShrinePortalComponent.generated.h"

/**
 * Shrine portal (V5): overlap or interact teleports pawn to a linked shrine actor.
 * Homestead <-> Return only. Simple arrive teleport for MVP FALLBACK slice.
 * Night gate optional via bRequireNight (default false for PIE demo) or CVar hw.Portal.RequireNight.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldShrinePortalComponent : public UBoxComponent
{
	GENERATED_BODY()

public:
	UHomeWorldShrinePortalComponent(const FObjectInitializer& ObjectInitializer);

	/** Actor label of destination shrine (e.g. ANCHOR_SM_Shrine_Return or SM_Shrine_Return). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal|FALLBACK")
	FName DestinationLabel;

	/** When true, portal only fires during night phase. Default false for PIE demo. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal|FALLBACK")
	bool bRequireNight = false;

	/** Cooldown between teleports (seconds) to prevent bounce loops. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Portal|FALLBACK", meta = (ClampMin = "0.5"))
	float TeleportCooldownSeconds = 2.0f;

	/** Attempt portal transit for overlapping pawn (called from overlap or interact). */
	UFUNCTION(BlueprintCallable, Category = "Portal|FALLBACK")
	bool TryPortalTransit(AActor* InstigatorActor);

	virtual void PostInitProperties() override;
	virtual void BeginPlay() override;

protected:
	UFUNCTION()
	void OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	AActor* FindDestinationActor(UWorld* World) const;
	bool IsNightGateOpen(UWorld* World) const;
	FVector GetArriveLocation(AActor* Destination) const;

	float LastTeleportTime = -1000.0f;
};
