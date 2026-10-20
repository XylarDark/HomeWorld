// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldTestWorld.h"

/**
 * The opening night wisp loop: deposit, timer, healed follower.
 *
 * INVARIANTS, NOT TUNING
 *
 * The 20 second heal, the 600 cm spring range, and the one-herb cost are first-pass
 * placeholders in HomeWorldCharacter.cpp. Luke tunes them after the replay. A test
 * that pins those numbers would turn a pending playtest decision into a regression.
 * These cases pin only the shape:
 *
 *   - a deposit needs a carried wisp and an herb;
 *   - a deposit spends one carried wisp and at least one herb;
 *   - a deposit starts one timer;
 *   - a completed timer heals one wisp and adds one follower at the legs.
 *
 * The click-heart gesture and the follower arc stay human checks. This is the state
 * machine behind them, not a replacement for the replay.
 */
namespace HomeWorldOpeningNightTest
{
	static AActor* SpawnNamed(UWorld* World, const TCHAR* Name, const FVector& Location)
	{
		FActorSpawnParameters Params;
		Params.Name = FName(Name);
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* Actor = World->SpawnActor<AStaticMeshActor>(
			Location, FRotator::ZeroRotator, Params);
#if WITH_EDITOR
		if (Actor)
		{
			Actor->SetActorLabel(Name);
		}
#endif
		return Actor;
	}

	static AHomeWorldCharacter* BeginNight(
		FAutomationTestBase* Test, UWorld* World, AActor*& OutSpring)
	{
		AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(World);
		if (!Test->TestNotNull(TEXT("opening night character"), Character))
		{
			return nullptr;
		}

		Character->SetActorLocation(FVector::ZeroVector);
		AActor* Bed = SpawnNamed(World, TEXT("SM_Size_Bed"), FVector(150.f, 0.f, 0.f));
		OutSpring = SpawnNamed(World, TEXT("Water_HotSpring"), FVector(0.f, 300.f, 0.f));
		if (!Test->TestNotNull(TEXT("bed"), Bed))
		{
			return nullptr;
		}
		if (!Test->TestNotNull(TEXT("hot spring"), OutSpring))
		{
			return nullptr;
		}

		if (!Test->TestTrue(
			TEXT("sleeping at the bed starts opening night"),
			Character->TryOpeningBedInFront()))
		{
			return nullptr;
		}
		if (!Test->TestTrue(
			TEXT("opening night is spirit"),
			Character->IsOpeningNightSpirit()))
		{
			return nullptr;
		}
		return Character;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningNightWispDepositStartsHeal,
	"HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningNightWispDepositStartsHeal::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening night wisp deposit"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AActor* Spring = nullptr;
	AHomeWorldCharacter* Character = HomeWorldOpeningNightTest::BeginNight(this, Scope.World, Spring);
	if (!Character)
	{
		return false;
	}

	Character->DebugSeedOpeningWispLoop(1, 2);
	const int32 HerbsBefore = Character->GetOpeningHerbTenthsForTest();
	this->TestEqual(TEXT("one wisp is carried before the deposit"),
		Character->GetOpeningWispsCarriedForTest(), 1);
	this->TestTrue(TEXT("at least one herb is banked before the deposit"), HerbsBefore >= 1);
	this->TestEqual(TEXT("no heal timer runs before the deposit"),
		Character->GetOpeningWispHealTimerCountForTest(), 0);

	if (!this->TestTrue(TEXT("E at the hot spring deposits a wisp"),
		Character->TryOpeningHotSpringHealInFront()))
	{
		return false;
	}

	this->TestEqual(TEXT("the deposit takes one carried wisp"),
		Character->GetOpeningWispsCarriedForTest(), 0);
	this->TestTrue(TEXT("the deposit spends at least one herb"),
		Character->GetOpeningHerbTenthsForTest() < HerbsBefore);
	this->TestEqual(TEXT("one heal timer is running"),
		Character->GetOpeningWispHealTimerCountForTest(), 1);
	this->TestEqual(TEXT("the wisp is not healed at the instant of deposit"),
		Character->GetOpeningWispsHealedForTest(), 0);
	this->TestEqual(TEXT("no follower exists at the instant of deposit"),
		Character->GetOpeningWispFollowerCountForTest(), 0);

	Character->DebugAdvanceOpeningNight(1000.f);

	this->TestEqual(TEXT("the completed timer heals one wisp"),
		Character->GetOpeningWispsHealedForTest(), 1);
	this->TestEqual(TEXT("the completed timer leaves no timer behind"),
		Character->GetOpeningWispHealTimerCountForTest(), 0);
	this->TestEqual(TEXT("the healed wisp follows at the legs"),
		Character->GetOpeningWispFollowerCountForTest(), 1);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningNightWispDepositNeedsHerb,
	"HomeWorld.Systems.Opening.NightWisp.DepositNeedsHerb",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningNightWispDepositNeedsHerb::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening night deposit without herb"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AActor* Spring = nullptr;
	AHomeWorldCharacter* Character = HomeWorldOpeningNightTest::BeginNight(this, Scope.World, Spring);
	if (!Character)
	{
		return false;
	}

	Character->DebugSeedOpeningWispLoop(1, 0);
	const int32 HerbsBefore = Character->GetOpeningHerbTenthsForTest();
	Character->TryOpeningHotSpringHealInFront();

	this->TestEqual(TEXT("a deposit without an herb keeps the carried wisp"),
		Character->GetOpeningWispsCarriedForTest(), 1);
	this->TestEqual(TEXT("a deposit without an herb spends no herb"),
		Character->GetOpeningHerbTenthsForTest(), HerbsBefore);
	this->TestEqual(TEXT("a deposit without an herb starts no timer"),
		Character->GetOpeningWispHealTimerCountForTest(), 0);

	Character->DebugAdvanceOpeningNight(1000.f);
	this->TestEqual(TEXT("a deposit without an herb heals no wisp"),
		Character->GetOpeningWispsHealedForTest(), 0);
	this->TestEqual(TEXT("a deposit without an herb creates no follower"),
		Character->GetOpeningWispFollowerCountForTest(), 0);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningNightWispDepositNeedsWisp,
	"HomeWorld.Systems.Opening.NightWisp.DepositNeedsWisp",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningNightWispDepositNeedsWisp::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening night deposit without wisp"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AActor* Spring = nullptr;
	AHomeWorldCharacter* Character = HomeWorldOpeningNightTest::BeginNight(this, Scope.World, Spring);
	if (!Character)
	{
		return false;
	}

	Character->DebugSeedOpeningWispLoop(0, 2);
	const int32 HerbsBefore = Character->GetOpeningHerbTenthsForTest();
	Character->TryOpeningHotSpringHealInFront();

	this->TestEqual(TEXT("a deposit without a carried wisp keeps the herbs"),
		Character->GetOpeningHerbTenthsForTest(), HerbsBefore);
	this->TestEqual(TEXT("a deposit without a carried wisp starts no timer"),
		Character->GetOpeningWispHealTimerCountForTest(), 0);

	Character->DebugAdvanceOpeningNight(1000.f);
	this->TestEqual(TEXT("a deposit without a carried wisp heals no wisp"),
		Character->GetOpeningWispsHealedForTest(), 0);
	this->TestEqual(TEXT("a deposit without a carried wisp creates no follower"),
		Character->GetOpeningWispFollowerCountForTest(), 0);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningNightWispDepositNeedsSpringRange,
	"HomeWorld.Systems.Opening.NightWisp.DepositNeedsSpringRange",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningNightWispDepositNeedsSpringRange::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening night deposit range"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AActor* Spring = nullptr;
	AHomeWorldCharacter* Character = HomeWorldOpeningNightTest::BeginNight(this, Scope.World, Spring);
	if (!Character)
	{
		return false;
	}

	Character->DebugSeedOpeningWispLoop(1, 2);
	const int32 HerbsBefore = Character->GetOpeningHerbTenthsForTest();

	// Far enough that no plausible spring range includes it. This tests the need to be
	// at the spring without pinning the current 600 cm placeholder.
	Spring->SetActorLocation(FVector(5000.f, 0.f, 0.f));
	this->TestFalse(TEXT("a spring far away does not accept the deposit"),
		Character->TryOpeningHotSpringHealInFront());
	this->TestEqual(TEXT("an out-of-range deposit keeps the carried wisp"),
		Character->GetOpeningWispsCarriedForTest(), 1);
	this->TestEqual(TEXT("an out-of-range deposit spends no herb"),
		Character->GetOpeningHerbTenthsForTest(), HerbsBefore);
	this->TestEqual(TEXT("an out-of-range deposit starts no timer"),
		Character->GetOpeningWispHealTimerCountForTest(), 0);

	Spring->SetActorLocation(FVector(200.f, 0.f, 0.f));
	this->TestTrue(TEXT("the spring in range accepts the deposit"),
		Character->TryOpeningHotSpringHealInFront());
	this->TestEqual(TEXT("the in-range deposit takes one carried wisp"),
		Character->GetOpeningWispsCarriedForTest(), 0);
	this->TestEqual(TEXT("the in-range deposit starts one timer"),
		Character->GetOpeningWispHealTimerCountForTest(), 1);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
