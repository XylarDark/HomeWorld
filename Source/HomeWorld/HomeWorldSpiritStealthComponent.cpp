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
	// T0 #14 NODE_GUARD — spirit stealth avoid (not convert; not lit-volume alone as beat).
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
		// Prefer hidden / unlit cue when near guard — stealth path, not convert.
		const bool bHidden = IsSpiritHiddenCueActive();
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_GUARD avoid ok (actor present; hidden_cue=%d; not convert; not GP_SS_Lit alone)"),
			bHidden ? 1 : 0);
	}
	else
	{
		// KEEP-LOCAL soft: Present?=N — no umap guard; Source emit without .uasset/.umap.
		UE_LOG(LogHomeWorld, Log,
			TEXT("STEALTH: NODE_GUARD avoid soft latch (KEEP-LOCAL actor missing; Present?=N; not script-only GP_SS_Lit; not convert)"));
	}
	return true;
}

bool UHomeWorldSpiritStealthComponent::TrySootheNodeSleeper()
{
	// T0 #14 NODE_SLEEPER — soothe care verb. convert != soothe (never ReportFoeConverted here).
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
