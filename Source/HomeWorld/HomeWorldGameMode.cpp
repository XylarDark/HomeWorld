// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameMode.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldNightEncounterPlaceholder.h"
#include "HomeWorldPlayerController.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Actor.h"
#include "GameFramework/GameStateBase.h"
#include "Kismet/GameplayStatics.h"
#include "TimerManager.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"

AHomeWorldGameMode::AHomeWorldGameMode()
{
	DefaultPawnClass = AHomeWorldCharacter::StaticClass();
	PlayerControllerClass = AHomeWorldPlayerController::StaticClass();
	PlayerStateClass = AHomeWorldPlayerState::StaticClass();
	PrimaryActorTick.bCanEverTick = true;
}

void AHomeWorldGameMode::OnAstralDeath(APlayerController* PlayerController)
{
	UWorld* World = GetWorld();
	if (!World) return;
	if (!PlayerController)
	{
		PlayerController = World->GetFirstPlayerController();
	}
	if (!PlayerController) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	const bool bReturningFromDayAstral = bAstralByDay;
	if (bReturningFromDayAstral)
	{
		bAstralByDay = false;
		if (TimeOfDay)
		{
			TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
		}
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Return from astral-by-day — phase restored to Day."));
		// Do not clear day restoration (same day continues); only respawn.
	}
	else
	{
		if (TimeOfDay)
		{
			TimeOfDay->AdvanceToDawn();
		}
		// Day restoration: clear day buff, meals count, meals-with-family, and love level at dawn so they must be earned again (DAY_RESTORATION_LOOP.md, DAY_LOVE_OR_BOND.md, T2 caretaker).
		AHomeWorldPlayerState* PS = Cast<AHomeWorldPlayerState>(PlayerController->PlayerState);
		if (PS)
		{
			PS->ClearDayRestorationBuff();
			PS->ResetMealsConsumedToday();
			PS->ResetMealsWithFamilyToday();
			PS->ClearLoveLevel();
			PS->ResetLoveTasksCompletedToday();
			PS->ResetGamesWithChildToday();
		}
	}
	RestartPlayer(PlayerController);
}

void AHomeWorldGameMode::RequestAstralDeath(UObject* WorldContextObject)
{
	UWorld* World = GEngine ? GEngine->GetWorldFromContextObject(WorldContextObject, EGetWorldErrorMode::ReturnNull) : nullptr;
	if (!World || !World->IsGameWorld())
	{
		return;
	}
	AHomeWorldGameMode* HWGM = Cast<AHomeWorldGameMode>(World->GetAuthGameMode());
	if (!HWGM)
	{
		return;
	}
	APlayerController* PC = UGameplayStatics::GetPlayerController(World, 0);
	if (!PC)
	{
		return;
	}
	HWGM->OnAstralDeath(PC);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: RequestAstralDeath executed (dawn + respawn at start)."));
}

bool AHomeWorldGameMode::CanEnterAstralByDay(APlayerController* PlayerController) const
{
	// MVP (List 61): No gate — always allowed. Future: check PlayerState GetTutorialComplete(), GetLoveLevel() >= threshold, or config flag.
	(void)PlayerController;
	return true;
}

void AHomeWorldGameMode::EnterAstralByDay()
{
	UWorld* World = GetWorld();
	if (!World) return;
	APlayerController* PC = World->GetFirstPlayerController();
	if (!CanEnterAstralByDay(PC))
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: EnterAstralByDay — progression gate not met (astral-by-day not unlocked)."));
		return;
	}
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay) return;
	const EHomeWorldTimeOfDayPhase Current = TimeOfDay->GetCurrentPhase();
	if (Current != EHomeWorldTimeOfDayPhase::Day && Current != EHomeWorldTimeOfDayPhase::Dusk)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: EnterAstralByDay — only from Day or Dusk (current phase %d). Use hw.GoToBed or hw.TimeOfDay.Phase 2 for night."), static_cast<int32>(Current));
		return;
	}
	bAstralByDay = true;
	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Enter astral during day — phase set to Night. Return with hw.AstralDeath or F8 to restore Day."));
}

void AHomeWorldGameMode::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	// T3: Defend phase end — when transitioning from Night to Dawn, log, return family to gather, and let Try* clear Defend state.
	UWorld* World = GetWorld();
	if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World ? World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>() : nullptr)
	{
		const bool bIsNight = TimeOfDay->GetIsNight();
		if (bIsNight && !bWasDefendPhaseActiveLastTick)
		{
			bFamilyReturnedThisDawn = false; // entering night so next dawn we can run return again
		}
		if (bWasDefendPhaseActiveLastTick && !bIsNight)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defend phase end (dawn)."));
			TryReturnFamilyFromDefendAtDawn();
		}
		bWasDefendPhaseActiveLastTick = bIsNight;
	}

	TryTriggerNightEncounter();
	TrySpiritualPowerRegenAtNight(DeltaTime);
	TryLogDefendPhaseActive();
	TryLogDefendPositions();
	TryMoveFamilyToDefendPositions();
}

void AHomeWorldGameMode::TrySpiritualPowerRegenAtNight(float DeltaTime)
{
	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsNight())
	{
		NightSpiritualPowerRegenAccumulator = 0.f;
		return;
	}
	if (SpiritualPowerRegenIntervalSeconds <= 0.f || SpiritualPowerRegenAmount <= 0) return;

	NightSpiritualPowerRegenAccumulator += DeltaTime;
	if (NightSpiritualPowerRegenAccumulator < SpiritualPowerRegenIntervalSeconds) return;

	int32 PlayerCount = 0;
	if (AGameStateBase* GS = GetGameState<AGameStateBase>())
	{
		for (APlayerState* PS : GS->PlayerArray)
		{
			if (AHomeWorldPlayerState* HWPS = Cast<AHomeWorldPlayerState>(PS))
			{
				HWPS->AddSpiritualPower(SpiritualPowerRegenAmount);
				PlayerCount++;
			}
		}
	}
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spiritual power regen at night +%d (players: %d); observable on HUD as Spiritual power: N."), SpiritualPowerRegenAmount, PlayerCount);
	NightSpiritualPowerRegenAccumulator = FMath::Max(0.f, NightSpiritualPowerRegenAccumulator - SpiritualPowerRegenIntervalSeconds);
}

void AHomeWorldGameMode::TryTriggerNightEncounter()
{
	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay) return;

	const bool bIsNight = TimeOfDay->GetIsNight();
	if (!bIsNight)
	{
		bNightEncounterTriggered = false;
		bPlanetoidPackSpawnedThisNight = false;
		bKeyPointBossSpawnedThisNight = false;
		bDefensePositionsSpawnedThisNight = false;
		CurrentNightEncounterWave = 0;
		ConvertedFoesThisNight = 0;
		ConvertedFoeRolesThisNight.Empty();
		if (NightEncounterWave2TimerHandle.IsValid())
		{
			World->GetTimerManager().ClearTimer(NightEncounterWave2TimerHandle);
		}
		if (NightEncounterWave3TimerHandle.IsValid())
		{
			World->GetTimerManager().ClearTimer(NightEncounterWave3TimerHandle);
		}
		return;
	}

	if (bNightEncounterTriggered) return;
	bNightEncounterTriggered = true;
	CurrentNightEncounterWave = 1;

	const float SpawnDist = NightEncounterSpawnDistance;
	const float HeightOffset = NightEncounterSpawnHeightOffset;

	// Spawn a visible placeholder so night encounter is observable in world. See docs/tasks/NIGHT_ENCOUNTER.md.
	FVector SpawnLocation(SpawnDist, 0.f, 100.f + HeightOffset);
	APlayerController* PC = World->GetFirstPlayerController();
	if (APawn* Pawn = PC ? PC->GetPawn() : nullptr)
	{
		SpawnLocation = Pawn->GetActorLocation() + Pawn->GetActorForwardVector() * SpawnDist + FVector(0.f, 0.f, HeightOffset);
	}

	auto SpawnOnePlaceholder = [World](const FVector& Location) -> bool
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AHomeWorldNightEncounterPlaceholder* Placeholder = World->SpawnActor<AHomeWorldNightEncounterPlaceholder>(Location, FRotator::ZeroRotator, Params);
		if (!Placeholder) return false;
		if (UStaticMeshComponent* MeshComp = Placeholder->GetStaticMeshComponent())
		{
			if (UStaticMesh* CubeMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")))
			{
				MeshComp->SetStaticMesh(CubeMesh);
			}
		}
		return true;
	};

	if (SpawnOnePlaceholder(SpawnLocation))
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 1 — spawned placeholder at %s (distance=%.0f)"), *SpawnLocation.ToString(), SpawnDist);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Night encounter Wave 1 — spawn failed at %s"), *SpawnLocation.ToString());
	}

	// Second encounter type: optional second placeholder at NightEncounterSecondSpawnDistance (e.g. different spawn radius).
	if (NightEncounterSecondSpawnDistance > 0.f && PC)
	{
		if (APawn* Pawn = PC->GetPawn())
		{
			// Spawn second at offset (e.g. 90° right of forward) so two placeholders are distinguishable.
			const FVector Forward = Pawn->GetActorForwardVector();
			const FVector Right = Pawn->GetActorRightVector();
			FVector SecondLocation = Pawn->GetActorLocation() + Forward * NightEncounterSecondSpawnDistance * 0.7f + Right * NightEncounterSecondSpawnDistance * 0.5f + FVector(0.f, 0.f, HeightOffset);
			if (SpawnOnePlaceholder(SecondLocation))
			{
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter second spawn at %s (distance=%.0f)"), *SecondLocation.ToString(), NightEncounterSecondSpawnDistance);
			}
		}
	}

	// Wave stub: optional second wave after delay (spawn more placeholders).
	if (NightEncounterWave2DelaySeconds > 0.f && !NightEncounterWave2TimerHandle.IsValid())
	{
		World->GetTimerManager().SetTimer(
			NightEncounterWave2TimerHandle,
			this,
			&AHomeWorldGameMode::SpawnNightEncounterWave2,
			NightEncounterWave2DelaySeconds,
			false);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 2 scheduled in %.1fs"), NightEncounterWave2DelaySeconds);
	}

	// T8: Defenses around homestead — spawn defense position placeholders from config offsets. See docs/tasks/DEFEND_DEFENSES.md.
	if (DefensePositionOffsets.Num() > 0 && !bDefensePositionsSpawnedThisNight && PC)
	{
		if (APawn* Pawn = PC->GetPawn())
		{
			const FVector HomeLocation = Pawn->GetActorLocation();
			UStaticMesh* CylinderMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
			if (!CylinderMesh)
			{
				CylinderMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
			}
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			static const FName DefendPositionTag(TEXT("DefendPosition"));
			int32 Spawned = 0;
			for (const FVector& Offset : DefensePositionOffsets)
			{
				const FVector Loc = HomeLocation + Offset;
				AStaticMeshActor* DefenseActor = World->SpawnActor<AStaticMeshActor>(Loc, FRotator::ZeroRotator, Params);
				if (DefenseActor)
				{
					DefenseActor->Tags.Add(DefendPositionTag);
					if (UStaticMeshComponent* MeshComp = DefenseActor->GetStaticMeshComponent())
					{
						if (CylinderMesh)
						{
							MeshComp->SetStaticMesh(CylinderMesh);
						}
					}
					++Spawned;
				}
			}
			bDefensePositionsSpawnedThisNight = true;
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defense positions (T8): spawned %d placeholder(s) at offsets (DefendPosition tag)."), Spawned);
		}
	}

	// T3/T5: Planetoid pack(s) (spawn away from home) — configurable count at angular spread so "defend then explore" has multiple packs.
	if (PlanetoidPackSpawnDistance > 0.f && !bPlanetoidPackSpawnedThisNight && PC)
	{
		if (APawn* Pawn = PC->GetPawn())
		{
			const int32 PackCount = FMath::Clamp(PlanetoidPackCount, 1, 10);
			const FVector HomeLocation = Pawn->GetActorLocation();
			const FVector Forward = Pawn->GetActorForwardVector();
			const FVector Right = Pawn->GetActorRightVector();
			const float PackHeightOffset = NightEncounterSpawnHeightOffset;

			UStaticMesh* ConeMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cone.Cone"));
			if (!ConeMesh)
			{
				ConeMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
			}
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

			int32 Spawned = 0;
			for (int32 i = 0; i < PackCount; ++i)
			{
				const float Angle = (PackCount > 1) ? (2.f * UE_PI * static_cast<float>(i) / static_cast<float>(PackCount)) : 0.f;
				const FVector Dir = Forward * FMath::Cos(Angle) + Right * FMath::Sin(Angle);
				const FVector PackLocation = HomeLocation + Dir * PlanetoidPackSpawnDistance + FVector(0.f, 0.f, PackHeightOffset);

				AHomeWorldNightEncounterPlaceholder* PackPlaceholder = World->SpawnActor<AHomeWorldNightEncounterPlaceholder>(PackLocation, FRotator::ZeroRotator, Params);
				if (PackPlaceholder)
				{
					if (PackPlaceholder->GetStaticMeshComponent() && ConeMesh)
					{
						PackPlaceholder->GetStaticMeshComponent()->SetStaticMesh(ConeMesh);
					}
					++Spawned;
					UE_LOG(LogTemp, Log, TEXT("HomeWorld: Planetoid pack %d/%d (away from home) spawned at %s (distance=%.0f)"), i + 1, PackCount, *PackLocation.ToString(), PlanetoidPackSpawnDistance);
				}
				else
				{
					UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Planetoid pack %d/%d spawn failed at %s"), i + 1, PackCount, *PackLocation.ToString());
				}
			}
			if (Spawned > 0)
			{
				bPlanetoidPackSpawnedThisNight = true;
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Planetoid packs (away from home): %d of %d spawned at distance=%.0f."), Spawned, PackCount, PlanetoidPackSpawnDistance);
			}
		}
	}

	// T5: Key-point / boss placeholder — spawn one "bigger" placeholder at KeyPoint-tagged actor or at configurable distance. See NIGHT_ENCOUNTER.md §1.2.
	if (!bKeyPointBossSpawnedThisNight && PC)
	{
		static const FName KeyPointTag(TEXT("KeyPoint"));
		TArray<AActor*> KeyPointActors;
		UGameplayStatics::GetAllActorsWithTag(World, KeyPointTag, KeyPointActors);

		FVector BossSpawnLocation;
		bool bHasValidSpawn = false;
		if (KeyPointActors.Num() > 0 && KeyPointActors[0])
		{
			BossSpawnLocation = KeyPointActors[0]->GetActorLocation() + FVector(0.f, 0.f, 50.f);
			bHasValidSpawn = true;
		}
		else if (KeyPointBossSpawnDistance > 0.f)
		{
			if (APawn* Pawn = PC->GetPawn())
			{
				const FVector HomeLocation = Pawn->GetActorLocation();
				const FVector Forward = Pawn->GetActorForwardVector();
				BossSpawnLocation = HomeLocation + Forward * KeyPointBossSpawnDistance + FVector(0.f, 0.f, NightEncounterSpawnHeightOffset);
				bHasValidSpawn = true;
			}
		}

		if (bHasValidSpawn)
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			AHomeWorldNightEncounterPlaceholder* BossPlaceholder = World->SpawnActor<AHomeWorldNightEncounterPlaceholder>(BossSpawnLocation, FRotator::ZeroRotator, Params);
			if (BossPlaceholder)
			{
				UStaticMeshComponent* MeshComp = BossPlaceholder->GetStaticMeshComponent();
				if (MeshComp)
				{
					UStaticMesh* CubeMesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
					if (CubeMesh)
					{
						MeshComp->SetStaticMesh(CubeMesh);
					}
					// Larger scale so it reads as "bigger monster" vs wave/pack placeholders.
					BossPlaceholder->SetActorScale3D(FVector(2.5f, 2.5f, 2.5f));
				}
				bKeyPointBossSpawnedThisNight = true;
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Key-point boss placeholder spawned at %s (conversion not kill; strip sin -> loved)."), *BossSpawnLocation.ToString());
			}
		}
	}
}

void AHomeWorldGameMode::SpawnNightEncounterWave2()
{
	UWorld* World = GetWorld();
	if (!World) return;
	if (NightEncounterWave2TimerHandle.IsValid())
	{
		World->GetTimerManager().ClearTimer(NightEncounterWave2TimerHandle);
	}

	APlayerController* PC = World->GetFirstPlayerController();
	APawn* Pawn = PC ? PC->GetPawn() : nullptr;
	if (!Pawn) return;

	const int32 Count = FMath::Max(1, NightEncounterWave2SpawnCount);
	const float SpawnDist = NightEncounterSpawnDistance * 1.2f; // Wave 2 slightly farther so it's distinguishable
	const float HeightOffset = NightEncounterSpawnHeightOffset;
	const FVector Forward = Pawn->GetActorForwardVector();
	const FVector Right = Pawn->GetActorRightVector();
	const FVector Origin = Pawn->GetActorLocation();

	// T5: Wave 2 uses Sphere mesh as "different type" stub (distinct from Wave 1 Cube).
	UStaticMesh* Wave2Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Sphere.Sphere"));
	if (!Wave2Mesh)
	{
		Wave2Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	}

	int32 Spawned = 0;
	for (int32 i = 0; i < Count; ++i)
	{
		// Spread positions: offset per index so wave-2 placeholders are distinguishable.
		const float Angle = (i / static_cast<float>(FMath::Max(1, Count))) * 2.f * UE_PI;
		const float Dist = SpawnDist * (0.7f + 0.3f * (i % 2));
		FVector Wave2Location = Origin + Forward * (Dist * FMath::Cos(Angle) * 0.8f) + Right * (Dist * FMath::Sin(Angle) * 0.4f) + FVector(0.f, 0.f, HeightOffset);

		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AHomeWorldNightEncounterPlaceholder* Placeholder = World->SpawnActor<AHomeWorldNightEncounterPlaceholder>(Wave2Location, FRotator::ZeroRotator, Params);
		if (Placeholder)
		{
			if (UStaticMeshComponent* MeshComp = Placeholder->GetStaticMeshComponent())
			{
				if (Wave2Mesh)
				{
					MeshComp->SetStaticMesh(Wave2Mesh);
				}
			}
			++Spawned;
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 2 — spawned placeholder %d/%d at %s"), i + 1, Count, *Wave2Location.ToString());
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Night encounter Wave 2 — spawn %d/%d failed at %s"), i + 1, Count, *Wave2Location.ToString());
		}
	}

	CurrentNightEncounterWave = 2;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 2 (difficulty stub): %d enemies spawned (different type/count from Wave 1)."), Spawned);

	// T5: Optional wave 3 after delay (configurable spawn count per wave).
	if (NightEncounterWave3DelaySeconds > 0.f && !NightEncounterWave3TimerHandle.IsValid())
	{
		World->GetTimerManager().SetTimer(
			NightEncounterWave3TimerHandle,
			this,
			&AHomeWorldGameMode::SpawnNightEncounterWave3,
			NightEncounterWave3DelaySeconds,
			false);
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 3 scheduled in %.1fs"), NightEncounterWave3DelaySeconds);
	}
}

void AHomeWorldGameMode::SpawnNightEncounterWave3()
{
	UWorld* World = GetWorld();
	if (!World) return;
	if (NightEncounterWave3TimerHandle.IsValid())
	{
		World->GetTimerManager().ClearTimer(NightEncounterWave3TimerHandle);
	}

	APlayerController* PC = World->GetFirstPlayerController();
	APawn* Pawn = PC ? PC->GetPawn() : nullptr;
	if (!Pawn) return;

	const int32 Count = FMath::Max(1, NightEncounterWave3SpawnCount);
	const float SpawnDist = NightEncounterSpawnDistance * 1.5f; // Wave 3 farther than wave 2
	const float HeightOffset = NightEncounterSpawnHeightOffset;
	const FVector Forward = Pawn->GetActorForwardVector();
	const FVector Right = Pawn->GetActorRightVector();
	const FVector Origin = Pawn->GetActorLocation();

	// T5: Wave 3 uses Cylinder mesh as distinct type (Wave 1 = Cube, Wave 2 = Sphere).
	UStaticMesh* Wave3Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (!Wave3Mesh)
	{
		Wave3Mesh = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
	}

	int32 Spawned = 0;
	for (int32 i = 0; i < Count; ++i)
	{
		const float Angle = (i / static_cast<float>(FMath::Max(1, Count))) * 2.f * UE_PI;
		const float Dist = SpawnDist * (0.8f + 0.2f * (i % 3));
		FVector Wave3Location = Origin + Forward * (Dist * FMath::Cos(Angle) * 0.7f) + Right * (Dist * FMath::Sin(Angle) * 0.5f) + FVector(0.f, 0.f, HeightOffset);

		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AHomeWorldNightEncounterPlaceholder* Placeholder = World->SpawnActor<AHomeWorldNightEncounterPlaceholder>(Wave3Location, FRotator::ZeroRotator, Params);
		if (Placeholder)
		{
			if (UStaticMeshComponent* MeshComp = Placeholder->GetStaticMeshComponent())
			{
				if (Wave3Mesh)
				{
					MeshComp->SetStaticMesh(Wave3Mesh);
				}
			}
			++Spawned;
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 3 — spawned placeholder %d/%d at %s"), i + 1, Count, *Wave3Location.ToString());
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Night encounter Wave 3 — spawn %d/%d failed at %s"), i + 1, Count, *Wave3Location.ToString());
		}
	}

	CurrentNightEncounterWave = 3;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Night encounter Wave 3 (configurable spawn count): %d enemies spawned (Cylinder mesh, distinct from Wave 1/2)."), Spawned);
}

void AHomeWorldGameMode::ReportFoeConverted(AActor* Foe)
{
	ConvertedFoesThisNight++;
	const FString FoeName = Foe ? Foe->GetName() : FString(TEXT("(test)"));
	// T2: assign stub role round-robin (Vendor, Helper, QuestGiver, Pet, Worker)
	const int32 RoleIndex = ConvertedFoeRolesThisNight.Num() % static_cast<int32>(EConvertedFoeRole::Max);
	const EConvertedFoeRole AssignedRole = static_cast<EConvertedFoeRole>(RoleIndex);
	ConvertedFoeRolesThisNight.Add(AssignedRole);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Foe converted (strip sin → loved); Foe=%s; ConvertedFoesThisNight=%d; role: %s"), *FoeName, ConvertedFoesThisNight, *GetConvertedFoeRoleDisplayName(AssignedRole));
}

FString AHomeWorldGameMode::GetConvertedFoeRoleDisplayName(EConvertedFoeRole InRole)
{
	switch (InRole)
	{
		case EConvertedFoeRole::Vendor:     return TEXT("Vendor");
		case EConvertedFoeRole::Helper:     return TEXT("Helper");
		case EConvertedFoeRole::QuestGiver: return TEXT("Quest Giver");
		case EConvertedFoeRole::Pet:        return TEXT("Pet");
		case EConvertedFoeRole::Worker:     return TEXT("Worker");
		default:                            return TEXT("Vendor");
	}
}

EConvertedFoeRole AHomeWorldGameMode::GetConvertedFoeRole(int32 Index) const
{
	if (ConvertedFoeRolesThisNight.IsValidIndex(Index))
	{
		return ConvertedFoeRolesThisNight[Index];
	}
	return EConvertedFoeRole::Vendor;
}

void AHomeWorldGameMode::TryLogDefendPhaseActive()
{
	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay) return;

	const bool bIsNight = TimeOfDay->GetIsNight();
	if (!bIsNight)
	{
		bDefendPhaseLogged = false;
		return;
	}
	if (bDefendPhaseLogged) return;
	bDefendPhaseLogged = true;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defend phase active (TimeOfDay Phase 2)."));
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defend active — convert attackers (VISION: convert, not kill). Call ReportFoeConverted when a foe is stripped of sin."));
}

void AHomeWorldGameMode::TryLogDefendPositions()
{
	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsDefendPhaseActive())
	{
		bDefendPositionsLogged = false;
		return;
	}
	if (bDefendPositionsLogged) return;
	bDefendPositionsLogged = true;

	static const FName DefendPositionTag(TEXT("DefendPosition"));
	TArray<AActor*> Found;
	UGameplayStatics::GetAllActorsWithTag(World, DefendPositionTag, Found);
	const int32 Num = Found.Num();
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defend positions (T3): %d actor(s) with tag DefendPosition."), Num);
	const int32 MaxLog = 5;
	for (int32 i = 0; i < FMath::Min(Num, MaxLog); i++)
	{
		if (Found.IsValidIndex(i) && Found[i])
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld:   [%d] %s at %s"), i, *Found[i]->GetName(), *Found[i]->GetActorLocation().ToString());
		}
	}
	if (Num > MaxLog)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld:   ... and %d more. Family move to these via State Tree MoveTo (see DAY12, AUTOMATION_GAPS Gap 2)."), Num - MaxLog);
	}
	else if (Num == 0)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld:   Place actors with tag DefendPosition in level; then complete State Tree Night? branch (AUTOMATION_GAPS Gap 2) for family to move there."));
	}
}

void AHomeWorldGameMode::TryMoveFamilyToDefendPositions()
{
	UWorld* World = GetWorld();
	if (!World) return;

	UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TimeOfDay || !TimeOfDay->GetIsDefendPhaseActive())
	{
		bFamilyMovedToDefendThisNight = false;
		return;
	}
	if (bFamilyMovedToDefendThisNight) return;

	static const FName DefendPositionTag(TEXT("DefendPosition"));
	static const FName FamilyTag(TEXT("Family"));
	TArray<AActor*> DefendPositions;
	UGameplayStatics::GetAllActorsWithTag(World, DefendPositionTag, DefendPositions);
	TArray<AActor*> FamilyActors;
	UGameplayStatics::GetAllActorsWithTag(World, FamilyTag, FamilyActors);

	const int32 NumPositions = DefendPositions.Num();
	const int32 NumFamily = FamilyActors.Num();
	if (NumPositions == 0 || NumFamily == 0)
	{
		bFamilyMovedToDefendThisNight = true;
		if (NumPositions == 0)
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 move family to DefendPosition skipped (no DefendPosition actors; add tag DefendPosition to level actors)."));
		}
		else
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 move family to DefendPosition skipped (no Family actors; add tag Family to family/representation actors for teleport)."));
		}
		return;
	}

	int32 Moved = 0;
	for (int32 i = 0; i < NumFamily; i++)
	{
		AActor* FamilyActor = FamilyActors[i];
		if (!FamilyActor) continue;
		const int32 PosIndex = i % NumPositions;
		AActor* Target = DefendPositions[PosIndex];
		if (!Target) continue;
		FamilyActor->SetActorLocation(Target->GetActorLocation());
		Moved++;
	}
	bFamilyMovedToDefendThisNight = true;
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 moved %d family actor(s) to DefendPosition (teleport)."), Moved);
}

void AHomeWorldGameMode::TryReturnFamilyFromDefendAtDawn()
{
	UWorld* World = GetWorld();
	if (!World) return;
	if (bFamilyReturnedThisDawn) return;
	bFamilyReturnedThisDawn = true;

	static const FName FamilyTag(TEXT("Family"));
	static const FName GatherPositionTag(TEXT("GatherPosition"));
	TArray<AActor*> FamilyActors;
	UGameplayStatics::GetAllActorsWithTag(World, FamilyTag, FamilyActors);
	TArray<AActor*> GatherPositions;
	UGameplayStatics::GetAllActorsWithTag(World, GatherPositionTag, GatherPositions);

	const int32 NumFamily = FamilyActors.Num();
	if (NumFamily == 0)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 return from Defend at dawn — no Family-tagged actors (add tag Family to family actors)."));
		return;
	}

	const int32 NumGather = GatherPositions.Num();
	int32 Returned = 0;
	if (NumGather > 0)
	{
		for (int32 i = 0; i < NumFamily; i++)
		{
			AActor* FamilyActor = FamilyActors[i];
			if (!FamilyActor) continue;
			const int32 PosIndex = i % NumGather;
			AActor* Target = GatherPositions[PosIndex];
			if (!Target) continue;
			FamilyActor->SetActorLocation(Target->GetActorLocation());
			Returned++;
		}
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 return from Defend at dawn — moved %d family actor(s) to GatherPosition (teleport)."), Returned);
	}
	else
	{
		for (AActor* FamilyActor : FamilyActors)
		{
			if (!FamilyActor) continue;
			FamilyActor->SetActorLocation(GatherReturnOffset);
			Returned++;
		}
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: T3 return from Defend at dawn — moved %d family actor(s) to GatherReturnOffset %s (no GatherPosition actors; add tag GatherPosition for return spots)."), Returned, *GatherReturnOffset.ToString());
	}
}

void AHomeWorldGameMode::LogDefendStatus() const
{
	UWorld* World = GetWorld();
	if (!World)
	{
		UE_LOG(LogTemp, Warning, TEXT("HomeWorld: Defend status — no world."));
		return;
	}
	const UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	const int32 Phase = TimeOfDay ? static_cast<int32>(TimeOfDay->GetCurrentPhase()) : -1;
	const bool bDefendActive = TimeOfDay && TimeOfDay->GetIsDefendPhaseActive();
	static const FName DefendPositionTag(TEXT("DefendPosition"));
	static const FName FamilyTag(TEXT("Family"));
	TArray<AActor*> DefendPositions;
	UGameplayStatics::GetAllActorsWithTag(World, DefendPositionTag, DefendPositions);
	TArray<AActor*> FamilyActors;
	UGameplayStatics::GetAllActorsWithTag(World, FamilyTag, FamilyActors);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Defend status — Phase=%d (0=Day,1=Dusk,2=Night,3=Dawn), DefendActive=%s, DefendPosition actors=%d, Family actors=%d, family moved this night=%s. Use hw.TimeOfDay.Phase 2 for night; add DefendPosition/Family tags for T3 teleport. See DAY12_ROLE_PROTECTOR.md."),
		Phase, bDefendActive ? TEXT("true") : TEXT("false"), DefendPositions.Num(), FamilyActors.Num(), bFamilyMovedToDefendThisNight ? TEXT("true") : TEXT("false"));
}

// #region agent log
void AHomeWorldGameMode::BeginPlay()
{
	Super::BeginPlay();

	// T3 Homestead-on-planetoid stub: set flag when level name indicates planetoid (DemoMap or name contains "Planetoid"). See docs/tasks/PLANETOID_HOMESTEAD.md.
	UWorld* World = GetWorld();
	if (World)
	{
		const FString LevelName = UGameplayStatics::GetCurrentLevelName(this);
		const bool bIsPlanetoid = LevelName.Contains(TEXT("Planetoid"), ESearchCase::IgnoreCase)
			|| LevelName.Equals(TEXT("DemoMap"), ESearchCase::IgnoreCase);
		if (bIsPlanetoid)
		{
			bHomesteadLandedOnPlanetoid = true;
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Homestead landed on planetoid (stub); Level=%s"), *LevelName);
		}
		else
		{
			UE_LOG(LogTemp, Log, TEXT("HomeWorld: Homestead not on planetoid; Level=%s"), *LevelName);
		}

		// T1 (List 2): Tutorial start = morning. When loading DemoMap or a level named like tutorial/homestead, set time-of-day to Day (0 = morning). See MVP_TUTORIAL_PLAN List 2, CONSOLE_COMMANDS hw.TimeOfDay.Phase.
		const bool bIsTutorialMap = LevelName.Equals(TEXT("DemoMap"), ESearchCase::IgnoreCase)
			|| LevelName.Contains(TEXT("Demo"), ESearchCase::IgnoreCase)
			|| LevelName.Contains(TEXT("Homestead"), ESearchCase::IgnoreCase);
		if (bIsTutorialMap)
		{
			if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
			{
				TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
				UE_LOG(LogTemp, Log, TEXT("HomeWorld: Tutorial start — time-of-day set to morning (Phase Day); Level=%s"), *LevelName);
			}
		}
	}

	const FString Path = FPaths::ProjectSavedDir() + TEXT("debug-e79282.log");
	const int64 Timestamp = FDateTime::UtcNow().ToUnixTimestamp() * 1000;
	const UClass* PawnClass = GetDefaultPawnClassForController(nullptr);
	const FString DataJson = FString::Printf(TEXT("{\"defaultPawnClass\":\"%s\"}"), PawnClass ? *PawnClass->GetName() : TEXT("null"));
	const FString Line = FString::Printf(TEXT("{\"sessionId\":\"e79282\",\"timestamp\":%lld,\"location\":\"HomeWorldGameMode.cpp:BeginPlay\",\"message\":\"GameMode BeginPlay\",\"data\":%s,\"hypothesisId\":\"H1\"}\n"),
		Timestamp, *DataJson);
	if (FArchive* Ar = IFileManager::Get().CreateFileWriter(*Path, 0x08))
	{
		FTCHARToUTF8 Utf8(*Line);
		Ar->Serialize(const_cast<char*>(Utf8.Get()), Utf8.Length());
		Ar->Close();
		delete Ar;
	}
}
// #endregion
