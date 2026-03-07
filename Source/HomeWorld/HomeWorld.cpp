// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorld.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"
#include "HAL/IConsoleManager.h"
#include "HomeWorldBuildOrder.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldSpiritBurstAbility.h"
#include "HomeWorldSpiritShieldAbility.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "AbilitySystemComponent.h"

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

	void CmdAstralDeath(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.AstralDeath requires a play world (PIE or game)."));
			return;
		}
		AGameModeBase* GM = World->GetAuthGameMode();
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(GM);
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		HWGM->OnAstralDeath(PC);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.AstralDeath executed (dawn + respawn at start)."));
	}

	void CmdCompleteBuildOrder(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.CompleteBuildOrder requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC || !PC->GetPawn())
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player pawn for hw.CompleteBuildOrder."));
			return;
		}
		const FVector PlayerLoc = PC->GetPawn()->GetActorLocation();
		TArray<AActor*> Found;
		UGameplayStatics::GetAllActorsOfClass(World, AHomeWorldBuildOrder::StaticClass(), Found);
		AHomeWorldBuildOrder* Nearest = nullptr;
		float NearestDistSq = FLT_MAX;
		for (AActor* A : Found)
		{
			AHomeWorldBuildOrder* BO = Cast<AHomeWorldBuildOrder>(A);
			if (!BO || BO->bBuildCompleted) continue;
			const float DistSq = FVector::DistSquared(PlayerLoc, BO->GetActorLocation());
			if (DistSq < NearestDistSq)
			{
				NearestDistSq = DistSq;
				Nearest = BO;
			}
		}
		if (!Nearest)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.CompleteBuildOrder — no incomplete build order in range. Place one with hw.PlaceWall or key P."));
			return;
		}
		Nearest->CompleteBuildOrder();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.CompleteBuildOrder executed on %s."), *Nearest->GetName());
	}

	void CmdSimulateBuildOrderActivation(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SimulateBuildOrderActivation requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC || !PC->GetPawn())
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player pawn for hw.SimulateBuildOrderActivation."));
			return;
		}
		const FVector PlayerLoc = PC->GetPawn()->GetActorLocation();
		TArray<AActor*> Found;
		UGameplayStatics::GetAllActorsOfClass(World, AHomeWorldBuildOrder::StaticClass(), Found);
		AHomeWorldBuildOrder* Nearest = nullptr;
		float NearestDistSq = FLT_MAX;
		for (AActor* A : Found)
		{
			AHomeWorldBuildOrder* BO = Cast<AHomeWorldBuildOrder>(A);
			if (!BO || BO->bBuildCompleted) continue;
			const float DistSq = FVector::DistSquared(PlayerLoc, BO->GetActorLocation());
			if (DistSq < NearestDistSq)
			{
				NearestDistSq = DistSq;
				Nearest = BO;
			}
		}
		if (!Nearest)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SimulateBuildOrderActivation — no incomplete build order in range. Place one with hw.PlaceWall or key P."));
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: SO_WallBuilder activation (simulated). Completing build order on %s."), *Nearest->GetName());
		Nearest->CompleteBuildOrder();
	}

	void CmdSpiritualPower(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpiritualPower requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player state is not AHomeWorldPlayerState.")); return; }
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual power: %d, Spiritual artefacts: %d"),
			PS->GetSpiritualPowerCollected(), PS->GetSpiritualArtefactsCollected());
	}

	void CmdSpendSpiritualPower(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpendSpiritualPower requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player state is not AHomeWorldPlayerState.")); return; }
		const int32 Amount = Args.Num() > 0 ? FCString::Atoi(*Args[0]) : 1;
		if (Amount <= 0)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpendSpiritualPower N — N must be positive. Example: hw.SpendSpiritualPower 5"));
			return;
		}
		if (PS->SpendSpiritualPower(Amount))
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.SpendSpiritualPower spent %d; remaining: %d (stub: upgrade unlocked)."), Amount, PS->GetSpiritualPowerCollected());
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpendSpiritualPower %d failed — insufficient spiritual power (have %d)."), Amount, PS->GetSpiritualPowerCollected());
		}
	}

	void CmdGoods(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Goods requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No game instance.")); return; }
		UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		const int32 Physical = Inv ? Inv->GetTotalPhysicalGoods() : 0;
		const int32 SpiritualPower = PS ? PS->GetSpiritualPowerCollected() : 0;
		const int32 SpiritualArtefacts = PS ? PS->GetSpiritualArtefactsCollected() : 0;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Goods — Physical (day): %d, Spiritual power (night): %d, Spiritual artefacts (night): %d"),
			Physical, SpiritualPower, SpiritualArtefacts);
	}

	void CmdSpiritBurst(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpiritBurst requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		UAbilitySystemComponent* ASC = Char->GetAbilitySystemComponent();
		if (!ASC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No AbilitySystemComponent on player.")); return; }
		const bool bActivated = ASC->TryActivateAbilityByClass(UHomeWorldSpiritBurstAbility::StaticClass());
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.SpiritBurst %s (set hw.TimeOfDay.Phase 2 for night)."), bActivated ? TEXT("activated") : TEXT("failed — ensure Phase 2 or ability granted"));
	}

	void CmdSpiritShield(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.SpiritShield requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		UAbilitySystemComponent* ASC = Char->GetAbilitySystemComponent();
		if (!ASC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No AbilitySystemComponent on player.")); return; }
		const bool bActivated = ASC->TryActivateAbilityByClass(UHomeWorldSpiritShieldAbility::StaticClass());
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.SpiritShield %s (set hw.TimeOfDay.Phase 2 for night)."), bActivated ? TEXT("activated") : TEXT("failed — ensure Phase 2 or ability granted"));
	}

	void CmdRestoreMeal(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.RestoreMeal requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		const bool bOk = Char->ConsumeMealRestore();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.RestoreMeal %s (day only; restores Health + sets day buff for night)."), bOk ? TEXT("succeeded") : TEXT("skipped or failed — ensure day phase"));
	}

	// Same formula as AHomeWorldSpiritualCollectible: BasePower + day buff bonus + love bonus. For PIE regression (pie_test_runner day buff bonus at night).
	void CmdTestGrantSpiritualCollect(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.TestGrantSpiritualCollect requires a play world (PIE or game)."));
			return;
		}
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
		if (!TimeOfDay || !TimeOfDay->GetIsNight())
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.TestGrantSpiritualCollect only at night (set hw.TimeOfDay.Phase 2)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player state is not AHomeWorldPlayerState.")); return; }
		constexpr int32 BasePower = 1;
		const int32 BonusFromDayBuff = PS->GetHasDayRestorationBuff() ? 1 : 0;
		const int32 LoveBonus = FMath::Min(PS->GetLoveLevel(), 5);
		const int32 TotalPower = BasePower + BonusFromDayBuff + LoveBonus;
		PS->AddSpiritualPower(TotalPower);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: TestGrantSpiritualCollect granted %d (base %d + day buff %d + love %d); power now %d"),
			TotalPower, BasePower, BonusFromDayBuff, LoveBonus, PS->GetSpiritualPowerCollected());
	}

	void CmdConversionTest(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Conversion.Test requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		HWGM->ReportFoeConverted(nullptr);
		const int32 Count = HWGM->GetConvertedFoesThisNight();
		const EConvertedFoeRole AssignedRole = HWGM->GetConvertedFoeRole(Count - 1);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Conversion.Test executed (conversion hook triggered; ConvertedFoesThisNight=%d; Role=%d)."), Count, static_cast<int32>(AssignedRole));
	}

	void CmdCombatStubs(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.CombatStubs requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player state is not AHomeWorldPlayerState.")); return; }
		const TCHAR* DefendStr = PS->GetDefendCombatMode() == EDefendCombatMode::Ranged ? TEXT("Ranged") : TEXT("GroundAOE");
		const TCHAR* PlanetoidStr = PS->GetPlanetoidCombatStyle() == EPlanetoidCombatStyle::Combo ? TEXT("Combo") : TEXT("SingleTarget");
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Combat stubs — DefendCombatMode=%s, PlanetoidCombatStyle=%s, ComboHitCount=%d"),
			DefendStr, PlanetoidStr, PS->GetComboHitCount());
	}

	void CmdPlanetoidComplete(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Planetoid.Complete requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		HWGM->SetPlanetoidComplete(true);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: planetoid complete (bPlanetoidComplete set). Use for PIE testing of complete → travel-to-next flow. See PLANETOID_HOMESTEAD.md §5."));
	}

	void CmdSinVirtuePride(const TArray<FString>& Args)
	{
		// Stub: design only per SIN_VIRTUE_SPECTRUM.md; no gameplay implementation yet.
		constexpr float StubPride = 0.0f;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Pride: %g (stub; sin/virtue axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, CONSOLE_COMMANDS.md."), StubPride);
	}

	void CmdSinVirtueGreed(const TArray<FString>& Args)
	{
		// Stub: design only per SIN_VIRTUE_SPECTRUM.md; no gameplay implementation yet.
		constexpr float StubGreed = 0.0f;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Greed: %g (stub; sin/virtue axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, CONSOLE_COMMANDS.md."), StubGreed);
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
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.AstralDeath"),
		TEXT("Simulate astral death: advance time to dawn and respawn player at start. Use in PIE to test astral-return-on-death. See ASTRAL_DEATH_AND_DAY_SAFETY.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdAstralDeath),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.CompleteBuildOrder"),
		TEXT("Complete the nearest incomplete build order (e.g. wall hologram). Use in PIE to test agentic building flow. See DAY10_AGENTIC_BUILDING.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdCompleteBuildOrder),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SimulateBuildOrderActivation"),
		TEXT("Simulate SO_WallBuilder activation on nearest incomplete build order (log + CompleteBuildOrder). Use in PIE so SO activation is triggerable and observable. See DAY10_AGENTIC_BUILDING.md T3."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSimulateBuildOrderActivation),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SpiritualPower"),
		TEXT("Log spiritual power collected at night (night collectible stub). Set hw.TimeOfDay.Phase 2, overlap spiritual collectible, then run this to verify."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSpiritualPower),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SpendSpiritualPower"),
		TEXT("Spend N spiritual power (e.g. hw.SpendSpiritualPower 5). Deducts from SpiritualPowerCollected if sufficient; logs stub 'upgrade unlocked'. Use in PIE to verify spend path."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSpendSpiritualPower),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Goods"),
		TEXT("Log physical (day) and spiritual (night) goods counters. Physical = inventory (day harvest); spiritual = night collectible. T5 tagging."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGoods),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SpiritBurst"),
		TEXT("Trigger spirit/night-combat ability (GA_SpiritBurst). Only succeeds when hw.TimeOfDay.Phase 2 (night). Run create_ga_spirit_burst.py to add ability to character."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSpiritBurst),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SpiritShield"),
		TEXT("Trigger second spirit ability (GA_SpiritShield). Only succeeds when hw.TimeOfDay.Phase 2 (night). Run create_ga_spirit_shield.py to add ability and bind key."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSpiritShield),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.RestoreMeal"),
		TEXT("Day restoration: consume meal (day only). Restores Health +25 and sets day buff for next night. At night HUD shows 'Day buff: active' if set. See DAY_RESTORATION_LOOP.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdRestoreMeal),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.TestGrantSpiritualCollect"),
		TEXT("Test-only: grant one spiritual collect using same formula as SpiritualCollectible (base + day buff + love). Night only. For pie_test_runner day-buff-bonus check."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdTestGrantSpiritualCollect),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Conversion.Test"),
		TEXT("Trigger conversion hook (ReportFoeConverted) for testing. Logs 'Foe converted (strip sin → loved)' and increments ConvertedFoesThisNight. See CONVERSION_NOT_KILL.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdConversionTest),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.CombatStubs"),
		TEXT("Log DefendCombatMode (Ranged|GroundAOE), PlanetoidCombatStyle (Combo|SingleTarget), ComboHitCount. Use in PIE to verify combat stubs. See DEFEND_COMBAT.md, PLANETOID_COMBAT.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdCombatStubs),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Planetoid.Complete"),
		TEXT("Set planetoid-complete flag on GameMode for PIE testing of complete → travel-to-next flow. See PLANETOID_HOMESTEAD.md §5, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdPlanetoidComplete),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SinVirtue.Pride"),
		TEXT("Log current Pride axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSinVirtuePride),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SinVirtue.Greed"),
		TEXT("Log current Greed axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSinVirtueGreed),
		ECVF_Cheat);
}

void FHomeWorldModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_PRIMARY_GAME_MODULE(FHomeWorldModule, HomeWorld, "HomeWorld");
