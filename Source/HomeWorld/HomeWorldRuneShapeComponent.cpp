// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldRuneShapeComponent.h"

#include "HomeWorldWispPlacement.h"

#include "Components/SplineMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "Materials/MaterialInterface.h"

namespace
{
	constexpr float HeartScaleCm = 5.2f;
	constexpr int32 HeartOutlineCount = 48;
	constexpr float PointMinArcCm = 34.f;
	constexpr float TraceCorridorCm = 70.f;
	constexpr int32 RuneSectionCount = 10;
	constexpr float PointClickCm = 28.f;
	constexpr float TraceStepCm = 18.f;

	void HeartLocal(float Turn, float& X, float& Y)
	{
		X = 16.f * FMath::Pow(FMath::Sin(Turn), 3.f);
		Y = 13.f * FMath::Cos(Turn) - 5.f * FMath::Cos(2.f * Turn) - 2.f * FMath::Cos(3.f * Turn) - FMath::Cos(4.f * Turn);
	}

	float ArcBetween(const TArray<float>& Arc, int32 A, int32 B)
	{
		if (Arc.Num() == 0)
		{
			return 0.f;
		}
		const float Total = Arc.Last();
		const float Forward = FMath::Abs(Arc[B] - Arc[A]);
		return FMath::Min(Forward, Total - Forward);
	}

	int32 RandomInRun(const TArray<int32>& Indices, FRandomStream& Stream)
	{
		if (Indices.Num() == 0)
		{
			return 0;
		}
		const int32 Margin = FMath::Max(1, Indices.Num() / 6);
		const int32 Begin = FMath::Min(Margin, Indices.Num() - 1);
		const int32 Last = FMath::Max(Begin, Indices.Num() - Margin - 1);
		return Indices[Stream.RandRange(Begin, Last)];
	}

	float DistanceToOutline(const FVector& Point, const TArray<FVector>& Outline, bool bClosed)
	{
		float Best = TNumericLimits<float>::Max();
		const int32 Segments = bClosed ? Outline.Num() : FMath::Max(0, Outline.Num() - 1);
		for (int32 Index = 0; Index < Segments; ++Index)
		{
			const FVector& A = Outline[Index];
			const FVector& B = Outline[(Index + 1) % Outline.Num()];
			const FVector Segment = B - A;
			const float LengthSq = Segment.SizeSquared();
			float Along = 0.f;
			if (LengthSq > KINDA_SMALL_NUMBER)
			{
				Along = FMath::Clamp(FVector::DotProduct(Point - A, Segment) / LengthSq, 0.f, 1.f);
			}
			Best = FMath::Min(Best, FVector::Dist(Point, A + Segment * Along));
		}
		return Best;
	}
}

UHomeWorldRuneShapeComponent::UHomeWorldRuneShapeComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false;
}

void UHomeWorldRuneShapeComponent::EnsureRibbon(int32 SegmentCount)
{
	UStaticMesh* Cylinder = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	AActor* Owner = GetOwner();
	while (Segments.Num() < SegmentCount && Owner)
	{
		// Outer is this component, so bounds measurement can tell rune ribbons from the prop.
		USplineMeshComponent* Segment = NewObject<USplineMeshComponent>(this);
		if (!Segment)
		{
			break;
		}
		if (Cylinder)
		{
			Segment->SetStaticMesh(Cylinder);
		}
		Segment->SetMobility(EComponentMobility::Movable);
		Segment->SetUsingAbsoluteLocation(true);
		Segment->SetUsingAbsoluteRotation(true);
		Segment->SetUsingAbsoluteScale(true);
		Segment->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		Segment->SetForwardAxis(ESplineMeshAxis::Z, false);
		Segment->SetStartScale(FVector2D(0.12f, 0.12f), false);
		Segment->SetEndScale(FVector2D(0.12f, 0.12f), false);
		Segment->SetupAttachment(Owner->GetRootComponent());
		Segment->RegisterComponent();
		Segments.Add(Segment);
	}
}

void UHomeWorldRuneShapeComponent::PickClickPoints()
{
	ClickOrder.Reset();
	if (bCustomShape)
	{
		// A custom outline has no heart regions: mark the first, middle, and last points.
		const int32 Count = HeartLocalPoints.Num();
		if (Count >= 3)
		{
			ClickOrder.Add(0);
			ClickOrder.Add(Count / 2);
			ClickOrder.Add(Count - 1);
		}
		return;
	}
	float MinY = TNumericLimits<float>::Max();
	float MaxY = TNumericLimits<float>::Lowest();
	for (const FVector2D& Point : HeartLocalPoints)
	{
		MinY = FMath::Min(MinY, Point.Y);
		MaxY = FMath::Max(MaxY, Point.Y);
	}
	const float Split = MinY + (MaxY - MinY) * 0.42f;
	TArray<int32> TopRight;
	TArray<int32> Bottom;
	TArray<int32> TopLeft;
	for (int32 Index = 0; Index < HeartLocalPoints.Num(); ++Index)
	{
		if (HeartLocalPoints[Index].Y <= Split)
		{
			Bottom.Add(Index);
		}
		else if (HeartLocalPoints[Index].X >= 0.f)
		{
			TopRight.Add(Index);
		}
		else
		{
			TopLeft.Add(Index);
		}
	}
	FRandomStream Stream(FPlatformTime::Cycles());
	int32 Picked[3] = {
		RandomInRun(TopRight, Stream),
		RandomInRun(Bottom, Stream),
		RandomInRun(TopLeft, Stream)
	};
	for (int32 Attempt = 0; Attempt < 8; ++Attempt)
	{
		const bool bFar = ArcBetween(Arc, Picked[0], Picked[1]) >= PointMinArcCm
			&& ArcBetween(Arc, Picked[1], Picked[2]) >= PointMinArcCm
			&& ArcBetween(Arc, Picked[0], Picked[2]) >= PointMinArcCm;
		if (bFar)
		{
			break;
		}
		Picked[0] = RandomInRun(TopRight, Stream);
		Picked[1] = RandomInRun(Bottom, Stream);
		Picked[2] = RandomInRun(TopLeft, Stream);
	}
	ClickOrder.Add(Picked[0]);
	ClickOrder.Add(Picked[1]);
	ClickOrder.Add(Picked[2]);
}

void UHomeWorldRuneShapeComponent::Rebuild(const FVector& Right, const FVector& Up, const FVector& Center)
{
	if (bCustomShape)
	{
		if (HeartLocalPoints.Num() != UnitShapePoints.Num())
		{
			HeartLocalPoints.Reset();
			for (const FVector2D& Unit : UnitShapePoints)
			{
				HeartLocalPoints.Add(FVector2D((Unit.X - 0.5f) * CustomSizeCm, (Unit.Y - 0.5f) * CustomSizeCm));
			}
		}
	}
	else if (HeartLocalPoints.Num() != HeartOutlineCount)
	{
		HeartLocalPoints.Reset();
		for (int32 Index = 0; Index < HeartOutlineCount; ++Index)
		{
			const float Turn = (TWO_PI * Index) / HeartOutlineCount;
			float X = 0.f;
			float Y = 0.f;
			HeartLocal(Turn, X, Y);
			HeartLocalPoints.Add(FVector2D(X, Y));
		}
	}
	Outline.Reset();
	Arc.Reset();
	float Length = 0.f;
	for (int32 Index = 0; Index < HeartLocalPoints.Num(); ++Index)
	{
		const float LocalScale = bCustomShape ? 1.f : HeartScaleCm;
		const FVector Point = Center + Right * HeartLocalPoints[Index].X * LocalScale + Up * HeartLocalPoints[Index].Y * LocalScale;
		if (Index > 0)
		{
			Length += FVector::Dist(Outline.Last(), Point);
		}
		Outline.Add(Point);
		Arc.Add(Length);
	}
	if (Outline.Num() > 1 && bOutlineClosed)
	{
		Length += FVector::Dist(Outline.Last(), Outline[0]);
	}
	Arc.Add(Length);
	if (DrawMode == EHomeWorldRuneDrawMode::Points && ClickOrder.Num() != 3)
	{
		PickClickPoints();
	}
	Goals.Reset();
	if (DrawMode == EHomeWorldRuneDrawMode::Points)
	{
		for (int32 Index : ClickOrder)
		{
			if (Outline.IsValidIndex(Index))
			{
				Goals.Add(Outline[Index]);
			}
		}
	}
	else if (bCustomShape)
	{
		// The trace starts at the outline's first point and walks it in order.
		for (const FVector& Point : Outline)
		{
			Goals.Add(Point);
		}
	}
	else
	{
		const int32 Bottom = HeartOutlineCount / 2;
		for (int32 Index = 0; Index < Outline.Num(); ++Index)
		{
			Goals.Add(Outline[(Bottom + Index) % Outline.Num()]);
		}
	}
	ApplyRibbon();
	ApplyProgress();
}

void UHomeWorldRuneShapeComponent::ApplyRibbon()
{
	EnsureRibbon(Outline.Num());
	const int32 Surface = bOutlineClosed ? Outline.Num() : FMath::Max(0, Outline.Num() - 1);
	for (int32 Index = 0; Index < Segments.Num(); ++Index)
	{
		USplineMeshComponent* Segment = Segments[Index];
		if (!Segment)
		{
			continue;
		}
		if (Index < Surface)
		{
			const FVector Origin = GetOwner() ? GetOwner()->GetActorLocation() : FVector::ZeroVector;
			const FVector Start = Outline[Index] - Origin;
			const FVector End = Outline[(Index + 1) % Outline.Num()] - Origin;
			const FVector Tangent = End - Start;
			Segment->SetWorldLocation(Origin);
			Segment->SetWorldRotation(FRotator::ZeroRotator);
			Segment->SetStartAndEnd(Start, Tangent, End, Tangent, true);
			const TCHAR* RibbonPath = bCustomShape
				? TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Purple.MI_Greybox_Purple")
				: (DrawMode == EHomeWorldRuneDrawMode::Points
					? TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Slate.MI_Greybox_Slate")
					: TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Stone.MI_Greybox_Stone"));
			if (UMaterialInterface* Ribbon = LoadObject<UMaterialInterface>(nullptr, RibbonPath))
			{
				Segment->SetMaterial(0, Ribbon);
			}
			Segment->SetHiddenInGame(false);
			Segment->SetVisibility(true);
		}
		else
		{
			Segment->SetHiddenInGame(true);
		}
	}
	UStaticMesh* Sphere = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	AActor* Owner = GetOwner();
	while (ClickMarks.Num() < 3 && Owner)
	{
		// Outer is this component, so bounds measurement can tell rune marks from the prop.
		UStaticMeshComponent* Mark = NewObject<UStaticMeshComponent>(this);
		if (!Mark)
		{
			break;
		}
		if (Sphere)
		{
			Mark->SetStaticMesh(Sphere);
		}
		Mark->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		Mark->SetUsingAbsoluteLocation(true);
		Mark->SetUsingAbsoluteScale(true);
		Mark->SetWorldScale3D(FVector(0.32f));
		Mark->SetupAttachment(Owner->GetRootComponent());
		Mark->RegisterComponent();
		ClickMarks.Add(Mark);
	}
	for (int32 Index = 0; Index < ClickMarks.Num(); ++Index)
	{
		if (!ClickMarks[Index])
		{
			continue;
		}
		const bool bShow = DrawMode == EHomeWorldRuneDrawMode::Points && Goals.IsValidIndex(Index);
		ClickMarks[Index]->SetHiddenInGame(!bShow);
		ClickMarks[Index]->SetVisibility(bShow);
		if (bShow)
		{
			ClickMarks[Index]->SetWorldLocation(Goals[Index]);
			if (UMaterialInterface* MarkGrey = LoadObject<UMaterialInterface>(nullptr,
				TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Stone.MI_Greybox_Stone")))
			{
				ClickMarks[Index]->SetMaterial(0, MarkGrey);
			}
		}
	}
}

void UHomeWorldRuneShapeComponent::ApplyProgress()
{
	if (DrawMode == EHomeWorldRuneDrawMode::Points)
	{
		for (int32 Index = 0; Index < ClickMarks.Num(); ++Index)
		{
			if (ClickMarks[Index])
			{
				const bool bShow = Index >= Progress && Goals.IsValidIndex(Index);
				ClickMarks[Index]->SetHiddenInGame(!bShow);
				ClickMarks[Index]->SetVisibility(bShow);
			}
		}
		return;
	}
}

void UHomeWorldRuneShapeComponent::ShowHeart(EHomeWorldRuneDrawMode Draw, EHomeWorldRuneOrientation InOrientation, APlayerController* InViewer)
{
	bCustomShape = false;
	bOutlineClosed = true;
	HeartLocalPoints.Reset();
	DrawMode = Draw;
	Orientation = InOrientation;
	Viewer = InViewer;
	bShown = true;
	bBasisLocked = false;
	bInSection = false;
	Progress = 0;
	SectionsEarned = 0;
	ClickOrder.Reset();
	AlignToViewer(InViewer);
	SetComponentTickEnabled(true);
	FVector MeshCenter = FVector::ZeroVector;
	FVector MeshExtent = FVector::ZeroVector;
	if (GetOwner())
	{
		HomeWorldWisp::MeasureBounds(GetOwner(), MeshCenter, MeshExtent);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_rune: %s heart, %s, reward %d, center %s, owner %s mesh %s + %s"),
		Draw == EHomeWorldRuneDrawMode::Points ? TEXT("points") : TEXT("trace"),
		InOrientation == EHomeWorldRuneOrientation::Static ? TEXT("static") : TEXT("camera"),
		GetReward(),
		*PlaneOrigin.ToString(),
		GetOwner() ? *GetOwner()->GetActorNameOrLabel() : TEXT("none"),
		*MeshCenter.ToString(),
		*MeshExtent.ToString());
}

void UHomeWorldRuneShapeComponent::ShowShape(const TArray<FVector2D>& UnitPoints, float SizeCm, bool bCloseLoop,
	EHomeWorldRuneDrawMode Draw, EHomeWorldRuneOrientation InOrientation, APlayerController* InViewer)
{
	if (UnitPoints.Num() < 2)
	{
		return;
	}
	bCustomShape = true;
	bOutlineClosed = bCloseLoop;
	UnitShapePoints = UnitPoints;
	CustomSizeCm = FMath::Max(20.f, SizeCm);
	HeartLocalPoints.Reset();
	DrawMode = Draw;
	Orientation = InOrientation;
	Viewer = InViewer;
	bShown = true;
	bBasisLocked = false;
	bInSection = false;
	Progress = 0;
	SectionsEarned = 0;
	ClickOrder.Reset();
	AlignToViewer(InViewer);
	SetComponentTickEnabled(true);
	UE_LOG(LogTemp, Log, TEXT("opening_rune: %s shape, %s, size %.0f, %d points"),
		Draw == EHomeWorldRuneDrawMode::Points ? TEXT("points") : TEXT("trace"),
		InOrientation == EHomeWorldRuneOrientation::Static ? TEXT("static") : TEXT("camera"),
		CustomSizeCm, UnitPoints.Num());
}

void UHomeWorldRuneShapeComponent::HideShape()
{
	bShown = false;
	Progress = 0;
	SetComponentTickEnabled(false);
	for (USplineMeshComponent* Segment : Segments)
	{
		if (Segment)
		{
			Segment->SetHiddenInGame(true);
			Segment->SetVisibility(false);
		}
	}
	for (UStaticMeshComponent* Mark : ClickMarks)
	{
		if (Mark)
		{
			Mark->SetHiddenInGame(true);
			Mark->SetVisibility(false);
		}
	}
}

void UHomeWorldRuneShapeComponent::AlignToViewer(APlayerController* InViewer)
{
	if (!bShown || !GetOwner())
	{
		return;
	}
	if (InViewer)
	{
		Viewer = InViewer;
	}
	const FVector OwnerLocation = GetOwner()->GetActorLocation();
	if (Orientation == EHomeWorldRuneOrientation::Static && bBasisLocked)
	{
		const FVector Center = OwnerLocation + LockedOffset;
		PlaneOrigin = Center;
		PlaneRight = LockedRight;
		PlaneUp = LockedUp;
		Rebuild(LockedRight, LockedUp, Center);
		return;
	}
	FVector TowardView(0.f, -1.f, 0.f);
	FVector PlayerLocation = OwnerLocation;
	FVector CameraLocation = OwnerLocation;
	if (APlayerController* PC = Viewer.Get())
	{
		FRotator CameraRotation = FRotator::ZeroRotator;
		PC->GetPlayerViewPoint(CameraLocation, CameraRotation);
		(void)CameraRotation;
		const FVector ToCamera = CameraLocation - OwnerLocation;
		if (ToCamera.SizeSquared2D() > 1.f)
		{
			TowardView = ToCamera.GetSafeNormal2D();
		}
		if (APawn* Pawn = PC->GetPawn())
		{
			PlayerLocation = Pawn->GetActorLocation();
		}
	}
	const FVector Side(-TowardView.Y, TowardView.X, 0.f);
	// Beside the object, not on top of it: the same bounds rule as the shoulder wisp.
	// The fixed offset stays as the fallback when the object has no mesh to measure.
	FVector Center = FVector::ZeroVector;
	if (!HomeWorldWisp::HeartPoint(GetOwner(), CameraLocation, OwnerLocation.Z + 160.f, Center))
	{
		Center = OwnerLocation + Side * 180.f + FVector(0.f, 0.f, 160.f);
	}
	const float HeartReach = 110.f;
	const float BodyClear = 90.f;
	const float Have = FVector::Dist2D(Center, PlayerLocation);
	const float Need = HeartReach + BodyClear;
	if (Have < Need)
	{
		FVector Push = (Center - PlayerLocation).GetSafeNormal2D();
		if (Push.IsNearlyZero())
		{
			Push = Side.GetSafeNormal();
		}
		Center += Push * (Need - Have);
	}
	FVector Face = TowardView;
	if (Viewer.Get())
	{
		const FVector ToCamera = CameraLocation - Center;
		if (ToCamera.SizeSquared2D() > 1.f)
		{
			Face = ToCamera.GetSafeNormal2D();
		}
	}
	const FVector Right = FVector(Face.Y, -Face.X, 0.f).GetSafeNormal();
	const FVector Up = FVector::UpVector;
	LockedRight = Right;
	LockedUp = Up;
	LockedOffset = Center - OwnerLocation;
	PlaneOrigin = Center;
	PlaneRight = Right;
	PlaneUp = Up;
	if (Orientation == EHomeWorldRuneOrientation::Static)
	{
		bBasisLocked = true;
	}
	Rebuild(Right, Up, Center);
}

void UHomeWorldRuneShapeComponent::SetCursor(const FVector& WorldCursor)
{
	Cursor = WorldCursor;
}

bool UHomeWorldRuneShapeComponent::TryClick()
{
	if (!bShown || DrawMode != EHomeWorldRuneDrawMode::Points || !Goals.IsValidIndex(Progress))
	{
		return false;
	}
	if (FVector::Dist(Cursor, Goals[Progress]) >= PointClickCm)
	{
		return false;
	}
	++Progress;
	ApplyProgress();
	UE_LOG(LogTemp, Log, TEXT("opening_rune: click %d, chunks %d"), Progress, GetScore());
	return true;
}

bool UHomeWorldRuneShapeComponent::AdvanceTrace()
{
	if (!bShown || Outline.Num() == 0 || Progress >= RuneSectionCount)
	{
		return false;
	}
	const bool bInside = DistanceToOutline(Cursor, Outline, bOutlineClosed) <= TraceCorridorCm;
	const int32 SectionEnd = ((Progress + 1) * Goals.Num()) / RuneSectionCount;
	const int32 EndIndex = FMath::Clamp(SectionEnd - 1, 0, Goals.Num() - 1);
	if (!bInside)
	{
		if (bInSection)
		{
			bInSection = false;
			++Progress;
			UE_LOG(LogTemp, Log, TEXT("opening_rune: left section %d, score %d/%d"), Progress, SectionsEarned, RuneSectionCount);
			ApplyProgress();
		}
		return false;
	}
	bInSection = true;
	if (FVector::Dist(Cursor, Goals[EndIndex]) < 36.f)
	{
		bInSection = false;
		++SectionsEarned;
		++Progress;
		UE_LOG(LogTemp, Log, TEXT("opening_rune: section %d kept, score %d/%d"), Progress, SectionsEarned, RuneSectionCount);
		ApplyProgress();
	}
	return true;
}

bool UHomeWorldRuneShapeComponent::IsComplete() const
{
	if (!bShown)
	{
		return false;
	}
	if (DrawMode == EHomeWorldRuneDrawMode::Points)
	{
		return Progress >= 3;
	}
	return Progress >= RuneSectionCount;
}

int32 UHomeWorldRuneShapeComponent::GetScore() const
{
	if (DrawMode == EHomeWorldRuneDrawMode::Points)
	{
		if (Progress <= 0)
		{
			return 0;
		}
		if (Progress == 1)
		{
			return 3;
		}
		if (Progress == 2)
		{
			return 6;
		}
		return 10;
	}
	return SectionsEarned;
}

void UHomeWorldRuneShapeComponent::GetPlane(FVector& Origin, FVector& Right, FVector& Up) const
{
	Origin = PlaneOrigin;
	Right = PlaneRight;
	Up = PlaneUp;
}

FVector UHomeWorldRuneShapeComponent::GetStartPoint() const
{
	return Goals.Num() > 0 ? Goals[0] : (GetOwner() ? GetOwner()->GetActorLocation() : FVector::ZeroVector);
}

void UHomeWorldRuneShapeComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bShown)
	{
		AlignToViewer(Viewer.Get());
	}
}
