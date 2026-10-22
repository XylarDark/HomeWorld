// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningReveal.h"

#include "HomeWorldCharacter.h"
#include "HomeWorldOpeningWalker.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"
#include "Materials/MaterialInterface.h"
#include "UObject/ConstructorHelpers.h"

namespace
{
	constexpr float StandOffCm = 180.f;
	constexpr float FollowGapCm = 160.f;
	constexpr float PartnerMeetCm = 280.f;
	/** Cottage origin (-800, 0). East wall inner face is world x 985. */
	constexpr float CounterCenterX = 910.f;
	constexpr float CounterCenterY = 80.f;
	constexpr float CounterDepthCm = 70.f;
	constexpr float CounterLengthCm = 520.f;
	/** Half the 200 cm played body. The shell counter and this grown fallback agree. */
	constexpr float CounterHeightCm = 100.f;
	/** Floor spot west of the counter (local x 1560). The pail owns the north end. */
	const FVector PartnerStandCm(760.f, 0.f, 0.f);
	const FVector PartnerRouteCm[] = {
		FVector(-950.f, -500.f, 0.f),
		FVector(-950.f, -180.f, 0.f),
		FVector(-200.f, 0.f, 0.f),
		PartnerStandCm,
	};
	/** The dog-yard wait point: east of the lane line and short of the knock ring, so the follower can pass. */
	constexpr float ChildYardOffsetX = 150.f;
	constexpr float ChildYardOffsetY = -610.f;
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
		Source->Tags.Remove(FName(TEXT("NPC_CHILD")));
		Source->Tags.Remove(FName(TEXT("NPC_PARTNER")));
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
	static ConstructorHelpers::FObjectFinder<UMaterialInterface> SpiritPurple(
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Purple.MI_Greybox_Purple"));
	if (SpiritPurple.Succeeded())
	{
		Spirit->SetMaterial(0, SpiritPurple.Object);
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

TArray<FVector> AHomeWorldOpeningReveal::ChildRaceRoute(const FVector& DogPoint, float FloorZ)
{
	// Through the north back door into the tame yard. The front door stays the way home.
	TArray<FVector> Route;
	Route.Add(FVector(-400.f, 800.f, FloorZ));
	Route.Add(FVector(-390.f, 900.f, FloorZ));
	Route.Add(FVector(-390.f, 1200.f, FloorZ));
	Route.Add(FVector(DogPoint.X + ChildYardOffsetX, DogPoint.Y + ChildYardOffsetY, FloorZ));
	return Route;
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
	if (SpiritHit)
	{
		SpiritHit->SetCollisionEnabled(ECollisionEnabled::NoCollision);
		SpiritHit->SetCollisionResponseToAllChannels(ECR_Ignore);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: spirit claimed"));
	return true;
}

bool AHomeWorldOpeningReveal::IsSpiritVisible() const
{
	return Spirit && Spirit->IsVisible() && !bClaimed;
}

FVector AHomeWorldOpeningReveal::GetPartnerStandCm() const
{
	return PartnerStandCm;
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
	if (bPartnerLeading || bPartnerWaiting)
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
	PartnerPoints.Reset();
	for (const FVector& Spot : PartnerRouteCm)
	{
		PartnerPoints.Add(FVector(Spot.X, Spot.Y, From.Z));
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
	SpiritHit = NewObject<UBoxComponent>(this, TEXT("SpiritInteract"));
	if (SpiritHit && Spirit)
	{
		SpiritHit->SetupAttachment(Spirit);
		SpiritHit->RegisterComponent();
		SpiritHit->SetBoxExtent(FVector(80.f));
		SpiritHit->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
		SpiritHit->SetCollisionResponseToAllChannels(ECR_Ignore);
		SpiritHit->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
	}
	PlaceKettleCounter();
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
	if (const AHomeWorldCharacter* NightPlayer = Cast<AHomeWorldCharacter>(Pawn))
	{
		if (NightPlayer->IsOpeningNightSpirit())
		{
			return;
		}
	}
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
	if (!bHomecoming && bClaimed && Partner && FollowTarget && Child
		&& FVector::Dist2D(FollowTarget->GetActorLocation(), Partner->GetActorLocation()) <= PartnerMeetCm)
	{
		BeginHomecoming();
	}
	if (!bChildRacing && !bChildAtYard && bHomecoming && !bChildLeading && Child)
	{
		const AHomeWorldCharacter* PlayerChar = Cast<AHomeWorldCharacter>(FollowTarget);
		if (PlayerChar && PlayerChar->IsTeaSprintGateActive())
		{
			BeginChildRace();
		}
	}
	if (bChildLeading)
	{
		LeadChild(DeltaSeconds);
		return;
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
			bPartnerWaiting = true;
			Walker->SetActorRotation(FRotator(0.f, 0.f, 0.f));
			if (UCharacterMovementComponent* Move = Walker->GetCharacterMovement())
			{
				Move->StopMovementImmediately();
				Move->DisableMovement();
			}
			UE_LOG(LogTemp, Log, TEXT("opening_reveal: partner waiting beside the counter"));
		}
	}
}

void AHomeWorldOpeningReveal::BeginHomecoming()
{
	if (bHomecoming)
	{
		return;
	}
	bHomecoming = true;
	bFollowing = false;
	bRunning = false;
	if (!Partner)
	{
		Partner = FindTagged(TEXT("NPC_PARTNER"));
	}
	const float FloorZ = Child ? Child->GetActorLocation().Z : 0.f;
	ChildPoints.Reset();
	ChildPoints.Add(FVector(-950.f, -520.f, FloorZ));
	ChildPoints.Add(FVector(-950.f, -180.f, FloorZ));
	ChildPoints.Add(FVector(-360.f, 400.f, FloorZ));
	ChildPoints.Add(FVector(-360.f, 680.f, FloorZ));
	ChildPoints.Add(FVector(-400.f, 800.f, FloorZ));
	bChildLeading = Child != nullptr;
	ChildLeg = 0;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child))
	{
		Walker->SetMoveSpeed(ChildRunSpeed);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: child follows the partner in, then to their room"));
}

void AHomeWorldOpeningReveal::BeginChildRace()
{
	if (bChildRacing || bChildAtYard || !Child)
	{
		return;
	}
	const float FloorZ = Child->GetActorLocation().Z;
	// The sheet spot is the fallback; the dog actor wins when it is in the map.
	FVector DogPoint(-390.f, 2000.f, FloorZ);
	if (const AActor* Dog = FindTagged(TEXT("NODE_OPENING_DOG")))
	{
		DogPoint = Dog->GetActorLocation();
	}
	ChildPoints = ChildRaceRoute(DogPoint, FloorZ);
	bChildRacing = true;
	bChildLeading = true;
	ChildLeg = 0;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child))
	{
		// The race uses the sprint the tea just granted; the walk falls behind on purpose.
		Walker->SetMoveSpeed(PlayerMaxSpeed);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: the child races to the dog yard (%d points)"), ChildPoints.Num());
}

void AHomeWorldOpeningReveal::LeadChild(float DeltaSeconds)
{
	(void)DeltaSeconds;
	if (!Child)
	{
		bChildLeading = false;
		return;
	}
	if (ChildLeg < 0 || ChildLeg >= ChildPoints.Num())
	{
		bChildLeading = false;
		UE_LOG(LogTemp, Log, TEXT("opening_reveal: child in their room"));
		return;
	}
	AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child);
	if (!Walker)
	{
		bChildLeading = false;
		return;
	}
	Walker->SetMoveSpeed(bChildRacing ? PlayerMaxSpeed : ChildRunSpeed);
	if (Walker->WalkToward(ChildPoints[ChildLeg], 60.f))
	{
		++ChildLeg;
		if (ChildLeg >= ChildPoints.Num())
		{
			bChildLeading = false;
			if (bChildRacing)
			{
				bChildRacing = false;
				bChildAtYard = true;
				if (bChildGoHomeAfterTame)
				{
					BeginChildReturnHome();
					return;
				}
				if (const AActor* Dog = FindTagged(TEXT("NODE_OPENING_DOG")))
				{
					FVector ToDog = Dog->GetActorLocation() - Child->GetActorLocation();
					ToDog.Z = 0.f;
					if (!ToDog.IsNearlyZero())
					{
						Child->SetActorRotation(ToDog.Rotation());
					}
				}
				UE_LOG(LogTemp, Log, TEXT("opening_reveal: child waits at the dog yard"));
			}
			else
			{
				UE_LOG(LogTemp, Log, TEXT("opening_reveal: child in their room"));
			}
		}
	}
}

void AHomeWorldOpeningReveal::StopForOpeningNight()
{
	bFollowing = false;
	bRunning = false;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child))
	{
		if (UCharacterMovementComponent* Move = Walker->GetCharacterMovement())
		{
			Move->StopMovementImmediately();
		}
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: night is solo, the child stays"));
}

void AHomeWorldOpeningReveal::BeginChildReturnHome()
{
	if (!Child)
	{
		return;
	}
	if (!bChildAtYard)
	{
		bChildGoHomeAfterTame = true;
		return;
	}
	const float FloorZ = Child->GetActorLocation().Z;
	ChildPoints.Reset();
	ChildPoints.Add(FVector(-390.f, 1200.f, FloorZ));
	ChildPoints.Add(FVector(-390.f, 900.f, FloorZ));
	ChildPoints.Add(FVector(-400.f, 800.f, FloorZ));
	bChildGoHomeAfterTame = false;
	bChildAtYard = false;
	bChildRacing = false;
	bChildLeading = true;
	ChildLeg = 0;
	if (AHomeWorldOpeningWalker* Walker = Cast<AHomeWorldOpeningWalker>(Child))
	{
		Walker->SetMoveSpeed(ChildRunSpeed);
	}
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: child walks back to their room"));
}

void AHomeWorldOpeningReveal::PlaceKettleCounter()
{
	AActor* Kettle = FindTagged(TEXT("NODE_KETTLE"));
	if (!Kettle)
	{
		return;
	}
	// Make the kettle movable and tan once, whether it ends on the shell counter or on the fallback.
	if (UStaticMeshComponent* KettleComp = Kettle->FindComponentByClass<UStaticMeshComponent>())
	{
		KettleComp->SetMobility(EComponentMobility::Movable);
		if (UMaterialInterface* Tan = LoadObject<UMaterialInterface>(nullptr,
			TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Tan.MI_Greybox_Tan")))
		{
			KettleComp->SetMaterial(0, Tan);
		}
	}
	FVector KettleOrigin = FVector::ZeroVector;
	FVector KettleExtent = FVector::ZeroVector;
	Kettle->GetActorBounds(false, KettleOrigin, KettleExtent);
	const float KettleBaseZ = KettleOrigin.Z - KettleExtent.Z;
	const float KettleLift = Kettle->GetActorLocation().Z - KettleBaseZ;

	// The cabin shell now owns the counter run. Use it as the station instead of growing a
	// second box on top: 90 cm on top of 90 cm is what read chest-high in play.
	AActor* Counter = FindTagged(TEXT("KettleCounter"));
	if (!Counter)
	{
		Counter = FindTagged(TEXT("NODE_CONSUMABLE_STATION"));
	}
	if (Counter)
	{
		FVector CounterOrigin = FVector::ZeroVector;
		FVector CounterExtent = FVector::ZeroVector;
		Counter->GetActorBounds(false, CounterOrigin, CounterExtent);
		Kettle->SetActorLocation(FVector(CounterOrigin.X, CounterOrigin.Y,
			CounterOrigin.Z + CounterExtent.Z + KettleLift));
		Kettle->Tags.Add(FName(TEXT("KettleProp")));
		Kettle->Tags.Remove(FName(TEXT("NODE_KETTLE")));
		Counter->Tags.AddUnique(FName(TEXT("KettleCounter")));
		Counter->Tags.AddUnique(FName(TEXT("NODE_CONSUMABLE_STATION")));
		UE_LOG(LogTemp, Log, TEXT("opening_reveal: kettle on the single kitchen counter, %.0f x %.0f x %.0f"),
			CounterExtent.X * 2.f, CounterExtent.Y * 2.f, CounterExtent.Z * 2.f);
		return;
	}

	UWorld* World = GetWorld();
	UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (!World || !Cube)
	{
		return;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	const FVector KettleLocation = Kettle->GetActorLocation();
	AStaticMeshActor* GrownCounter = World->SpawnActor<AStaticMeshActor>(KettleLocation, FRotator::ZeroRotator, Params);
	if (!GrownCounter || !GrownCounter->GetStaticMeshComponent())
	{
		return;
	}
	UStaticMeshComponent* Mesh = GrownCounter->GetStaticMeshComponent();
	Mesh->SetStaticMesh(Cube);
	if (UMaterialInterface* Grey = LoadObject<UMaterialInterface>(nullptr,
		TEXT("/Game/HomeWorld/Materials/Instances/MI_Greybox_Stone.MI_Greybox_Stone")))
	{
		Mesh->SetMaterial(0, Grey);
	}
	const float FloorZ = KettleBaseZ;
	Mesh->SetMobility(EComponentMobility::Movable);
	Mesh->SetCollisionProfileName(FName(TEXT("BlockAll")));
	Mesh->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
	GrownCounter->SetActorScale3D(FVector(CounterDepthCm / 100.f, CounterLengthCm / 100.f, CounterHeightCm / 100.f));
	const float CenterZ = FloorZ + CounterHeightCm * 0.5f;
	GrownCounter->SetActorLocation(FVector(CounterCenterX, CounterCenterY, CenterZ));
	Kettle->SetActorLocation(FVector(CounterCenterX, CounterCenterY, FloorZ + CounterHeightCm + KettleLift));
	Kettle->Tags.Add(FName(TEXT("KettleProp")));
	GrownCounter->Tags.Add(FName(TEXT("KettleCounter")));
	// The counter is the kitchen consumable station. The kettle on top is a prop: the station
	// press opens, mixes, then brews on it, so the kettle itself is not a target.
	GrownCounter->Tags.Add(FName(TEXT("NODE_CONSUMABLE_STATION")));
	Kettle->Tags.Remove(FName(TEXT("NODE_KETTLE")));
	UE_LOG(LogTemp, Log, TEXT("opening_reveal: grew the kettle counter, %.0f x %.0f x %.0f at the east wall"),
		CounterDepthCm, CounterLengthCm, CounterHeightCm);
}
