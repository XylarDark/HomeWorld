// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorld.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldInventorySubsystem.h"

#define LOCTEXT_NAMESPACE "FHomeWorldModule"

namespace
{
	void CmdSave(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Save requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldSaveGameSubsystem* Save = GI->GetSubsystem<UHomeWorldSaveGameSubsystem>();
		if (!Save) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SaveGameSubsystem not found.")); return; }
		const bool bOk = Save->SaveGameToSlot(FString(), 0);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Save %s"), bOk ? TEXT("succeeded") : TEXT("failed"));
	}

	void CmdLoad(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Load requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldSaveGameSubsystem* Save = GI->GetSubsystem<UHomeWorldSaveGameSubsystem>();
		if (!Save) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SaveGameSubsystem not found.")); return; }
		const bool bOk = Save->LoadGameFromSlot(FString(), 0);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Load %s"), bOk ? TEXT("succeeded") : TEXT("failed"));
	}

	void CmdReportDeath(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.ReportDeath requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		Char->ReportDeathAndAddSpirit();
	}

	void CmdGrantBossReward(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.GrantBossReward requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
		if (!Inv) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: InventorySubsystem not found.")); return; }
		const int32 Amount = Args.Num() > 0 ? FCString::Atoi(*Args[0]) : 100;
		Inv->AddResource(FName("Wood"), Amount);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.GrantBossReward granted Wood +%d (boss reward placeholder)."), Amount);
	}

	void CmdPlaceWall(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.PlaceWall requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		const bool bOk = Char->TryPlaceAtCursor();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.PlaceWall %s"), bOk ? TEXT("succeeded") : TEXT("failed"));
	}
}

void FHomeWorldModule::StartupModule()
{
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Save"),
		TEXT("Save game (roles + spirit roster) to default slot. Use in PIE for T5 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSave),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Load"),
		TEXT("Load game from default slot. Use in PIE for T5 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdLoad),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.ReportDeath"),
		TEXT("Report player death and add to spirit roster (T5 / Day 21 verification)."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdReportDeath),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.GrantBossReward"),
		TEXT("Grant boss reward (Wood amount, default 100). Use in PIE for T5 / Day 25 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGrantBossReward),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.PlaceWall"),
		TEXT("Place PlaceActorClass (e.g. BP_BuildOrder_Wall) at cursor. Requires PIE; run create_bp_build_order_wall.py first."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdPlaceWall),
		ECVF_Cheat);
}

void FHomeWorldModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_PRIMARY_GAME_MODULE(FHomeWorldModule, HomeWorld, "HomeWorld");
