// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldHUD.h"
#include "AbilitySystemComponent.h"
#include "HomeWorldAttributeSet.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldPlayerState.h"
#include "HomeWorldSpiritBurstAbility.h"
#include "HomeWorldSpiritShieldAbility.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "AbilitySystemInterface.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"

void AHomeWorldHUD::DrawHUD()
{
	Super::DrawHUD();

	if (!Canvas) return;

	APlayerController* PC = Cast<APlayerController>(GetOwner());
	if (!PC) return;

	int32 Physical = 0;
	int32 Spiritual = 0;
	int32 LoveLevel = 0;

	if (UGameInstance* GI = PC->GetGameInstance())
	{
		if (UHomeWorldInventorySubsystem* Inv = GI->GetSubsystem<UHomeWorldInventorySubsystem>())
		{
			Physical = Inv->GetTotalPhysicalGoods();
		}
	}
	if (AHomeWorldPlayerState* PS = PC->GetPlayerState<AHomeWorldPlayerState>())
	{
		Spiritual = PS->GetSpiritualPowerCollected();
		LoveLevel = PS->GetLoveLevel();
	}

	UFont* Font = GEngine ? GEngine->GetSmallFont() : nullptr;
	if (!Font) return;

	const float X = TextOffsetX;
	float Y = TextOffsetY;

	// T5: TimeOfDay phase label (Day/Night) so player sees current phase without console.
	UWorld* World = PC->GetWorld();
	FString PhaseLabel = TEXT("Phase: —");
	if (World)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			switch (TimeOfDay->GetCurrentPhase())
			{
				case EHomeWorldTimeOfDayPhase::Day:  PhaseLabel = TEXT("Phase: Day");  break;
				case EHomeWorldTimeOfDayPhase::Dusk: PhaseLabel = TEXT("Phase: Dusk"); break;
				case EHomeWorldTimeOfDayPhase::Night: PhaseLabel = TEXT("Phase: Night"); break;
				case EHomeWorldTimeOfDayPhase::Dawn: PhaseLabel = TEXT("Phase: Dawn"); break;
				default: PhaseLabel = TEXT("Phase: Day"); break;
			}
		}
	}
	Canvas->SetDrawColor(FColor::White);
	Canvas->DrawText(Font, PhaseLabel, X, Y, TextScale, TextScale);
	Y += LineSpacing;

	const FString PhysicalLine = FString::Printf(TEXT("Physical: %d"), Physical);
	const FString SpiritualLine = FString::Printf(TEXT("Spiritual: %d"), Spiritual);
	const FString LoveLine = FString::Printf(TEXT("Love: %d"), LoveLevel);

	// One-time log so "did the HUD run?" is answerable from Output Log (log-driven validation).
	static bool bLoggedOnce = false;
	if (!bLoggedOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Physical=%d Spiritual=%d (counts will update when harvesting/collecting)."), Physical, Spiritual);
		bLoggedOnce = true;
	}

	Canvas->DrawText(Font, PhysicalLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	Canvas->DrawText(Font, SpiritualLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	Canvas->DrawText(Font, LoveLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;

	// Boss reward toast: show "Boss reward: +N Wood" for a few seconds after hw.GrantBossReward (T3 observable feedback).
	static bool bLoggedBossRewardToastOnce = false;
	UHomeWorldInventorySubsystem* Inv = PC->GetGameInstance() ? PC->GetGameInstance()->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (World && Inv)
	{
		int32 RewardAmount = 0;
		float DisplayUntil = 0.f;
		if (Inv->GetLastBossRewardForHUD(RewardAmount, DisplayUntil) && World->GetTimeSeconds() < DisplayUntil)
		{
			const FString BossRewardLine = FString::Printf(TEXT("Boss reward: +%d Wood"), RewardAmount);
			Canvas->SetDrawColor(FColor::Yellow);
			Canvas->DrawText(Font, BossRewardLine, X, Y, TextScale, TextScale);
			Canvas->SetDrawColor(FColor::White);
			Y += LineSpacing;
			if (!bLoggedBossRewardToastOnce)
			{
				UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Boss reward toast shown (+N Wood) for 4s after hw.GrantBossReward (T3 observable effect)."));
				bLoggedBossRewardToastOnce = true;
			}
		}
	}

	// T3 (vision-aligned UI): Sin/virtue spectrum stub — four axes (Pride, Greed, Wrath, Envy) -1..0..+1. Design only; values from stubs. See SIN_VIRTUE_SPECTRUM.md, CONSOLE_COMMANDS hw.SinVirtue.Pride / .Greed / .Wrath / .Envy.
	constexpr float SinVirtuePrideStub = 0.0f;
	constexpr float SinVirtueGreedStub = 0.0f;
	constexpr float SinVirtueWrathStub = 0.0f;
	constexpr float SinVirtueEnvyStub = 0.0f;
	const FString PrideLine = FString::Printf(TEXT("Pride: %g (sin/virtue stub)"), SinVirtuePrideStub);
	Canvas->DrawText(Font, PrideLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	const FString GreedLine = FString::Printf(TEXT("Greed: %g (sin/virtue stub)"), SinVirtueGreedStub);
	Canvas->DrawText(Font, GreedLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	const FString WrathLine = FString::Printf(TEXT("Wrath: %g (sin/virtue stub)"), SinVirtueWrathStub);
	Canvas->DrawText(Font, WrathLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	const FString EnvyLine = FString::Printf(TEXT("Envy: %g (sin/virtue stub)"), SinVirtueEnvyStub);
	Canvas->DrawText(Font, EnvyLine, X, Y, TextScale, TextScale);
	Y += LineSpacing;
	static bool bLoggedPrideOnce = false;
	if (!bLoggedPrideOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Pride: %g (sin/virtue stub; axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, hw.SinVirtue.Pride in CONSOLE_COMMANDS."), SinVirtuePrideStub);
		bLoggedPrideOnce = true;
	}
	static bool bLoggedGreedOnce = false;
	if (!bLoggedGreedOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Greed: %g (sin/virtue stub; axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, hw.SinVirtue.Greed in CONSOLE_COMMANDS."), SinVirtueGreedStub);
		bLoggedGreedOnce = true;
	}
	static bool bLoggedWrathOnce = false;
	if (!bLoggedWrathOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Wrath: %g (sin/virtue stub; axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, hw.SinVirtue.Wrath in CONSOLE_COMMANDS."), SinVirtueWrathStub);
		bLoggedWrathOnce = true;
	}
	static bool bLoggedEnvyOnce = false;
	if (!bLoggedEnvyOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Envy: %g (sin/virtue stub; axis -1..0..+1). See SIN_VIRTUE_SPECTRUM.md, hw.SinVirtue.Envy in CONSOLE_COMMANDS."), SinVirtueEnvyStub);
		bLoggedEnvyOnce = true;
	}

	// T4: One-time log so "Love: N on HUD" is validatable from Output Log (PlayerState AddLovePoints/SetLoveLevel or save/load).
	static bool bLoggedLoveOnce = false;
	if (!bLoggedLoveOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Love: %d shown (day or night); value from PlayerState (AddLovePoints/SetLoveLevel or save/load)."), LoveLevel);
		bLoggedLoveOnce = true;
	}

	// T4: During day (Phase 0 or 3), show "Restored today: N" so player sees meals/restoration count (reset at dawn).
	static bool bLoggedRestoredTodayOnce = false;
	if (World)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (!TimeOfDay->GetIsNight())
			{
				AHomeWorldPlayerState* PSForMeals = PC->GetPlayerState<AHomeWorldPlayerState>();
				if (PSForMeals)
				{
					const int32 Meals = PSForMeals->GetMealsConsumedToday();
					const FString RestoredLine = FString::Printf(TEXT("Restored today: %d"), Meals);
					Canvas->DrawText(Font, RestoredLine, X, Y, TextScale, TextScale);
					Y += LineSpacing;
					const int32 MealsWithFamily = PSForMeals->GetMealsWithFamilyToday();
					const FString MealsWithFamilyLine = FString::Printf(TEXT("Meals with family: %d"), MealsWithFamily);
					Canvas->DrawText(Font, MealsWithFamilyLine, X, Y, TextScale, TextScale);
					Y += LineSpacing;
					const int32 GamesWithChild = PSForMeals->GetGamesWithChildToday();
					const FString GamesWithChildLine = FString::Printf(TEXT("Games with child: %d"), GamesWithChild);
					Canvas->DrawText(Font, GamesWithChildLine, X, Y, TextScale, TextScale);
					Y += LineSpacing;
					if (!bLoggedRestoredTodayOnce)
					{
						UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Restored today count shown during day (use hw.RestoreMeal to increment). Games with child count shown (use hw.GameWithChild.Complete to increment; MVP tutorial List 5)."));
						bLoggedRestoredTodayOnce = true;
					}
				}
			}
		}
	}

	// T5: one-time log so "TimeOfDay phase on HUD" is validatable from Output Log.
	static bool bLoggedPhaseOnce = false;
	if (!bLoggedPhaseOnce)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: TimeOfDay phase label shown (change with hw.TimeOfDay.Phase 0|1|2|3)."));
		bLoggedPhaseOnce = true;
	}

	// T1: At night (Phase 2), show astral HP so player sees Health and that lethal damage triggers RequestAstralDeath.
	// T4: at night also show SpiritBurst cooldown (ready or N.Xs).
	static bool bLoggedAstralOnce = false;
	static bool bLoggedSpiritBurstOnce = false;
	if (World)
	{
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			// T4: When at night, show "time until dawn" countdown (stub: fixed duration or decreasing from SetPhase(Night)).
			static bool bLoggedDawnCountdownOnce = false;
			if (TimeOfDay->GetIsNight())
			{
				// T5: Night encounter wave counter on HUD (Wave 1 / Wave 2 when encounter has triggered).
				static int32 LastLoggedWave = 0;
				if (AHomeWorldGameMode* HWGM = World->GetAuthGameMode<AHomeWorldGameMode>())
				{
					const int32 Wave = HWGM->GetCurrentNightEncounterWave();
					if (Wave > 0)
					{
						const FString WaveLine = FString::Printf(TEXT("Wave %d"), Wave);
						Canvas->DrawText(Font, WaveLine, X, Y, TextScale, TextScale);
						Y += LineSpacing;
						if (Wave != LastLoggedWave)
						{
							UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Night encounter Wave %d shown (set hw.TimeOfDay.Phase 2 to trigger)."), Wave);
							LastLoggedWave = Wave;
						}
					}
					else
					{
						LastLoggedWave = 0;
					}
					// T3: At night show ConvertedFoesThisNight so player sees how many foes converted this night.
					const int32 Converted = HWGM->GetConvertedFoesThisNight();
					const FString ConvertedLine = FString::Printf(TEXT("Converted: %d"), Converted);
					Canvas->DrawText(Font, ConvertedLine, X, Y, TextScale, TextScale);
					Y += LineSpacing;
					// T3: Show last converted foe role on HUD when at least one conversion this night.
					if (Converted > 0)
					{
						const EConvertedFoeRole LastRole = HWGM->GetConvertedFoeRole(Converted - 1);
						const FString RoleLine = FString::Printf(TEXT("Last converted: %s"), *AHomeWorldGameMode::GetConvertedFoeRoleDisplayName(LastRole));
						Canvas->DrawText(Font, RoleLine, X, Y, TextScale, TextScale);
						Y += LineSpacing;
					}
					static bool bLoggedConvertedOnce = false;
					if (!bLoggedConvertedOnce)
					{
						UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: At night Converted: N shown (updates when ReportFoeConverted is called); last converted role shown when N > 0."));
						bLoggedConvertedOnce = true;
					}
				}
				const float SecondsUntilDawn = TimeOfDay->GetSecondsUntilDawn();
				if (SecondsUntilDawn >= 0.f)
				{
					const int32 Secs = FMath::Max(0, FMath::RoundToInt(SecondsUntilDawn));
					const FString DawnCountdown = FString::Printf(TEXT("Dawn in %ds"), Secs);
					Canvas->DrawText(Font, DawnCountdown, X, Y, TextScale, TextScale);
					Y += LineSpacing;
					if (!bLoggedDawnCountdownOnce)
					{
						UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Night countdown shown (Dawn in %ds). Set hw.TimeOfDay.Phase 2 for night."), Secs);
						bLoggedDawnCountdownOnce = true;
					}
				}
			}
			else
			{
				bLoggedDawnCountdownOnce = false;
			}
			if (TimeOfDay->GetIsNight())
			{
				float Health = 0.f;
				float MaxHealth = 100.f;
				if (APawn* Pawn = PC->GetPawn())
				{
					if (IAbilitySystemInterface* ASI = Cast<IAbilitySystemInterface>(Pawn))
					{
						if (UAbilitySystemComponent* ASC = ASI->GetAbilitySystemComponent())
						{
							Health = ASC->GetNumericAttribute(UHomeWorldAttributeSet::GetHealthAttribute());
							MaxHealth = ASC->GetNumericAttribute(UHomeWorldAttributeSet::GetMaxHealthAttribute());
						}
					}
				}
				const FString AstralLine = FString::Printf(TEXT("Astral HP: %.0f / %.0f"), Health, MaxHealth);
				Canvas->DrawText(Font, AstralLine, X, Y + LineSpacing, TextScale, TextScale);

				// T2: At night show current spiritual power next to Astral HP and SpiritBurst (for SpiritBurst cost and spending).
				AHomeWorldPlayerState* PSNight = PC->GetPlayerState<AHomeWorldPlayerState>();
				if (PSNight)
				{
					const int32 PowerAtNight = PSNight->GetSpiritualPowerCollected();
					const FString SpiritualPowerLine = FString::Printf(TEXT("Spiritual power: %d"), PowerAtNight);
					Canvas->DrawText(Font, SpiritualPowerLine, X, Y + LineSpacing * 2.f, TextScale, TextScale);
					static bool bLoggedSpiritualPowerOnce = false;
					if (!bLoggedSpiritualPowerOnce)
					{
						UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: At night spiritual power count shown (Spiritual power: N) for SpiritBurst and spending."));
						bLoggedSpiritualPowerOnce = true;
					}
				}

				// T4: SpiritBurst cooldown on HUD at night (ready or "N.Xs remaining").
				float SpiritBurstY = Y + LineSpacing * 3.f;
				float CooldownRemaining = 0.f;
				if (APawn* PawnForASC = PC->GetPawn())
				{
					if (IAbilitySystemInterface* ASI = Cast<IAbilitySystemInterface>(PawnForASC))
					{
						if (UAbilitySystemComponent* ASC = ASI->GetAbilitySystemComponent())
						{
							CooldownRemaining = UHomeWorldSpiritBurstAbility::GetSpiritBurstCooldownRemaining(ASC, World);
						}
					}
				}
				const FString SpiritBurstLine = CooldownRemaining > 0.f
					? FString::Printf(TEXT("SpiritBurst: %.1fs"), CooldownRemaining)
					: TEXT("SpiritBurst: ready");
				Canvas->DrawText(Font, SpiritBurstLine, X, SpiritBurstY, TextScale, TextScale);

				// T4: SpiritShield (second ability) cooldown at night (ready or N.Xs).
				float SpiritShieldCooldown = 0.f;
				if (APawn* PawnShield = PC->GetPawn())
				{
					if (IAbilitySystemInterface* ASIShield = Cast<IAbilitySystemInterface>(PawnShield))
					{
						if (UAbilitySystemComponent* ASCShield = ASIShield->GetAbilitySystemComponent())
						{
							SpiritShieldCooldown = UHomeWorldSpiritShieldAbility::GetSpiritShieldCooldownRemaining(ASCShield, World);
						}
					}
				}
				const FString SpiritShieldLine = SpiritShieldCooldown > 0.f
					? FString::Printf(TEXT("SpiritShield: %.1fs"), SpiritShieldCooldown)
					: TEXT("SpiritShield: ready");
				Canvas->DrawText(Font, SpiritShieldLine, X, SpiritBurstY + LineSpacing, TextScale, TextScale);

				// T2: When SpiritBurst was blocked (e.g. insufficient spiritual power), show message on HUD for a few seconds.
				AHomeWorldPlayerState* PSForBlock = PC->GetPlayerState<AHomeWorldPlayerState>();
				if (PSForBlock && World)
				{
					const FString BlockMsg = PSForBlock->GetSpiritBurstBlockMessageForHUD(World, 4.0f);
					if (!BlockMsg.IsEmpty())
					{
						float MsgY = SpiritBurstY + LineSpacing * 2.f;
						Canvas->SetDrawColor(FColor::Yellow);
						Canvas->DrawText(Font, BlockMsg, X, MsgY, TextScale, TextScale);
						Canvas->SetDrawColor(FColor::White);
						static bool bLoggedBlockMsgOnce = false;
						if (!bLoggedBlockMsgOnce)
						{
							UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: SpiritBurst block message shown on screen (e.g. 'Not enough spiritual power')."));
							bLoggedBlockMsgOnce = true;
						}
					}
				}

				// T1 Day restoration: at night show day buff if earned during the day (ConsumeMealRestore / hw.RestoreMeal).
				AHomeWorldPlayerState* HWPS = PC->GetPlayerState<AHomeWorldPlayerState>();
				if (HWPS && HWPS->GetHasDayRestorationBuff())
				{
					const FString DayBuffLine = TEXT("Day buff: active");
					Canvas->DrawText(Font, DayBuffLine, X, SpiritBurstY + LineSpacing * 3.f, TextScale, TextScale);
				}

				// T4: one-time log so "SpiritBurst cooldown on HUD" is validatable from Output Log.
				if (!bLoggedSpiritBurstOnce)
				{
					UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: SpiritBurst cooldown at night — %s"), CooldownRemaining > 0.f ? TEXT("on cooldown") : TEXT("ready"));
					bLoggedSpiritBurstOnce = true;
				}

				// Log once per night phase so "astral HP visible at night" is validatable from Output Log.
				if (!bLoggedAstralOnce)
				{
					UE_LOG(LogTemp, Log, TEXT("HomeWorld HUD: Night phase — Astral HP %.0f/%.0f (lethal damage triggers RequestAstralDeath)."), Health, MaxHealth);
					bLoggedAstralOnce = true;
				}
			}
			else
			{
				bLoggedAstralOnce = false;
				bLoggedSpiritBurstOnce = false;
			}
		}
	}
}
