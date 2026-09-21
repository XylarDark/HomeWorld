// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldBossPlaceholderVolume.generated.h"

class UBoxComponent;
class UHomeWorldBossSealComponent;

/**
 * CD-A model boss placeholder — overlap sets DayBoss/NightBoss from time-of-day; logs BOSS:PHASE_*.
 * Planet / tutorial path only (HOMESTEAD never combat).
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldBossPlaceholderVolume : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldBossPlaceholderVolume();

	UFUNCTION(BlueprintCallable, Category = "CD|Boss")
	UHomeWorldBossSealComponent* GetSealComponent() const { return SealComponent; }

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "CD|Boss")
	TObjectPtr<UBoxComponent> TriggerVolume;

	UPROPERTY(VisibleAnywhere, Category = "CD|Boss")
	TObjectPtr<UHomeWorldBossSealComponent> SealComponent;

	UPROPERTY(Transient)
	bool bLoggedThisOverlap = false;

	UFUNCTION()
	void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);
};
