// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AbilitySystemInterface.h"
#include "GameFramework/Character.h"
#include "InputActionValue.h"
#include "HomeWorldMealTypes.h"
#include "HomeWorldStrokeReportComponent.h"
#include "HomeWorldQuestLog.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "HomeWorldOpeningSupply.h"
#include "HomeWorldBonkArc.h"
#include "HomeWorldOpeningHover.h"

/** Where a family member stands. One place, not a dialogue tree. */
UENUM(BlueprintType)
enum class EHomeWorldFamilyPlace : uint8
{
	ByBed,
	InGarden,
	Away
};

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
class UHomeWorldStressComponent;
class UHomeWorldTraversalComponent;
class UHomeWorldSpiritStealthComponent;
class UHomeWorldCloudWisp;
class UHomeWorldVirtueComponent;
class AHomeWorldEasePad;
class AHomeWorldParadoxToy;
class UTextRenderComponent;

/** One in-reach actor and how far its screen point sits from the look point, in NDC squared. */
struct FOpeningLookCandidate
{
	AActor* Actor = nullptr;
	float LookDistSq = 0.f;
};

UCLASS(Blueprintable)
/**
 * Third-person character: movement and camera in C++; mesh and Animation Blueprint in Blueprint.
 * AnimBP can use GetVelocity() or GetCharacterMovement()->Velocity for Idle/Locomotion blend.
 */
class HOMEWORLD_API AHomeWorldCharacter : public ACharacter, public IAbilitySystemInterface
{
	GENERATED_BODY()

public:
	friend AActor* HomeWorldOpeningHover::PickFrom(AHomeWorldCharacter* Character, TFunctionRef<void(TFunctionRef<void(AActor*)>)> ForEach);
	AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer);

	/** Half-extent of the aim box around screen center, in normalized screen space. The drawn frame uses this. */
	static constexpr float OpeningViewCenterNdc = 0.3f;

	/** Resting camera pitch at spawn, in degrees. Positive is up. */
	static constexpr float OpeningLookRestPitch = -12.f;

	/** The aim rectangle is a development view of that box. Off after the 2026-10-21 pass. */
	static constexpr bool bDrawOpeningAimBox = false;

	static bool IsOpeningInteractInReach(float Dist2DCm);
	static bool IsOpeningLookInside(float NdcX, float TargetNdcY, float LookNdcY);
	static bool IsInFrontOfBody(const FVector& FlatForward, const FVector& FlatToTarget);
	static AActor* PickOpeningLookTarget(AActor* Perch, const TArray<FOpeningLookCandidate>& Candidates);
	float GetOpeningLookCenterNdcY() const;

	/** Press E. Registered verbs run in spec priority for this level's chain. */
	bool ResolveOpeningTarget();

	/** A test world has no map name. Production leaves this unset and reads the level. */
	void SetInteractChainForTest(bool bSizeTest);
	bool UsesSizeTestInteractChain() const;

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

	/** Size-test spirit: hide the sphere, show the shoulder wisp, and send the child after the player. */
	bool TryOpeningSpiritInFront();

	/** Size-test partner: interact sends them inside, to the kettle. A second press takes the armor gift. */
	bool TryPartnerLeadInside();

	/** Party invite. The existing interact, at home, after the rescue. A second press sends that person home. */
	bool TryPartyInviteInFront();

	/** Size-test stations: the kitchen consumable table (one output) and the armory table. */
	bool TryOpeningStationInFront();

	/** Beat 4 dog: eased Wrath takes the mixed herb. Too close or too fast knocks you back. */
	UFUNCTION(BlueprintCallable, Category = "Opening|T0", meta = (DisplayName = "Try Opening Dog In Front"))
	bool TryOpeningDogInFront();
	bool TryOpeningFish();

	/** Size-test bed: sleep grants spirit and stays on the island. Night alone does not. */
	bool TryOpeningBedInFront();

	/** Opening island night. The encounter HUD stays off until a later night. */
	bool IsOpeningNightSpirit() const { return bOpeningNightSpirit; }

	/** Size-test night: the click heart on a world wisp collects it. */
	bool TryOpeningNightSetInFront();

	/** Size-test night: deposit a damaged wisp in the hot springs with one mixed herb. */
	bool TryOpeningHotSpringHealInFront();

	/** Dawn chest: one wood, one silk, one metal. Not the six-slot carry. */
	void StockOpeningDawnChest();
	bool TryCraftOpeningGlider();
	bool IsOpeningGliderCrafted() const;
	void GrantOpeningGliderForTest();
	int32 GetOpeningDawnCountForTest(FName Material) const;
	int32 GetOpeningDeliveryCountForTest(FName Material) const;

	/** E on a wood, herb, or stone node. One delivery, then that node refuses. */
	bool TryOpeningDeliveryInFront();

	/** A matched step on a guard pad. The fourth step sleeps that guard. A wrong step does not. */
	bool TryCommitOpeningGuardPad(AHomeWorldEasePad* Pad, EHomeWorldStrokeStep Played);

	/** Wait while the pad still offers Grace. The glide home runs. The guard stays awake. */
	bool TryWaitOpeningGuardPad(AHomeWorldEasePad* Pad);

	/** Spirit, within the opening reach, and that guard is still awake. The light box is not the reach. */
	bool TryReachOpeningGuard(AActor* Guard);

	/** One E on the opening shrine after the three sleeps. A missing guard refuses. */
	bool TryOpeningShrineInFront();

	/** Finish the bound pads, spawn the captive and the shrine, and do not press E. */
	void RunOpeningShrineStop();

	void ApplyOpeningGuardSleep(AHomeWorldEasePad* Pad);
	bool TryDeliverOpeningNode(AActor* Node);

	/** Fast-forward and test seed. One healed follower. Does not start a heal timer. */
	void SeedOpeningHealedWisp();

	/** Test hooks: seed the wisp loop and print the tracker the HUD is showing. */
	void DebugSeedOpeningWispLoop(int32 Carried, int32 Herbs);
	FString GetOpeningTrackerText() const;

	/** Test hook: advance the night timer without waiting on a PIE tick. */
	void DebugAdvanceOpeningNight(float DeltaSeconds);

	/** Click-heart seconds to hot-spring heal seconds. 3.0 is 20, 3.1 and 4.0 are 30, 4.1 is 40. */
	static float OpeningHealSecondsForHeart(float HeartSeconds);

	/** Test hook: queue one wisp's heal from a finished heart, without drawing it. */
	void DebugQueueOpeningWispHeart(float HeartSeconds);

	/** Test hook: start the collect heart on a wisp actor. */
	bool DebugBeginOpeningWispHeart(AActor* Wisp);

	/** Test hook: advance the open heart. A wisp collect heart does not end at 3 seconds. */
	void DebugAdvanceOpeningWispHeart(float DeltaSeconds);

	bool IsOpeningWispHeartActiveForTest() const { return bOpeningWispCollect && bOpeningRuneActive; }

	float GetOpeningWispHealTimerForTest(int32 Index) const
	{
		return OpeningWispHealTimers.IsValidIndex(Index) ? OpeningWispHealTimers[Index] : -1.f;
	}
	int32 GetOpeningWispsCarriedForTest() const { return OpeningWispsCarried; }
	int32 GetOpeningHerbTenthsForTest() const { return OpeningHerbTenths; }
	int32 GetOpeningWispHealTimerCountForTest() const { return OpeningWispHealTimers.Num(); }
	int32 GetOpeningWispsHealedForTest() const { return OpeningWispsHealed; }
	int32 GetOpeningWispFollowerCountForTest() const { return OpeningWispLegMeshes.Num(); }

	/** Read-only snapshot for the in-editor quest suite. No gameplay effect. */
	UFUNCTION(BlueprintPure, Category = "Opening|Playtest")
	FString GetPlaytestStateJson() const;

	int32 GetStressPoints() const;

	/** Test hook: play the opening beats in order, for real, and stop ready to test one beat.
	 *  Beat text: spirit, herbs, backpack, kettle, station, dog, fish, sleep, night, collect,
	 *  heal, glider, delivery, daycamp, dawnglide, nightglide, stealth, ease. Empty = night; "list" prints the names. Start a fresh PIE for every run. */
	void DebugFastForwardOpening(const FString& Beat);

	/** Test hook: call the hot-spring deposit the E chain calls. */
	void DebugHealOpeningWispAtSpring();

	/** E at the second-floor perch rides the line down to the fishing pond. */
	UFUNCTION(BlueprintCallable, Category = "Opening|T0", meta = (DisplayName = "Try Opening Zipline In Front"))
	bool TryOpeningZiplineInFront();

	/** Size-test: the interact ability reports whether E actually did something. */
	void NoteSizeTestInteract(bool bHandled);

	/** Stations: true once the consumable table is open. */
	UFUNCTION(BlueprintCallable, Category = "Opening|T0", meta = (DisplayName = "Is Opening Consumable Station Open"))
	bool IsOpeningConsumableStationOpen() const { return bOpeningConsumableOpen; }

	/** Stations: the herb mixed with a spirit, carried. The dog beat spends one. */
	UFUNCTION(BlueprintCallable, Category = "Opening|T0", meta = (DisplayName = "Get Opening Mixed Herbs"))
	int32 GetOpeningMixedHerbs() const { return OpeningMixedHerbs; }

	/** Stations: true once the partner has given the armor piece. No numbers change. */
	UFUNCTION(BlueprintCallable, Category = "Opening|T0", meta = (DisplayName = "Has Opening Armor Gift"))
	bool HasOpeningArmorGift() const { return bOpeningArmorGiftGiven; }

	/** FALLBACK V2: start scripted CRUMB glide when near GP_GlideStart / glider perch. Day/body only. */
	UFUNCTION(BlueprintCallable, Category = "Transit|FALLBACK", meta = (DisplayName = "Try Start Fallback Glide"))
	bool TryStartFallbackGlide();

	/** Active V2: launch the freely steered cloud descent from GP_GlideStart during day/body. */
	UFUNCTION(BlueprintCallable, Category = "Transit|Cloud Descent", meta = (DisplayName = "Try Start Cloud Descent"))
	bool TryStartCloudDescent();

	UFUNCTION(BlueprintCallable, Category = "Transit|Cloud Descent", meta = (DisplayName = "Is Cloud Descent Active"))
	bool IsCloudDescentActive() const { return bCloudDescentActive; }

	/** Add one carried route wisp. Night descent only, and only up to the night cap. */
	UFUNCTION(BlueprintCallable, Category = "Transit|Cloud Descent", meta = (DisplayName = "Collect Cloud Wisp"))
	bool CollectCloudWisp(AHomeWorldCloudWisp* Wisp);

	UFUNCTION(BlueprintCallable, Category = "Transit|Cloud Descent", meta = (DisplayName = "Get Carried Cloud Wisps"))
	int32 GetCarriedCloudWisps() const { return CarriedCloudWisps; }

	/** True while a day descent is showing camp smoke as its one sign. */
	UFUNCTION(BlueprintCallable, Category = "Transit|Cloud Descent")
	bool HasDayGlideSmokeSign() const { return bDayGlideSmokeSign; }

	UFUNCTION(BlueprintCallable, Category = "Garden|T0")
	bool TryPickGardenHerb();

	/** West bed is the edge hint. East bed is the porch crawl. A pick with no bed is west. */
	UFUNCTION(BlueprintCallable, Category = "Garden|T0")
	bool TryPickGardenHerbFromEast(bool bEast, int32 Amount = 1);

	bool IsPorchCrawlOpen() const { return bPorchCrawlOpen; }

	/** True when a body of this radius fits the porch gap. The player is 42. A guard is wider. */
	UFUNCTION(BlueprintCallable, Category = "Garden|T0")
	bool DoesBodyFitPorchGap(float RadiusCm) const;

	/** First landing wins. Wind and the bull path are the two faces. Night wakes the one left asleep. */
	UFUNCTION(BlueprintCallable, Category = "Field|T0")
	bool ChooseFieldLanding(bool bWind);

	bool IsWindColumnAwake() const { return bWindColumnAwake; }
	bool IsBullPathAwake() const { return bBullPathAwake; }

	/** One guard is already pacing. A second call keeps that guard. */
	UFUNCTION(BlueprintCallable, Category = "Camp|T0")
	void ArriveAtCamp();

	int32 GetPacingGuard() const { return PacingGuard; }

	/** Opens that guard's gap. The gaps already open stay open. */
	UFUNCTION(BlueprintCallable, Category = "Camp|T0")
	bool RecordGuardEased(int32 Ordinal);

	bool IsGuardGapOpen(int32 Ordinal) const;

	bool HasPullStar() const { return bPullStarHeld; }

	/** One crossing. The star is spent. */
	UFUNCTION(BlueprintCallable, Category = "Wound|T0")
	bool TrySpendPullStar();

	/** Night wakes the face the day left asleep. The phase change calls this. */
	void NotifyPocketNight();

	UFUNCTION(BlueprintCallable, Category = "Wound|T0")
	bool TryGiveNightWispToWound();

	/** Look at NODE_GARDEN and pick one herb. Day body only. */
	bool TryGardenInteractInFront();

	/** Look at NODE_WOUND. Day sees it. Night spends one carried wisp. */
	bool TryWoundInteractInFront();

	/** Look at NODE_DUNG and carry one. */
	bool TryDungInteractInFront();

	/** Look at NODE_MIX at the homestead. One dung plus one night wisp. */
	bool TryMixFertilizerInteractInFront();

	/** Look at NODE_BULL in the field. Uses the existing mount speed. */
	bool TryBullInteractInFront();

	/** Look at NODE_BARN after a shrine return with the bull. */
	bool TryBarnInteractInFront();

	/** Look at one NODE_GUARD and ease that guard. Spirit at night. */
	bool TryEaseGuardInFront();

	/** Look at NODE_CAPTIVE after the three guards are eased. */
	bool TryFreeCaptiveInFront();

	UFUNCTION(BlueprintCallable, Category = "Wound|T0")
	bool IsHomesteadWoundHealed() const { return bHomesteadWoundHealed; }

	UFUNCTION(BlueprintCallable, Category = "Wound|T0")
	int32 GetFollowingWoundWispCount() const { return FollowingWoundWispCount; }

	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	bool TryAddCarriedDung();

	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	bool TryMixHomesteadFertilizer();

	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	int32 GetCarriedDung() const { return CarriedDung; }

	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	int32 GetCarriedFertilizer() const { return CarriedFertilizer; }

	/** Night flight. Healed wound wisps are the flight. The mixed fertilizer is the load. */
	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	bool TrySpreadFertilizerOnNightFlight();

	UFUNCTION(BlueprintCallable, Category = "Fertilizer|T0")
	int32 GetMorningHerbPiles() const { return MorningHerbPiles; }

	UFUNCTION(BlueprintCallable, Category = "Shrine|T0")
	void NotifyLeftHomestead();

	UFUNCTION(BlueprintCallable, Category = "Shrine|T0")
	bool HasLeftHomestead() const { return bHasLeftHomestead; }

	UFUNCTION(BlueprintCallable, Category = "Shrine|T0")
	void SetRidingBull(bool bRiding);

	UFUNCTION(BlueprintCallable, Category = "Shrine|T0")
	bool IsRidingBull() const { return bRidingBull; }

	UFUNCTION(BlueprintCallable, Category = "Shrine|T0")
	bool IsWalkToBarn() const { return bWalkToBarn; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	void NotifyPartnerTaken();

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	void NotifyPartnerReadyToReturn();

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	bool IsPartnerReadyToReturn() const { return bPartnerReadyToReturn; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	bool IsPartnerWalkingHome() const { return bPartnerWalkingHome; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	EHomeWorldFamilyPlace GetPartnerPlace() const { return PartnerPlace; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	EHomeWorldFamilyPlace GetChildPlace() const { return ChildPlace; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	bool HasFamilyHintFired() const { return bFamilyHintFired; }

	UFUNCTION(BlueprintCallable, Category = "Family|T0")
	FString GetFamilyHint() const { return FamilyHint; }

	void CompleteShrineReturn();

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

	/**
	 * T0 #11 hook: grant sleep gate then sync form.
	 * The bed is the form change.
	 */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Grant Spirit Sleep Gate"))
	void GrantSpiritSleepGate();

	/** Clear sleep gate (bed wake, or the fifth-stack landing). Dawn does not clear it. */
	UFUNCTION(BlueprintCallable, Category = "Form|Gates", meta = (DisplayName = "Clear Spirit Sleep Gate"))
	void ClearSpiritSleepGate();

	/**
	 * Dawn does not end spirit. Still out: one stack immediately, then one every ten seconds, five max.
	 * Touching the bed clears stacks and stays spirit. Waking at the bed ends spirit.
	 * A late wake slows walk and glide by 15 percent for one minute. The fifth stack is a live glide home.
	 * Vision board, 2026-10-08.
	 */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Get Spirit Sickness Stacks"))
	int32 GetSpiritSicknessStacks() const { return SpiritSicknessStacks; }

	/** Scarf read: one colder step per stack. No number, no bar. */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Get Spirit Sickness Scarf Step"))
	int32 GetSpiritSicknessScarfStep() const { return SpiritSicknessStacks; }

	/** 0.85 while stacks are up or the late-wake minute is running. Otherwise 1. */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Get Spirit Sickness Move Scale"))
	float GetSpiritSicknessMoveScale() const;

	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Is Spirit Sickness Boot Pending"))
	bool IsSpiritSicknessBootPending() const { return bSpiritSicknessBooting; }

	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Tick Spirit Sickness"))
	void TickSpiritSickness(float DeltaTime);

	/** Clears stacks. Stays spirit. Does not sleep. */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Touch Spirit Bed"))
	void TouchSpiritBed();

	/** The bed ends spirit. A late outing then slows movement for one minute. */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Wake From Spirit At Bed"))
	void WakeFromSpiritAtBed();

	/** Live-glide landing: at the bed, then body. No cut. */
	UFUNCTION(BlueprintCallable, Category = "Form|Sickness", meta = (DisplayName = "Notify Spirit Sickness Landed"))
	void NotifySpiritSicknessLanded();

	/** Once, before the first night out. The line is the bed and the dawn. */
	UFUNCTION(BlueprintCallable, Category = "Family|T0", meta = (DisplayName = "Try Tell Child Dawn Rule"))
	bool TryTellChildDawnRule();

	/** Sleep gate at night. Phase alone never grants spirit (T0 TOD_NIGHT_HOME). The rune latch is not required. */
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
	 * Marks same slot identity #12 nurture uses (day plant only -- not spirit nurture).
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
	 * T0 #12 NODE_PLANT_SLOT: spirit nurture on same N1 slot as day plant (#3).
	 * Prefer existing TryNurture / HomeWorldNurtureComponent -- no parallel nurture service (Arch B).
	 * Prereq: #3 day plant mark + #11 spirit path (FORM_SPIRIT / TOD_NIGHT_SPIRIT).
	 * Not different-slot N2; not body-form nurture; not day-plant-alone (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "Nurture|T0", meta = (DisplayName = "Try Nurture NODE_PLANT_SLOT Spirit"))
	bool TryNurtureNodePlantSlot();

	/** True if N1 NODE_PLANT_SLOT is day-planted and spirit-nurtured (M_Nurtured) this session. */
	UFUNCTION(BlueprintCallable, Category = "Nurture|T0", meta = (DisplayName = "Is NODE_PLANT_SLOT Spirit Nurtured"))
	bool IsNodePlantSlotSpiritNurtured() const;

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
	 * Bull charge-and-boot (Lead 2026-10-07, Docs/context/HOMEWORLD_ROUTE.md):
	 * threat meter full or too close without an offering -> charge -> EJECT_HOME.
	 * Prefer existing UHomeWorldFallbackGlideComponent::StartGlideHome -- no parallel
	 * eject service (Arch B). Distinct from MUST #8 TryEjectNodeDayCamp (day camp)
	 * and #10 TryBootPlanetsideNightHome (night glider). Repeatable by design: the
	 * encounter component resets its meter on delivery instead of a session latch.
	 */
	UFUNCTION(BlueprintCallable, Category = "Beast|T0", meta = (DisplayName = "Try Boot Beast Charge Home"))
	bool TryBootBeastChargeHome();

	/**
	 * T0 #11 NODE_BED: bed sleep at night -> spirit. The rune latch stays locked.
	 * Prefer existing GrantSpiritSleepGate / CanEnterSpiritForm / ApplyFormForPhase -- no parallel form service (Arch B).
	 * Day and dawn stay FORM_BODY. Phase-alone / soft-kidnap = closed_fail. #9 w/o bed stay FORM_BODY.
	 */
	UFUNCTION(BlueprintCallable, Category = "Bed|T0", meta = (DisplayName = "Try Bed Sleep Spirit"))
	bool TryBedSleepSpirit();

	/** True after NODE_BED bed->spirit latch this session (night sleep). */
	UFUNCTION(BlueprintCallable, Category = "Bed|T0", meta = (DisplayName = "Is Bed Spirit Granted"))
	bool IsBedSpiritGranted() const { return bBedSpiritGranted; }

	/**
	 * T0 #13 NODE_PORTAL_HOME -> NODE_PORTAL_CAMP: spirit home portal to camp.
	 * Prefer existing HomeWorldShrinePortal* TryPortalTransitToDestination -- no parallel portal service (Arch B).
	 * Prereq: #11 spirit path (FORM_SPIRIT / TOD_NIGHT_SPIRIT via the bed).
	 * Not home<->planet return alone (GP_PortalA<->B); not body portal; not shrine-dress-as-camp (those = closed_fail).
	 */
	UFUNCTION(BlueprintCallable, Category = "Portal|T0", meta = (DisplayName = "Try Portal Home To Camp"))
	bool TryPortalHomeToCamp();

	/** True after NODE_PORTAL_HOME -> NODE_PORTAL_CAMP latch this session. */
	UFUNCTION(BlueprintCallable, Category = "Portal|T0", meta = (DisplayName = "Is Portal Home To Camp Granted"))
	bool IsPortalHomeToCampGranted() const { return bPortalHomeToCampGranted; }


	/**
	 * T0 #14 camp night: avoid 1 NODE_GUARD + soothe 2 NODE_SLEEPER (CAM_T0_CAMP_NIGHT).
	 * Prefer UHomeWorldSpiritStealthComponent -- no parallel stealth service (Arch B).
	 * Prereq: #11 spirit path (FORM_SPIRIT / TOD_NIGHT_SPIRIT via the bed).
	 * convert != soothe (never ReportFoeConverted); stealth-alone / GP_SS_Lit alone / convert-as-soothe = closed_fail.
	 */
	UFUNCTION(BlueprintCallable, Category = "CampNight|T0", meta = (DisplayName = "Try Camp Night Avoid Soothe"))
	bool TryCampNight();

	/** True after camp night avoid-1 + soothe-2 latch this session. */
	UFUNCTION(BlueprintCallable, Category = "CampNight|T0", meta = (DisplayName = "Is Camp Night Granted"))
	bool IsCampNightGranted() const { return bCampNightGranted; }

	/** MV-A: parkour-lite mantle/vault (body, day). */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A", meta = (DisplayName = "Try Mantle Or Vault"))
	bool TryMantleOrVault();

	/** MV-A: spirit blink toward shrine/anchor tags (night/spirit). */
	UFUNCTION(BlueprintCallable, Category = "Movement|MV-A", meta = (DisplayName = "Try Spirit Blink"))
	bool TrySpiritBlink();

	/** Level the view. Pitch stays -12. Yaw follows the pawn. */
	void ApplySpawnControlPitch();

	/** Hold, cursor sample, and release. These are the stroke input path. A size-test map does not run them. */
	void BeginStrokeFromInput();
	void SampleStrokeFromInput(FVector2D ScreenPoint, float Time);
	EHomeWorldStrokeReport EndStrokeFromInput();

	void SetStrokePad(AHomeWorldEasePad* Pad);
	void SetStrokeHerb(EHomeWorldHerbVerb Verb, UHomeWorldVirtueComponent* Target);
	void SetParadoxToy(AHomeWorldParadoxToy* Toy);

	UHomeWorldStrokeReportComponent* GetStrokeReport() const { return StrokeReport; }

	virtual void Jump() override;

	/** Public so automation can assert the cloud-descent landing handoff. Engine declares this public. */
	virtual void Landed(const FHitResult& Hit) override;

protected:
	virtual void PossessedBy(AController* NewController) override;

	/** FALLBACK scripted glide along CRUMB_* (no free-flight). */
	UPROPERTY(VisibleAnywhere, Category = "Transit|FALLBACK")
	TObjectPtr<UHomeWorldFallbackGlideComponent> FallbackGlideComponent;

	/** V1 soft pushback when leaving hero island bounds (no navmesh). */
	UPROPERTY(VisibleAnywhere, Category = "Walk|Bounds")
	TObjectPtr<UHomeWorldSoftBoundsComponent> SoftBoundsComponent;

	UPROPERTY(VisibleAnywhere, Category = "Stress")
	TObjectPtr<UHomeWorldStressComponent> StressComponent;

	/** MV-A: sprint / mantle / blink / mount boost on single CMC. */
	UPROPERTY(VisibleAnywhere, Category = "Movement|MV-A")
	TObjectPtr<UHomeWorldTraversalComponent> TraversalComponent;

	/** SS-A: spirit lit / alert stub (spirit form only). */
	UPROPERTY(VisibleAnywhere, Category = "Stealth|SS-A")
	TObjectPtr<UHomeWorldSpiritStealthComponent> SpiritStealthComponent;

	/** Ease stroke. Present on the pawn. Input does not run it on L_SizeTest. */
	UPROPERTY(VisibleAnywhere, Category = "Stroke")
	TObjectPtr<UHomeWorldStrokeReportComponent> StrokeReport;

	UPROPERTY()
	TObjectPtr<AHomeWorldEasePad> StrokePad;

	UPROPERTY()
	TObjectPtr<UHomeWorldVirtueComponent> HerbTarget;

	EHomeWorldHerbVerb HerbVerb = EHomeWorldHerbVerb::None;

	UPROPERTY()
	TObjectPtr<AHomeWorldParadoxToy> ParadoxToy;

	bool IsSizeTestLevel() const;
	void ApplyMarkedHerbOnMatch();
	void DiscoverStrokePad();
	void DiscoverParadoxToy();
	void SetStrokeCursorHeld(bool bHeld);

	bool bStrokeCursorHeld = false;

	/** True only between active V2 launch and landing. Steering is unrestricted. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Transit|Cloud Descent")
	bool bCloudDescentActive = false;

	/** Route wisps carried this night; intentionally separate from the six-resource inventory. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Transit|Cloud Descent")
	int32 CarriedCloudWisps = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Transit|Cloud Descent")
	bool bDayGlideSmokeSign = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fertilizer|T0")
	int32 CarriedDung = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fertilizer|T0")
	int32 CarriedFertilizer = 0;

	/** Stays zero. Dawn does not spawn a pile. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Fertilizer|T0")
	int32 MorningHerbPiles = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Wound|T0")
	bool bHomesteadWoundHealed = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Wound|T0")
	int32 FollowingWoundWispCount = 0;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Shrine|T0")
	bool bHasLeftHomestead = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Shrine|T0")
	bool bRidingBull = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Shrine|T0")
	bool bWalkToBarn = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	EHomeWorldFamilyPlace PartnerPlace = EHomeWorldFamilyPlace::ByBed;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	EHomeWorldFamilyPlace ChildPlace = EHomeWorldFamilyPlace::InGarden;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	bool bPartnerTaken = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	bool bPartnerReadyToReturn = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	bool bPartnerWalkingHome = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	bool bFamilyHintFired = false;

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Family|T0")
	FString FamilyHint;

	bool bHasSidedHerb = false;
	bool bCarriedHerbIsEast = false;
	bool bEdgeFaceAwake = false;
	bool bPorchCrawlOpen = false;
	bool bFieldLandingChosen = false;
	bool bWindColumnAwake = false;
	bool bBullPathAwake = false;
	bool bCampArrived = false;
	int32 PacingGuard = 0;
	bool bGuardGapOpen[3] = { false, false, false };
	bool bPullStarHeld = false;

	void WakeUnpickedPocketFace();
	void OpenPorchCrawlActors();

	/** T0 #9: spirit form flag — granted by the bed at night, not by phase alone. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form")
	bool bIsSpiritForm = false;

	/** T0 #11: bed/sleep gate. Cleared by the bed wake or the fifth-stack landing. */
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Form|Gates")
	bool bSpiritSleepGateGranted = false;

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

	/** Ground hop. Uses the existing jump speed on the traversal component. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> JumpAction;

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

	AActor* ResolveOpeningAim(FHitResult& Hit);
	bool TraceEyeInteract(FHitResult& OutHit) const;
	void UpdateSizeTestWalk();
	void UpdateSizeTestWisp(float DeltaTime);
	void UpdateOpeningBonk();
	/** Fly the body onto the pad edge nearest the hit, set in from the rim.
	 *  A clear shot is the normal arc. No clearance pops straight up, then plays
	 *  that same arc from the air. A new bonk does not replace one in flight. */
	void BeginBonkReturn(const FVector& PadOrigin, const FVector& PadExtent);
	// HomeWorld.Opening.BonkReentry calls the return and reads the arc mid-flight.
	friend class FBonkReentryTest;
	// HomeWorld.Opening.BonkClearance reads the pop and the arc mid-flight.
	friend class FBonkClearanceTest;
	void TickBonkReturn(float DeltaSeconds);
	bool IsBonkReturning() const { return bOpeningBonkReturning; }
	void ClearPartyOnAbsenceVolumes();
	void UpdateOpeningNight(float DeltaTime);
	void UpdateOpeningWispLegs();
	void EnsureOpeningNightProps();
	void ApplyOpeningWalkSpeed();
	void UpdateOpeningWalkScroll();
	int32 OpeningSpeedStep = 0;
	bool bSizeTestWalkPlaying = false;

	/** The kitchen consumable table's open, mix, and brew branches. Shared by E and the playtest fast-forward. */
	void UseOpeningConsumableStation();

	/** The bed's night transition once the bed is resolved. Shared by E and the playtest fast-forward. */
	bool BeginOpeningNight();

	/** Fast-forward only. Returns the body at dawn and does not stock the chest. */
	void ReturnOpeningBodyForDawnPlaytest();

	/** Playtest fast-forward: 0 idle, 1..9 the beat being played. */
	void TickDebugFastForward(float DeltaTime);
	int32 DebugFastForwardStep = 0;
	float DebugFastForwardStepClock = 0.f;

	/** The beat the run stops at: 1..8 leave that step for the player, 9..11 run every step
	 *  and then carry the player to the beat - night, the copse wisp, or the hot springs. */
	int32 DebugFastForwardStop = 9;
	/** Set at the ready line: the beat name and the pawn's 2D distance to its target. */
	FString PlaytestReadyFor;
	float PlaytestReadyDistanceCm = -1.f;
	void ReadyForOpeningPlaytest();
	void PlaceForOpeningPlaytest(AActor* Target, float Distance);
	void PlaceForOpeningPlaytestAtPond(AActor* Pond);
	void CollectNightWispsForPlaytest();

	/** Greybox shoulder follower on SizeTest only. After the spirit is claimed, it marks the interact target. */
	UPROPERTY(Transient)
	TObjectPtr<UStaticMeshComponent> SizeTestWisp;

	/** Wisp cursor while E is held. Movement stays on. */
	UPROPERTY(Transient)
	TObjectPtr<UStaticMeshComponent> SizeTestCursorWisp;

	bool bSizeTestInteractCursor = false;
	bool bSizeTestInteractHandled = false;
	TObjectPtr<AActor> OpeningWispReleased;
	UPROPERTY(Transient)
	TObjectPtr<AActor> OpeningLookPerch;
	UPROPERTY(Transient)
	TObjectPtr<UTextRenderComponent> OpeningInteractPrompt;
	bool bOpeningWispReturning = false;
	float OpeningWispReturnLeft = 0.f;
	FVector OpeningWispReturnFrom = FVector::ZeroVector;
	FVector OpeningBonkSafe = FVector::ZeroVector;
	bool bOpeningBonkSafe = false;
	// One return at a time. While this is set the fall cannot start another flight.
	bool bOpeningBonkReturning = false;
	HomeWorldBonk::FArc BonkArc;
	float BonkElapsed = 0.f;
	// Set only when the shot to the landing has no clearance. The pop plays first.
	bool bBonkPop = false;
	FVector BonkPopFrom = FVector::ZeroVector;
	FVector BonkPopTo = FVector::ZeroVector;
	float BonkPopDuration = 0.f;
	bool bOpeningNightSpirit = false;
	bool bOpeningWispCollect = false;
	UPROPERTY(Transient)
	int32 OpeningWispsCollected = 0;
	FVector OpeningNightChestPoint = FVector::ZeroVector;
	TObjectPtr<UStaticMeshComponent> OpeningSpiritBody;
	TObjectPtr<AActor> OpeningCopseWisp;
	TObjectPtr<AActor> OpeningPondWisp;
	TObjectPtr<AActor> OpeningSpringWisp;

	/** Damaged wisps in the backpack, waiting for the hot springs. */
	UPROPERTY(Transient)
	int32 OpeningWispsCarried = 0;

	/** One entry per wisp healing in the hot springs; seconds left. */
	UPROPERTY(Transient)
	TArray<float> OpeningWispHealTimers;

	/** Heal length for each collected wisp, in collect order. Empty means the fast heart, 20 seconds. */
	TArray<float> OpeningWispHealDurations;

	/** Seconds the open wisp collect heart has been running. */
	float OpeningWispHeartElapsed = 0.f;

	/** Healed wisps that follow near the legs. */
	UPROPERTY(Transient)
	int32 OpeningWispsHealed = 0;

	/** One purple sphere per healed wisp at the player's legs. */
	UPROPERTY(Transient)
	TArray<TObjectPtr<UStaticMeshComponent>> OpeningWispLegMeshes;
	void SnapSizeTestWispHome(AActor* Finished);
	bool bOpeningRuneActive = false;
	FVector OpeningRuneCursor = FVector::ZeroVector;
	TObjectPtr<AActor> OpeningRuneBed;
	TObjectPtr<class UHomeWorldRuneShapeComponent> OpeningRuneShape;
	struct FOpeningHerbReturn
	{
		TObjectPtr<AActor> Bed;
		TObjectPtr<AActor> Plant;
		bool bEast = false;
		float Time = -1.f;
	};
	TArray<FOpeningHerbReturn> OpeningHerbReturns;
	int32 OpeningHerbTenths = 0;
	/** Successful chunks from the two beds. Brewing does not lower this. A miss adds nothing. */
	int32 OpeningHerbsGathered = 0;
	bool bOpeningHerbFromWest = false;
	bool bOpeningHerbFromEast = false;
	bool bOpeningKettleBrewed = false;
	float OpeningPointTime = -1.f;

	/** Opening stations: the shoulder spirit claim, the consumable table, and its mixed herb output. */
	bool bOpeningSpiritClaimed = false;
	bool bOpeningConsumableOpen = false;
	UPROPERTY(Transient)
	int32 OpeningMixedHerbs = 0;

	/** The partner gave the armor piece. The armory table opens; walk speed and bonk tries stay as they are. */
	bool bOpeningArmorGiftGiven = false;
	bool TryOpeningArmorGift();
	bool bOpeningFishCaught = false;

	AActor* FindOpeningProximityTarget();

	/** Look-point distance squared, in NDC. False when the target is behind the camera or off the viewport. */
	bool OpeningLookDistSq(const AActor* Target, float& OutDistSq) const;
	void SetOpeningInteractPrompt(bool bShow, const FVector& At);
	void ShowOpeningProximityLine();
	void RefreshOpeningQuest();
	void PublishOpeningFact(EHomeWorldOpeningFact Fact, bool bValue);
	void PublishOpeningHerbsGathered();
	void PublishOpeningMixedHerb();
	/** Range, wrath, and tame. Live reads: each can clear, including when the dog is gone. */
	void PublishOpeningDogFacts();
	void MaybeLeadPartnerAfterHerbs();
	bool HasOpeningHerbQuota() const;
	void StartOpeningHerbRune(AActor* Bed);
	void UpdateOpeningHerbRune(float DeltaTime);
	void FinishOpeningHerbRune(int32 Tenths);
	void UpdateOpeningHerbPreview();
	void RestoreOpeningHerb();
	void UpdateSizeTestInteractCursor();

	/** Beat 4: the injured dog. Knock on too close or too fast; trace Grace; then the mixed herb. */
	void UpdateOpeningDog(float DeltaTime);
	void UpdateOpeningDogDraw(float DeltaTime);
	void StartOpeningDogDraw(class AHomeWorldOpeningDog* Dog);
	void FinishOpeningDogDraw();
	void KnockFromOpeningDog(class AHomeWorldOpeningDog* Dog, const FString& Why, float Dist, float Speed);
	void FailOpeningDogTrace();
	void SucceedOpeningDogTrace(class AHomeWorldOpeningDog* Dog);
	TObjectPtr<class AHomeWorldOpeningDog> OpeningDog;
	UPROPERTY(Transient)
	TObjectPtr<UHomeWorldQuestLog> QuestLog;

	UPROPERTY()
	TObjectPtr<UHomeWorldOpeningSupply> OpeningSupply;
	bool bOpeningDogDrawActive = false;
	bool bOpeningDogSlowLatched = false;
	FVector OpeningDogCursor = FVector::ZeroVector;
	float OpeningDogKnockCooldown = 0.f;
	float OpeningDogSlowWarnAt = -1.f;

	/** Capsule radius (cm). Human-sized default; override in Blueprint for different characters. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "200.0"))
	float CapsuleRadius = 42.0f;

	/** Capsule half-height (cm). Human-sized default; override in Blueprint for different characters. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "500.0"))
	float CapsuleHalfHeight = 88.0f;

	/** Max distance (cm) to GP_GlideStart / CRUMB_Depart_Lookout / GlideStart tag to allow interact glide. */
	UPROPERTY(EditDefaultsOnly, Category = "Transit|FALLBACK", meta = (ClampMin = "50.0", ClampMax = "2000.0"))
	float GlideStartProximityCm = 450.0f;

	/**
	 * True on the greybox body maps (SizeTest, L_Field). Set once in BeginPlay.
	 * The hero-island walk bounds do not fit these maps (SCENE_SETUP practice 5), so Tick
	 * must not re-enable them there.
	 */
	bool bGreyboxBodyLevel = false;

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
	void OnJumpStarted(const FInputActionValue& Value);
	void OnJumpCompleted(const FInputActionValue& Value);
	void OnStrokeInputStarted(const FInputActionValue& Value);
	void OnStrokeInputSampled(const FInputActionValue& Value);
	void OnStrokeInputReleased(const FInputActionValue& Value);

	void ApplyFormForPhase(EHomeWorldTimeOfDayPhase Phase);
	void NoteStillOutPastDawn(EHomeWorldTimeOfDayPhase Phase);
	void AddSpiritSicknessStack();
	void BeginSpiritSicknessBoot();
	void RefreshSpiritSicknessMovement();
	/** Docs/27 NF2-A: soft glow + optional sound/particle when form actually changes. */
	void PlaySoftFormSwapFeedback(EHomeWorldTimeOfDayPhase Phase, bool bSpirit);
	UFUNCTION()
	void OnTimeOfDayPhaseChanged(EHomeWorldTimeOfDayPhase NewPhase);
	UFUNCTION()
	void OnSpiritSicknessGlideCompleted();

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

	/** T0 #11: bed->spirit latch after GrantSpiritSleepGate at night (NODE_BED this session). */
	bool bBedSpiritGranted = false;

	/** Vision 2026-10-08. Dawn out of bed. Five stacks, ten seconds apart. The fifth flies home. */
	int32 SpiritSicknessStacks = 0;
	float SpiritSicknessSecondsUntilNext = -1.f;
	float LateWakeSlowSecondsRemaining = 0.f;
	bool bHadSpiritSicknessThisOuting = false;
	bool bSpiritSicknessPausedAtBed = false;
	bool bSpiritSicknessBooting = false;
	bool bChildDawnRuleTold = false;

	/** T0 #13: spirit home->camp portal latch (NODE_PORTAL_HOME -> NODE_PORTAL_CAMP this session). */
	bool bPortalHomeToCampGranted = false;


	/** T0 #14: camp night avoid-1 guard + soothe-2 sleepers latch this session. */
	bool bCampNightGranted = false;

	/** VP-C PA-06: on-screen interact feedback (debug overlay). */
	void ShowInteractFeedback(const FString& Message, FColor Color = FColor::Green) const;
	bool TraceInteractHit(FHitResult& OutHit) const;
	bool FindInteractTargetInCone(FHitResult& OutHit) const;
	/** True when no world geometry blocks the chest-height sightline to the target. Walls stop E. */
	bool HasOpeningLineOfSight(const AActor* Target) const;
	static bool ActorHasInteractableComponent(const AActor* Actor);
	AActor* GetInteractTargetActor(const FHitResult& Hit) const;
	FString BuildInteractRangeHint(AActor* Target) const;
	void UpdateInteractRangeHint(float DeltaTime);

	UPROPERTY(EditDefaultsOnly, Category = "Interaction|Feedback", meta = (ClampMin = "50.0", ClampMax = "1000.0"))
	float InteractTraceLengthCm = 280.f;

	UPROPERTY(EditDefaultsOnly, Category = "Interaction|Feedback", meta = (ClampMin = "0.1", ClampMax = "2.0"))
	float InteractHintRefreshSeconds = 0.35f;

	float InteractHintAccumulator = 0.f;

	bool bInteractChainOverride = false;
	bool bSizeTestInteractChain = false;
};
