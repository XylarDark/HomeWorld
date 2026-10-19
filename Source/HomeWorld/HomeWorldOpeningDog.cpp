// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningDog.h"

#include "HomeWorldBeastTameComponent.h"
#include "HomeWorldRuneShapeComponent.h"
#include "Components/SceneComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"

AHomeWorldOpeningDog::AHomeWorldOpeningDog()
{
	PrimaryActorTick.bCanEverTick = true;

	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	TameComponent = CreateDefaultSubobject<UHomeWorldBeastTameComponent>(TEXT("Tame"));
	// The kept homestead walk stays as it is: this tame grants no mount boost.
	TameComponent->bGrantMountBoostOnTame = false;

	RuneShape = CreateDefaultSubobject<UHomeWorldRuneShapeComponent>(TEXT("GraceRune"));

	const auto Part = [this](const TCHAR* Name, const FVector& CenterCm, const FVector& SizeCm, float PitchDeg)
	{
		UStaticMeshComponent* Mesh = CreateDefaultSubobject<UStaticMeshComponent>(Name);
		Mesh->SetupAttachment(Root);
		Mesh->SetRelativeLocation(CenterCm);
		Mesh->SetRelativeRotation(FRotator(PitchDeg, 0.f, 0.f));
		Mesh->SetRelativeScale3D(SizeCm / 100.f);
		Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		Mesh->SetMobility(EComponentMobility::Movable);
		GreyboxParts.Add(Mesh);
	};

	// A low, hunched greybox dog: about 50 cm at the shoulder, nose to tail under a metre.
	Part(TEXT("DogTorso"), FVector(2.f, 0.f, 34.f), FVector(46.f, 24.f, 24.f), 0.f);
	Part(TEXT("DogHead"), FVector(32.f, 0.f, 40.f), FVector(20.f, 17.f, 17.f), 0.f);
	Part(TEXT("DogSnout"), FVector(45.f, 0.f, 35.f), FVector(14.f, 10.f, 9.f), 0.f);
	Part(TEXT("DogEarL"), FVector(27.f, 7.5f, 50.f), FVector(4.5f, 3.5f, 8.5f), 0.f);
	Part(TEXT("DogEarR"), FVector(27.f, -7.5f, 50.f), FVector(4.5f, 3.5f, 8.5f), 0.f);
	Part(TEXT("DogLegFL"), FVector(16.f, 8.5f, 11.f), FVector(7.5f, 7.5f, 22.f), 0.f);
	Part(TEXT("DogLegFR"), FVector(16.f, -8.5f, 11.f), FVector(7.5f, 7.5f, 22.f), 0.f);
	Part(TEXT("DogLegBL"), FVector(-13.f, 8.5f, 11.f), FVector(7.5f, 7.5f, 22.f), 0.f);
	Part(TEXT("DogLegBR"), FVector(-13.f, -8.5f, 11.f), FVector(7.5f, 7.5f, 22.f), 0.f);
	Part(TEXT("DogTail"), FVector(-26.f, 0.f, 40.f), FVector(20.f, 5.f, 5.f), 25.f);

	// The beat-node contract by tag; the interact gate also admits the tame component.
	Tags.Add(FName(TEXT("NODE_OPENING_DOG")));
}

void AHomeWorldOpeningDog::BeginPlay()
{
	Super::BeginPlay();

	if (UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
	{
		for (UStaticMeshComponent* Part : GreyboxParts)
		{
			if (Part)
			{
				Part->SetStaticMesh(Cube);
			}
		}
	}
	ApplyGreyboxColor(false);
	UE_LOG(LogTemp, Log, TEXT("opening_dog: injured, afflicted by Wrath, on the island"));
}

void AHomeWorldOpeningDog::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (!IsDogTamed())
	{
		return;
	}
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!Player)
	{
		return;
	}
	const FVector PlayerLoc = Player->GetActorLocation();
	FVector Behind = -Player->GetActorForwardVector();
	Behind.Z = 0.f;
	if (Behind.IsNearlyZero())
	{
		Behind = FVector(-1.f, 0.f, 0.f);
	}
	Behind.Normalize();
	const FVector Goal(PlayerLoc.X + Behind.X * 180.f, PlayerLoc.Y + Behind.Y * 180.f, GetActorLocation().Z);
	const FVector From = GetActorLocation();
	FVector Step = Goal - From;
	Step.Z = 0.f;
	const float Dist = Step.Size();
	if (Dist < 80.f)
	{
		return;
	}
	Step = Step.GetSafeNormal() * FMath::Min(Dist - 70.f, 450.f * DeltaSeconds);
	const FVector Next = From + Step;
	// Cottage footprint in cm. The follow stops at the walls instead of walking through them.
	const bool bIntoCottage = Next.X > -1500.f && Next.X < 400.f && Next.Y > -800.f && Next.Y < 1200.f;
	const bool bAlreadyInside = From.X > -1500.f && From.X < 400.f && From.Y > -800.f && From.Y < 1200.f;
	if (bIntoCottage && !bAlreadyInside)
	{
		return;
	}
	SetActorLocation(Next, false, nullptr, ETeleportType::TeleportPhysics);
	SetActorRotation(Step.Rotation());
}

void AHomeWorldOpeningDog::NoteGraceDrawn()
{
	bWrathEased = true;
	ApplyGreyboxColor(false);
}

bool AHomeWorldOpeningDog::IsDogTamed() const
{
	if (!TameComponent)
	{
		return false;
	}
	const EHomeWorldBeastTameState State = TameComponent->GetTameState();
	return State == EHomeWorldBeastTameState::Tamed || State == EHomeWorldBeastTameState::Helper;
}

bool AHomeWorldOpeningDog::TryTameWithMixedHerb(AHomeWorldCharacter* Character)
{
	if (!Character || !TameComponent || IsDogTamed())
	{
		return false;
	}
	const bool bTamed = TameComponent->NoteCraftedOffering(Character);
	if (bTamed)
	{
		ApplyGreyboxColor(false);
	}
	return bTamed;
}

UMaterialInterface* AHomeWorldOpeningDog::DangerRedMaterial()
{
	if (UMaterialInterface* Instanced = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_DangerRed.MI_Greybox_DangerRed")))
	{
		return Instanced;
	}
	if (DangerRedDynamic)
	{
		return DangerRedDynamic;
	}
	UMaterialInterface* Master = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Masters/M_SpiritUnlit.M_SpiritUnlit"));
	if (!Master)
	{
		Master = LoadObject<UMaterialInterface>(nullptr,
			TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Slate.MI_Greybox_Slate"));
	}
	if (!Master)
	{
		return nullptr;
	}
	DangerRedDynamic = UMaterialInstanceDynamic::Create(Master, this);
	if (!DangerRedDynamic)
	{
		return nullptr;
	}
	const FLinearColor Red(0.75f, 0.07f, 0.05f, 1.f);
	DangerRedDynamic->SetVectorParameterValue(FName(TEXT("BaseColor")), Red);
	DangerRedDynamic->SetVectorParameterValue(FName(TEXT("Emissive")), Red);
	DangerRedDynamic->SetScalarParameterValue(FName(TEXT("NightMix")), 0.f);
	UE_LOG(LogTemp, Log, TEXT("opening_dog: greybox red is a runtime tint of %s"), *Master->GetName());
	return DangerRedDynamic;
}

void AHomeWorldOpeningDog::ApplyGreyboxColor(bool bGraceDrawAvailable)
{
	const uint8 Key = IsDogTamed() ? 3 : ((bWrathEased || bGraceDrawAvailable) ? 2 : 1);
	if (Key == GreyboxColorKey)
	{
		return;
	}
	const TCHAR* Path = nullptr;
	UMaterialInterface* Material = nullptr;
	if (Key == 3)
	{
		Path = TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Olive.MI_Greybox_Olive");
	}
	else if (Key == 2)
	{
		Path = TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Tan.MI_Greybox_Tan");
	}
	else
	{
		Material = DangerRedMaterial();
	}
	if (Path)
	{
		Material = LoadObject<UMaterialInterface>(nullptr, Path);
	}
	if (!Material)
	{
		return;
	}
	for (UStaticMeshComponent* Part : GreyboxParts)
	{
		if (Part)
		{
			Part->SetMaterial(0, Material);
		}
	}
	GreyboxColorKey = Key;
}

void AHomeWorldOpeningDog::ShowGraceRune(APlayerController* Viewer)
{
	if (!RuneShape)
	{
		return;
	}
	// Same trace as the east herb heart: the ribbon faces the camera and the mouse follows it.
	RuneShape->ShowShape(GraceUnitShape(), GraceSizeCm, true,
		EHomeWorldRuneDrawMode::Trace, EHomeWorldRuneOrientation::CameraParallel, Viewer);
}

const TArray<FVector2D>& AHomeWorldOpeningDog::GraceUnitShape()
{
	// Side profile facing left. A sharp beak, a round head, one high wing, a long tail,
	// and a full breast, so the outline reads as a dove.
	static const TArray<FVector2D> Shape = {
		FVector2D(0.02f, 0.56f),
		FVector2D(0.07f, 0.62f),
		FVector2D(0.11f, 0.60f),
		FVector2D(0.15f, 0.66f),
		FVector2D(0.18f, 0.72f),
		FVector2D(0.24f, 0.76f),
		FVector2D(0.30f, 0.74f),
		FVector2D(0.34f, 0.68f),
		FVector2D(0.36f, 0.60f),
		FVector2D(0.42f, 0.66f),
		FVector2D(0.48f, 0.76f),
		FVector2D(0.56f, 0.84f),
		FVector2D(0.66f, 0.86f),
		FVector2D(0.76f, 0.80f),
		FVector2D(0.84f, 0.70f),
		FVector2D(0.90f, 0.58f),
		FVector2D(0.97f, 0.48f),
		FVector2D(0.90f, 0.40f),
		FVector2D(0.80f, 0.36f),
		FVector2D(0.70f, 0.32f),
		FVector2D(0.58f, 0.26f),
		FVector2D(0.46f, 0.22f),
		FVector2D(0.34f, 0.22f),
		FVector2D(0.24f, 0.28f),
		FVector2D(0.16f, 0.36f),
		FVector2D(0.10f, 0.46f),
		FVector2D(0.07f, 0.52f),
		FVector2D(0.05f, 0.55f),
	};
	return Shape;
}
