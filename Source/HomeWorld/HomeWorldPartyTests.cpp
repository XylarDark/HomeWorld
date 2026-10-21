// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HomeWorldAIController.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldGameMode.h"
#include "HomeWorldOpeningWalker.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldTimeOfDaySubsystem.h"

/**
 * Docs/41_COMPANION_PARTY_DESIGN.md — the party record and the load forces.
 * Setups are derived. An old save, an unfinished rescue, and a night load are solo.
 * Positions are not stored.
 */

namespace HomeWorldPartyTest
{
	static UHomeWorldFamilySubsystem* MakeFamily()
	{
		if (!GEngine)
		{
			return nullptr;
		}
		UGameInstance* GameInstance = NewObject<UGameInstance>(GEngine);
		if (!GameInstance)
		{
			return nullptr;
		}
		GameInstance->Init();
		return GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>();
	}

	struct FScopedWorld
	{
		UWorld* World = nullptr;

		FScopedWorld()
		{
			World = UWorld::CreateWorld(EWorldType::Game, false);
		}

		~FScopedWorld()
		{
			if (World)
			{
				World->DestroyWorld(false);
				World = nullptr;
			}
		}
	};
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartyRecordDefaultsTest,
	"HomeWorld.Party.RecordDefaults",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartyRecordDefaultsTest::RunTest(const FString& Parameters)
{
	UHomeWorldFamilySubsystem* Family = HomeWorldPartyTest::MakeFamily();
	if (!TestNotNull(TEXT("family subsystem"), Family))
	{
		return false;
	}

	TestFalse(TEXT("partner starts home"), Family->IsPartnerOut());
	TestFalse(TEXT("child starts home"), Family->IsChildOut());
	TestEqual(TEXT("both home is solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);
	TestFalse(TEXT("rescue starts unfinished"), Family->IsRescueComplete());

	TestFalse(TEXT("partner invite refused before the rescue"), Family->TryInvitePartner(false, false, false));
	TestFalse(TEXT("child invite refused before the rescue"), Family->TryInviteChild(false, false, false));
	TestEqual(TEXT("a refusal stays solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);

	Family->SetRescueComplete(true);
	TestFalse(TEXT("night refuses the partner"), Family->TryInvitePartner(true, false, false));
	TestFalse(TEXT("spirit refuses the child"), Family->TryInviteChild(false, true, false));
	TestFalse(TEXT("camp refuses the partner"), Family->TryInvitePartner(false, false, true));
	TestFalse(TEXT("cave refuses the child"), Family->TryInviteChild(false, false, true));
	TestEqual(TEXT("refusals leave the record solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);

	TestTrue(TEXT("partner may come by day"), Family->TryInvitePartner(false, false, false));
	TestEqual(TEXT("partner only"), Family->GetPartySetup(), EHomeWorldPartySetup::Partner);
	TestFalse(TEXT("a refused child invite leaves the partner out"), Family->TryInviteChild(false, false, true));
	TestTrue(TEXT("partner still out"), Family->IsPartnerOut());
	TestFalse(TEXT("child still home"), Family->IsChildOut());

	TestTrue(TEXT("child may come by day"), Family->TryInviteChild(false, false, false));
	TestEqual(TEXT("both out"), Family->GetPartySetup(), EHomeWorldPartySetup::AllThree);

	Family->SetRescueComplete(false);
	TestEqual(TEXT("clearing the rescue sends both home"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartySaveRoundTripTest,
	"HomeWorld.Party.SaveRoundTrip",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartySaveRoundTripTest::RunTest(const FString& Parameters)
{
	UHomeWorldFamilySubsystem* Family = HomeWorldPartyTest::MakeFamily();
	UHomeWorldSaveGame* Save = NewObject<UHomeWorldSaveGame>();
	if (!TestNotNull(TEXT("family subsystem"), Family) || !TestNotNull(TEXT("save object"), Save))
	{
		return false;
	}

	TestFalse(TEXT("a fresh save is solo"), Save->bSavedPartnerOut);
	TestFalse(TEXT("a fresh save leaves the child home"), Save->bSavedChildOut);

	Family->DeserializeFromSaveGame(Save);
	TestEqual(TEXT("an old save restores solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);

	Family->SetRescueComplete(true);
	TestTrue(TEXT("invite partner"), Family->TryInvitePartner(false, false, false));
	TestTrue(TEXT("invite child"), Family->TryInviteChild(false, false, false));
	Family->SerializeToSaveGame(Save);
	TestTrue(TEXT("save stores the partner out"), Save->bSavedPartnerOut);
	TestTrue(TEXT("save stores the child out"), Save->bSavedChildOut);

	UHomeWorldFamilySubsystem* Loaded = HomeWorldPartyTest::MakeFamily();
	if (!TestNotNull(TEXT("loaded family"), Loaded))
	{
		return false;
	}
	Loaded->DeserializeFromSaveGame(Save);
	Loaded->ApplyLoadForces(true, false, nullptr);
	TestEqual(TEXT("a day load after the rescue keeps both out"), Loaded->GetPartySetup(), EHomeWorldPartySetup::AllThree);

	Loaded->ApplyLoadForces(false, false, nullptr);
	TestEqual(TEXT("an unfinished rescue forces solo"), Loaded->GetPartySetup(), EHomeWorldPartySetup::Solo);

	Loaded->DeserializeFromSaveGame(Save);
	Loaded->ApplyLoadForces(true, true, nullptr);
	TestEqual(TEXT("night forces solo"), Loaded->GetPartySetup(), EHomeWorldPartySetup::Solo);
	TestTrue(TEXT("night load still records the rescue"), Loaded->IsRescueComplete());

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartyLoadSendsHomeTest,
	"HomeWorld.Party.LoadSendsHome",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartyLoadSendsHomeTest::RunTest(const FString& Parameters)
{
	UHomeWorldFamilySubsystem* Family = HomeWorldPartyTest::MakeFamily();
	HomeWorldPartyTest::FScopedWorld Scope;
	if (!TestNotNull(TEXT("family subsystem"), Family) || !TestNotNull(TEXT("world"), Scope.World))
	{
		return false;
	}

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldOpeningWalker* Partner = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	AHomeWorldOpeningWalker* Child = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	if (!TestNotNull(TEXT("partner walker"), Partner) || !TestNotNull(TEXT("child walker"), Child))
	{
		return false;
	}
	Partner->Tags.Add(TEXT("NPC_PARTNER"));
	Child->Tags.Add(TEXT("NPC_CHILD"));

	const FVector PartnerHome(10.f, 20.f, 30.f);
	const FVector ChildHome(-40.f, 50.f, 60.f);
	const FVector Field(8000.f, 0.f, 30.f);
	Family->RememberPartnerHome(PartnerHome);
	Family->RememberChildHome(ChildHome);
	Partner->SetActorLocation(Field);
	Child->SetActorLocation(Field);

	UHomeWorldSaveGame* Save = NewObject<UHomeWorldSaveGame>();
	Save->bSavedPartnerOut = true;
	Save->bSavedChildOut = true;
	Family->DeserializeFromSaveGame(Save);
	TestTrue(TEXT("the partner is the one still out"), Family->IsActorOut(Partner));
	Family->ApplyLoadForces(true, true, Scope.World);

	TestFalse(TEXT("night load clears the partner"), Family->IsPartnerOut());
	TestFalse(TEXT("night load clears the child"), Family->IsChildOut());
	TestFalse(TEXT("a cleared partner is not out"), Family->IsActorOut(Partner));
	TestEqual(TEXT("partner is back on the remembered home"), Partner->GetActorLocation(), PartnerHome);
	TestEqual(TEXT("child is back on the remembered home"), Child->GetActorLocation(), ChildHome);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartyOutingClearTest,
	"HomeWorld.Party.OutingClear",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartyOutingClearTest::RunTest(const FString& Parameters)
{
	UHomeWorldFamilySubsystem* Family = HomeWorldPartyTest::MakeFamily();
	HomeWorldPartyTest::FScopedWorld Scope;
	if (!TestNotNull(TEXT("family subsystem"), Family) || !TestNotNull(TEXT("world"), Scope.World))
	{
		return false;
	}

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldOpeningWalker* Partner = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	AHomeWorldOpeningWalker* Child = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	if (!TestNotNull(TEXT("partner walker"), Partner) || !TestNotNull(TEXT("child walker"), Child))
	{
		return false;
	}
	Partner->Tags.Add(TEXT("NPC_PARTNER"));
	Child->Tags.Add(TEXT("NPC_CHILD"));

	const FVector PartnerHome(0.f, 0.f, 0.f);
	const FVector ChildHome(0.f, 300.f, 0.f);
	Family->RememberPartnerHome(PartnerHome);
	Family->RememberChildHome(ChildHome);
	Child->SetActorLocation(ChildHome);
	Partner->SetActorLocation(FVector(5000.f, 0.f, 0.f));

	Family->SetRescueComplete(true);
	TestTrue(TEXT("only the partner is invited"), Family->TryInvitePartner(false, false, false));
	Family->EndOuting(EHomeWorldPartyAbsence::Bonk, Scope.World);

	TestEqual(TEXT("a bonk is solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);
	TestEqual(TEXT("the partner is home"), Partner->GetActorLocation(), PartnerHome);
	TestEqual(TEXT("the child who stayed home is unmoved"), Child->GetActorLocation(), ChildHome);

	Family->SetRescueComplete(true);
	TestTrue(TEXT("both may come"), Family->TryInvitePartner(false, false, false) && Family->TryInviteChild(false, false, false));
	Partner->SetActorLocation(FVector(5000.f, 0.f, 0.f));
	Child->SetActorLocation(FVector(5000.f, 300.f, 0.f));
	Family->EndOuting(EHomeWorldPartyAbsence::Stroke, Scope.World);
	TestEqual(TEXT("a stroke sends the partner home"), Partner->GetActorLocation(), PartnerHome);
	TestEqual(TEXT("a stroke sends the child home"), Child->GetActorLocation(), ChildHome);
	Family->EndOuting(EHomeWorldPartyAbsence::Camp, Scope.World);
	TestEqual(TEXT("a second clear stays solo"), Family->GetPartySetup(), EHomeWorldPartySetup::Solo);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartyNightTeleportTest,
	"HomeWorld.Party.NightTeleport",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartyNightTeleportTest::RunTest(const FString& Parameters)
{
	if (!TestNotNull(TEXT("engine"), GEngine))
	{
		return false;
	}
	HomeWorldPartyTest::FScopedWorld Scope;
	UGameInstance* GameInstance = NewObject<UGameInstance>(GEngine);
	if (!TestNotNull(TEXT("world"), Scope.World) || !TestNotNull(TEXT("game instance"), GameInstance))
	{
		return false;
	}
	GameInstance->Init();
	Scope.World->SetGameInstance(GameInstance);

	UHomeWorldFamilySubsystem* Family = GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>();
	UHomeWorldTimeOfDaySubsystem* TimeOfDay = Scope.World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>();
	if (!TestNotNull(TEXT("family"), Family) || !TestNotNull(TEXT("time of day"), TimeOfDay))
	{
		return false;
	}

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldOpeningWalker* Partner = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	AHomeWorldOpeningWalker* Defend = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	AHomeWorldGameMode* GameMode = Scope.World->SpawnActor<AHomeWorldGameMode>(Params);
	if (!TestNotNull(TEXT("partner"), Partner) || !TestNotNull(TEXT("defend point"), Defend) || !TestNotNull(TEXT("game mode"), GameMode))
	{
		return false;
	}
	Partner->Tags.Add(TEXT("NPC_PARTNER"));
	Partner->Tags.Add(TEXT("Family"));
	Defend->Tags.Add(TEXT("DefendPosition"));
	const FVector Home(1.f, 2.f, 3.f);
	const FVector Field(4000.f, 0.f, 3.f);
	const FVector DefendAt(20.f, 30.f, 3.f);
	Defend->SetActorLocation(DefendAt);
	Family->RememberPartnerHome(Home);

	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	UHomeWorldSaveGame* Save = NewObject<UHomeWorldSaveGame>();
	Save->bSavedPartnerOut = true;
	Family->DeserializeFromSaveGame(Save);
	Partner->SetActorLocation(Field);
	GameMode->TryMoveFamilyToDefendPositions();
	TestFalse(TEXT("night clear sends the partner home before the teleport"), Family->IsPartnerOut());
	TestEqual(TEXT("once home, the existing defend teleport still runs"), Partner->GetActorLocation(), DefendAt);

	TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Family->DeserializeFromSaveGame(Save);
	Partner->SetActorLocation(Field);
	GameMode->TryReturnFamilyFromDefendAtDawn();
	TestTrue(TEXT("a missed clear stays out"), Family->IsPartnerOut());
	TestEqual(TEXT("the dawn teleport skips someone still out"), Partner->GetActorLocation(), Field);

	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FPartyFollowLeashTest,
	"HomeWorld.Party.FollowLeash",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FPartyFollowLeashTest::RunTest(const FString& Parameters)
{
	UHomeWorldFamilySubsystem* Family = HomeWorldPartyTest::MakeFamily();
	HomeWorldPartyTest::FScopedWorld Scope;
	if (!TestNotNull(TEXT("family"), Family) || !TestNotNull(TEXT("world"), Scope.World))
	{
		return false;
	}
	UGameInstance* GameInstance = NewObject<UGameInstance>(GEngine);
	if (!TestNotNull(TEXT("game instance"), GameInstance))
	{
		return false;
	}
	GameInstance->Init();
	Scope.World->SetGameInstance(GameInstance);
	Family = GameInstance->GetSubsystem<UHomeWorldFamilySubsystem>();

	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldCharacter* Player = Scope.World->SpawnActor<AHomeWorldCharacter>(Params);
	AHomeWorldOpeningWalker* Partner = Scope.World->SpawnActor<AHomeWorldOpeningWalker>(Params);
	if (!TestNotNull(TEXT("player"), Player) || !TestNotNull(TEXT("partner"), Partner) || !TestNotNull(TEXT("family on the world"), Family))
	{
		return false;
	}
	Player->SetActorLocation(FVector(0.f, 0.f, 100.f));
	Player->SetActorRotation(FRotator(0.f, 0.f, 0.f));
	const FVector Expected = Player->GetActorLocation() - Player->GetActorForwardVector() * AHomeWorldAIController::FollowGapCm;
	TestEqual(TEXT("the leash goal is 160 cm behind the player"), AHomeWorldAIController::FollowGoal(Player), Expected);
	TestEqual(TEXT("the gap is the opening follow gap"), AHomeWorldAIController::FollowGapCm, 160.f);

	Partner->Tags.Add(TEXT("NPC_PARTNER"));
	const FVector Stood(12.f, 24.f, 36.f);
	Partner->SetActorLocation(Stood);
	AHomeWorldAIController::DriveUnpossessedFollow(Partner, Player);
	TestFalse(TEXT("before the rescue the walker is not leashed"), Partner->ActorHasTag(TEXT("PartyLeash")));
	TestNull(TEXT("the walker is not possessed"), Partner->GetController());

	Family->SetRescueComplete(true);
	TestTrue(TEXT("invite"), Family->TryInvitePartner(false, false, false, Scope.World));
	Partner->SetActorLocation(FVector(900.f, 0.f, 36.f));
	Family->EndOuting(EHomeWorldPartyAbsence::Bed, Scope.World);
	TestEqual(TEXT("the invite remembered where they stood"), Partner->GetActorLocation(), Stood);
	TestTrue(TEXT("invite again"), Family->TryInvitePartner(false, false, false, Scope.World));
	AHomeWorldAIController::DriveUnpossessedFollow(Partner, Player);
	TestTrue(TEXT("an outing walker takes the leash"), Partner->ActorHasTag(TEXT("PartyLeash")));
	TestNull(TEXT("the leash does not possess"), Partner->GetController());

	Family->EndOuting(EHomeWorldPartyAbsence::Bonk, Scope.World);
	AHomeWorldAIController::DriveUnpossessedFollow(Partner, Player);
	TestFalse(TEXT("a cleared outing drops the leash"), Partner->ActorHasTag(TEXT("PartyLeash")));

	return true;
}

#endif
