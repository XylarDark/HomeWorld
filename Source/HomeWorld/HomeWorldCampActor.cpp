// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCampActor.h"
#include "Components/CapsuleComponent.h"
#include "Components/TextRenderComponent.h"
#include "HomeWorldGameMode.h"

namespace
{
	/**
	 * The label each role is discovered by. These three strings are the contract with
	 * `FindCampActorInWorld`, which tries `NODE_<ROLE>` first for each role.
	 */
	const TCHAR* GetCampNodeLabel(EHomeWorldCampRole Role)
	{
		switch (Role)
		{
		case EHomeWorldCampRole::Guard:
			return TEXT("NODE_GUARD");
		case EHomeWorldCampRole::Sleeper:
			return TEXT("NODE_SLEEPER");
		case EHomeWorldCampRole::Captive:
			return TEXT("NODE_CAPTIVE");
		default:
			return TEXT("NODE_CAMP");
		}
	}

	/** Short readable name for the greybox text. The guard is the one you have to reach. */
	const TCHAR* GetCampShortName(EHomeWorldCampRole Role)
	{
		switch (Role)
		{
		case EHomeWorldCampRole::Guard:
			return TEXT("GUARD");
		case EHomeWorldCampRole::Sleeper:
			return TEXT("SLEEPER");
		case EHomeWorldCampRole::Captive:
			return TEXT("COMPANION");
		default:
			return TEXT("CAMP");
		}
	}
}

AHomeWorldCampActor::AHomeWorldCampActor()
{
	PrimaryActorTick.bCanEverTick = false;

	// Never possessed: a camp actor must not take input, drive a camera, or enter the
	// player's possession. AI-driven patrol for the guard is NOT implemented yet - see the
	// CAMP.json `open_questions` entry on clearing layout, which is the Lead's.
	SetCanBeDamaged(false);

	// ACharacter already creates its own CapsuleComponent; do not make a second one. The
	// capsule still gives the actor a physical presence and a profile a player is blocked by.

	// The default Character meshes/arms are absent by design; a visible body is art work that
	// is waiting on the paused camp image.
	if (USkeletalMeshComponent* CampMesh = GetMesh())
	{
		CampMesh->SetVisibility(false, true);
	}

	LabelText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("LabelText"));
	if (LabelText)
	{
		LabelText->SetupAttachment(GetCapsuleComponent());
		LabelText->SetHorizontalAlignment(EHTA_Center);
		LabelText->SetVerticalAlignment(EVRTA_TextCenter);
		LabelText->SetWorldSize(60.f);
		LabelText->SetRelativeLocation(FVector(0.f, 0.f, 110.f));
	}

	RefreshCampIdentity();
}

void AHomeWorldCampActor::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	// Re-run on every edit so flipping CampRole cannot leave a stale tag behind - a stale tag
	// would let the gate count the same person twice, or count nobody.
	RefreshCampIdentity();
}

void AHomeWorldCampActor::RefreshCampIdentity()
{
	const FName Label(GetCampNodeLabel(CampRole));
	Tags.AddUnique(Label);

	if (LabelText)
	{
		LabelText->SetText(FText::FromString(GetCampShortName(CampRole)));
	}

#if WITH_EDITOR
	// Make the actor's label in the editor match what the runtime will look for. Discovery also
	// tries GetName(), and a named actor `NODE_GUARD_0` satisfies that - but the label is what
	// a human reads in the outliner, so it should be the honest one.
	//
	// A deliberately QUALIFIED label is preserved. Two sleepers both resolve as
	// `NODE_SLEEPER`, so `NODE_SLEEPER_A` / `NODE_SLEEPER_B` is the only thing that lets a
	// human - or a re-run of the placement script - tell the two people apart. Only a label
	// naming the WRONG person is repaired.
	const FString Existing = GetActorLabel();
	if (!Existing.StartsWith(Label.ToString(), ESearchCase::CaseSensitive))
	{
		SetActorLabel(Label.ToString());
	}
#endif
}

FText AHomeWorldCampActor::GetCampLabelText() const
{
	return FText::FromString(GetCampNodeLabel(CampRole));
}

void AHomeWorldCampActor::BeginPlay()
{
	Super::BeginPlay();
	// Cheap and idempotent, but worth doing at runtime as well: it means an actor that was
	// placed before this class existed, or duplicated from a template with the wrong tag,
	// still self-heals instead of silently not counting.
	RefreshCampIdentity();

	UE_LOG(LogHomeWorld, Log,
		TEXT("CAMP: actor present role=%s label=%s sleeping_at_start=%d"),
		HomeWorldCampNight::GetRoleLogName(CampRole),
		GetCampNodeLabel(CampRole),
		HomeWorldCampNight::StartsAsleep(CampRole) ? 1 : 0);
}