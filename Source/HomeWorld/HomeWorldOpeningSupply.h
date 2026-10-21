// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldOpeningSupply.generated.h"

/** Dawn-chest and delivery-chest names. These are not the six RES_* carry slots. */
namespace HomeWorldOpeningMaterials
{
	inline const FName Wood = FName(TEXT("Wood"));
	inline const FName Herb = FName(TEXT("Herb"));
	inline const FName Stone = FName(TEXT("Stone"));
	inline const FName Silk = FName(TEXT("Silk"));
	inline const FName Metal = FName(TEXT("Metal"));
	inline const FName Fiber = FName(TEXT("Fiber"));
}

/** One field node. Wood, herb, or stone can deliver once. Silk, fiber, and metal cannot. */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldOpeningDeliveryNode : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldOpeningDeliveryNode();

	void SetMaterial(FName InMaterial) { Material = InMaterial; }
	FName GetMaterial() const { return Material; }
	bool IsDelivered() const { return bDelivered; }
	void MarkDelivered() { bDelivered = true; }

private:
	UPROPERTY()
	FName Material = NAME_None;

	UPROPERTY()
	bool bDelivered = false;
};

/**
 * Opening chest stock that is not the six-slot carry.
 * The dawn chest holds the first glider's wood, silk, and metal.
 * A delivery credits the matching wood, herb, or stone chest.
 */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldOpeningSupply : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldOpeningSupply();

	static bool IsDeliveryMaterial(FName Material);
	static AActor* SpawnDeliveryNode(UWorld* World, FName Material, const FVector& Location);

	/** Sets the dawn chest to one wood, one silk, and one metal. A crafted glider does not restock. */
	void StockDawnChest();
	bool HasDawnStock() const;
	int32 GetDawnCount(FName Material) const;
	bool TryCraftGlider();
	bool IsGliderCrafted() const { return bGliderCrafted; }

	/** Existing descent tests call this so they still measure steering. */
	void GrantCraftedForTest() { bGliderCrafted = true; }

	int32 GetDeliveryCount(FName Material) const;

	/** Fills the matching chest by 10 and spends the node. A second call on that node is refused. */
	bool TryDeliver(UHomeWorldOpeningDeliveryNode* Node);

private:
	UPROPERTY()
	int32 DawnWood = 0;

	UPROPERTY()
	int32 DawnSilk = 0;

	UPROPERTY()
	int32 DawnMetal = 0;

	UPROPERTY()
	bool bGliderCrafted = false;

	UPROPERTY()
	int32 DeliveryWood = 0;

	UPROPERTY()
	int32 DeliveryHerb = 0;

	UPROPERTY()
	int32 DeliveryStone = 0;
};
