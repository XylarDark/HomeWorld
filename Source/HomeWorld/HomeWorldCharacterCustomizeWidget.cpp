// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacterCustomizeWidget.h"
#include "HomeWorldCharacterCustomizationSubsystem.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

void UHomeWorldCharacterCustomizeWidget::OnConfirmClicked()
{
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Character Confirm clicked; saving profile and closing."));
	UWorld* World = GetWorld();
	UGameInstance* GI = World ? World->GetGameInstance() : nullptr;
	if (UHomeWorldCharacterCustomizationSubsystem* Sub = GI ? GI->GetSubsystem<UHomeWorldCharacterCustomizationSubsystem>() : nullptr)
	{
		Sub->SaveCustomizationToProfile();
	}
	RemoveFromParent();
}

void UHomeWorldCharacterCustomizeWidget::OnBackClicked()
{
	RemoveFromParent();
}
