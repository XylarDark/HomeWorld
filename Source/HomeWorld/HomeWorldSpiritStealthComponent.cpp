// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldSpiritLitVolume.h"
#include "Components/PointLightComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/Character.h"
#include "EngineUtils.h"

UHomeWorldSpiritStealthComponent::UHomeWorldSpiritStealthComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.TickInterval = 0.05f;

	// The three camp actors, built up front so the freedom gate is never evaluated against
	// an empty array. An empty array trivially satisfies "all of them are calm", which is
	// precisely the fail-open that the bSoftLatch field exists to contain.
	CampActors.Reserve(HomeWorldCampNight::GetGatedActorCount());

	for (int32 Index = 0; Index < HomeWorldCampNight::GetGatedActorCount(); ++Index)
	{
		FHomeWorldCampActorCalm Guard;
		Guard.Role = EHomeWorldCampRole::Guard;
		Guard.bAsleep = HomeWorldCampNight::StartsAsleep(EHomeWorldCampRole::Guard);
		CampActors.Add(Guard);
	}
}

void UHomeWorldSpiritStealthComponent::BeginPlay()
{
	Super::BeginPlay();
}

void UHomeWorldSpiritStealthComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		if (LitOverlapCount > 0)
		{
			LitOverlapCount = 0;
		}
		if (AlertLevel > 0.f)
		{
			AlertLevel = 0.f;
		}
		bLoggedAlertThisLitSession = false;
		bLoggedQuickWindowThisLitSession = false;
		bWasLitLastFrame = false;
		bForceLitCheat = false;
		return;
	}

	const bool bLitNow = IsSpiritLit();
	if (bLitNow)
	{
		UpdateAlert(DeltaTime);
	}
	else
	{
		TryLogClear();
		if (AlertLevel > 0.f)
		{
			AlertLevel = FMath::Max(0.f, AlertLevel - AlertDecayPerSecond * DeltaTime);
		}
		if (AlertLevel <= KINDA_SMALL_NUMBER)
		{
			bLoggedAlertThisLitSession = false;
			bLoggedQuickWindowThisLitSession = false;
		}
	}

	bWasLitLastFrame = bLitNow;
	UpdateFeelVisuals();
}

void UHomeWorldSpiritStealthComponent::NotifyLitVolumeEntered(EHomeWorldSpiritLitSourceKind SourceKind, AHomeWorldSpiritLitVolume* Volume)
{
	(void)Volume;
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		return;
	}
	if (!HomeWorldSpiritStealth::RevealsSpiritInVolume(SourceKind))
	{
		return;
	}

	const bool bWasLit = IsSpiritLit();
	LitOverlapCount = FMath::Max(0, LitOverlapCount) + 1;
	LastEnterSourceKind = SourceKind;

	if (!bWasLit)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: LIT enter (%s)"), HomeWorldSpiritStealth::GetLitSourceLogName(SourceKind));
	}
}

void UHomeWorldSpiritStealthComponent::NotifyLitVolumeExited(AHomeWorldSpiritLitVolume* Volume)
{
	(void)Volume;
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		return;
	}

	LitOverlapCount = FMath::Max(0, LitOverlapCount - 1);
	if (!IsSpiritLit())
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: CLEAR"));
		bLoggedAlertThisLitSession = false;
		bLoggedQuickWindowThisLitSession = false;
		AlertLevel = 0.f;
	}
}

void UHomeWorldSpiritStealthComponent::NotifyInteractWhileLit()
{
	if (!IsSpiritLit() || bLoggedQuickWindowThisLitSession)
	{
		return;
	}
	bLoggedQuickWindowThisLitSession = true;
	UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: QUICK_WINDOW"));
}

void UHomeWorldSpiritStealthComponent::SetForceLitCheat(bool bForce)
{
	bForceLitCheat = bForce;
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (bForce && Character && Character->GetIsSpiritForm() && !bWasLitLastFrame)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: LIT enter (ForceLit)"));
	}
	if (!bForce && LitOverlapCount == 0)
	{
		TryLogClear();
	}
}

void UHomeWorldSpiritStealthComponent::LogStatus() const
{
	const TCHAR* FeelLabel = IsSpiritRevealedCueActive() ? TEXT("revealed") : TEXT("hidden");
	UE_LOG(LogHomeWorld, Log, TEXT("STEALTH:STATUS lit=%d alert=%.2f overlaps=%d force=%d feel=%s"),
		IsSpiritLit() ? 1 : 0, AlertLevel, LitOverlapCount, bForceLitCheat ? 1 : 0, FeelLabel);
}

bool UHomeWorldSpiritStealthComponent::IsSpiritHiddenCueActive() const
{
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		return false;
	}
	return !IsSpiritRevealedCueActive();
}

bool UHomeWorldSpiritStealthComponent::IsSpiritRevealedCueActive() const
{
	return IsSpiritLit() || AlertLevel > 0.02f;
}

void UHomeWorldSpiritStealthComponent::EnsureFeelLight()
{
	if (FeelLight || bFeelLightSpawned)
	{
		return;
	}
	AActor* Owner = GetOwner();
	if (!Owner)
	{
		return;
	}
	FeelLight = NewObject<UPointLightComponent>(Owner, TEXT("SS_FeelLight"));
	if (!FeelLight)
	{
		return;
	}
	FeelLight->SetupAttachment(Owner->GetRootComponent());
	FeelLight->RegisterComponent();
	FeelLight->SetMobility(EComponentMobility::Movable);
	FeelLight->SetCastShadows(false);
	FeelLight->SetAttenuationRadius(260.f);
	bFeelLightSpawned = true;
}

void UHomeWorldSpiritStealthComponent::ApplyMeshFeelTint(bool bRevealed, float Alert01)
{
	ACharacter* Character = Cast<ACharacter>(GetOwner());
	if (!Character)
	{
		return;
	}
	USkeletalMeshComponent* Mesh = Character->GetMesh();
	if (!Mesh)
	{
		return;
	}
	const int32 SlotCount = Mesh->GetNumMaterials();
	for (int32 Slot = 0; Slot < SlotCount; ++Slot)
	{
		UMaterialInstanceDynamic* MID = Mesh->CreateAndSetMaterialInstanceDynamic(Slot);
		if (!MID)
		{
			continue;
		}
		const float HiddenOpacity = 0.78f;
		const float RevealedOpacity = FMath::Lerp(0.88f, 1.f, Alert01);
		const float Opacity = bRevealed ? RevealedOpacity : HiddenOpacity;
		MID->SetScalarParameterValue(FName(TEXT("Opacity")), Opacity);
		MID->SetScalarParameterValue(FName(TEXT("Desaturation")), bRevealed ? 0.f : 0.35f);
		if (bRevealed)
		{
			MID->SetVectorParameterValue(FName(TEXT("EmissiveColor")),
				FLinearColor(0.55f + Alert01 * 0.35f, 0.22f, 0.08f));
		}
		else
		{
			MID->SetVectorParameterValue(FName(TEXT("EmissiveColor")), FLinearColor(0.08f, 0.12f, 0.28f));
		}
	}
}

void UHomeWorldSpiritStealthComponent::UpdateFeelVisuals()
{
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		if (FeelLight)
		{
			FeelLight->SetVisibility(false);
		}
		bLastRevealedCue = false;
		return;
	}

	const bool bRevealed = IsSpiritRevealedCueActive();
	const float Alert01 = FMath::Clamp(AlertLevel, 0.f, 1.f);

	EnsureFeelLight();
	if (FeelLight)
	{
		FeelLight->SetVisibility(true);
		if (bRevealed)
		{
			FeelLight->SetLightColor(FLinearColor(1.f, 0.48f + Alert01 * 0.2f, 0.18f));
			FeelLight->SetIntensity(350.f + Alert01 * 950.f);
		}
		else
		{
			FeelLight->SetLightColor(FLinearColor(0.35f, 0.45f, 0.85f));
			FeelLight->SetIntensity(140.f);
		}
	}

	ApplyMeshFeelTint(bRevealed, Alert01);

	if (bRevealed != bLastRevealedCue)
	{
		UE_LOG(LogHomeWorld, Verbose, TEXT("STEALTH: feel %s alert=%.2f"),
			bRevealed ? TEXT("revealed") : TEXT("hidden"), Alert01);
		bLastRevealedCue = bRevealed;
	}
}

void UHomeWorldSpiritStealthComponent::UpdateAlert(float DeltaTime)
{
	AlertLevel = FMath::Clamp(AlertLevel + AlertRisePerSecond * DeltaTime, 0.f, 1.f);
	if (!bLoggedAlertThisLitSession && AlertLevel >= AlertThreshold)
	{
		bLoggedAlertThisLitSession = true;
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: ALERT"));
	}
}

void UHomeWorldSpiritStealthComponent::TryLogClear()
{
	if (bWasLitLastFrame && !IsSpiritLit())
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: CLEAR"));
		bLoggedAlertThisLitSession = false;
		bLoggedQuickWindowThisLitSession = false;
	}
}

bool UHomeWorldSpiritStealthComponent::TryAvoidNodeGuard()
{
	// T0 #14 NODE_GUARD � spirit stealth avoid (not convert; not lit-volume alone as beat).
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: NODE_GUARD avoid skipped - need FORM_SPIRIT"));
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	static const FName GuardLabels[] = {
		FName(TEXT("NODE_GUARD")),
		FName(TEXT("GP_CampNight_Guard")),
		FName(TEXT("ANCHOR_NODE_GUARD")),
	};

	auto ActorMatchesLabel = [](AActor* Actor, const FName& Label) -> bool
	{
		if (!Actor || Label.IsNone())
		{
			return false;
		}
#if WITH_EDITOR
		if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return true;
		}
#endif
		if (Actor->GetName().Contains(Label.ToString()))
		{
			return true;
		}
		if (Actor->ActorHasTag(Label))
		{
			return true;
		}
		return false;
	};

	AActor* GuardActor = nullptr;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		for (const FName& Label : GuardLabels)
		{
			if (ActorMatchesLabel(Actor, Label))
			{
				GuardActor = Actor;
				break;
			}
		}
		if (GuardActor)
		{
			break;
		}
	}

	// Cap at 1 for MUST #14 beat (avoid 1 guard).
	if (GuardsAvoidedCount >= 1)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: NODE_GUARD already avoided (count=%d)"), GuardsAvoidedCount);
		return true;
	}

	GuardsAvoidedCount = 1;
	if (GuardActor)
	{
		// Prefer hidden / unlit cue when near guard � stealth path, not convert.
		const bool bHidden = IsSpiritHiddenCueActive();
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_GUARD avoid ok (actor present; hidden_cue=%d; not convert; not GP_SS_Lit alone)"),
			bHidden ? 1 : 0);
	}
	else
	{
		// KEEP-LOCAL soft: Present?=N � no umap guard; Source emit without .uasset/.umap.
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_GUARD avoid soft latch (KEEP-LOCAL actor missing; Present?=N; not script-only GP_SS_Lit; not convert)"));
	}
	return true;
}

bool UHomeWorldSpiritStealthComponent::TrySootheNodeSleeper()
{
	// T0 #14 NODE_SLEEPER � soothe care verb. convert != soothe (never ReportFoeConverted here).
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: NODE_SLEEPER soothe skipped - need FORM_SPIRIT"));
		return false;
	}
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	static const FName SleeperLabels[] = {
		FName(TEXT("NODE_SLEEPER")),
		FName(TEXT("GP_CampNight_Sleeper")),
		FName(TEXT("ANCHOR_NODE_SLEEPER")),
	};

	auto ActorMatchesLabel = [](AActor* Actor, const FName& Label) -> bool
	{
		if (!Actor || Label.IsNone())
		{
			return false;
		}
#if WITH_EDITOR
		if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return true;
		}
#endif
		if (Actor->GetName().Contains(Label.ToString()))
		{
			return true;
		}
		if (Actor->ActorHasTag(Label))
		{
			return true;
		}
		return false;
	};

	int32 WorldSleeperCount = 0;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Actor = *It;
		if (!Actor)
		{
			continue;
		}
		for (const FName& Label : SleeperLabels)
		{
			if (ActorMatchesLabel(Actor, Label))
			{
				++WorldSleeperCount;
				break;
			}
		}
	}

	if (SleepersSoothedCount >= 2)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("STEALTH: NODE_SLEEPER already soothed (count=%d)"), SleepersSoothedCount);
		return true;
	}

	++SleepersSoothedCount;
	if (WorldSleeperCount > 0)
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_SLEEPER soothe ok (count=%d world=%d; soothe != convert; not ReportFoeConverted)"),
			SleepersSoothedCount, WorldSleeperCount);
	}
	else
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_SLEEPER soothe soft latch (count=%d; KEEP-LOCAL actor missing; Present?=N; soothe != convert; not stealth-alone)"),
			SleepersSoothedCount);
	}
	return true;
}

// =====================================================================================
// T0 #14 / #15 / #16 - the three-actor camp night
// =====================================================================================

const FHomeWorldCampActorCalm* UHomeWorldSpiritStealthComponent::FindCampActor(
	EHomeWorldCampRole Role, int32 Ordinal) const
{
	int32 Seen = 0;
	for (const FHomeWorldCampActorCalm& Actor : CampActors)
	{
		if (Actor.Role != Role)
		{
			continue;
		}
		if (Seen == Ordinal)
		{
			return &Actor;
		}
		++Seen;
	}
	return nullptr;
}

FHomeWorldCampActorCalm* UHomeWorldSpiritStealthComponent::FindCampActor(
	EHomeWorldCampRole Role, int32 Ordinal)
{
	// Non-const overload needs its own walk; a const_cast would hand out a writable
	// pointer into a UPROPERTY that UHT still believes is const to Blueprint.
	return const_cast<FHomeWorldCampActorCalm*>(
		static_cast<const UHomeWorldSpiritStealthComponent*>(this)->FindCampActor(Role, Ordinal));
}

/** Locate the world actor carrying a T0 label, or null when the camp is not built yet. */
static AActor* FindCampActorInWorld(UWorld* World, EHomeWorldCampRole Role, int32 Ordinal)
{
	if (!World)
	{
		return nullptr;
	}

	static const FName GuardLabels[] = {
		FName(TEXT("NODE_GUARD")), FName(TEXT("GP_CampNight_Guard")), FName(TEXT("ANCHOR_NODE_GUARD")),
	};
	static const FName SleeperLabels[] = {
		FName(TEXT("NODE_SLEEPER")), FName(TEXT("GP_CampNight_Sleeper")), FName(TEXT("ANCHOR_NODE_SLEEPER")),
	};
	static const FName CaptiveLabels[] = {
		FName(TEXT("NODE_CAPTIVE")), FName(TEXT("GP_CampNight_Captive")), FName(TEXT("ANCHOR_NODE_CAPTIVE")),
	};

	const FName* Labels = GuardLabels;
	int32 LabelCount = UE_ARRAY_COUNT(GuardLabels);
	if (Role == EHomeWorldCampRole::Sleeper)
	{
		Labels = SleeperLabels;
		LabelCount = UE_ARRAY_COUNT(SleeperLabels);
	}
	else if (Role == EHomeWorldCampRole::Captive)
	{
		Labels = CaptiveLabels;
		LabelCount = UE_ARRAY_COUNT(CaptiveLabels);
	}

	auto Matches = [](AActor* Actor, const FName& Label) -> bool
	{
		if (!Actor || Label.IsNone())
		{
			return false;
		}
#if WITH_EDITOR
		if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
		{
			return true;
		}
#endif
		return Actor->GetName().Contains(Label.ToString()) || Actor->ActorHasTag(Label);
	};

	int32 Seen = 0;
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		AActor* Candidate = *It;
		if (!Candidate)
		{
			continue;
		}
		for (int32 Index = 0; Index < LabelCount; ++Index)
		{
			if (Matches(Candidate, Labels[Index]))
			{
				if (Seen == Ordinal)
				{
					return Candidate;
				}
				++Seen;
				break;
			}
		}
	}
	return nullptr;
}

bool UHomeWorldSpiritStealthComponent::TryEaseCampActor(EHomeWorldCampRole Role, int32 Ordinal)
{
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: ease skipped - need FORM_SPIRIT (role=%s)"),
			HomeWorldCampNight::GetRoleLogName(Role));
		return false;
	}
	if (Role == EHomeWorldCampRole::Captive)
	{
		// The captive is not eased, they are untied. Freeing them is TryFreeCaptive, which
		// is gated on the other three. Refuse loudly rather than silently doing nothing.
		UE_LOG(LogHomeWorld, Log, TEXT("CAMP: ease refused - the captive is FREED, not eased (M16)"));
		return false;
	}

	FHomeWorldCampActorCalm* State = FindCampActor(Role, Ordinal);
	if (!State)
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: ease failed - no tracked actor (role=%s ordinal=%d)"),
			HomeWorldCampNight::GetRoleLogName(Role), Ordinal);
		return false;
	}

	AActor* Found = FindCampActorInWorld(GetWorld(), Role, Ordinal);
	if (Found)
	{
		State->bSoftLatch = false;
	}
	else
	{
		// KEEP-LOCAL soft path, kept because the camp has no .umap yet. It is marked so the
		// strict gate can reject it - a count granted without an actor is a courtesy, not
		// evidence, and conflating the two is what let #14 certify itself with nothing there.
		State->bSoftLatch = true;
	}

	State->bEased = true;

	if (Role == EHomeWorldCampRole::Guard)
	{
		// "ease their thoughts so that they fall asleep" - easing the guard IS the act that
		// puts them to sleep. There is no separate sleep verb for them.
		State->bAsleep = true;
	}
	else
	{
		// "ease their thoughts too to keep them sleeping" - this verb only maintains. If the
		// sleeper is somehow awake, easing them is not keeping them asleep, so bAsleep is
		// deliberately left alone and the gate stays shut.
		if (!State->bAsleep)
		{
			UE_LOG(LogHomeWorld, Log,
				TEXT("CAMP: sleeper %d eased while AWAKE - keep-sleeping does not apply, gate stays shut"),
				Ordinal);
		}
	}

	UE_LOG(LogHomeWorld, Log,
		TEXT("CAMP: ease ok (role=%s ordinal=%d eased=1 asleep=%d world_actor=%d soft_latch=%d; soothe != convert)"),
		HomeWorldCampNight::GetRoleLogName(Role), Ordinal, State->bAsleep ? 1 : 0,
		Found ? 1 : 0, State->bSoftLatch ? 1 : 0);

	// Keep the legacy counters in step so old logs stay readable. They are not the gate.
	if (Role == EHomeWorldCampRole::Guard && GuardsAvoidedCount < 1)
	{
		GuardsAvoidedCount = 1;
	}
	else if (Role == EHomeWorldCampRole::Sleeper && !State->bSoftLatch && SleepersSoothedCount < 2)
	{
		++SleepersSoothedCount;
	}

	return true;
}

void UHomeWorldSpiritStealthComponent::NotifyCampActorWoke(EHomeWorldCampRole Role, int32 Ordinal)
{
	if (FHomeWorldCampActorCalm* State = FindCampActor(Role, Ordinal))
	{
		if (!State->bAsleep)
		{
			return;
		}
		State->bAsleep = false;
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: %s %d WOKE - freedom gate closed (eased=%d; keeping them sleeping can fail)"),
			HomeWorldCampNight::GetRoleLogName(Role), Ordinal, State->bEased ? 1 : 0);
	}
}

void UHomeWorldSpiritStealthComponent::NotifyCampActorKilled(EHomeWorldCampRole Role, int32 Ordinal)
{
	if (FHomeWorldCampActorCalm* State = FindCampActor(Role, Ordinal))
	{
		State->bKilled = true;
		State->bAsleep = false;
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: %s %d KILLED - anti-case, a dead actor is not a calmed one"),
			HomeWorldCampNight::GetRoleLogName(Role), Ordinal);
	}
}

void UHomeWorldSpiritStealthComponent::NotifyCampActorConverted(EHomeWorldCampRole Role, int32 Ordinal)
{
	if (FHomeWorldCampActorCalm* State = FindCampActor(Role, Ordinal))
	{
		State->bConverted = true;
		State->bAsleep = false;
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: %s %d CONVERTED - anti-case, conversion is what happens to foes you defeat; it is not care"),
			HomeWorldCampNight::GetRoleLogName(Role), Ordinal);
	}
}

int32 UHomeWorldSpiritStealthComponent::GetCalmedActorCount() const
{
	int32 Count = 0;
	for (const FHomeWorldCampActorCalm& Actor : CampActors)
	{
		if (HomeWorldCampNight::CountsInFreedomGate(Actor.Role) && Actor.SatisfiesFreedomGateStrict())
		{
			++Count;
		}
	}
	return Count;
}

bool UHomeWorldSpiritStealthComponent::IsFreedomUnlockedStrict() const
{
	int32 Seen = 0;
	for (const FHomeWorldCampActorCalm& Actor : CampActors)
	{
		if (!HomeWorldCampNight::CountsInFreedomGate(Actor.Role))
		{
			continue;
		}
		++Seen;
		if (!Actor.SatisfiesFreedomGateStrict())
		{
			return false;
		}
	}
	// Counting the array as well as the gate is deliberate. If someone adds a fourth camp
	// actor without widening GetGatedActorCount, this returns false rather than passing on
	// a subset - a narrower gate is a beat the player cannot complete, and that must be loud.
	return Seen == HomeWorldCampNight::GetGatedActorCount();
}

bool UHomeWorldSpiritStealthComponent::IsFreedomUnlocked() const
{
	int32 Seen = 0;
	bool bAllSoft = true;
	for (const FHomeWorldCampActorCalm& Actor : CampActors)
	{
		if (!HomeWorldCampNight::CountsInFreedomGate(Actor.Role))
		{
			continue;
		}
		++Seen;
		if (!Actor.SatisfiesFreedomGate())
		{
			return false;
		}
		if (!Actor.bSoftLatch)
		{
			bAllSoft = false;
		}
	}

	if (Seen == HomeWorldCampNight::GetGatedActorCount() && bAllSoft && !bLoggedSoftLatchOnly)
	{
		bLoggedSoftLatchOnly = true;
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: SOFT_LATCH_ONLY - gameplay gate is open but every count came from a missing actor. "
				"Treat M14 as NOT PROVEN; IsFreedomUnlockedStrict() is the evidence."));
	}

	return Seen == HomeWorldCampNight::GetGatedActorCount();
}

bool UHomeWorldSpiritStealthComponent::TryFreeCaptive()
{
	if (bCaptiveFreed)
	{
		UE_LOG(LogHomeWorld, Log, TEXT("CAMP: captive already freed"));
		return true;
	}

	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	if (!Character || !Character->GetIsSpiritForm())
	{
		UE_LOG(LogHomeWorld, Log, TEXT("CAMP: free refused - need FORM_SPIRIT"));
		return false;
	}

	// M15: untying lashings is an Allowed spirit touch. Assert the rule rather than assume
	// it, so a later edit that flips the verdict fails here instead of quietly contradicting
	// the touch table.
	const EHomeWorldSpiritTouchVerdict Touch =
		HomeWorldCampNight::GetSpiritTouchVerdict(EHomeWorldSpiritTouchTarget::Lashings);
	if (Touch != EHomeWorldSpiritTouchVerdict::Allowed)
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: free refused - M15 says a spirit may not touch LASHINGS (%s)"),
			HomeWorldCampNight::GetSpiritTouchReason(EHomeWorldSpiritTouchTarget::Lashings));
		return false;
	}

	if (!IsFreedomUnlocked())
	{
		UE_LOG(LogHomeWorld, Log,
			TEXT("CAMP: free REFUSED - %d/%d calm, strict=%d (a killed or converted actor does not count)"),
			GetCalmedActorCount(), HomeWorldCampNight::GetGatedActorCount(),
			IsFreedomUnlockedStrict() ? 1 : 0);
		return false;
	}

	bCaptiveFreed = true;
	UE_LOG(LogHomeWorld, Log,
		TEXT("CAMP: CAPTIVE FREED (%d/%d calm, strict=%d; lashings untied by spirit; no force option)"),
		GetCalmedActorCount(), HomeWorldCampNight::GetGatedActorCount(),
		IsFreedomUnlockedStrict() ? 1 : 0);
	return true;
}

EHomeWorldSpiritTouchVerdict UHomeWorldSpiritStealthComponent::EvaluateSpiritTouch(
	EHomeWorldSpiritTouchTarget Target) const
{
	AHomeWorldCharacter* Character = Cast<AHomeWorldCharacter>(GetOwner());
	const bool bSpirit = Character && Character->GetIsSpiritForm();
	const EHomeWorldSpiritTouchVerdict Verdict = HomeWorldCampNight::GetSpiritTouchVerdict(Target);

	// Every verdict is logged. A refusal the player cannot see reads as a broken game, so
	// silence is the failure mode this avoids - not the wrongness of the verdict.
	UE_LOG(LogHomeWorld, Log,
		TEXT("TOUCH: target=%s form=%s verdict=%s - %s"),
		HomeWorldCampNight::GetSpiritTouchTargetLogName(Target),
		bSpirit ? TEXT("SPIRIT") : TEXT("BODY"),
		Verdict == EHomeWorldSpiritTouchVerdict::Allowed ? TEXT("ALLOWED") : TEXT("REFUSED"),
		HomeWorldCampNight::GetSpiritTouchReason(Target));

	return Verdict;
}

bool UHomeWorldSpiritStealthComponent::GetCampActorState(
	EHomeWorldCampRole Role, int32 Ordinal, bool& bOutEased, bool& bOutAsleep) const
{
	if (const FHomeWorldCampActorCalm* State = FindCampActor(Role, Ordinal))
	{
		bOutEased = State->bEased;
		bOutAsleep = State->bAsleep;
		return true;
	}
	bOutEased = false;
	bOutAsleep = false;
	return false;
}

bool UHomeWorldSpiritStealthComponent::IsCampNightBeatComplete() const
{
	return IsFreedomUnlocked();
}
