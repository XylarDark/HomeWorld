// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldEasePad.h"

#include "Components/SceneComponent.h"

AHomeWorldEasePad::AHomeWorldEasePad()
{
	PrimaryActorTick.bCanEverTick = false;
	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	SetRootComponent(Root);
	Focus = CreateDefaultSubobject<USceneComponent>(TEXT("Focus"));
	Focus->SetupAttachment(Root);
	Focus->SetRelativeLocation(FVector(300.f, 0.f, 0.f));
	Tags.Add(FName(TEXT("EasePad")));
}

EHomeWorldStrokeStep AHomeWorldEasePad::GetOfferedStep() const
{
	switch (CompletedSteps)
	{
	case 0:
		return EHomeWorldStrokeStep::Grace;
	case 1:
		return EHomeWorldStrokeStep::Wrath;
	case 2:
		return EHomeWorldStrokeStep::Paradox;
	default:
		return EHomeWorldStrokeStep::ParadoxExtraPoint;
	}
}

bool AHomeWorldEasePad::NoteMatch(EHomeWorldStrokeStep Played)
{
	if (CompletedSteps >= 4 || Played != GetOfferedStep())
	{
		return false;
	}
	++CompletedSteps;
	return true;
}

FVector AHomeWorldEasePad::GetFocusPoint() const
{
	return Focus ? Focus->GetComponentLocation() : GetActorLocation();
}

float AHomeWorldEasePad::WindUpTimeAt(float WorldSeconds) const
{
	const float Open = FMath::Max(0.f, WindowMax - WindowMin);
	const float Cycle = FMath::Max(Open * 2.f, KINDA_SMALL_NUMBER);
	return WindowMin + FMath::Fmod(FMath::Max(0.f, WorldSeconds), Cycle);
}
