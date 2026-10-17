// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldFallbackGlideComponent.h"
#include "HomeWorldStrokeCheck.h"
#include "HomeWorldStrokeReportComponent.h"
#include "HomeWorldVirtueComponent.h"

namespace HomeWorldStrokeTest
{
	static FHomeWorldStrokeSample Sample(float X, float Y, float Time)
	{
		FHomeWorldStrokeSample Value;
		Value.Point = FVector2D(X, Y);
		Value.Time = Time;
		return Value;
	}

	static TArray<FHomeWorldStrokeSample> FromShape(const TArray<FVector2D>& Shape, float Time)
	{
		TArray<FHomeWorldStrokeSample> Stroke;
		for (const FVector2D& Point : Shape)
		{
			Stroke.Add(Sample(Point.X, Point.Y, Time));
		}
		return Stroke;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeGraceMatchesItsShape,
	"HomeWorld.Systems.Stroke.GraceMatchesItsShape",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeGraceMatchesItsShape::RunTest(const FString& Parameters)
{
	const TArray<FHomeWorldStrokeSample> Stroke = HomeWorldStrokeTest::FromShape(HomeWorldStroke::GraceShape(), 9.f);
	const EHomeWorldStrokeResult Result = HomeWorldStroke::Evaluate(
		EHomeWorldStrokeStep::Grace, Stroke, 0.f, 1.f, FVector2D(50.f, 50.f));
	TestEqual(TEXT("grace ignores the window and the extra point"), Result, EHomeWorldStrokeResult::Match);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeWrongShapeMisses,
	"HomeWorld.Systems.Stroke.WrongShapeMisses",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeWrongShapeMisses::RunTest(const FString& Parameters)
{
	const TArray<FHomeWorldStrokeSample> Horizontal = {
		HomeWorldStrokeTest::Sample(0.f, 0.f, 0.f),
		HomeWorldStrokeTest::Sample(1.f, 0.f, 0.f) };
	TestEqual(TEXT("a horizontal stroke is not grace"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::Grace, Horizontal, 0.f, 1.f, FVector2D::ZeroVector),
		EHomeWorldStrokeResult::Miss);
	TestEqual(TEXT("a grace stroke is not the paradox"),
		HomeWorldStroke::Evaluate(
			EHomeWorldStrokeStep::Paradox,
			HomeWorldStrokeTest::FromShape(HomeWorldStroke::GraceShape(), 0.5f),
			0.f, 1.f, FVector2D::ZeroVector),
		EHomeWorldStrokeResult::Miss);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeLateStartMisses,
	"HomeWorld.Systems.Stroke.LateStartMisses",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeLateStartMisses::RunTest(const FString& Parameters)
{
	const TArray<FHomeWorldStrokeSample> InTime = { HomeWorldStrokeTest::Sample(4.f, 4.f, 0.5f) };
	TestEqual(TEXT("wrath matches inside the window and ignores the shape"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::Wrath, InTime, 0.f, 1.f, FVector2D::ZeroVector),
		EHomeWorldStrokeResult::Match);

	const TArray<FHomeWorldStrokeSample> Late = HomeWorldStrokeTest::FromShape(HomeWorldStroke::ParadoxShape(), 5.f);
	TestEqual(TEXT("a late paradox start is a miss"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::Paradox, Late, 0.f, 1.f, FVector2D::ZeroVector),
		EHomeWorldStrokeResult::Miss);
	TestEqual(TEXT("a late wrath start is the same miss"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::Wrath, { HomeWorldStrokeTest::Sample(0.f, 0.f, 5.f) }, 0.f, 1.f, FVector2D::ZeroVector),
		EHomeWorldStrokeResult::Miss);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeExtraPoint,
	"HomeWorld.Systems.Stroke.ExtraPoint",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeExtraPoint::RunTest(const FString& Parameters)
{
	TArray<FHomeWorldStrokeSample> Stroke;
	Stroke.Add(HomeWorldStrokeTest::Sample(0.f, 0.f, 0.2f));
	Stroke.Add(HomeWorldStrokeTest::Sample(0.5f, 0.5f, 0.2f));
	Stroke.Add(HomeWorldStrokeTest::Sample(1.f, 1.f, 0.2f));
	const FVector2D OnLine(0.5f, 0.5f);
	TestEqual(TEXT("the extra point on the stroke matches"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::ParadoxExtraPoint, Stroke, 0.f, 1.f, OnLine),
		EHomeWorldStrokeResult::Match);
	TestEqual(TEXT("a far extra point misses"),
		HomeWorldStroke::Evaluate(EHomeWorldStrokeStep::ParadoxExtraPoint, Stroke, 0.f, 1.f, FVector2D(8.f, -3.f)),
		EHomeWorldStrokeResult::Miss);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeReportUsesExistingEaseAndGlide,
	"HomeWorld.Systems.Stroke.ReportUsesExistingEaseAndGlide",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeReportUsesExistingEaseAndGlide::RunTest(const FString& Parameters)
{
	UHomeWorldStrokeReportComponent* Report = NewObject<UHomeWorldStrokeReportComponent>();
	UHomeWorldFallbackGlideComponent* Glide = NewObject<UHomeWorldFallbackGlideComponent>();
	UHomeWorldVirtueComponent* Virtue = NewObject<UHomeWorldVirtueComponent>();
	if (!TestNotNull(TEXT("report"), Report) || !TestNotNull(TEXT("glide"), Glide) || !TestNotNull(TEXT("virtue"), Virtue))
	{
		return false;
	}

	const TArray<FHomeWorldStrokeSample> Grace = HomeWorldStrokeTest::FromShape(HomeWorldStroke::GraceShape(), 0.f);
	const EHomeWorldStrokeReport Matched = Report->ReportStroke(
		EHomeWorldStrokeStep::Grace, Grace, 0.f, 1.f, FVector2D::ZeroVector, Virtue, Glide);
	TestEqual(TEXT("a grace match is reported"), Matched, EHomeWorldStrokeReport::Matched);
	TestTrue(TEXT("a grace match records the drawn pole"), Virtue->HasDrawnPole(EHomeWorldVirtuePole::Grace));
	TestFalse(TEXT("a grace match does not glide home"), Report->WasGlideHomeInvoked());

	const TArray<FHomeWorldStrokeSample> Late = { HomeWorldStrokeTest::Sample(0.f, 0.f, 4.f) };
	const FVector Focus(100.f, 0.f, 0.f);
	const EHomeWorldStrokeReport Weak = Report->ReportStroke(
		EHomeWorldStrokeStep::Wrath, Late, 0.f, 1.f, FVector2D::ZeroVector, Virtue, Glide, true, Focus);
	TestEqual(TEXT("a wrath miss is the weak hit"), Weak, EHomeWorldStrokeReport::WeakHit);
	TestFalse(TEXT("a weak hit does not glide home"), Report->WasGlideHomeInvoked());
	TestTrue(TEXT("a focused weak hit steps away"), Report->WasWeakHitMoved());
	const FVector Expected = HomeWorldStroke::WeakHitStep(FVector::ZeroVector, Focus);
	TestTrue(TEXT("the step leaves the focus"), FVector::Dist(Expected, Focus) > FVector::Dist(FVector::ZeroVector, Focus));
	TestTrue(TEXT("the reported offset matches the step"), Report->GetLastWeakHitOffset().Equals(Expected, 0.1f));

	const TArray<FHomeWorldStrokeSample> Paradox = HomeWorldStrokeTest::FromShape(HomeWorldStroke::ParadoxShape(), 9.f);
	const EHomeWorldStrokeReport Bonk = Report->ReportStroke(
		EHomeWorldStrokeStep::Paradox, Paradox, 0.f, 1.f, FVector2D::ZeroVector, Virtue, Glide);
	TestEqual(TEXT("a paradox miss is a bonk"), Bonk, EHomeWorldStrokeReport::Bonk);
	TestTrue(TEXT("a bonk calls the existing glide home"), Report->WasGlideHomeInvoked());
	TestFalse(TEXT("a bonk does not step away"), Report->WasWeakHitMoved());
	TestTrue(TEXT("a paradox match is not this miss"), !Virtue->HasDrawnPole(EHomeWorldVirtuePole::Wrath));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeCursorFeedsTheCheck,
	"HomeWorld.Systems.Stroke.CursorFeedsTheCheck",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeCursorFeedsTheCheck::RunTest(const FString& Parameters)
{
	UHomeWorldStrokeReportComponent* Report = NewObject<UHomeWorldStrokeReportComponent>();
	UHomeWorldVirtueComponent* Virtue = NewObject<UHomeWorldVirtueComponent>();
	if (!TestNotNull(TEXT("report"), Report) || !TestNotNull(TEXT("virtue"), Virtue))
	{
		return false;
	}

	Report->SampleCursor(0.f);
	TestEqual(TEXT("a cursor sample without a held stroke is ignored"), Report->GetHeldStroke().Num(), 0);

	Report->BeginStrokeHold();
	Report->SampleCursor(0.f);
	TestEqual(TEXT("no player cursor leaves the stroke empty"), Report->GetHeldStroke().Num(), 0);

	for (const FVector2D& Point : HomeWorldStroke::GraceShape())
	{
		Report->AppendCursorSample(Point, 0.f);
	}
	TestEqual(TEXT("held samples are the cursor points"), Report->GetHeldStroke().Num(), 2);
	const EHomeWorldStrokeReport Matched = Report->EndStrokeHold(
		EHomeWorldStrokeStep::Grace, 0.f, 1.f, FVector2D::ZeroVector, Virtue);
	TestEqual(TEXT("ending the hold feeds the stroke check"), Matched, EHomeWorldStrokeReport::Matched);
	TestFalse(TEXT("the hold ends"), Report->IsStrokeHeld());
	TestEqual(TEXT("the held stroke is cleared"), Report->GetHeldStroke().Num(), 0);
	TestTrue(TEXT("the match records Grace"), Virtue->HasDrawnPole(EHomeWorldVirtuePole::Grace));

	Report->BeginStrokeHold();
	for (const FVector2D& Point : HomeWorldStroke::ParadoxShape())
	{
		Report->AppendCursorSample(Point, 0.2f);
	}
	Report->EndStrokeHold(EHomeWorldStrokeStep::Paradox, 0.f, 1.f, FVector2D::ZeroVector, Virtue);
	TestTrue(TEXT("a paradox match records Wrath as well"), Virtue->HasDrawnPole(EHomeWorldVirtuePole::Wrath));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeCarriedPointPersists,
	"HomeWorld.Systems.Stroke.CarriedPointPersists",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeCarriedPointPersists::RunTest(const FString& Parameters)
{
	UHomeWorldStrokeReportComponent* Report = NewObject<UHomeWorldStrokeReportComponent>();
	if (!TestNotNull(TEXT("report"), Report))
	{
		return false;
	}

	const FVector2D Kept(4.f, 4.f);
	const EHomeWorldStrokeReport Matched = Report->ReportStroke(
		EHomeWorldStrokeStep::Grace,
		HomeWorldStrokeTest::FromShape(HomeWorldStroke::GraceShape(), 0.f),
		0.f, 1.f, Kept);
	TestEqual(TEXT("a match stores the extra point"), Matched, EHomeWorldStrokeReport::Matched);
	TestTrue(TEXT("the point is in hand"), Report->HasCarriedPoint());
	TestEqual(TEXT("the stored point is the extra point"), Report->GetCarriedPoint(), Kept);

	const TArray<FHomeWorldStrokeSample> Aside = {
		HomeWorldStrokeTest::Sample(1.f, 0.f, 0.5f),
		HomeWorldStrokeTest::Sample(2.f, 0.f, 0.6f)
	};
	const EHomeWorldStrokeReport Weak = Report->ReportStroke(
		EHomeWorldStrokeStep::Wrath, Aside, 0.f, 1.f, FVector2D::ZeroVector);
	TestEqual(TEXT("a stroke that misses the carried point is a weak hit"), Weak, EHomeWorldStrokeReport::WeakHit);
	TestTrue(TEXT("a weak hit keeps the point"), Report->HasCarriedPoint());
	TestEqual(TEXT("the kept point is unchanged"), Report->GetCarriedPoint(), Kept);

	TArray<FHomeWorldStrokeSample> Through = Aside;
	Through.Add(HomeWorldStrokeTest::Sample(Kept.X, Kept.Y, 0.7f));
	const EHomeWorldStrokeReport Again = Report->ReportStroke(
		EHomeWorldStrokeStep::Wrath, Through, 0.f, 1.f, FVector2D(9.f, 1.f));
	TestEqual(TEXT("a stroke through the carried point can match"), Again, EHomeWorldStrokeReport::Matched);
	TestEqual(TEXT("the match stores the new extra point"), Report->GetCarriedPoint(), FVector2D(9.f, 1.f));

	const EHomeWorldStrokeReport Bonk = Report->ReportStroke(
		EHomeWorldStrokeStep::Paradox,
		HomeWorldStrokeTest::FromShape(HomeWorldStroke::ParadoxShape(), 5.f),
		0.f, 1.f, FVector2D::ZeroVector);
	TestEqual(TEXT("a paradox miss is a bonk"), Bonk, EHomeWorldStrokeReport::Bonk);
	TestFalse(TEXT("a bonk drops the point"), Report->HasCarriedPoint());
	return true;
}
#endif
