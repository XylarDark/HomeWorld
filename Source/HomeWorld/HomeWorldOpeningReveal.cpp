// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningReveal.h"

#include "HomeWorldOpeningWalker.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "EngineUtils.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"
#include "NavigationSystem.h"
#include "NavigationPath.h"
#include "NavFilters/NavigationQueryFilter.h"
#include "UObject/ConstructorHelpers.h"

namespace
{
	constexpr float StandOffCm = 180.f;
	constexpr float FollowGapCm = 160.f;
	constexpr float PartnerMeetCm = 280.f;
	/** Cottage origin (-800, 0). South entry is local x -150, opening through y -280. */
	const FVector PartnerRouteCm[] = {
		FVector(-950.f, -500.f, 0.f),
		FVector(-950.f, -150.f, 0.f),
		FVector(180.f, -120.f, 0.f),
	};
	AActor* PromoteWalker(UWorld* World, AActor* Source)
	{
		if (!World || !Source || Source->IsA<AHomeWorldOpeningWalker>())
		{
			return Source;
		}
		const float Half = 100.f * Source->GetActorScale3D().Z;
		const FVector Location = Source->GetActorLocation() + FVector(0.f, 0.f, Half);
		const FTransform Spawn(Source->GetActorRotation(), Location, Source->GetActorScale3D());
		AHomeWorldOpeningWalker* Walker = World->SpawnActorDeferred<AHomeWorldOpeningWalker>(
			AHomeWorldOpeningWalker::StaticClass(), Spawn, nullptr, nullptr,
			ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn);
		if (!Walker)
		{
			return Source;
		}
		Walker->CopyAppearance(Source);
		UGameplayStatics::FinishSpawningActor(Walker, Spawn);
		Source->Tags.Empty();
		Source->SetActorHiddenInGame(true);
		Source->SetActorEnableCollision(false);
		return Walker;
	}
}

AHomeWorldOpeningReveal::AHomeWorldOpeningReveal()
{
	PrimaryActorTick.bCanEverTick = true;
	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);

	Spirit = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Spirit"));
	Spirit->SetupAttachment(Root);
	Spirit->SetRelativeScale3D(FVector(0.25f));
	Spirit->SetRelativeLocation(FVector(0.f, 0.f, 40.f));
	Spirit->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Spirit->SetCollisionResponseToAllChannels(ECR_Ignore);
	Spirit->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> SphereMesh(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (SphereMesh.Succeeded())
	{
		Spirit->SetStaticMesh(SphereMesh.Object);
	}

	Crest = CreateDefaultSubobject<UBoxComponent>(TEXT("Crest"));
	Crest->SetupAttachment(Root);
	Crest->SetBoxExtent(FVector(800.f, 400.f, 300.f));
	Crest->SetRelativeLocation(FVector(-600.f, -2530.f, 150.f));
	Crest->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Crest->SetCollisionResponseToAllChannels(ECR_Ignore);
	Crest->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	Crest->SetGenerateOverlapEvents(true);

	Tags.Add(FName(TEXT("OpeningReveal")));
}

FVector AHomeWorldOpeningReveal::StepToward(const FVector& From, const FVector& Goal, float MaxStep)
{
	const FVector Delta(Goal.X - From.X, Goal.Y - From.Y, 0.f);
	const float Distance = Delta.Size();
	if (Distance <= FMath::Max(MaxStep, 1.f))
	{
		return FVector(Goal.X, Goal.Y, From.Z);
	}
	return From + Delta.GetSafeNormal() * MaxStep;
}

bool AHomeWorldOpeningReveal::ChildArrivesFirst(float PlayerDistance, float ChildDistance)
{
	if (PlayerMaxSpeed <= 0.f || ChildRunSpeed <= 0.f || PlayerDistance < 0.f || ChildDistance < 0.f)
	{
		return false;
	}
	const float PlayerTime = PlayerDistance / PlayerMaxSpeed;
	const float ChildTime = ChildDistance / ChildRunSpeed;
	return ChildTime <= PlayerTime;
}

FVector AHomeWorldOpeningReveal::StandNear(const FVector& From, const FVector& SpiritPoint, float InStandOffCm)
{
	FVector Away(From.X - SpiritPoint.X, From.Y - SpiritPoint.Y, 0.f);
	if (Away.SizeSquared() < 1.f)
	{
		Away = FVector(0.f, -1.f, 0.f);
	}
	const FVector Stand = SpiritPoint + Away.GetSafeNormal() * InStandOffCm;
	return FVector(Stand.X, Stand.Y, From.Z);
}

bool AHomeWorldOpeningReveal::TryClaim(APawn* Player)
{
	if (!Player || bClaimed || !Spirit || !Spirit->IsVisible())
	{
		return false;
	}
	bClaimed = true;
	bRunning = false;
	bFollowing = true;
	FollowTarget = Player;
	Spirit->SetVisibility(false);
	Spirit->SetHiddenInGame(true);
	Spirit->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: spirit claimed"));
	return true;
}

bool AHomeWorldOpeningReveal::IsSpiritVisible() const
{
	return Spirit && Spirit->IsVisible() && !bClaimed;
}

AActor* AHomeWorldOpeningReveal::FindTagged(const TCHAR* Tag) const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		return nullptr;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(FName(Tag)))
		{
			return *It;
		}
	}
	return nullptr;
}

bool AHomeWorldOpeningReveal::TryLeadPartner()
{
	if (bPartnerLeading)
	{
		return false;
	}
	if (!Partner)
	{
		Partner = FindTagged(TEXT("NPC_PARTNER"));
	}
	if (!Partner)
	{
		return false;
	}
	const FVector From = Partner->GetActorLocation();
	const FVector Kettle(180.f, -120.f, From.Z);
	PartnerPoints.Reset();
	if (UNavigationSystemV1* Nav = UNavigationSystemV1::GetCurrent(GetWorld()))
	{
		if (UNavigationPath* Path = UNavigationSystemV1::FindPathToLocationSynchronously(
			this, From, Kettle, Partner, UNavigationQueryFilter::StaticClass()))
		{
			if (Path->PathPoints.Num() > 1)
			{
				PartnerPoints = Path->PathPoints;
			}
		}
	}
	if (PartnerPoints.Num() < 2)
	{
		PartnerPoints.Reset();
		for (const FVector& Spot : PartnerRouteCm)
		{
			PartnerPoints.Add(FVector(Spot.X, Spot.Y, From.Z));
		}
	}
	bPartnerLeading = true;
	bPartnerBlockLogged = false;
	PartnerLeg = 0;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Partner))
	{
		Walker->SetMoveSpeed(ChildRunSpeed);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: partner walking to the kettle (%d points)"), PartnerPoints.Num());
	return true;
}

void AHomeWorldOpeningReveal::FitInteractBounds(AActor* Actor) const
{
	if (!Actor)
	{
		return;
	}
	FVector Origin = FVector::ZeroVector;
	FVector Extent = FVector::ZeroVector;
	Actor->GetActorBounds(false, Origin, Extent);
	const float Wide = FMath::Max(FMath::Max(Extent.X, Extent.Y), 50.f);
	Extent.X = FMath::Max(Extent.X, Wide);
	Extent.Y = FMath::Max(Extent.Y, Wide);
	Extent.Z = FMath::Max(Extent.Z, 50.f);
	UBoxComponent* Box = NewObject<UBoxComponent>(Actor, TEXT("InteractBounds"));
	if (!Box)
	{
		return;
	}
	Box->SetupAttachment(Actor->GetRootComponent());
	Box->RegisterComponent();
	Box->SetWorldLocation(Origin);
	Box->SetBoxExtent(Extent);
	Box->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	Box->SetCollisionResponseToAllChannels(ECR_Ignore);
	Box->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
}

void AHomeWorldOpeningReveal::BeginPlay()
{
	Super::BeginPlay();
	if (Spirit)
	{
		Spirit->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		Spirit->SetCollisionResponseToAllChannels(ECR_Ignore);
		Spirit->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	}
	Crest->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldOpeningReveal::OnCrestOverlap);
	if (UWorld* World = GetWorld())
	{
		AActor* FoundChild = nullptr;
		AActor* FoundPartner = nullptr;
		TArray<AActor*> Props;
		for (TActorIterator<AActor> It(World); It; ++It)
		{
			if (!FoundChild && It->ActorHasTag(FName(TEXT("NPC_CHILD"))))
			{
				FoundChild = *It;
			}
			else if (!FoundPartner && It->ActorHasTag(FName(TEXT("NPC_PARTNER"))))
			{
				FoundPartner = *It;
			}
			if (It->ActorHasTag(FName(TEXT("NODE_KETTLE")))
				|| It->ActorHasTag(FName(TEXT("NODE_GARDEN"))))
			{
				Props.Add(*It);
			}
		}
		Child = PromoteWalker(World, FoundChild);
		Partner = PromoteWalker(World, FoundPartner);
		if (Child)
		{
			FitInteractBounds(Child);
		}
		if (Partner)
		{
			FitInteractBounds(Partner);
		}
		for (AActor* Prop : Props)
		{
			FitInteractBounds(Prop);
		}
	}
	UBoxComponent* SpiritHit = NewObject<UBoxComponent>(this, TEXT("SpiritInteract"));
	if (SpiritHit && Spirit)
	{
		SpiritHit->SetupAttachment(Spirit);
		SpiritHit->RegisterComponent();
		SpiritHit->SetBoxExtent(FVector(80.f));
		SpiritHit->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		SpiritHit->SetCollisionResponseToAllChannels(ECR_Ignore);
		SpiritHit->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	}
}

void AHomeWorldOpeningReveal::OnCrestOverlap(
	UPrimitiveComponent* OverlappedComponent,
	AActor* OtherActor,
	UPrimitiveComponent* OtherComp,
	int32 OtherBodyIndex,
	bool bFromSweep,
	const FHitResult& SweepResult)
{
	(void)OverlappedComponent;
	(void)OtherComp;
	(void)OtherBodyIndex;
	(void)bFromSweep;
	(void)SweepResult;
	APawn* Pawn = Cast<APawn>(OtherActor);
	if (bRunning || !Pawn || !Pawn->IsPlayerControlled())
	{
		return;
	}
	const FVector SpiritPoint = GetActorLocation();
	const float PlayerDistance = FVector::Dist2D(Pawn->GetActorLocation(), SpiritPoint);
	float ChildDistance = 0.f;
	if (Child)
	{
		ChildDistance = FVector::Dist2D(Child->GetActorLocation(), SpiritPoint);
	}
	if (!ChildArrivesFirst(PlayerDistance, ChildDistance))
	{
		UE_LOG(LogTemp, Warning, TEXT("opening_reveal: FAIL child is late, player %.0f cm, child %.0f cm"),
			PlayerDistance, ChildDistance);
		return;
	}
	bRunning = true;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child))
	{
		Walker->SetMoveSpeed(ChildRunSpeed);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: child running, player %.0f cm at %.0f cm/s, child %.0f cm at %.0f cm/s"),
		PlayerDistance, PlayerMaxSpeed, ChildDistance, ChildRunSpeed);
}

void AHomeWorldOpeningReveal::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	if (Spirit && !bClaimed && GetWorld())
	{
		const float Bob = FMath::Sin(GetWorld()->GetTimeSeconds() * 2.f) * 12.f;
		Spirit->SetRelativeLocation(FVector(0.f, 0.f, 40.f + Bob));
	}
	if (bPartnerLeading)
	{
		LeadPartner(DeltaSeconds);
	}
	if (!Child)
	{
		return;
	}
	if (bFollowing)
	{
		FollowChild(DeltaSeconds);
		return;
	}
	if (!bRunning)
	{
		return;
	}
	AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child);
	if (!Walker)
	{
		return;
	}
	Walker->SetMoveSpeed(ChildRunSpeed);
	const FVector From = Child->GetActorLocation();
	const FVector Stand = StandNear(From, GetActorLocation(), StandOffCm);
	if (FVector::Dist2D(From, GetActorLocation()) <= StandOffCm || Walker->WalkToward(Stand, 40.f))
	{
		bRunning = false;
		UE_LOG(LogTemp, Log, TEXT("opening_reveal: child beside the spirit"));
	}
}

void AHomeWorldOpeningReveal::FollowChild(float DeltaSeconds)
{
	if (!Child || !FollowTarget)
	{
		return;
	}
	if (!Partner)
	{
		Partner = FindTagged(TEXT("NPC_PARTNER"));
	}
	AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child);
	if (!Walker)
	{
		return;
	}
	Walker->SetMoveSpeed(ChildRunSpeed);
	FVector Goal = FollowTarget->GetActorLocation() - FollowTarget->GetActorForwardVector() * FollowGapCm;
	float Accept = 80.f;
	if (Partner && FVector::Dist2D(FollowTarget->GetActorLocation(), Partner->GetActorLocation()) <= PartnerMeetCm)
	{
		Goal = Partner->GetActorLocation() + FVector(80.f, 0.f, 0.f);
		if (Walker->WalkToward(Goal, Accept))
		{
			bFollowing = false;
			UE_LOG(LogTemp, Log, TEXT("opening_reveal: child with the partner"));
		}
		return;
	}
	Walker->WalkToward(Goal, Accept);
}

void AHomeWorldOpeningReveal::LeadPartner(float DeltaSeconds)
{
	if (!Partner)
	{
		bPartnerLeading = false;
		return;
	}
	if (PartnerLeg < 0 || PartnerLeg >= PartnerPoints.Num())
	{
		bPartnerLeading = false;
		return;
	}
	AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Partner);
	if (!Walker)
	{
		bPartnerLeading = false;
		return;
	}
	Walker->SetMoveSpeed(ChildRunSpeed);
	const FVector Spot = PartnerPoints[PartnerLeg];
	if (Walker->WalkToward(Spot, 60.f))
	{
		++PartnerLeg;
		if (PartnerLeg >= PartnerPoints.Num())
		{
			bPartnerLeading = false;
			UE_LOG(LogTemp, Log, TEXT("opening_reveal: partner beside the kettle"));
		}
	}
}
