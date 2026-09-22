// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritStealthComponent.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldSpiritLitVolume.h"

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
	UE_LOG(LogHomeWorld, Log, TEXT("STEALTH:STATUS lit=%d alert=%.2f overlaps=%d force=%d"),
		IsSpiritLit() ? 1 : 0, AlertLevel, LitOverlapCount, bForceLitCheat ? 1 : 0);
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
