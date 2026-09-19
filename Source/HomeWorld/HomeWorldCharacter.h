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

	/** NP-C: true when TimeOfDay phase is Night or Dusk (spirit form; no free-flight). */
	UFUNCTION(BlueprintCallable, Category = "Form", meta = (DisplayName = "Is Spirit Form"))
	bool GetIsSpiritForm() const { return bIsSpiritForm; }

	/** Apply body/spirit form from current TimeOfDay phase. Callable from Blueprint for tests. */
	UFUNCTION(BlueprintCallable, Category = "Form", meta = (DisplayName = "Sync Form With Time Of Day"))
	void SyncFormWithTimeOfDay();

protected:
	virtual void PossessedBy(AController* NewController) override;

	/** FALLBACK scripted glide along CRUMB_* (no free-flight). */
	UPROPERTY(VisibleAnywhere, Category = "Transit|FALLBACK")
	TObjectPtr<UHomeWorldFallbackGlideComponent> FallbackGlideComponent;

	/** V1 soft pushback when leaving hero island bounds (no navmesh). */
	UPROPERTY(VisibleAnywhere, Category = "Walk|Bounds")
	TObjectPtr<UHomeWorldSoftBoundsComponent> SoftBoundsComponent;

	/** NP-C: spirit form flag — Night/Dusk true, Day/Dawn false. SYS reads via GetIsSpiritForm(). */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form")
	bool bIsSpiritForm = false;

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

	void ApplyFormForPhase(EHomeWorldTimeOfDayPhase Phase);
	/** Docs/27 NF2-A: soft glow + optional sound/particle when form actually changes. */
	void PlaySoftFormSwapFeedback(EHomeWorldTimeOfDayPhase Phase, bool bSpirit);
	UFUNCTION()
	void OnTimeOfDayPhaseChanged(EHomeWorldTimeOfDayPhase NewPhase);

	/** Net forward/right axis from the four directional keys. Used when using MoveForward/MoveBack/StrafeLeft/StrafeRight. */
	float MovementForwardAxis = 0.f;
	float MovementRightAxis = 0.f;

	EHomeWorldTimeOfDayPhase LastAppliedFormPhase = EHomeWorldTimeOfDayPhase::Day;

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
