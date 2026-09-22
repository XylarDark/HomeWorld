// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "HomeWorldSpiritLitVolume.h"
#include "HomeWorldSpiritNpcTorchCarrier.generated.h"

class UPointLightComponent;
class UStaticMeshComponent;
class UTextRenderComponent;

/**
 * SS-B: labeled NPC torch prop + moving (or static) NpcTorch lit volume on planet path.
 * Overlap / reveal behavior inherited from AHomeWorldSpiritLitVolume.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldSpiritNpcTorchCarrier : public AHomeWorldSpiritLitVolume
{
	GENERATED_BODY()

public:
	AHomeWorldSpiritNpcTorchCarrier();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stealth|SS-B")
	bool bPatrolEnabled = true;

	/** Half-length of back-and-forth patrol along PatrolAxis (cm). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stealth|SS-B", meta = (ClampMin = "0"))
	float PatrolHalfLength = 280.f;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stealth|SS-B")
	FVector PatrolAxis = FVector(1.f, 0.f, 0.f);

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Stealth|SS-B", meta = (ClampMin = "0"))
	float PatrolSpeed = 0.35f;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-B")
	TObjectPtr<UStaticMeshComponent> TorchMesh;

	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-B")
	TObjectPtr<UPointLightComponent> TorchLight;

	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-B")
	TObjectPtr<UTextRenderComponent> LabelText;

	FVector PatrolOrigin = FVector::ZeroVector;
	float PatrolPhase = 0.f;
};
