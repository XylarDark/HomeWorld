// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningZipline.h"

#include "HomeWorldCharacter.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Materials/MaterialInterface.h"

AHomeWorldOpeningZipline::AHomeWorldOpeningZipline()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.bStartWithTickEnabled = false;

	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	auto MakeBlock = [this](const TCHAR* Name)
	{
		UStaticMeshComponent* Mesh = CreateDefaultSubobject<UStaticMeshComponent>(Name);
		Mesh->SetupAttachment(GetRootComponent());
		Mesh->SetCollisionProfileName(FName(TEXT("BlockAll")));
		return Mesh;
	};
	Perch = MakeBlock(TEXT("Perch"));
	Step1 = MakeBlock(TEXT("Step1"));
	Step2 = MakeBlock(TEXT("Step2"));
	Step3 = MakeBlock(TEXT("Step3"));
	SideStep1 = MakeBlock(TEXT("SideStep1"));
	SideStep2 = MakeBlock(TEXT("SideStep2"));
	SideStep3 = MakeBlock(TEXT("SideStep3"));
	StartPole = MakeBlock(TEXT("StartPole"));
	EndPole = MakeBlock(TEXT("EndPole"));
	EndPerch = MakeBlock(TEXT("EndPerch"));
	Cable = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Cable"));
	Cable->SetupAttachment(GetRootComponent());
	Cable->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Tags.Add(FName(TEXT("NODE_ZIPLINE")));
}

void AHomeWorldOpeningZipline::SetLine(FVector PerchFeet, FVector LandingFeet)
{
	RideStart = PerchFeet;
	RideEnd = LandingFeet;
	SetActorLocation(PerchFeet);
	BuildVisuals();
}

void AHomeWorldOpeningZipline::SetStairs(FVector DirA, FVector DirB, bool bAtPerch)
{
	DirA.Z = 0.f;
	DirB.Z = 0.f;
	StairA = DirA.GetSafeNormal();
	StairB = DirB.GetSafeNormal();
	if (StairA.IsNearlyZero())
	{
		StairA = FVector(0.f, -1.f, 0.f);
	}
	if (StairB.IsNearlyZero())
	{
		StairB = FVector(1.f, 0.f, 0.f);
	}
	bStairsAtPerch = bAtPerch;
	BuildVisuals();
}

void AHomeWorldOpeningZipline::BuildVisuals()
{
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	UStaticMesh* Cylinder = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	auto PlaceStep = [Cube](UStaticMeshComponent* Mesh, const FVector& RelativeCm, const FVector& SizeCm)
	{
		if (!Mesh || !Cube)
		{
			return;
		}
		Mesh->SetStaticMesh(Cube);
		Mesh->SetRelativeLocation(RelativeCm);
		Mesh->SetRelativeScale3D(SizeCm / 100.f);
	};
	UMaterialInterface* Blue = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Cyan.MI_Greybox_Cyan"));
	UMaterialInterface* PathGreen = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Olive.MI_Greybox_Olive"));
	auto Paint = [](UStaticMeshComponent* Mesh, UMaterialInterface* Material)
	{
		if (Mesh && Material)
		{
			Mesh->SetMaterial(0, Material);
		}
	};
	PlaceStep(Perch, FVector(0.f, 0.f, -20.f), FVector(300.f, 240.f, 40.f));
	Paint(Perch, Blue);
	auto HideStep = [](UStaticMeshComponent* Mesh)
	{
		if (!Mesh)
		{
			return;
		}
		Mesh->SetVisibility(false);
		Mesh->SetHiddenInGame(true);
		Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	};
	HideStep(Step2);
	HideStep(Step3);
	HideStep(SideStep2);
	HideStep(SideStep3);
	// Landing feet are 1.5 m above the pad, so that is the ground under either corner.
	const float PadZ = RideEnd.Z - 150.f;
	auto PlaceRamp = [&](UStaticMeshComponent* Mesh, const FVector& Dir)
	{
		if (!Mesh || !Cube)
		{
			return;
		}
		const FVector Base = bStairsAtPerch ? RideStart : RideEnd;
		const float Rise = FMath::Max(Base.Z - PadZ, 40.f);
		constexpr float SlopeDeg = 22.f;
		const float Run = Rise / FMath::Tan(FMath::DegreesToRadians(SlopeDeg));
		const FVector Top = Base + Dir * 160.f;
		const FVector Bottom = FVector(Top.X, Top.Y, PadZ) + Dir * Run;
		const FVector Uphill = (Top - Bottom).GetSafeNormal();
		const FVector Side = FVector::UpVector.Cross(Dir).GetSafeNormal();
		FVector Normal = Side.Cross(Uphill).GetSafeNormal();
		if (Normal.Z < 0.f)
		{
			Normal *= -1.f;
		}
		constexpr float Thickness = 30.f;
		constexpr float Width = 180.f;
		const float Length = FVector::Dist(Top, Bottom);
		Mesh->SetStaticMesh(Cube);
		Mesh->SetVisibility(true);
		Mesh->SetHiddenInGame(false);
		Mesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
		Mesh->SetCollisionProfileName(FName(TEXT("BlockAll")));
		Mesh->SetWorldLocation((Top + Bottom) * 0.5f - Normal * (Thickness * 0.5f));
		Mesh->SetWorldRotation(FRotationMatrix::MakeFromXZ(Uphill, Normal).Rotator());
		Mesh->SetWorldScale3D(FVector(Length / 100.f, Width / 100.f, Thickness / 100.f));
		Paint(Mesh, PathGreen);
	};
	PlaceRamp(Step1, StairA);
	PlaceRamp(SideStep1, StairB);
	const FVector CableStart = RideStart + FVector(0.f, 0.f, 230.f);
	const FVector CableEnd = RideEnd + FVector(0.f, 0.f, 230.f);
	if (StartPole && Cylinder)
	{
		StartPole->SetStaticMesh(Cylinder);
		StartPole->SetWorldLocation(RideStart + FVector(0.f, 0.f, 115.f));
		StartPole->SetWorldRotation(FRotator::ZeroRotator);
		StartPole->SetWorldScale3D(FVector(0.15f, 0.15f, 2.3f));
		Paint(StartPole, Blue);
	}
	if (EndPerch && Cube)
	{
		EndPerch->SetStaticMesh(Cube);
		EndPerch->SetWorldLocation(RideEnd + FVector(0.f, 0.f, -20.f));
		EndPerch->SetWorldRotation(FRotator::ZeroRotator);
		EndPerch->SetWorldScale3D(FVector(2.4f, 2.4f, 0.4f));
		Paint(EndPerch, Blue);
	}
	if (EndPole && Cylinder)
	{
		const float GroundZ = RideStart.Z - 400.f;
		const float CableZ = RideEnd.Z + 230.f;
		const float PoleCm = FMath::Max(CableZ - GroundZ, 250.f);
		EndPole->SetStaticMesh(Cylinder);
		EndPole->SetWorldLocation(FVector(RideEnd.X, RideEnd.Y, GroundZ + PoleCm * 0.5f));
		EndPole->SetWorldRotation(FRotator::ZeroRotator);
		EndPole->SetWorldScale3D(FVector(0.35f, 0.35f, PoleCm / 100.f));
		Paint(EndPole, Blue);
	}
	if (!Cable || !Cylinder)
	{
		return;
	}
	Cable->SetStaticMesh(Cylinder);
	const FVector Span = CableEnd - CableStart;
	const float Length = Span.Size();
	if (Length < 1.f)
	{
		return;
	}
	Cable->SetWorldLocation((CableStart + CableEnd) * 0.5f);
	Cable->SetWorldRotation(FRotationMatrix::MakeFromZ(Span).Rotator());
	Cable->SetWorldScale3D(FVector(0.04f, 0.04f, Length / 100.f));
	Paint(Cable, Blue);
}

bool AHomeWorldOpeningZipline::TryRide(AHomeWorldCharacter* Character)
{
	if (!Character || Rider)
	{
		return Rider != nullptr;
	}
	if (FVector::Dist2D(Character->GetActorLocation(), RideStart) > 280.f)
	{
		return false;
	}
	Rider = Character;
	RideDistance = 0.f;
	if (UCharacterMovementComponent* Move = Character->GetCharacterMovement())
	{
		Move->StopMovementImmediately();
		Move->DisableMovement();
	}
	SetActorTickEnabled(true);
	UE_LOG(LogTemp, Log, TEXT("opening_zipline: ride started"));
	return true;
}

void AHomeWorldOpeningZipline::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (!Rider)
	{
		SetActorTickEnabled(false);
		return;
	}
	const float Length = FVector::Dist(RideStart, RideEnd);
	RideDistance += 900.f * DeltaSeconds;
	const float Alpha = Length > 1.f ? FMath::Clamp(RideDistance / Length, 0.f, 1.f) : 1.f;
	const FVector Feet = FMath::Lerp(RideStart, RideEnd, Alpha);
	const FVector Capsule = Feet + FVector(0.f, 0.f, 90.f);
	Rider->SetActorLocation(Capsule);
	const FVector Along = (RideEnd - RideStart).GetSafeNormal2D();
	if (!Along.IsNearlyZero())
	{
		Rider->SetActorRotation(Along.Rotation());
	}
	if (Alpha >= 1.f)
	{
		if (UCharacterMovementComponent* Move = Rider->GetCharacterMovement())
		{
			Move->SetMovementMode(MOVE_Walking);
		}
		UE_LOG(LogTemp, Log, TEXT("opening_zipline: arrived at the pond"));
		Rider = nullptr;
		SetActorTickEnabled(false);
	}
}
