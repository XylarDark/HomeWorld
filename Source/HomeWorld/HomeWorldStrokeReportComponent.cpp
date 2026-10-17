// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldStrokeReportComponent.h"

#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldVirtueComponent.h"

void UHomeWorldStrokeReportComponent::BeginStrokeHold()
{
	HeldStroke.Reset();
	bStrokeHeld = true;
}

void UHomeWorldStrokeReportComponent::AppendCursorSample(FVector2D ScreenPoint, float Time)
{
	if (!bStrokeHeld)
	{
		return;
	}
	FHomeWorldStrokeSample Sample;
	Sample.Point = ScreenPoint;
	Sample.Time = Time;
	HeldStroke.Add(Sample);
}

void UHomeWorldStrokeReportComponent::SampleCursor(float Time)
{
	if (!bStrokeHeld)
	{
		return;
	}
	const APawn* Pawn = Cast<APawn>(GetOwner());
	const APlayerController* Controller = Pawn ? Cast<APlayerController>(Pawn->GetController()) : nullptr;
	if (!Controller)
	{
		return;
	}
	float X = 0.f;
	float Y = 0.f;
	if (!Controller->GetMousePosition(X, Y))
	{
		return;
	}
	AppendCursorSample(FVector2D(X, Y), Time);
}

void UHomeWorldStrokeReportComponent::RecordDrawnPoles(EHomeWorldStrokeStep Step, UHomeWorldVirtueComponent* Virtue) const
{
	if (!Virtue)
	{
		return;
	}
	if (Step == EHomeWorldStrokeStep::Grace)
	{
		Virtue->RecordDrawnPole(EHomeWorldVirtuePole::Grace);
		return;
	}
	if (Step == EHomeWorldStrokeStep::Paradox || Step == EHomeWorldStrokeStep::ParadoxExtraPoint)
	{
		Virtue->RecordDrawnPole(EHomeWorldVirtuePole::Grace);
		Virtue->RecordDrawnPole(EHomeWorldVirtuePole::Wrath);
	}
}

void UHomeWorldStrokeReportComponent::ApplyWeakHit(const FVector& FocusPoint)
{
	const FVector From = GetOwner() ? GetOwner()->GetActorLocation() : FVector::ZeroVector;
	LastWeakHitOffset = HomeWorldStroke::WeakHitStep(From, FocusPoint);
	bWeakHitMoved = true;
	if (AActor* Owner = GetOwner())
	{
		Owner->SetActorLocation(From + LastWeakHitOffset);
	}
}

EHomeWorldStrokeReport UHomeWorldStrokeReportComponent::EndStrokeHold(
	EHomeWorldStrokeStep Step,
	float WindowMin,
	float WindowMax,
	FVector2D ExtraPoint,
	UHomeWorldVirtueComponent* VirtueOverride,
	UHomeWorldFallbackGlideComponent* GlideOverride,
	bool bHasFocus,
	FVector FocusPoint)
{
	const TArray<FHomeWorldStrokeSample> Stroke = HeldStroke;
	bStrokeHeld = false;
	HeldStroke.Reset();
	return ReportStroke(Step, Stroke, WindowMin, WindowMax, ExtraPoint, VirtueOverride, GlideOverride, bHasFocus, FocusPoint);
}

EHomeWorldStrokeReport UHomeWorldStrokeReportComponent::ReportStroke(
	EHomeWorldStrokeStep Step,
	const TArray<FHomeWorldStrokeSample>& Stroke,
	float WindowMin,
	float WindowMax,
	FVector2D ExtraPoint,
	UHomeWorldVirtueComponent* VirtueOverride,
	UHomeWorldFallbackGlideComponent* GlideOverride,
	bool bHasFocus,
	FVector FocusPoint)
{
	bGlideHomeInvoked = false;
	bWeakHitMoved = false;
	LastWeakHitOffset = FVector::ZeroVector;

	const bool bHadCarriedPoint = bHasCarriedPoint;
	const FVector2D HeldPoint = CarriedPoint;
	EHomeWorldStrokeResult Result = HomeWorldStroke::Evaluate(Step, Stroke, WindowMin, WindowMax, ExtraPoint);
	if (Result == EHomeWorldStrokeResult::Match && bHadCarriedPoint
		&& !HomeWorldStroke::PassesThroughPoint(Stroke, HeldPoint))
	{
		Result = EHomeWorldStrokeResult::Miss;
	}
	const bool bParadox = Step == EHomeWorldStrokeStep::Paradox || Step == EHomeWorldStrokeStep::ParadoxExtraPoint;
	if (Result == EHomeWorldStrokeResult::Miss)
	{
		if (bParadox)
		{
			LastReport = EHomeWorldStrokeReport::Bonk;
			bHasCarriedPoint = false;
			CarriedPoint = FVector2D::ZeroVector;
			UHomeWorldFallbackGlideComponent* Glide = GlideOverride;
			if (!Glide && GetOwner())
			{
				Glide = GetOwner()->FindComponentByClass<UHomeWorldFallbackGlideComponent>();
			}
			if (Glide)
			{
				bGlideHomeInvoked = true;
				Glide->StartGlideHome(false);
			}
			return LastReport;
		}
		LastReport = EHomeWorldStrokeReport::WeakHit;
		if (bHasFocus)
		{
			ApplyWeakHit(FocusPoint);
		}
		return LastReport;
	}

	LastReport = EHomeWorldStrokeReport::Matched;
	CarriedPoint = ExtraPoint;
	bHasCarriedPoint = true;
	UHomeWorldVirtueComponent* Virtue = VirtueOverride;
	if (!Virtue && GetOwner())
	{
		Virtue = GetOwner()->FindComponentByClass<UHomeWorldVirtueComponent>();
	}
	RecordDrawnPoles(Step, Virtue);
	return LastReport;
}
