// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldGcPlaceholderTypes.h"
#include "HomeWorldGcPlaceholderVolume.generated.h"

class UBoxComponent;

/**
 * GC-C: shop / cottage room foreshadow — overlap logs only, no RES spend or craft menus.
 * Idempotent logging: one line per overlap visit; resets on EndOverlap so re-entry logs again.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldGcPlaceholderVolume : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldGcPlaceholderVolume();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "GC|Placeholder")
	EHomeWorldGcPlaceholderKind PlaceholderKind = EHomeWorldGcPlaceholderKind::Woodshop;

	UFUNCTION(BlueprintCallable, Category = "GC|Placeholder")
	EHomeWorldGcPlaceholderKind GetPlaceholderKind() const { return PlaceholderKind; }

protected:
	virtual void BeginPlay() override;

	UPROPERTY(VisibleAnywhere, Category = "GC|Placeholder")
	TObjectPtr<UBoxComponent> TriggerVolume;

	UPROPERTY(Transient)
	bool bLoggedThisOverlap = false;

	UFUNCTION()
	void OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult);

	UFUNCTION()
	void OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
		UPrimitiveComponent* OtherComp, int32 OtherBodyIndex);

	static bool bKitchenRebindHintLogged;
};
