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
	// Destinations are usually TargetPoints, not portal actors, so check every portal trigger in the
	// world: if the arrival point is inside one (plus pawn capsule margin), step forward until clear.
	const FVector Base = Destination->GetActorLocation();
	const FVector Forward = Destination->GetActorForwardVector();
	constexpr float CapsuleMargin = 60.0f;
	constexpr float StepCm = 50.0f;
	constexpr int32 MaxSteps = 40;

	TArray<const UHomeWorldShrinePortalComponent*> Portals;
	if (UWorld* World = GetWorld())
	{
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			TInlineComponentArray<UHomeWorldShrinePortalComponent*> Comps(*It);
			for (const UHomeWorldShrinePortalComponent* Comp : Comps)
			{
				Portals.Add(Comp);
			}
		}
	}

	auto IsInsideAnyPortal = [&Portals, CapsuleMargin](const FVector& Point)
	{
		for (const UHomeWorldShrinePortalComponent* Comp : Portals)
		{
			const FTransform Unscaled(Comp->GetComponentQuat(), Comp->GetComponentLocation());
			const FVector Local = Unscaled.InverseTransformPosition(Point);
			const FVector Extent = Comp->GetScaledBoxExtent() + FVector(CapsuleMargin);
			if (FMath::Abs(Local.X) <= Extent.X && FMath::Abs(Local.Y) <= Extent.Y && FMath::Abs(Local.Z) <= Extent.Z)
			{
				return true;
			}
		}
		return false;
	};

	float Offset = 80.0f;
	FVector ArriveLoc = Base + Forward * Offset;
	for (int32 Step = 0; Step < MaxSteps && IsInsideAnyPortal(ArriveLoc); ++Step)
	{
		Offset += StepCm;
		ArriveLoc = Base + Forward * Offset;
	}
	return ArriveLoc;
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

	// Stamp cooldown on all portals BEFORE moving: the teleport fires overlap events synchronously,
	// and stamping after let the destination trigger send the pawn back (recursive ping-pong crash).
	// Destinations are TargetPoints, so stamp every portal in the world, not just a component on Destination.
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		TInlineComponentArray<UHomeWorldShrinePortalComponent*> Comps(*It);
		for (UHomeWorldShrinePortalComponent* Comp : Comps)
		{
			Comp->LastTeleportTime = Now;
		}
	}

	const FVector ArriveLoc = GetArriveLocation(Destination);
	const FRotator ArriveRot(0.0f, Destination->GetActorRotation().Yaw + 180.0f, 0.0f);
	Pawn->SetActorLocationAndRotation(ArriveLoc, ArriveRot, false, nullptr, ETeleportType::TeleportPhysics);

	LOG_PORTAL_FALLBACK(TEXT("transit %s -> %s @ %s"),
		*GetOwner()->GetName(), *Destination->GetName(), *ArriveLoc.ToString());
	return true;
}

bool UHomeWorldShrinePortalComponent::TryPortalTransitToDestination(AActor* InstigatorActor, FName OverrideDestinationLabel)
{
	// T0 #13 home->camp: reuse TryPortalTransit with temporary DestinationLabel override.
	// Architecture Trade-Offs B: no parallel portal service. Restore label so home<->planet pair stays intact.
	if (OverrideDestinationLabel.IsNone())
	{
		LOG_PORTAL_FALLBACK(TEXT("failed -- OverrideDestinationLabel none (NODE_PORTAL_CAMP required for #13)"));
		return false;
	}
	const FName SavedLabel = DestinationLabel;
	DestinationLabel = OverrideDestinationLabel;
	const bool bOk = TryPortalTransit(InstigatorActor);
	DestinationLabel = SavedLabel;
	if (bOk)
	{
		LOG_PORTAL_FALLBACK(TEXT("T0 camp transit via override '%s' (not home<->planet alone)"),
			*OverrideDestinationLabel.ToString());
	}
	return bOk;
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
