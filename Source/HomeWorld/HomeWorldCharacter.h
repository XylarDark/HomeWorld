// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AbilitySystemInterface.h"
#include "GameFramework/Character.h"
#include "InputActionValue.h"
#include "HomeWorldMealTypes.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "HomeWorldCharacter.generated.h"

struct FOnAttributeChangeData;
class USoundBase;
class UParticleSystem;
class AActor;
class UAbilitySystemComponent;
class UAttributeSet;
class UGameplayAbility;
class USpringArmComponent;
class UCameraComponent;
class UInputAction;
class UInputMappingContext;
class UHomeWorldFallbackGlideComponent;
class UHomeWorldSoftBoundsComponent;
class UHomeWorldTraversalComponent;
class UHomeWorldSpiritStealthComponent;

UCLASS(Blueprintable)
/**
 * Third-person character: movement and camera in C++; mesh and Animation Blueprint in Blueprint.
 * AnimBP can use GetVelocity() or GetCharacterMovement()->Velocity for Idle/Locomotion blend.
 */
class HOMEWORLD_API AHomeWorldCharacter : public ACharacter, public IAbilitySystemInterface
{
	GENERATED_BODY()

public:
	AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer);

	virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

	/** Trace forward and offer tame food on beast pad (V4). Day/body only. Called from GA_Interact before harvest. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Tame Beast In Front"))
	bool TryTameBeastInFront();

	/** Trace forward and heal spirit wisp (V6). Night/spirit only. Used by GA_Heal and GA_Interact. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Heal Spirit In Front"))
	bool TryHealSpiritInFront();

	/** Trace forward and nurture homestead target (V7). Night/spirit only. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Nurture In Front"))
	bool TryNurtureInFront();

	/** PL-C: Trace forward Stored prop — deposit inventory→stored or withdraw. Day/body. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Store Transfer In Front"))
	bool TryStoreTransferInFront();

	/** GC-B: Trace forward craft station (hub / campfire / kitchen). Day/body. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Craft In Front"))
	bool TryCraftInFront();

	/** CD-A: Trace forward minigame stub or boss seal (planet only). */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Minigame In Front"))
	bool TryMinigameInFront();

	/** CD-A: Trace forward boss seal stub when inside placeholder volume. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Boss Seal In Front"))
	bool TryBossSealInFront();

	/** Trace forward and harvest the first resource pile hit; adds RES_* +1 to six-slot inventory. Called from GA_Interact / UHomeWorldInteractAbility. */
	UFUNCTION(BlueprintCallable, Category = "Interaction", meta = (DisplayName = "Try Harvest In Front"))
	bool TryHarvestInFront();

	/** FALLBACK V2: start scripted CRUMB glide when near GP_GlideStart / glider perch. Day/body only. */
	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK", meta = (DisplayName = "Try Start Fallback Glide"))
	bool TryStartFallbackGlide();

	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK", meta = (DisplayName = "Cancel Fallback Glide"))
	void CancelFallbackGlide();

	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK", meta = (DisplayName = "Is Fallback Gliding"))
	bool IsFallbackGliding() const;

	/** Try shrine portal transit on hit actor (V5 both ways). */
	UFUNCTION(BlueprintCallable, Category = "Portal|FALLBACK", meta = (DisplayName = "Try Shrine Portal Interact"))
	bool TryShrinePortalInteract();

	/** Trace from camera via GetPlacementTransform and spawn PlaceActorClass at hit. Called from GA_Place / UHomeWorldPlaceAbility. */
	UFUNCTION(BlueprintCallable, Category = "Build|Placement", meta = (DisplayName = "Try Place At Cursor"))
	bool TryPlaceAtCursor();

	/** Request astral death: advance to dawn and respawn at start (same as hw.AstralDeath). Call from in-game astral-defeat logic or bind to IA_AstralDeath for testing. See ASTRAL_DEATH_AND_DAY_SAFETY.md. */
	UFUNCTION(BlueprintCallable, Category = "HomeWorld|Astral", meta = (DisplayName = "Request Astral Death"))
	void RequestAstralDeath();

	/** Day restoration: consume a meal (day only). Restores Health and sets day buff for next night; sets LastMealTriggered on PlayerState. No effect at night. List 57: use MealType for in-world breakfast/lunch/dinner triggers. */
	UFUNCTION(BlueprintCallable, Category = "Day Restoration", meta = (DisplayName = "Consume Meal Restore"))
	bool ConsumeMealRestore(EMealType MealType = EMealType::Breakfast);

	/** Report death and add this character to the spirit roster (Day 21). Call from Blueprint or game code when Health reaches 0 (e.g. GAS effect or damage handler). */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Report Death And Add Spirit"))
	void ReportDeathAndAddSpirit();

	/** Unique ID used when adding this character as a spirit (actor name + unique ID). */
	UFUNCTION(BlueprintCallable, Category = "Spirit", meta = (DisplayName = "Get Spirit Id For Death"))
	FName GetSpiritIdForDeath();

	/** T0 #9: true only when named spirit gates grant form (not phase alone). */
	UFUNCTION(BlueprintCallable, Category = "Form", meta = (DisplayName = "Is Spirit Form"))
	bool GetIsSpiritForm() const { return bIsSpiritForm; }

	/** T0 #9: sleep gate granted (bed path). Default false until #11. */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Is Spirit Sleep Gate Granted"))
	bool IsSpiritSleepGateGranted() const { return bSpiritSleepGateGranted; }

	/** T0 #7 hook: rune unlock before bed→spirit. Default false until #7. */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Is Rune Gate Unlocked"))
	bool IsRuneGateUnlocked() const { return bRuneGateUnlocked; }

	/** T0 #7: unlock/clear rune gate (no spirit until sleep gate also granted). */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Set Rune Gate Unlocked"))
	void SetRuneGateUnlocked(bool bUnlocked);

	/**
	 * T0 #11 hook: grant sleep gate then sync form.
	 * Spirit still requires rune gate (#7). Does not invent a second form service.
	 */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Grant Spirit Sleep Gate"))
	void GrantSpiritSleepGate();

	/** Clear sleep gate (Day/Dawn / wake). */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Clear Spirit Sleep Gate"))
	void ClearSpiritSleepGate();

	/** Named gates: sleep + rune. Phase alone never grants spirit (T0 TOD_NIGHT_HOME). */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Can Enter Spirit Form"))
	bool CanEnterSpiritForm() const;

	/** Day body verbs (sprint/mantle/craft-day path): Day or Dawn only. Off at Dusk/Night. */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Are Day Body Abilities Allowed"))
	bool AreDayBodyAbilitiesAllowed() const;

	/** Apply body/spirit form from current TimeOfDay phase + named gates. Callable from Blueprint for tests. */
	UFUNCTION(BlueprintCallable, Category = "Form", meta = (DisplayName = "Sync Form With Time Of Day"))
	void SyncFormWithTimeOfDay();

	/**
	 * T0 #1 NODE_WAKE: emit named homestead start-day wake beat (TOD_DAY / FORM_BODY / CAM_T0_WAKE).
	 * Extends existing PlayerStart / UHomeWorldTimeOfDaySubsystem hooks -- no parallel wake service (Arch B).
	 * Not PlayerStart alone; not PROXY SM_ProxyWakeMarker; not bed->Dawn alone (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "Wake|T0", meta = (DisplayName = "Try Emit NODE_WAKE Start-Day Beat"))
	void TryEmitNodeWakeStartDayBeat();

	/**
	 * T0 #2 NODE_KETTLE: brew tea from herbs (RES_HERB) via existing inventory + day-verb sprint gate.
	 * Extends inventory / Traversal day-verb hooks -- no parallel tea service, no new schema (Arch B).
	 * Not PROXY SM_ProxyKettle alone; not meal-BP-as-tea; not ungated sprint alone (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "Kettle|T0", meta = (DisplayName = "Try Brew NODE_KETTLE Tea"))
	bool TryBrewNodeKettleTea();

	/** Trace/tag NODE_KETTLE / Kettle interact -> TryBrewNodeKettleTea (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "Kettle|T0", meta = (DisplayName = "Try NODE_KETTLE Interact In Front"))
	bool TryNodeKettleInteractInFront();

	/** True while tea sprint gate is active (TOD_DAY / FORM_BODY, within ~half-day window). */
	UFUNCTION(BlueprintCallable, Category = "Kettle|T0", meta = (DisplayName = "Is Tea Sprint Gate Active"))
	bool IsTeaSprintGateActive() const;

	/**
	 * T0 #3 NODE_PLANT_SLOT: day plant given herb (RES_HERB) into plant slot.
	 * Extends HomeWorldNurtureTarget / N1 / inventory -- no parallel plant service, no new schema (Arch B).
	 * Not GP_N1_Crop nurture-only; not PROXY SM_ProxyPlantSlot alone; not TryNurtureInFront (closed_fail).
	 * Marks same slot identity later #12 uses -- does NOT implement #12.
	 */
	UFUNCTION(BlueprintCallable, Category = "Plant|T0", meta = (DisplayName = "Try Plant NODE_PLANT_SLOT Herb"))
	bool TryPlantNodePlantSlotHerb();

	/** Trace/tag NODE_PLANT_SLOT / PlantSlot / N1 interact -> TryPlantNodePlantSlotHerb (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "Plant|T0", meta = (DisplayName = "Try NODE_PLANT_SLOT Interact In Front"))
	bool TryNodePlantSlotInteractInFront();

	/** True if N1 NODE_PLANT_SLOT has been day-planted with given herb this session. */
	UFUNCTION(BlueprintCallable, Category = "Plant|T0", meta = (DisplayName = "Is NODE_PLANT_SLOT Day Planted"))
	bool IsNodePlantSlotDayPlanted() const;

	/**
	 * T0 #4 NODE_BACKPACK: equip backpack -> inventory access gate.
	 * Extends existing UHomeWorldInventorySubsystem -- no parallel inventory service, no new schema (Arch B).
	 * Not inventory-lite alone; not PROXY SM_ProxyBackpack alone (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "Backpack|T0", meta = (DisplayName = "Try Equip NODE_BACKPACK"))
	bool TryEquipNodeBackpack();

	/** Trace/tag NODE_BACKPACK / Backpack interact -> TryEquipNodeBackpack (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "Backpack|T0", meta = (DisplayName = "Try NODE_BACKPACK Interact In Front"))
	bool TryNodeBackpackInteractInFront();

	/** True after NODE_BACKPACK equip latch this session. */
	UFUNCTION(BlueprintCallable, Category = "Backpack|T0", meta = (DisplayName = "Is Backpack Equipped"))
	bool IsBackpackEquipped() const { return bBackpackEquipped; }

	/**
	 * Inventory open/use gated by backpack equip latch (existing inventory-lite slots).
	 * Ungated inventory-lite alone = closed_fail for MUST #4.
	 */
	UFUNCTION(BlueprintCallable, Category = "Backpack|T0", meta = (DisplayName = "Try Open Inventory Gated"))
	bool TryOpenInventoryGated();


	/**
	 * T0 #6 NODE_FIELD_GATHER: field herb/seed collect near landing (CAM_T0_FIELD).
	 * Extends existing inventory RES_HERB / RES_SEED -- no parallel gather service, no new schema (Arch B).
	 * Not dress-only; not GP_Store alone; not PROXY SM_ProxyFieldGather; not NODE_PLANT_SLOT (#3);
	 * not ungated hw.Gather.Flowers alone (those = closed_fail). Glide #5 cite only.
	 */
	UFUNCTION(BlueprintCallable, Category = "FieldGather|T0", meta = (DisplayName = "Try Collect NODE_FIELD_GATHER"))
	bool TryCollectNodeFieldGather();

	/** Trace/tag NODE_FIELD_GATHER / FieldGather interact -> TryCollectNodeFieldGather (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "FieldGather|T0", meta = (DisplayName = "Try NODE_FIELD_GATHER Interact In Front"))
	bool TryNodeFieldGatherInteractInFront();

	/** True after NODE_FIELD_GATHER field collect latch this session. */
	UFUNCTION(BlueprintCallable, Category = "FieldGather|T0", meta = (DisplayName = "Is Field Gather Collected"))
	bool IsFieldGatherCollected() const { return bFieldGatherCollected; }

	/**
	 * T0 #7 NODE_RUNE: day field-path rune unlock interact -> SetRuneGateUnlocked.
	 * Prefer existing gate hooks (bRuneGateUnlocked / CanEnterSpiritForm) -- no parallel form service (Arch B).
	 * Not PROXY SM_ProxyRune alone; not spirit on phase alone; bed->spirit without unlock = closed_fail.
	 */
	UFUNCTION(BlueprintCallable, Category = "Rune|T0", meta = (DisplayName = "Try Unlock NODE_RUNE"))
	bool TryUnlockNodeRune();

	/** Trace/tag NODE_RUNE / Rune interact -> TryUnlockNodeRune (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "Rune|T0", meta = (DisplayName = "Try NODE_RUNE Interact In Front"))
	bool TryNodeRuneInteractInFront();

	/**
	 * T0 #8 NODE_DAY_CAMP: day camp cartoon eject -> EJECT_HOME (launch->glider->home).
	 * Prefer existing UHomeWorldFallbackGlideComponent::StartGlideHome -- no parallel eject service (Arch B).
	 * Not FALLBACK island->planet StartGlide alone; not PROXY SM_ProxyDayCamp; not convert stub;
	 * not script-only GP_RS_HumanoidCamp* (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "DayCamp|T0", meta = (DisplayName = "Try Eject NODE_DAY_CAMP"))
	bool TryEjectNodeDayCamp();

	/** Trace/tag NODE_DAY_CAMP / DayCamp interact -> TryEjectNodeDayCamp (world beat, not PROXY alone). */
	UFUNCTION(BlueprintCallable, Category = "DayCamp|T0", meta = (DisplayName = "Try NODE_DAY_CAMP Interact In Front"))
	bool TryNodeDayCampInteractInFront();

	/** True after NODE_DAY_CAMP EJECT_HOME latch this session. */
	UFUNCTION(BlueprintCallable, Category = "DayCamp|T0", meta = (DisplayName = "Is Day Camp Eject Triggered"))
	bool IsDayCampEjectTriggered() const { return bDayCampEjectTriggered; }

	/**
	 * T0 #10 planetside night boot home: Night w/o bed + FORM_BODY -> EJECT_HOME via StartGlideHome.
	 * Prefer existing StartGlideHome (bAllowNightPhase) -- no parallel eject service (Arch B).
	 * Distinct from MUST #8 TryEjectNodeDayCamp / hw.DayCamp.Eject (day-camp cartoon).
	 * Not FALLBACK StartGlide / TryStartFallbackGlide down; not soft-kidnap-as-boot; cite #9 TOD_NIGHT_HOME law (do not re-Act #9).
	 */
	UFUNCTION(BlueprintCallable, Category = "Planetside|T0", meta = (DisplayName = "Try Boot Planetside Night Home"))
	bool TryBootPlanetsideNightHome();

	/** True after planetside night NODE_GLIDER EJECT_HOME boot latch this session. */
	UFUNCTION(BlueprintCallable, Category = "Planetside|T0", meta = (DisplayName = "Is Planetside Night Boot Triggered"))
	bool IsPlanetsideNightBootTriggered() const { return bPlanetsideNightBootTriggered; }

	/**
	 * T0 #11 NODE_BED: bed sleep-gate -> spirit (after NODE_RUNE).
	 * Prefer existing GrantSpiritSleepGate / CanEnterSpiritForm / ApplyFormForPhase -- no parallel form service (Arch B).
	 * Requires IsRuneGateUnlocked (#7). Phase-alone / spirit w/o bed+rune / soft-kidnap = closed_fail. #9 w/o bed stay FORM_BODY.
	 */
	UFUNCTION(BlueprintCallable, Category = "Bed|T0", meta = (DisplayName = "Try Bed Sleep Spirit"))
	bool TryBedSleepSpirit();

	/** True after NODE_BED bed->spirit latch this session (sleep+rune). */
	UFUNCTION(BlueprintCallable, Category = "Bed|T0", meta = (DisplayName = "Is Bed Spirit Granted"))
	bool IsBedSpiritGranted() const { return bBedSpiritGranted; }

	/** MV-A: parkour-lite mantle/vault (body, day). */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A", meta = (DisplayName = "Try Mantle Or Vault"))
	bool TryMantleOrVault();

	/** MV-A: spirit blink toward shrine/anchor tags (night/spirit). */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A", meta = (DisplayName = "Try Spirit Blink"))
	bool TrySpiritBlink();

	virtual void Jump() override;

protected:
	virtual void PossessedBy(AController* NewController) override;

	/** FALLBACK scripted glide along CRUMB_* (no free-flight). */
	UPROPERTY(VisibleAnywhere, Category = "Transit|FALLBACK")
	TObjectPtr<UHomeWorldFallbackGlideComponent> FallbackGlideComponent;

	/** V1 soft pushback when leaving hero island bounds (no navmesh). */
	UPROPERTY(VisibleAnywhere, Category = "Walk|Bounds")
	TObjectPtr<UHomeWorldSoftBoundsComponent> SoftBoundsComponent;

	/** MV-A: sprint / mantle / blink / mount boost on single CMC. */
	UPROPERTY(VisibleAnywhere, Category = "Movement|MV-A")
	TObjectPtr<UHomeWorldTraversalComponent> TraversalComponent;

	/** SS-A: spirit lit / alert stub (spirit form only). */
	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-A")
	TObjectPtr<UHomeWorldSpiritStealthComponent> SpiritStealthComponent;

	/** T0 #9: spirit form flag — granted only via named gates (sleep + rune), not phase alone. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form")
	bool bIsSpiritForm = false;

	/** T0 #11: bed/sleep gate. Cleared on Day/Dawn. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form|Gates")
	bool bSpiritSleepGateGranted = false;

	/** T0 #7: rune unlock gate. Set via TryUnlockNodeRune / hw.Rune.Unlock (NODE_RUNE). */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form|Gates")
	bool bRuneGateUnlocked = false;

	/**
	 * Docs/27 NF2-A: optional soft handmade sting on body↔spirit form swap.
	 * Null = log + glow pulse only (no asset required for evidence).
	 */
	UPROPERTY(EditDefaultsOnly, Category = "Form|Feel")
	TObjectPtr<USoundBase> SoftFormSwapSound;

	/** Optional soft particle (Cascade). Null = glow pulse only. */
	UPROPERTY(EditDefaultsOnly, Category = "Form|Feel")
	TObjectPtr<UParticleSystem> SoftFormSwapParticles;

	/** Ability system; used for GAS combat and attributes. */
	UPROPERTY(VisibleAnywhere, Category = "Abilities")
	TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

	/** Default attribute set (e.g. Health, Stamina). Subclass or add more in Blueprint. */
	UPROPERTY(VisibleAnywhere, Category = "Abilities")
	TObjectPtr<UAttributeSet> AttributeSet;

	/** Ability classes granted at spawn (e.g. 3 survivor skills). Assign in Blueprint defaults; no abilities granted if empty. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TArray<TSubclassOf<UGameplayAbility>> DefaultAbilities;

	/** Spring arm attached to capsule; camera follows controller rotation. */
	UPROPERTY(VisibleAnywhere, Category = "Camera")
	TObjectPtr<USpringArmComponent> CameraBoom;

	/** Follow camera attached to spring arm. */
	UPROPERTY(VisibleAnywhere, Category = "Camera")
	TObjectPtr<UCameraComponent> FollowCamera;

	/** Spring arm length (distance from character to camera). Tune in Editor. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "100.0", ClampMax = "2000.0"))
	float TargetArmLength = 400.0f;

	/** Follow camera field of view (degrees). */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "60.0", ClampMax = "120.0"))
	float CameraFOV = 90.0f;

	/** Minimum camera pitch (degrees). Prevents camera from going below horizon. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "-89.0", ClampMax = "0.0"))
	float MinPitch = -70.0f;

	/** Maximum camera pitch (degrees). Prevents camera from flipping over the top. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "0.0", ClampMax = "89.0"))
	float MaxPitch = 20.0f;

	/** Move input action (Axis2D fallback). Prefer the four directional actions below when available. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> MoveAction;

	/** Look input action (Axis2D: mouse delta). Assign in Editor or Blueprint defaults. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> LookAction;

	/** Optional: W key. When set with the other three, used for camera-relative movement (no IMC modifiers). */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> MoveForwardAction;

	/** Optional: S key. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> MoveBackAction;

	/** Optional: A key. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> StrafeLeftAction;

	/** Optional: D key. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> StrafeRightAction;

	/** Default mapping context (WASD + Mouse). Assign in Editor or Blueprint defaults. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputMappingContext> DefaultMappingContext;

	/** Primary attack (e.g. Left Mouse). Triggers PrimaryAttackAbilityClass if set. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> PrimaryAttackAction;

	/** Dodge/Sprint (e.g. Shift). Triggers DodgeAbilityClass if set. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> DodgeAction;

	/** Interact/Use (e.g. E). Triggers InteractAbilityClass if set. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> InteractAction;

	/** Place/Build (e.g. P). Triggers PlaceAbilityClass if set. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> PlaceAction;

	/** Optional: trigger astral death (dawn + respawn) for testing. Assign IA_AstralDeath or leave null. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> AstralDeathAction;

	/** Second spirit ability (e.g. R). Triggers SpiritShieldAbilityClass if set; night-only. */
	UPROPERTY(EditDefaultsOnly, Category = "Input|Abilities")
	TObjectPtr<UInputAction> SpiritShieldAction;

	/** Called when Health attribute changes (GAS). When Health <= 0 at night, invokes RequestAstralDeath so lethal astral damage triggers dawn + respawn. */
	void OnHealthChanged(const struct FOnAttributeChangeData& Data);

	/** Ability class to activate when PrimaryAttackAction fires. Assign in Blueprint; should match one of DefaultAbilities. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<UGameplayAbility> PrimaryAttackAbilityClass;

	/** Ability class to activate when DodgeAction fires. Assign in Blueprint; should match one of DefaultAbilities. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<UGameplayAbility> DodgeAbilityClass;

	/** Ability class to activate when InteractAction fires. Assign in Blueprint; should match one of DefaultAbilities. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<UGameplayAbility> InteractAbilityClass;

	/** Ability class to activate when PlaceAction fires. Assign in Blueprint; should match one of DefaultAbilities. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<UGameplayAbility> PlaceAbilityClass;

	/** Ability class to activate when SpiritShieldAction fires (e.g. GA_SpiritShield). Night-only; assign in Blueprint. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<UGameplayAbility> SpiritShieldAbilityClass;

	/** Actor class to spawn when placing (e.g. BP_BuildOrder_Wall). Assign in Blueprint; if null, placement logs and returns false. */
	UPROPERTY(EditDefaultsOnly, Category = "Abilities")
	TSubclassOf<AActor> PlaceActorClass;

	/** Scale applied to look input (mouse sensitivity). */
	UPROPERTY(EditDefaultsOnly, Category = "Input", meta = (ClampMin = "0.01", ClampMax = "10.0"))
	float LookSensitivity = 1.0f;

	/** Yaw rotation rate (deg/s) when orienting to movement. Tune in Editor for snappier or smoother turning. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "1440.0"))
	float RotationRateYaw = 720.0f;

	/** Offset (degrees) applied to the mesh relative rotation so mesh forward matches movement direction. Default -90: skeleton forward was 90° right of capsule forward. */
	UPROPERTY(EditDefaultsOnly, Category = "Mesh", meta = (ClampMin = "-180.0", ClampMax = "180.0"))
	float MeshForwardYawOffset = -90.0f;

	/** Capsule radius (cm). Human-sized default; override in Blueprint for different characters. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "200.0"))
	float CapsuleRadius = 42.0f;

	/** Capsule half-height (cm). Human-sized default; override in Blueprint for different characters. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "500.0"))
	float CapsuleHalfHeight = 88.0f;

	/** Max distance (cm) to GP_GlideStart / CRUMB_Depart_Lookout / GlideStart tag to allow interact glide. */
	UPROPERTY(EditDefaultsOnly, Category = "Transit|FALLBACK", meta = (ClampMin = "50.0", ClampMax = "2000.0"))
	float GlideStartProximityCm = 450.0f;

	virtual void BeginPlay() override;
	virtual void Tick(float DeltaTime) override;

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);

	/** Key down: add to axis. */
	void OnMoveForwardPressed(const FInputActionValue& Value);
	void OnMoveBackPressed(const FInputActionValue& Value);
	void OnStrafeLeftPressed(const FInputActionValue& Value);
	void OnStrafeRightPressed(const FInputActionValue& Value);
	/** Key up: subtract from axis so movement stops on release. */
	void OnMoveForwardReleased(const FInputActionValue& Value);
	void OnMoveBackReleased(const FInputActionValue& Value);
	void OnStrafeLeftReleased(const FInputActionValue& Value);
	void OnStrafeRightReleased(const FInputActionValue& Value);

	/** Activate ability by input (used for Primary Attack, Dodge, Interact, Place). */
	void OnPrimaryAttackTriggered(const FInputActionValue& Value);
	void OnDodgeTriggered(const FInputActionValue& Value);
	void OnInteractTriggered(const FInputActionValue& Value);
	void OnPlaceTriggered(const FInputActionValue& Value);
	void OnAstralDeathTriggered(const FInputActionValue& Value);
	void OnSpiritShieldTriggered(const FInputActionValue& Value);
	void OnSprintStarted(const FInputActionValue& Value);
	void OnSprintCompleted(const FInputActionValue& Value);

	void ApplyFormForPhase(EHomeWorldTimeOfDayPhase Phase);
	/** Docs/27 NF2-A: soft glow + optional sound/particle when form actually changes. */
	void PlaySoftFormSwapFeedback(EHomeWorldTimeOfDayPhase Phase, bool bSpirit);
	UFUNCTION()
	void OnTimeOfDayPhaseChanged(EHomeWorldTimeOfDayPhase NewPhase);

	/** Net forward/right axis from the four directional keys. Used when using MoveForward/MoveBack/StrafeLeft/StrafeRight. */
	float MovementForwardAxis = 0.f;
	float MovementRightAxis = 0.f;

	EHomeWorldTimeOfDayPhase LastAppliedFormPhase = EHomeWorldTimeOfDayPhase::Day;

	/** T0 #1: once per Day phase - NODE_WAKE start-day beat already emitted. */
	bool bNodeWakeEmittedForCurrentDay = false;

	/** T0 #2: world-time end of tea-gated sprint (~half day). 0 = inactive. */
	float TeaSprintEndWorldTime = 0.f;

	/** T0 #2: tea sprint duration seconds (~half day stub; night stub is 120s). */
	UPROPERTY(EditDefaultsOnly, Category = "Kettle|T0", meta = (ClampMin = "1.0"))
	float TeaSprintHalfDaySeconds = 60.f;

	/** T0 #4: backpack equip latch -- inventory open/use requires this (not inventory-lite alone). */
	bool bBackpackEquipped = false;
	bool bFieldGatherCollected = false;

	/** T0 #8: day camp EJECT_HOME latch (NODE_DAY_CAMP cartoon eject this session). */
	bool bDayCampEjectTriggered = false;

	/** T0 #10: planetside night glider boot home latch (NODE_GLIDER EJECT_HOME this session). */
	bool bPlanetsideNightBootTriggered = false;

	/** T0 #11: bed->spirit latch after GrantSpiritSleepGate + rune (NODE_BED this session). */
	bool bBedSpiritGranted = false;

	/** VP-C PA-06: on-screen interact feedback (debug overlay). */
	void ShowInteractFeedback(const FString& Message, FColor Color = FColor::Green) const;
	bool TraceInteractHit(FHitResult& OutHit) const;
	bool FindInteractTargetInCone(FHitResult& OutHit) const;
	static bool ActorHasInteractableComponent(const AActor* Actor);
	AActor* GetInteractTargetActor(const FHitResult& Hit) const;
	FString BuildInteractRangeHint(AActor* Target) const;
	void UpdateInteractRangeHint(float DeltaTime);

	UPROPERTY(EditDefaultsOnly, Category = "Interaction|Feedback", meta = (ClampMin = "50.0", ClampMax = "1000.0"))
	float InteractTraceLengthCm = 280.f;

	UPROPERTY(EditDefaultsOnly, Category = "Interaction|Feedback", meta = (ClampMin = "0.1", ClampMax = "2.0"))
	float InteractHintRefreshSeconds = 0.35f;

	float InteractHintAccumulator = 0.f;
};
