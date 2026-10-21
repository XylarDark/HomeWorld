// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldOpeningReveal.generated.h"

class UBoxComponent;
class UStaticMeshComponent;

/** The yard comes into view while the player is still moving. The child runs to the spirit. */
UCLASS()
class HOMEWORLD_API AHomeWorldOpeningReveal : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldOpeningReveal();

	/** Fastest the pawn can move. Sprint is 585. Tea gates it, so the opening walk is 450. The race uses 585. */
	static constexpr float PlayerMaxSpeed = 585.f;

	/** The child runs at the kept homestead walk. The shorter path is what makes them earlier. */
	static constexpr float ChildRunSpeed = 450.f;

	/** One step along the ground. Stops on the goal. */
	static FVector StepToward(const FVector& From, const FVector& Goal, float MaxStep);

	/** True when the child reaches the spirit at the same time as the player, or sooner, at PlayerMaxSpeed. */
	static bool ChildArrivesFirst(float PlayerDistance, float ChildDistance);

	/** A point beside the spirit, on the side the child came from. The child stops here and stays visible. */
	static FVector StandNear(const FVector& From, const FVector& SpiritPoint, float StandOffCm);

	/** The child's race to the dog yard: out of their room, out the south door, onto the lawn, beside the lane. */
	static TArray<FVector> ChildRaceRoute(const FVector& DogPoint, float FloorZ);

	/** Hide the sphere and send the child after the player. False once it has already been claimed. */
	bool TryClaim(APawn* Player);

	UFUNCTION(BlueprintPure, Category = "Opening")
	bool IsSpiritVisible() const;

	/** Walk the partner through the south door to a spot beside the kettle. False if they are already going. */
	bool TryLeadPartner();

	/** After the tame, the child walks back through the north door into their room. */
	void BeginChildReturnHome();

	/** Opening night is solo. Drops the tutorial chase so the child does not follow. */
	void StopForOpeningNight();

	/** True once the partner has walked inside and stands waiting beside the counter. */
	UFUNCTION(BlueprintPure, Category = "Opening")
	bool IsPartnerWaiting() const { return bPartnerWaiting; }

	/** The world point the partner stands on at the counter. Read-only, for the in-editor quest suite. */
	UFUNCTION(BlueprintPure, Category = "Opening")
	FVector GetPartnerStandCm() const;

protected:
	virtual void BeginPlay() override;
	virtual void Tick(float DeltaSeconds) override;

	UFUNCTION()
	void OnCrestOverlap(
		UPrimitiveComponent* OverlappedComponent,
		AActor* OtherActor,
		UPrimitiveComponent* OtherComp,
		int32 OtherBodyIndex,
		bool bFromSweep,
		const FHitResult& SweepResult);

	/** Separate visibility blocker for the spirit. Disclaimed once the sphere is taken. */
	UPROPERTY()
	TObjectPtr<UBoxComponent> SpiritHit;

	UPROPERTY(VisibleAnywhere, Category = "Opening")
	TObjectPtr<UStaticMeshComponent> Spirit;

	UPROPERTY(VisibleAnywhere, Category = "Opening")
	TObjectPtr<UBoxComponent> Crest;

	UPROPERTY()
	TObjectPtr<AActor> Child;

	UPROPERTY()
	TObjectPtr<AActor> Partner;

	UPROPERTY()
	TObjectPtr<APawn> FollowTarget;

	bool bRunning = false;
	bool bClaimed = false;
	bool bFollowing = false;
	bool bPartnerLeading = false;
	bool bPartnerWaiting = false;
	bool bPartnerBlockLogged = false;
	bool bHomecoming = false;
	bool bChildLeading = false;
	bool bChildRacing = false;
	bool bChildAtYard = false;
	bool bChildGoHomeAfterTame = false;
	int32 PartnerLeg = 0;
	int32 ChildLeg = 0;
	TArray<FVector> PartnerPoints;
	TArray<FVector> ChildPoints;

	void FollowChild(float DeltaSeconds);
	void LeadPartner(float DeltaSeconds);
	void LeadChild(float DeltaSeconds);
	void BeginHomecoming();
	void BeginChildRace();
	void PlaceKettleCounter();
	AActor* FindTagged(const TCHAR* Tag) const;
	void FitInteractBounds(AActor* Actor) const;
};
