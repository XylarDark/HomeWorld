// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldShrinePortalComponent.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "GameFramework/Pawn.h"
#include "Engine/World.h"
#include "HAL/IConsoleManager.h"
#include "EngineUtils.h"

namespace
{
	static TAutoConsoleVariable<int32> CVarPortalRequireNight(
		TEXT("hw.Portal.RequireNight"),
		-1,
		TEXT("Override shrine portal night gate: -1=use component bRequireNight, 0=allow day, 1=require night"),
		ECVF_Default);

}

#define LOG_PORTAL_FALLBACK(Format, ...) UE_LOG(LogTemp, Log, TEXT("FALLBACK: Portal " Format), ##__VA_ARGS__)

UHomeWorldShrinePortalComponent::UHomeWorldShrinePortalComponent(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void UHomeWorldShrinePortalComponent::PostInitProperties()
{
	Super::PostInitProperties();
	SetBoxExtent(FVector(120.0f, 120.0f, 150.0f));
	SetCollisionProfileName(FName("OverlapAllDynamic"));
	SetGenerateOverlapEvents(true);
}

void UHomeWorldShrinePortalComponent::BeginPlay()
{
	Super::BeginPlay();
	OnComponentBeginOverlap.AddDynamic(this, &UHomeWorldShrinePortalComponent::OnOverlapBegin);
	LOG_PORTAL_FALLBACK(TEXT("ready — destination '%s', bRequireNight=%s"),
		*DestinationLabel.ToString(), bRequireNight ? TEXT("true") : TEXT("false"));
}

bool UHomeWorldShrinePortalComponent::IsNightGateOpen(UWorld* World) const
{
	const int32 CVarOverride = CVarPortalRequireNight.GetValueOnGameThread();
	const bool bRequireNightEffective = (CVarOverride >= 0) ? (CVarOverride != 0) : bRequireNight;

	if (!bRequireNightEffective)
	{
		return true;
	}

	if (!World)
	{
		return false;
	}

	if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
	{
		return TimeOfDay->GetIsNight();
	}
	return false;
}

AActor* UHomeWorldShrinePortalComponent::FindDestinationActor(UWorld* World) const
{
	if (!World || DestinationLabel.IsNone())
	{
		return nullptr;
	}

	TArray<FName> LabelsToTry;
	LabelsToTry.Add(DestinationLabel);
	const FString DestStr = DestinationLabel.ToString();
	if (!DestStr.StartsWith(TEXT("ANCHOR_")))
	{
		LabelsToTry.Add(FName(*(FString(TEXT("ANCHOR_")) + DestStr)));
	}
	if (DestStr.StartsWith(TEXT("ANCHOR_")))
	{
		LabelsToTry.Add(FName(*DestStr.RightChop(7)));
	}

	for (const FName& Label : LabelsToTry)
	{
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			AActor* Actor = *It;
			if (!Actor || Actor == GetOwner())
			{
				continue;
			}
#if WITH_EDITOR
			if (Actor->GetActorLabel().Equals(Label.ToString(), ESearchCase::CaseSensitive))
			{
				return Actor;
			}
#endif
			if (Actor->GetName().Equals(Label.ToString(), ESearchCase::CaseSensitive))
			{
				return Actor;
			}
		}
	}
	return nullptr;
}

FVector UHomeWorldShrinePortalComponent::GetArriveLocation(AActor* Destination) const
{
	if (!Destination)
	{
		return FVector::ZeroVector;
	}
	// Offset slightly forward from shrine center for safe spawn.
	return Destination->GetActorLocation() + Destination->GetActorForwardVector() * 80.0f;
}

bool UHomeWorldShrinePortalComponent::TryPortalTransit(AActor* InstigatorActor)
{
	if (!InstigatorActor)
	{
		return false;
	}

	APawn* Pawn = Cast<APawn>(InstigatorActor);
	if (!Pawn)
	{
		return false;
	}

	UWorld* World = GetWorld();
	if (!World)
	{
		return false;
	}

	const float Now = World->GetTimeSeconds();
	if (Now - LastTeleportTime < TeleportCooldownSeconds)
	{
		LOG_PORTAL_FALLBACK(TEXT("cooldown — skip transit"));
		return false;
	}

	if (!IsNightGateOpen(World))
	{
		LOG_PORTAL_FALLBACK(TEXT("blocked — night gate closed (day/body; set bRequireNight=false or hw.Portal.RequireNight 0)"));
		return false;
	}

	AActor* Destination = FindDestinationActor(World);
	if (!Destination)
	{
		LOG_PORTAL_FALLBACK(TEXT("failed — destination '%s' not found in level"), *DestinationLabel.ToString());
		return false;
	}

	const FVector ArriveLoc = GetArriveLocation(Destination);
	const FRotator ArriveRot(0.0f, Destination->GetActorRotation().Yaw + 180.0f, 0.0f);
	Pawn->SetActorLocationAndRotation(ArriveLoc, ArriveRot, false, nullptr, ETeleportType::TeleportPhysics);

	LastTeleportTime = Now;
	LOG_PORTAL_FALLBACK(TEXT("transit %s -> %s @ %s"),
		*GetOwner()->GetName(), *Destination->GetName(), *ArriveLoc.ToString());
	return true;
}

void UHomeWorldShrinePortalComponent::OnOverlapBegin(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor)
	{
		return;
	}
	TryPortalTransit(OtherActor);
}
