// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldTimeOfDaySubsystem.h"
#include "HomeWorldPlayWorld.h"
#include "HomeWorldSaveGameSubsystem.h"
#include "HAL/IConsoleManager.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Kismet/KismetMaterialLibrary.h"
#include "Materials/MaterialParameterCollection.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Components/SkyAtmosphereComponent.h"
#include "EngineUtils.h"

namespace HomeWorldNightMix
{
	static const TCHAR* MPCAssetPath = TEXT("/Game/HomeWorld/Materials/MPC_HomeWorld_Time.MPC_HomeWorld_Time");
	static const FName NightMixParamName(TEXT("NightMix"));

	float NightMixForPhase(EHomeWorldTimeOfDayPhase Phase)
	{
		switch (Phase)
		{
		case EHomeWorldTimeOfDayPhase::Day:   return 0.f;
		case EHomeWorldTimeOfDayPhase::Dusk:  return 0.35f;
		case EHomeWorldTimeOfDayPhase::Night: return 0.85f; // homestead night target (place_vs_mvp_markers default)
		case EHomeWorldTimeOfDayPhase::Dawn:  return 0.15f;
		default:                              return 0.f;
		}
	}
}

namespace
{
	/** Guard: SetPhase sets the CVar; skip OnChanged re-entry. */
	bool GHomeWorldApplyingPhaseFromSetPhase = false;

	// Override phase for testing (e.g. Defend branch). 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = use default.
	static TAutoConsoleVariable<int32> CVarTimeOfDayPhase(
		TEXT("hw.TimeOfDay.Phase"), 0,
		TEXT("Override time-of-day phase for testing: 0=Day, 1=Dusk, 2=Night, 3=Dawn. -1 = default (Day). Calls SetPhase side effects when changed externally."));

	// Fixed duration of night phase in seconds for "time until dawn" stub countdown (T4 HUD). Default 120.
	static TAutoConsoleVariable<float> CVarNightDurationSeconds(
		TEXT("hw.TimeOfDay.NightDurationSeconds"), 120.f,
		TEXT("Night phase duration in seconds for stub countdown (Dawn in Ns). Used when phase is set to Night."));

	void OnTimeOfDayPhaseCVarChanged(IConsoleVariable* Var)
	{
		if (GHomeWorldApplyingPhaseFromSetPhase || !Var)
		{
			return;
		}

		const int32 Value = Var->GetInt();
		if (Value < 0 || Value > 3)
		{
			return;
		}

		UWorld* World = HomeWorldPlayWorld::Resolve(nullptr);
		if (!World)
		{
			return;
		}

		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			GHomeWorldApplyingPhaseFromSetPhase = true;
			TimeOfDay->SetPhase(static_cast<EHomeWorldTimeOfDayPhase>(Value));
			GHomeWorldApplyingPhaseFromSetPhase = false;
		}
	}

	struct FHomeWorldTimeOfDayCVarRegistrar
	{
		FHomeWorldTimeOfDayCVarRegistrar()
		{
			if (IConsoleVariable* CVar = IConsoleManager::Get().FindConsoleVariable(TEXT("hw.TimeOfDay.Phase")))
			{
				CVar->SetOnChangedCallback(FConsoleVariableDelegate::CreateStatic(&OnTimeOfDayPhaseCVarChanged));
			}
		}
	};

	static FHomeWorldTimeOfDayCVarRegistrar GHomeWorldTimeOfDayCVarRegistrar;
}

EHomeWorldTimeOfDayPhase UHomeWorldTimeOfDaySubsystem::GetCurrentPhase() const
{
	const int32 Override = CVarTimeOfDayPhase.GetValueOnGameThread();
	if (Override >= 0 && Override <= 3)
	{
		return static_cast<EHomeWorldTimeOfDayPhase>(Override);
	}
	// Stub: drive from DaySequence in Week 2+.
	return EHomeWorldTimeOfDayPhase::Day;
}

float UHomeWorldTimeOfDaySubsystem::GetNormalizedTime() const
{
	// Stub: 0.25 = day; implement with DaySequence.
	return 0.25f;
}

bool UHomeWorldTimeOfDaySubsystem::GetIsNight() const
{
	return GetCurrentPhase() == EHomeWorldTimeOfDayPhase::Night;
}

bool UHomeWorldTimeOfDaySubsystem::GetIsDefendPhaseActive() const
{
	return GetIsNight();
}

bool UHomeWorldTimeOfDaySubsystem::GetIsSpiritPhase() const
{
	const EHomeWorldTimeOfDayPhase Phase = GetCurrentPhase();
	return Phase == EHomeWorldTimeOfDayPhase::Night || Phase == EHomeWorldTimeOfDayPhase::Dusk;
}

void UHomeWorldTimeOfDaySubsystem::SetNightMixScalar(float NightMix)
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return;
	}
	UMaterialParameterCollection* MPC = LoadObject<UMaterialParameterCollection>(nullptr, HomeWorldNightMix::MPCAssetPath);
	if (!MPC)
	{
		UE_LOG(LogTemp, Verbose, TEXT("HomeWorld: NightMix MPC not found (%s) — skip (run place_vs_mvp_markers.py on Windows host)."), HomeWorldNightMix::MPCAssetPath);
		return;
	}
	UKismetMaterialLibrary::SetScalarParameterValue(World, MPC, HomeWorldNightMix::NightMixParamName, NightMix);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: NightMix=%.2f on MPC_HomeWorld_Time"), NightMix);
}

void UHomeWorldTimeOfDaySubsystem::ApplyNightMixForPhase(EHomeWorldTimeOfDayPhase Phase)
{
	SetNightMixScalar(HomeWorldNightMix::NightMixForPhase(Phase));
}

void UHomeWorldTimeOfDaySubsystem::SetPhase(EHomeWorldTimeOfDayPhase Phase)
{
	const EHomeWorldTimeOfDayPhase Previous = GetCurrentPhase();

	IConsoleVariable* CVar = IConsoleManager::Get().FindConsoleVariable(TEXT("hw.TimeOfDay.Phase"));
	if (CVar)
	{
		GHomeWorldApplyingPhaseFromSetPhase = true;
		CVar->Set(static_cast<int32>(Phase));
		GHomeWorldApplyingPhaseFromSetPhase = false;
	}
	// Start stub countdown when entering night so GetSecondsUntilDawn() and HUD "Dawn in Ns" work (T4).
	if (Phase == EHomeWorldTimeOfDayPhase::Night && GetWorld())
	{
		const float Duration = CVarNightDurationSeconds.GetValueOnGameThread();
		NightPhaseEndTime = GetWorld()->GetTimeSeconds() + Duration;
	}
	ApplyNightMixForPhase(Phase);

	if (Phase != EHomeWorldTimeOfDayPhase::Day)
	{
		bSkyDefaultDayEmittedForCurrentDay = false;
	}
	else
	{
		// Freeze default bright day skybeat on Day (not folded into kettle / other T0).
		EnsureDefaultBrightDaySky(true);
	}

	if (Phase == EHomeWorldTimeOfDayPhase::Dawn && GetWorld())
	{
		if (UGameInstance* GI = GetWorld()->GetGameInstance())
		{
			if (UHomeWorldSaveGameSubsystem* Save = GI->GetSubsystem<UHomeWorldSaveGameSubsystem>())
			{
				Save->PersistDawnSnapshot();
			}
		}
	}

	if (Phase != Previous)
	{
		LastBroadcastPhase = Phase;
		OnPhaseChanged.Broadcast(Phase);
		if (Phase == EHomeWorldTimeOfDayPhase::Night)
		{
			OnNightStarted.Broadcast();
		}
	}
}

void UHomeWorldTimeOfDaySubsystem::AdvanceToDawn()
{
	// Do not restore Health here — restoration is via day activities only (DAY_RESTORATION_LOOP.md, VISION).
	SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
}

float UHomeWorldTimeOfDaySubsystem::GetSecondsUntilDawn() const
{
	if (!GetIsNight() || !GetWorld()) return -1.f;
	const float Now = GetWorld()->GetTimeSeconds();
	// NightPhaseEndTime is set when SetPhase(Night) is called; if phase was set via console (CVar), use default duration from now.
	if (NightPhaseEndTime <= 0.f)
	{
		const float Duration = CVarNightDurationSeconds.GetValueOnGameThread();
		return Duration; // fixed stub: "Dawn in 120s" when phase set via hw.TimeOfDay.Phase 2
	}
	const float Remaining = NightPhaseEndTime - Now;
	return FMath::Max(0.f, Remaining);
}

bool UHomeWorldTimeOfDaySubsystem::EnsureDefaultBrightDaySky(bool bEmitBeatLog)
{
	// T0_DEFAULT_SKYBOX_DAY / SKY_DEFAULT_DAY / TOD_DAY / ENV_T0_HOME
	// Architecture Trade-Offs A-E: prefer existing TOD Day + NightMix=0 + Engine stock
	// SkyAtmosphere / DirectionalLight / SkyLight -- no parallel sky API, no custom HDRI, no new schema.
	// Anti closed_fail: NF2_B night lookdev-as-day; black/empty sky-as-pass; HDRI invent; .uasset/.umap.
	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	const EHomeWorldTimeOfDayPhase Phase = GetCurrentPhase();
	if (Phase != EHomeWorldTimeOfDayPhase::Day)
	{
		UE_LOG(LogTemp, Log,
			TEXT("SKY_DEFAULT_DAY: skipped - need TOD_DAY (not NF2_B night lookdev-as-day)"));
		return false;
	}

	// NightMix=0 for Day (existing TOD path).
	ApplyNightMixForPhase(EHomeWorldTimeOfDayPhase::Day);

	if (IConsoleVariable* SupportAtmo = IConsoleManager::Get().FindConsoleVariable(TEXT("r.SupportSkyAtmosphere")))
	{
		SupportAtmo->Set(1);
	}
	if (IConsoleVariable* SkyAtmoCVar = IConsoleManager::Get().FindConsoleVariable(TEXT("r.SkyAtmosphere")))
	{
		SkyAtmoCVar->Set(1);
	}

	FActorSpawnParameters SpawnParams;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	const FName DaySunTag(TEXT("HW_SKY_DEFAULT_DAY_Sun"));
	const FName DayAtmoTag(TEXT("HW_SKY_DEFAULT_DAY_Atmo"));
	const FName DaySkyTag(TEXT("HW_SKY_DEFAULT_DAY_SkyLight"));

	int32 AtmoCount = 0;
	int32 SunCount = 0;
	int32 SkyCount = 0;
	bool bSpawnedAtmo = false;
	bool bSpawnedSun = false;
	bool bSpawnedSky = false;

	// --- SkyAtmosphere (Engine stock defaults) ---
	ASkyAtmosphere* Atmo = nullptr;
	for (TActorIterator<ASkyAtmosphere> It(World); It; ++It)
	{
		Atmo = *It;
		++AtmoCount;
		break;
	}
	if (!Atmo)
	{
		Atmo = World->SpawnActor<ASkyAtmosphere>(ASkyAtmosphere::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, SpawnParams);
		if (Atmo)
		{
			Atmo->Tags.AddUnique(DayAtmoTag);
#if WITH_EDITOR
			Atmo->SetActorLabel(TEXT("HW_SKY_DEFAULT_DAY_Atmo"));
#endif
			bSpawnedAtmo = true;
			AtmoCount = 1;
		}
	}

	// --- Day DirectionalLight (prefer tagged day sun; else first non-moon; else spawn) ---
	ADirectionalLight* DaySun = nullptr;
	for (TActorIterator<ADirectionalLight> It(World); It; ++It)
	{
		ADirectionalLight* Light = *It;
		if (Light && Light->ActorHasTag(DaySunTag))
		{
			DaySun = Light;
			break;
		}
	}
	if (!DaySun)
	{
		for (TActorIterator<ADirectionalLight> It(World); It; ++It)
		{
			ADirectionalLight* Light = *It;
			if (!Light)
			{
				continue;
			}
			const FString Label = Light->GetActorNameOrLabel();
			// Skip night lookdev moon TMP actors (NF2_B) -- not day sun.
			if (Label.Contains(TEXT("Moon"), ESearchCase::IgnoreCase) || Label.Contains(TEXT("TMP_PA_E"), ESearchCase::IgnoreCase) || Label.Contains(TEXT("NF2"), ESearchCase::IgnoreCase))
			{
				continue;
			}
			DaySun = Light;
			break;
		}
	}
	if (!DaySun)
	{
		// Engine-typical day sun angle (pitch down).
		DaySun = World->SpawnActor<ADirectionalLight>(
			ADirectionalLight::StaticClass(),
			FVector::ZeroVector,
			FRotator(-46.f, -25.f, 0.f),
			SpawnParams);
		if (DaySun)
		{
			DaySun->Tags.AddUnique(DaySunTag);
#if WITH_EDITOR
			DaySun->SetActorLabel(TEXT("HW_SKY_DEFAULT_DAY_Sun"));
#endif
			bSpawnedSun = true;
		}
	}
	if (DaySun)
	{
		DaySun->Tags.AddUnique(DaySunTag);
		if (UDirectionalLightComponent* Dir = Cast<UDirectionalLightComponent>(DaySun->GetLightComponent()))
		{
			Dir->SetMobility(EComponentMobility::Movable);
			Dir->SetIntensity(10.f); // Engine stock directional default scale
			Dir->SetLightColor(FLinearColor(1.f, 0.98f, 0.92f));
			Dir->SetAtmosphereSunLight(true);
			Dir->SetAtmosphereSunLightIndex(0);
			Dir->SetVisibility(true);
			Dir->SetHiddenInGame(false);
		}
		// Keep a readable day pitch if nearly flat / pointing up.
		const FRotator Rot = DaySun->GetActorRotation();
		if (Rot.Pitch > -10.f || Rot.Pitch < -80.f)
		{
			DaySun->SetActorRotation(FRotator(-46.f, Rot.Yaw, 0.f));
		}
		SunCount = 1;
	}

	// --- SkyLight (captured scene / realtime for PIE readability) ---
	ASkyLight* Sky = nullptr;
	for (TActorIterator<ASkyLight> It(World); It; ++It)
	{
		Sky = *It;
		++SkyCount;
		break;
	}
	if (!Sky)
	{
		Sky = World->SpawnActor<ASkyLight>(ASkyLight::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, SpawnParams);
		if (Sky)
		{
			Sky->Tags.AddUnique(DaySkyTag);
#if WITH_EDITOR
			Sky->SetActorLabel(TEXT("HW_SKY_DEFAULT_DAY_SkyLight"));
#endif
			bSpawnedSky = true;
			SkyCount = 1;
		}
	}
	if (Sky)
	{
		if (USkyLightComponent* SkyComp = Sky->GetLightComponent())
		{
			SkyComp->SetMobility(EComponentMobility::Movable);
			SkyComp->SetIntensity(1.f);
			SkyComp->SetRealTimeCaptureEnabled(true);
			SkyComp->RecaptureSky();
		}
	}

	const bool bStackOk = (AtmoCount > 0 && SunCount > 0);
	if (!bStackOk)
	{
		UE_LOG(LogTemp, Warning,
			TEXT("SKY_DEFAULT_DAY: soft stack incomplete ENV_T0_HOME atmo=%d sun=%d sky=%d (black/empty sky alone = closed_fail)"),
			AtmoCount, SunCount, SkyCount);
	}

	if (bEmitBeatLog && !bSkyDefaultDayEmittedForCurrentDay)
	{
		bSkyDefaultDayEmittedForCurrentDay = true;
		UE_LOG(LogTemp, Log,
			TEXT("SKY_DEFAULT_DAY: bright day defaults TOD_DAY ENV_T0_HOME NightMix=0 atmo=%d(spawned=%d) sun=%d(spawned=%d) sky=%d(spawned=%d) (Engine stock; not NF2_B night lookdev; not HDRI invent)"),
			AtmoCount, bSpawnedAtmo ? 1 : 0, SunCount, bSpawnedSun ? 1 : 0, SkyCount, bSpawnedSky ? 1 : 0);
	}
	else if (bEmitBeatLog)
	{
		UE_LOG(LogTemp, Verbose,
			TEXT("SKY_DEFAULT_DAY: re-ensure TOD_DAY ENV_T0_HOME atmo=%d sun=%d sky=%d (beat already emitted this Day)"),
			AtmoCount, SunCount, SkyCount);
	}

	return bStackOk;
}
