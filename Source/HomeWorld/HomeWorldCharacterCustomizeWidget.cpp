// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacterCustomizeWidget.h"
#include "HomeWorldCharacterCustomizationSubsystem.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

void UHomeWorldCharacterCustomizeWidget::OnConfirmClicked()
{
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
