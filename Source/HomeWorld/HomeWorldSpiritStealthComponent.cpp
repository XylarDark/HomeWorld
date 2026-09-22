// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldSpiritLitVolume.h"
#include "Components/PointLightComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/Character.h"

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
