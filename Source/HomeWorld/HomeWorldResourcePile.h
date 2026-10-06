// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HomeWorldGatherSiteTypes.h"
#include "HomeWorldResourcePile.generated.h"

class UBoxComponent;
class UHomeWorldInventorySubsystem;

/**
 * Base actor for gather nodes (world harvest). Blueprint BP_WoodPile etc. inherit.
 * NP-D: +1 gather via TryHarvest. A node emptied once stays empty; nothing refills it.
 */
// D19-A: non-Abstract so Editor Python can spawn VS_MVP gather markers (BP subclasses still optional for art).
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldResourcePile : public AActor
{
	GENERATED_BODY()

public:
	AHomeWorldResourcePile();

	/** Resource type — legacy ("Wood") or RES_*; normalized on harvest when GatherSiteKind is None. */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource")
	FName ResourceType;

	/** GC-A: Docs/GATHER_CRAFT site→RES map; overrides ResourceType when not None (den/camp/special stay Docs/21). */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource")
	EHomeWorldGatherSiteKind GatherSiteKind = EHomeWorldGatherSiteKind::None;

	/** Amount granted per harvest (SYS default +1). */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource", meta = (ClampMin = "1"))
	int32 AmountPerHarvest = 1;

	/**
	 * DEPRECATED (interview #11, 3A). No longer read by any code path. A successful
	 * harvest always empties the node for the rest of the session, whatever this is
	 * set to. Kept only so saved levels and Blueprints holding a value still load.
	 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource", meta = (DeprecatedProperty, DeprecationMessage = "No longer read. A harvested pile always stays empty for the rest of the session. Kept only so existing values still load."))
	bool bDepleteUntilDawn = true;

	/**
	 * DEPRECATED (interview #11, 3A). No longer read by any code path. Kept only so
	 * saved levels and Blueprints holding a value for it still load.
	 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Resource", meta = (ClampMin = "0.0", DeprecatedProperty, DeprecationMessage = "No longer read. Harvesting applies no cooldown. Kept only so existing values still load."))
	float HarvestCooldownSeconds = 0.f;

	/** Try harvest into inventory; returns false when depleted, on cooldown, or inventory full. */
	UFUNCTION(BlueprintCallable, Category = "Resource")
	bool TryHarvest(UHomeWorldInventorySubsystem* Inventory);

	UFUNCTION(BlueprintCallable, Category = "Resource")
	bool IsHarvestAvailable() const;

protected:
	UPROPERTY(VisibleAnywhere, Category = "Resource")
	TObjectPtr<UBoxComponent> OverlapVolume;

private:
	/** Runtime depletion. Despite the name nothing clears this any more; it means "emptied". */
	bool bDepletedUntilDawn = false;
	float CooldownRemaining = 0.f;
	/** Flowers site: next harvest yields RES_HERB when true (alternate with RES_FIBER / grass). */
	bool bFlowerNextHarvestIsHerb = false;

	FName ResolveHarvestResourceId();

	void TickCooldown(float DeltaTime);
	virtual void Tick(float DeltaSeconds) override;
};
