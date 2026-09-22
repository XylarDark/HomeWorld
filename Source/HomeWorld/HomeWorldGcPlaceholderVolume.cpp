// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGcPlaceholderVolume.h"
#include "HomeWorldCraftSubsystem.h"
#include "Components/BoxComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "HomeWorldGameMode.h"

bool AHomeWorldGcPlaceholderVolume::bKitchenRebindHintLogged = false;

namespace
{
	const TCHAR* GetShortLabel(EHomeWorldGcPlaceholderKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldGcPlaceholderKind::Woodshop:
			return TEXT("WOODSHOP");
		case EHomeWorldGcPlaceholderKind::TextileShop:
			return TEXT("TEXTILE");
		case EHomeWorldGcPlaceholderKind::ResearchShop:
			return TEXT("RESEARCH");
		case EHomeWorldGcPlaceholderKind::CottageKitchen:
			return TEXT("KITCHEN");
		case EHomeWorldGcPlaceholderKind::CottageBedroom:
			return TEXT("BEDROOM");
		case EHomeWorldGcPlaceholderKind::CottageLivingCauldron:
			return TEXT("CAULDRON");
		default:
			return TEXT("ROOM");
		}
	}
}

AHomeWorldGcPlaceholderVolume::AHomeWorldGcPlaceholderVolume()
{
	PrimaryActorTick.bCanEverTick = false;

	TriggerVolume = CreateDefaultSubobject<UBoxComponent>(TEXT("TriggerVolume"));
	SetRootComponent(TriggerVolume);
	TriggerVolume->SetBoxExtent(FVector(120.f, 120.f, 100.f));
	TriggerVolume->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
	TriggerVolume->SetCollisionResponseToAllChannels(ECR_Ignore);
	TriggerVolume->SetCollisionResponseToChannel(ECC_Pawn, ECR_Overlap);
	TriggerVolume->SetGenerateOverlapEvents(true);

	VisualMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("VisualMesh"));
	VisualMesh->SetupAttachment(TriggerVolume);
	VisualMesh->SetRelativeLocation(FVector(0.f, 0.f, -20.f));
	VisualMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);

	LabelText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("LabelText"));
	LabelText->SetupAttachment(TriggerVolume);
	LabelText->SetHorizontalAlignment(EHTA_Center);
	LabelText->SetVerticalAlignment(EVRTA_TextCenter);
	LabelText->SetWorldSize(20.f);
	LabelText->SetRelativeLocation(FVector(0.f, 0.f, 130.f));

	Tags.AddUnique(FName(TEXT("GC_PlaceholderVolume")));
}

void AHomeWorldGcPlaceholderVolume::BeginPlay()
{
	Super::BeginPlay();
	RefreshDemoSpineVisuals();
	TriggerVolume->OnComponentBeginOverlap.AddDynamic(this, &AHomeWorldGcPlaceholderVolume::OnTriggerBeginOverlap);
	TriggerVolume->OnComponentEndOverlap.AddDynamic(this, &AHomeWorldGcPlaceholderVolume::OnTriggerEndOverlap);
}

void AHomeWorldGcPlaceholderVolume::RefreshDemoSpineVisuals()
{
	if (VisualMesh)
	{
		if (UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
		{
			VisualMesh->SetStaticMesh(Cube);
		}
		const bool bCottageRoom = HomeWorldGcPlaceholder::RequiresCottageUnlock(PlaceholderKind);
		VisualMesh->SetRelativeScale3D(bCottageRoom ? FVector(0.85f, 0.85f, 0.25f) : FVector(0.55f, 0.55f, 0.4f));
	}
	if (LabelText)
	{
		LabelText->SetText(FText::FromString(GetShortLabel(PlaceholderKind)));
	}
}

void AHomeWorldGcPlaceholderVolume::OnTriggerBeginOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	if (!OtherActor || bLoggedThisOverlap)
	{
		return;
	}

	APlayerController* PC = GetWorld() ? GetWorld()->GetFirstPlayerController() : nullptr;
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor != PlayerPawn)
	{
		return;
	}

	if (HomeWorldGcPlaceholder::RequiresCottageUnlock(PlaceholderKind))
	{
		UGameInstance* GI = GetWorld() ? GetWorld()->GetGameInstance() : nullptr;
		UHomeWorldCraftSubsystem* Craft = GI ? GI->GetSubsystem<UHomeWorldCraftSubsystem>() : nullptr;
		if (!Craft || !Craft->IsCottageUnlocked())
		{
			if (PlaceholderKind == EHomeWorldGcPlaceholderKind::CottageKitchen)
			{
				UE_LOG(LogHomeWorld, Log, TEXT("PLACEHOLDER:COTTAGE_KITCHEN locked"));
				bLoggedThisOverlap = true;
			}
			return;
		}

		if (PlaceholderKind == EHomeWorldGcPlaceholderKind::CottageKitchen && !bKitchenRebindHintLogged)
		{
			UE_LOG(LogHomeWorld, Log, TEXT("CRAFT: kitchen rebind TODO"));
			bKitchenRebindHintLogged = true;
		}
	}

	const TCHAR* Line = HomeWorldGcPlaceholder::GetEnterLogLine(PlaceholderKind);
	UE_LOG(LogHomeWorld, Log, TEXT("%s"), Line);
	bLoggedThisOverlap = true;
}

void AHomeWorldGcPlaceholderVolume::OnTriggerEndOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor,
	UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	if (!OtherActor || !GetWorld())
	{
		return;
	}

	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	APawn* PlayerPawn = PC ? PC->GetPawn() : nullptr;
	if (OtherActor == PlayerPawn)
	{
		bLoggedThisOverlap = false;
	}
}
