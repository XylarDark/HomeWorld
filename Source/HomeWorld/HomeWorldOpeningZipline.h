// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldOpeningZipline.generated.h"

class AHomeWorldCharacter;
class UStaticMeshComponent;

/** A greybox line from the cottage's second-floor perch to the fishing pond. */
UCLASS()
class HOMEWORLD_API AHomeWorldOpeningZipline : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldOpeningZipline();

	/** Perch feet and landing feet, in world centimeters. */
	UFUNCTION(BlueprintCallable, Category = "Opening|Zipline")
	void SetLine(FVector PerchFeet, FVector LandingFeet);

	/** Two ground directions away from the corner, and whether the stairs stand at the perch. */
	UFUNCTION(BlueprintCallable, Category = "Opening|Zipline")
	void SetStairs(FVector DirA, FVector DirB, bool bAtPerch);

	/** True when the press was at the perch and the ride started, or was already running. */
	bool TryRide(AHomeWorldCharacter* Character);

	virtual void Tick(float DeltaSeconds) override;

private:
	void BuildVisuals();

	UPROPERTY()
	FVector RideStart = FVector::ZeroVector;

	UPROPERTY()
	FVector RideEnd = FVector::ZeroVector;

	UPROPERTY()
	FVector StairA = FVector(0.f, -1.f, 0.f);

	UPROPERTY()
	FVector StairB = FVector(1.f, 0.f, 0.f);

	UPROPERTY()
	bool bStairsAtPerch = true;

	UPROPERTY()
	TObjectPtr<AHomeWorldCharacter> Rider;

	float RideDistance = 0.f;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> Perch;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> Cable;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> Step1;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> Step2;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> Step3;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> SideStep1;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> SideStep2;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> SideStep3;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> StartPole;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> EndPole;

	UPROPERTY()
	TObjectPtr<UStaticMeshComponent> EndPerch;
};
