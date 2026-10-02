// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "HomeWorldCampNightTypes.h"
#include "HomeWorldCampActor.generated.h"

class UTextRenderComponent;

/**
 * MUST #14/#16 - a person at the camp. Placed in the level so the night beat has something to
 * act on; without one of these in a `.umap` every calm count soft-latches.
 *
 * WHY A CHARACTER AND NOT A MESH. `Lib/02_Zones/combat/CAMP.json` lists
 * `modeling_an_actor_as_greybox_prop` under `rejects`. A guard you can walk through, or a
 * bedroll that counts as a person, would make the gate provable against geometry rather than
 * against someone - which is the same defect as a soft latch, one level down. A Character has a
 * capsule, a body and a presence, and is never possessed, so it takes no input and drives no
 * camera.
 *
 * WHY IT CARRIES NO SLEEP STATE. The calm state lives in `FHomeWorldCampActorCalm` on
 * `UHomeWorldSpiritStealthComponent` and is initialised from `HomeWorldCampNight::StartsAsleep`.
 * Duplicating it here would give the beat two sources of truth for "is this person asleep",
 * and the level copy would be the one nobody eases. This actor answers exactly one question to
 * the rest of the game: *is there actually someone here?*
 *
 * DISCOVERY. `FindCampActorInWorld` in HomeWorldSpiritStealthComponent.cpp matches, in order,
 * the editor actor label, then `GetName().Contains(Label)`, then `ActorHasTag(Label)`. That
 * first branch is `#if WITH_EDITOR` and never runs at runtime, so **the Actor tag is the only
 * reliable runtime path** - hence RefreshCampIdentity() in the constructor and OnConstruction.
 */
UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCampActor : public ACharacter
{
	GENERATED_BODY()

public:
	AHomeWorldCampActor();

	/** Which of the three this is. The guard wakes; both sleepers start asleep; the captive is held. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "CampNight")
	EHomeWorldCampRole CampRole = EHomeWorldCampRole::Sleeper;

	/** The NODE_ label this actor is discovered by, e.g. `NODE_GUARD`. Derived from CampRole. */
	UFUNCTION(BlueprintPure, Category = "CampNight")
	FText GetCampLabelText() const;

	/**
	 * Re-assert the tag and label for the current CampRole.
	 *
	 * Called from the constructor and OnConstruction so a placed instance is discoverable in the
	 * editor AND at runtime, and so flipping CampRole in the details panel cannot leave a stale
	 * tag behind pointing the gate at the wrong person.
	 */
	UFUNCTION(BlueprintCallable, Category = "CampNight")
	void RefreshCampIdentity();

protected:
	virtual void OnConstruction(const FTransform& Transform) override;
	virtual void BeginPlay() override;

	/** Greybox read only - enough to tell the guard from the sleepers from the captive at a glance. */
	UPROPERTY(VisibleAnywhere, Category = "CampNight")
	TObjectPtr<UTextRenderComponent> LabelText;
};