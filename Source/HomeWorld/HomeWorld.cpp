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
#include "HomeWorldPlanetoidTypes.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldSaveGameSubsystem.h"
#include "HomeWorldSpiritBurstAbility.h"
#include "HomeWorldSpiritRosterSubsystem.h"
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

	void CmdRoles(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Roles requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldFamilySubsystem* Family = GI->GetSubsystem<UHomeWorldFamilySubsystem>();
		if (!Family)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: FamilySubsystem not found."));
			return;
		}
		const int32 N = Family->GetMemberCount();
		if (N == 0)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Roles — no family members (member count 0). Set roles via FamilySubsystem or spawn family; then hw.Save / hw.Load to verify persistence. See DAY15_ROLE_PERSISTENCE.md."));
			return;
		}
		auto RoleName = [](EHomeWorldFamilyRole R) -> const TCHAR*
		{
			switch (R)
			{
				case EHomeWorldFamilyRole::Gatherer: return TEXT("Gatherer");
				case EHomeWorldFamilyRole::Protector: return TEXT("Protector");
				case EHomeWorldFamilyRole::Healer:    return TEXT("Healer");
				case EHomeWorldFamilyRole::Child:    return TEXT("Child");
				case EHomeWorldFamilyRole::Partner:  return TEXT("Partner");
				default: return TEXT("?");
			}
		};
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Roles — %d member(s) (index → role). Use hw.Save then hw.Load then hw.Roles to verify role persistence. See DAY15_ROLE_PERSISTENCE.md, CONSOLE_COMMANDS.md."), N);
		for (int32 i = 0; i < N; ++i)
		{
			EHomeWorldFamilyRole R = Family->GetRoleForIndex(i);
			UE_LOG(LogTemp, Log, TEXT("HomeWorld:   [%d] %s"), i, RoleName(R));
		}
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

	void CmdSpirits(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Spirits requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldSpiritRosterSubsystem* Spirits = GI->GetSubsystem<UHomeWorldSpiritRosterSubsystem>();
		if (!Spirits)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: SpiritRosterSubsystem not found."));
			return;
		}
		const int32 Count = Spirits->GetSpiritCount();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Spirits — roster has %d spirit(s). Use hw.ReportDeath then hw.Spirits to verify (T5 / Day 21)."), Count);
		const TArray<FName> Ids = Spirits->GetSpirits();
		for (int32 i = 0; i < Ids.Num(); ++i)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld:   [%d] %s"), i, *Ids[i].ToString());
		}
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
		Inv->SetLastBossRewardDisplay(Amount, World->GetTimeSeconds() + 4.0f);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.GrantBossReward granted Wood +%d (boss reward placeholder)."), Amount);
	}

	void CmdGatherOre(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Gather.Ore requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
		if (!Inv) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: InventorySubsystem not found.")); return; }
		const int32 Amount = Args.Num() > 0 ? FCString::Atoi(*Args[0]) : 10;
		if (Amount <= 0) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Gather.Ore amount must be positive.")); return; }
		Inv->AddResource(FName("Ore"), Amount);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Gather.Ore granted Ore +%d (stub for MVP tutorial List 6 step 5)."), Amount);
	}

	void CmdGatherFlowers(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Gather.Flowers requires a play world (PIE or game)."));
			return;
		}
		UGameInstance* GI = World->GetGameInstance();
		if (!GI) return;
		UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>();
		if (!Inv) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: InventorySubsystem not found.")); return; }
		const int32 Amount = Args.Num() > 0 ? FCString::Atoi(*Args[0]) : 5;
		if (Amount <= 0) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Gather.Flowers amount must be positive.")); return; }
		Inv->AddResource(FName("Flowers"), Amount);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Gather.Flowers granted Flowers +%d (stub for MVP tutorial List 6 step 5)."), Amount);
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

	void CmdEnterAstral(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.EnterAstral requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		HWGM->EnterAstralByDay();
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
		// List 6 verification: log Wood, Ore, Flowers so "collected all three" is verifiable via hw.Goods.
		if (Inv)
		{
			const int32 Wood = Inv->GetResource(FName(TEXT("Wood")));
			const int32 Ore = Inv->GetResource(FName(TEXT("Ore")));
			const int32 Flowers = Inv->GetResource(FName(TEXT("Flowers")));
			if (Wood > 0 || Ore > 0 || Flowers > 0)
			{
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Goods — Wood: %d, Ore: %d, Flowers: %d (MVP tutorial List 6 gather verification)."),
					Wood, Ore, Flowers);
			}
		}
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

	void CmdMealBreakfast(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Meal.Breakfast requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		const bool bOk = Char->ConsumeMealRestore(EMealType::Breakfast);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Meal.Breakfast %s (day only; same as RestoreMeal — Health, day buff, meals today, love; family count if Family-tagged actors)."), bOk ? TEXT("succeeded") : TEXT("skipped or failed — ensure day phase"));
	}

	void CmdMealLunch(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Meal.Lunch requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		const bool bOk = Char->ConsumeMealRestore(EMealType::Lunch);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Meal.Lunch %s (day only; same as RestoreMeal — Health, day buff, meals today, love; family count if Family-tagged actors)."), bOk ? TEXT("succeeded") : TEXT("skipped or failed — ensure day phase"));
	}

	void CmdMealDinner(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Meal.Dinner requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		APawn* Pawn = PC->GetPawn();
		AHomeWorldCharacter* Char = Cast<AHomeWorldCharacter>(Pawn);
		if (!Char) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Player pawn is not AHomeWorldCharacter.")); return; }
		const bool bOk = Char->ConsumeMealRestore(EMealType::Dinner);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Meal.Dinner %s (day only; same as RestoreMeal — Health, day buff, meals today, love; family count if Family-tagged actors)."), bOk ? TEXT("succeeded") : TEXT("skipped or failed — ensure day phase"));
	}

	void CmdLoveTaskComplete(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.LoveTask.Complete requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No HomeWorld PlayerState.")); return; }
		PS->CompleteOneLoveTask();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.LoveTask.Complete executed (Love +1, love tasks today: %d; HUD Love: N updates). MVP tutorial List 4 step 3."), PS->GetLoveTasksCompletedToday());
	}

	void CmdGameWithChildComplete(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.GameWithChild.Complete requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No HomeWorld PlayerState.")); return; }
		PS->CompleteOneGameWithChild();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.GameWithChild.Complete executed (Love +1, games with child today: %d). MVP tutorial List 5 step 4."), PS->GetGamesWithChildToday());
	}

	void CmdTutorialEnd(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.TutorialEnd requires a play world (PIE or game)."));
			return;
		}
		APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
		if (!PC) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No player controller.")); return; }
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PC->PlayerState);
		if (!PS) { UE_LOG(LogTemp, Warning, TEXT("HomeWorld: No HomeWorld PlayerState.")); return; }
		PS->SetTutorialComplete(true);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Family taken — tutorial complete; inciting incident. (bTutorialComplete set). MVP tutorial List 10 step 13."));
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

	void CmdDefendStatus(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Defend.Status requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		HWGM->LogDefendStatus();
	}

	static const TCHAR* AlignmentToStr(EPlanetoidAlignment A)
	{
		switch (A)
		{
			case EPlanetoidAlignment::Corrupted: return TEXT("Corrupted");
			case EPlanetoidAlignment::Neutral:   return TEXT("Neutral");
			case EPlanetoidAlignment::Positive: return TEXT("Positive");
			default: return TEXT("?");
		}
	}

	static const TCHAR* BiomeToStr(EBiomeType B)
	{
		switch (B)
		{
			case EBiomeType::Desert: return TEXT("Desert");
			case EBiomeType::Forest: return TEXT("Forest");
			case EBiomeType::Marsh:  return TEXT("Marsh");
			case EBiomeType::Canyon: return TEXT("Canyon");
			default: return TEXT("?");
		}
	}

	void CmdPlanetoidZoneAlignment(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Planetoid.ZoneAlignment requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		if (Args.Num() < 1)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: current zone alignment = %s (use Corrupted | Neutral | Positive to set). See PLANETOID_BIOMES.md §3, CONSOLE_COMMANDS.md."),
				AlignmentToStr(HWGM->GetCurrentZoneAlignment()));
			return;
		}
		const FString& Arg = Args[0];
		EPlanetoidAlignment NewAlign = EPlanetoidAlignment::Neutral;
		if (Arg.Equals(TEXT("Corrupted"), ESearchCase::IgnoreCase))      NewAlign = EPlanetoidAlignment::Corrupted;
		else if (Arg.Equals(TEXT("Neutral"), ESearchCase::IgnoreCase))  NewAlign = EPlanetoidAlignment::Neutral;
		else if (Arg.Equals(TEXT("Positive"), ESearchCase::IgnoreCase)) NewAlign = EPlanetoidAlignment::Positive;
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Planetoid.ZoneAlignment expects Corrupted, Neutral, or Positive; got '%s'."), *Arg);
			return;
		}
		HWGM->SetCurrentZoneAlignment(NewAlign);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: zone alignment set to %s (fight / harvest / empower). See PLANETOID_BIOMES.md §3."), AlignmentToStr(NewAlign));
	}

	void CmdPlanetoidZoneInfo(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Planetoid.ZoneInfo requires a play world (PIE or game)."));
			return;
		}
		AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
		if (!HWGM)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: GameMode is not AHomeWorldGameMode."));
			return;
		}
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: zone alignment=%s, biome=%s (read at runtime for fight/harvest/empower). See PLANETOID_BIOMES.md §3."),
			AlignmentToStr(HWGM->GetCurrentZoneAlignment()), BiomeToStr(HWGM->GetCurrentZoneBiome()));
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

	void CmdSinVirtueWrath(const TArray<FString>& Args)
	{
		// Stub: design only per SIN_VIRTUE_SPECTRUM.md; no gameplay implementation yet.
		constexpr float StubWrath = 0.0f;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Wrath: %g (stub; sin/virtue axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, CONSOLE_COMMANDS.md."), StubWrath);
	}

	void CmdSinVirtueEnvy(const TArray<FString>& Args)
	{
		// Stub: design only per SIN_VIRTUE_SPECTRUM.md; no gameplay implementation yet.
		constexpr float StubEnvy = 0.0f;
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Envy: %g (stub; sin/virtue axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, CONSOLE_COMMANDS.md."), StubEnvy);
	}

	void CmdGoToBed(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.GoToBed requires a play world (PIE or game)."));
			return;
		}
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
		if (!TimeOfDay)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: TimeOfDaySubsystem not found."));
			return;
		}
		TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.GoToBed — phase set to Night (Phase 2). Player \"wakes\" in astral / night phase. MVP tutorial List 8 step 8."));
	}

	void CmdWake(const TArray<FString>& Args)
	{
		UWorld* World = GEngine ? GEngine->GetCurrentPlayWorld() : nullptr;
		if (!World)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: hw.Wake requires a play world (PIE or game)."));
			return;
		}
		UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
		if (!TimeOfDay)
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: TimeOfDaySubsystem not found."));
			return;
		}
		if (!TimeOfDay->GetIsNight())
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Wake — not night; phase unchanged (use hw.GoToBed then hw.Wake to test wake)."));
			return;
		}
		TimeOfDay->AdvanceToDawn();
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: hw.Wake — phase set to Dawn (Phase 3). List 56 T3. For morning (Day/0) run hw.TimeOfDay.Phase 0."));
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
		TEXT("hw.Roles"),
		TEXT("Log current family roles (index → role). Use after hw.Save / hw.Load to verify role persistence. See DAY15_ROLE_PERSISTENCE.md, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdRoles),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.ReportDeath"),
		TEXT("Report player death and add to spirit roster (T5 / Day 21 verification)."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdReportDeath),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Spirits"),
		TEXT("List spirit roster: count and spirit IDs. Run hw.ReportDeath then hw.Spirits to verify death-to-spirit (T5 / Day 21)."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSpirits),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.GrantBossReward"),
		TEXT("Grant boss reward (Wood amount, default 100). Use in PIE for T5 / Day 25 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGrantBossReward),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Gather.Ore"),
		TEXT("Add Ore to inventory (default 10). Stub for MVP tutorial List 6 step 5. Use in PIE to verify 'mine some ore' or harvest from BP_HarvestableOre."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGatherOre),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Gather.Flowers"),
		TEXT("Add Flowers to inventory (default 5). Stub for MVP tutorial List 6 step 5. Use in PIE to verify 'pick some flowers' or harvest from BP_HarvestableFlower."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGatherFlowers),
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
		TEXT("hw.EnterAstral"),
		TEXT("List 61: Enter astral during the day (stub). From Day or Dusk, sets phase to Night; return with hw.AstralDeath restores Day. See ASTRAL_DEATH_AND_DAY_SAFETY.md, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdEnterAstral),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.AstralByDay"),
		TEXT("Alias for hw.EnterAstral: enter astral during day (List 61)."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdEnterAstral),
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
		TEXT("hw.Meal.Breakfast"),
		TEXT("MVP tutorial step 2: have breakfast (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, AddLovePoints(1), counts Family-tagged actors. Use in morning for List 3 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdMealBreakfast),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Meal.Lunch"),
		TEXT("MVP tutorial step 6: have lunch (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, love; counts Family-tagged actors. Use for List 7 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdMealLunch),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Meal.Dinner"),
		TEXT("MVP tutorial step 7: have dinner (day only). Same logic as hw.RestoreMeal — restores Health, sets day buff, increments meals today, love; counts Family-tagged actors. Use for List 7 verification."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdMealDinner),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.LoveTask.Complete"),
		TEXT("MVP tutorial List 4 step 3: complete one love task with partner. Adds 1 love (HUD Love: N) and increments love tasks completed today (reset at dawn). Use in PIE to verify 'one love task done'. See CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdLoveTaskComplete),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.GameWithChild.Complete"),
		TEXT("MVP tutorial List 5 step 4: complete one game with child. Adds 1 love and increments games with child today (reset at dawn). Use in PIE to verify 'played one game with child'. See CONSOLE_COMMANDS.md, MVP_TUTORIAL_PLAN List 5."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGameWithChildComplete),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.TutorialEnd"),
		TEXT("MVP tutorial List 10: mark 'family taken' / tutorial end. Sets bTutorialComplete on PlayerState and logs inciting incident. Use in PIE to verify step 13. See CONSOLE_COMMANDS.md, MVP_TUTORIAL_PLAN List 10."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdTutorialEnd),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.FamilyTaken"),
		TEXT("Alias for hw.TutorialEnd: mark family taken / tutorial complete (inciting incident). MVP tutorial List 10 step 13."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdTutorialEnd),
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
		TEXT("hw.Planetoid.ZoneAlignment"),
		TEXT("Get or set current zone alignment (Corrupted | Neutral | Positive). No arg = log current; with arg = set. Fight/harvest/empower read at runtime. See PLANETOID_BIOMES.md §3, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdPlanetoidZoneAlignment),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Planetoid.ZoneInfo"),
		TEXT("Log current zone alignment and biome (GameMode). Use in PIE to verify alignment/biome read at runtime. See PLANETOID_BIOMES.md §3, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdPlanetoidZoneInfo),
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
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SinVirtue.Wrath"),
		TEXT("Log current Wrath axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSinVirtueWrath),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.SinVirtue.Envy"),
		TEXT("Log current Envy axis stub value (e.g. 0). Design only; see SIN_VIRTUE_SPECTRUM.md §2, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdSinVirtueEnvy),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.GoToBed"),
		TEXT("Go to bed: set time-of-day to Night (Phase 2). Player \"wakes\" in astral / night phase. Use for MVP tutorial List 8 step 8 verification. Alternative: hw.TimeOfDay.Phase 2."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGoToBed),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Sleep"),
		TEXT("Alias for hw.GoToBed: set time-of-day to Night (Phase 2). MVP tutorial List 8 step 8."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdGoToBed),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Wake"),
		TEXT("Wake: advance time-of-day to Dawn (Phase 3). Only has effect when current phase is Night. Use in PIE for List 56 T3 verification. In-world: interact or overlap bed at night."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdWake),
		ECVF_Cheat);
	IConsoleManager::Get().RegisterConsoleCommand(
		TEXT("hw.Defend.Status"),
		TEXT("Act 2 prep: log Defend phase status (phase, DefendActive, DefendPosition count, Family count, family-moved-this-night). Use in PIE after hw.TimeOfDay.Phase 2. See DAY12_ROLE_PROTECTOR.md, CONSOLE_COMMANDS.md."),
		FConsoleCommandWithArgsDelegate::CreateStatic(&CmdDefendStatus),
		ECVF_Cheat);
}

void FHomeWorldModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_PRIMARY_GAME_MODULE(FHomeWorldModule, HomeWorld, "HomeWorld");
