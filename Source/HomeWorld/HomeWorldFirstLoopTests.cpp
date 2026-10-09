// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/GameInstance.h"
#include "HomeWorldCloudWisp.h"
#include "Kismet/GameplayStatics.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldShrinePortalComponent.h"
#include "HomeWorldTestWorld.h"

namespace HomeWorldFirstLoopTest
{
	static void AttachInventory(UWorld* World)
	{
		if (!World || World->GetGameInstance())
		{
			return;
		}
		UGameInstance* GameInstance = NewObject<UGameInstance>(World);
		GameInstance->Init();
		World->SetGameInstance(GameInstance);
	}

	static bool StartDescent(UWorld* World, AHomeWorldCharacter* Character)
	{
		TArray<AActor*> Markers;
		UGameplayStatics::GetAllActorsWithTag(World, FName(TEXT("GlideStart")), Markers);
		if (Markers.Num() == 0)
		{
			FActorSpawnParameters Params;
			Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
			if (AActor* Marker = World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, Params))
			{
				Marker->Tags.Add(FName(TEXT("GlideStart")));
			}
		}
		Character->SetActorLocation(FVector::ZeroVector);
		if (UHomeWorldTimeOfDaySubsystem* TimeOfDay = World->GetSubsystem<UHomeWorldTimeOfDaySubsystem>())
		{
			if (TimeOfDay->GetIsNight() && !Character->GetIsSpiritForm() && !Character->TryBedSleepSpirit())
			{
				return false;
			}
		}
		return Character->TryStartCloudDescent();
	}

	static UHomeWorldShrinePortalComponent* MakeShrine(UWorld* World, FName Destination)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* Shrine = World->SpawnActor<AActor>(AActor::StaticClass(), FTransform(FVector(5000.0, 0.0, 0.0)), Params);
		if (!Shrine)
		{
			return nullptr;
		}
		UHomeWorldShrinePortalComponent* Portal = NewObject<UHomeWorldShrinePortalComponent>(Shrine);
		Shrine->AddInstanceComponent(Portal);
		Portal->RegisterComponent();
		Portal->DestinationLabel = Destination;
		return Portal;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FGardenPickThenTeaTest,
	"HomeWorld.T0.FL2.GardenPickThenTea",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FGardenPickThenTeaTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL2 garden"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	HomeWorldFirstLoopTest::AttachInventory(Scope.World);
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("empty pack cannot brew"), Character->TryBrewNodeKettleTea());
	TestFalse(TEXT("empty pack leaves the sprint gate off"), Character->IsTeaSprintGateActive());

	TestTrue(TEXT("garden pick adds a herb"), Character->TryPickGardenHerb());
	UHomeWorldInventorySubsystem* Inventory = Scope.World->GetGameInstance()
		? Scope.World->GetGameInstance()->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	if (!TestNotNull(TEXT("inventory"), Inventory))
	{
		return false;
	}
	TestEqual(TEXT("pick yields one herb and does not spend it"),
		Inventory->GetResource(HomeWorldInventory::RES_HERB), 1);

	TestTrue(TEXT("tea spends the picked herb"), Character->TryBrewNodeKettleTea());
	TestTrue(TEXT("tea turns the day sprint on"), Character->IsTeaSprintGateActive());
	TestEqual(TEXT("brew spends the herb"), Inventory->GetResource(HomeWorldInventory::RES_HERB), 0);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNightWispCapTest,
	"HomeWorld.T0.FL4.NightGlideCarriesTwoWisps",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FNightWispCapTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL4 wisps"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) ||
		!TestTrue(TEXT("night descent starts"), HomeWorldFirstLoopTest::StartDescent(Scope.World, Character)))
	{
		return false;
	}
	TestFalse(TEXT("night descent is not the day smoke sign"), Character->HasDayGlideSmokeSign());

	AHomeWorldCloudWisp* First = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	AHomeWorldCloudWisp* Second = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	AHomeWorldCloudWisp* Third = Scope.World->SpawnActor<AHomeWorldCloudWisp>();
	TestTrue(TEXT("first night wisp"), Character->CollectCloudWisp(First));
	TestTrue(TEXT("second night wisp"), Character->CollectCloudWisp(Second));
	TestFalse(TEXT("third night wisp is refused"), Character->CollectCloudWisp(Third));
	TestEqual(TEXT("carried wisps stay at two"), Character->GetCarriedCloudWisps(), 2);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FWoundTakesOneNightWispTest,
	"HomeWorld.T0.FL5.WoundTakesOneNightWisp",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FWoundTakesOneNightWispTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL5 wound"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) ||
		!TestTrue(TEXT("descent"), HomeWorldFirstLoopTest::StartDescent(Scope.World, Character)))
	{
		return false;
	}
	TestTrue(TEXT("collect one"), Character->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>()));
	TestTrue(TEXT("night give heals the wound"), Character->TryGiveNightWispToWound());
	TestEqual(TEXT("the wisp is spent"), Character->GetCarriedCloudWisps(), 0);
	TestTrue(TEXT("wound reads healed"), Character->IsHomesteadWoundHealed());
	TestTrue(TEXT("healed wound wisps follow"), Character->GetFollowingWoundWispCount() > 0);

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Character->SyncFormWithTimeOfDay();
	AHomeWorldCharacter* DayCharacter = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("day character"), DayCharacter) ||
		!TestTrue(TEXT("day character leaves and glides at night first"), [&]()
		{
			Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
			if (!HomeWorldFirstLoopTest::StartDescent(Scope.World, DayCharacter))
			{
				return false;
			}
			if (!DayCharacter->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>()))
			{
				return false;
			}
			Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
			DayCharacter->SyncFormWithTimeOfDay();
			return true;
		}()))
	{
		return false;
	}
	const int32 Held = DayCharacter->GetCarriedCloudWisps();
	TestFalse(TEXT("day give fails"), DayCharacter->TryGiveNightWispToWound());
	TestEqual(TEXT("day give does not spend the wisp"), DayCharacter->GetCarriedCloudWisps(), Held);
	TestFalse(TEXT("day wound is not healed by the give"), DayCharacter->IsHomesteadWoundHealed());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FFertilizerMixTest,
	"HomeWorld.T0.FL6.FertilizerMix",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FFertilizerMixTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL6 mix"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}

	TestFalse(TEXT("mix fails with neither input"), Character->TryMixHomesteadFertilizer());
	TestTrue(TEXT("dung can be carried"), Character->TryAddCarriedDung());
	TestFalse(TEXT("mix fails with dung alone"), Character->TryMixHomesteadFertilizer());
	TestEqual(TEXT("dung is kept when the wisp is missing"), Character->GetCarriedDung(), 1);

	if (!TestTrue(TEXT("descent"), HomeWorldFirstLoopTest::StartDescent(Scope.World, Character)) ||
		!TestTrue(TEXT("wisp"), Character->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>())))
	{
		return false;
	}
	TestTrue(TEXT("mix consumes one dung and one wisp"), Character->TryMixHomesteadFertilizer());
	TestEqual(TEXT("dung spent"), Character->GetCarriedDung(), 0);
	TestEqual(TEXT("wisp spent"), Character->GetCarriedCloudWisps(), 0);
	TestEqual(TEXT("one fertilizer"), Character->GetCarriedFertilizer(), 1);

	AHomeWorldCharacter* WispOnly = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("wisp-only character"), WispOnly) ||
		!TestTrue(TEXT("wisp-only descent"), HomeWorldFirstLoopTest::StartDescent(Scope.World, WispOnly)) ||
		!TestTrue(TEXT("wisp-only collect"), WispOnly->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>())))
	{
		return false;
	}
	TestFalse(TEXT("mix fails with a wisp alone"), WispOnly->TryMixHomesteadFertilizer());
	TestEqual(TEXT("wisp is kept when dung is missing"), WispOnly->GetCarriedCloudWisps(), 1);
	TestEqual(TEXT("no fertilizer without both"), WispOnly->GetCarriedFertilizer(), 0);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FShrineReturnsHomeTest,
	"HomeWorld.T0.FL7.ShrineReturnsHome",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FShrineReturnsHomeTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL7 shrine"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters HomeParams;
	HomeParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AActor* Home = Scope.World->SpawnActor<AActor>(AActor::StaticClass(), FTransform::Identity, HomeParams);
	if (!TestNotNull(TEXT("home shrine marker"), Home))
	{
		return false;
	}
	const FName HomeLabel = Home->GetFName();

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	const FVector Away(8000.0, 0.0, 100.0);

	UHomeWorldShrinePortalComponent* CampShrine = HomeWorldFirstLoopTest::MakeShrine(Scope.World, FName(TEXT("NODE_PORTAL_CAMP")));
	if (!TestNotNull(TEXT("camp-labeled shrine"), CampShrine))
	{
		return false;
	}
	Character->SetActorLocation(Away);
	TestFalse(TEXT("homestead shrine does not transit to camp"), CampShrine->TryPortalTransit(Character));
	TestTrue(TEXT("a camp destination leaves the traveler in place"),
		FVector::DistSquared(Character->GetActorLocation(), Away) < 1.0);

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Character->SyncFormWithTimeOfDay();
	UHomeWorldShrinePortalComponent* BeforeLeaving = HomeWorldFirstLoopTest::MakeShrine(Scope.World, HomeLabel);
	if (!TestNotNull(TEXT("shrine before leaving"), BeforeLeaving))
	{
		return false;
	}
	TestFalse(TEXT("day return waits until the traveler has left"), BeforeLeaving->TryPortalTransit(Character));

	Character->NotifyLeftHomestead();
	UHomeWorldShrinePortalComponent* DayShrine = HomeWorldFirstLoopTest::MakeShrine(Scope.World, HomeLabel);
	Character->SetActorLocation(Away);
	TestTrue(TEXT("day body returns home"), DayShrine && DayShrine->TryPortalTransit(Character));
	TestTrue(TEXT("day return arrives at the home marker"),
		FVector::DistSquared(Character->GetActorLocation(), Home->GetActorLocation()) < FMath::Square(400.0));

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	Character->SyncFormWithTimeOfDay();
	Character->SetActorLocation(Away);
	UHomeWorldShrinePortalComponent* NightBody = HomeWorldFirstLoopTest::MakeShrine(Scope.World, HomeLabel);
	TestFalse(TEXT("night body is refused"), NightBody && NightBody->TryPortalTransit(Character));
	TestTrue(TEXT("refused night body stays away"),
		FVector::DistSquared(Character->GetActorLocation(), Away) < 1.0);

	TestTrue(TEXT("night bed grants spirit"), Character->TryBedSleepSpirit());
	Character->SetActorLocation(Away);
	UHomeWorldShrinePortalComponent* NightSpirit = HomeWorldFirstLoopTest::MakeShrine(Scope.World, HomeLabel);
	TestTrue(TEXT("night spirit returns home"), NightSpirit && NightSpirit->TryPortalTransit(Character));

	// Dawn and day do not end spirit. The bed does. Company return is the day body.
	Character->WakeFromSpiritAtBed();
	TestFalse(TEXT("the bed returns the body before the day company"), Character->GetIsSpiritForm());
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	Character->SyncFormWithTimeOfDay();
	Character->SetRidingBull(true);
	Character->NotifyPartnerReadyToReturn();
	Character->SetActorLocation(Away);
	UHomeWorldShrinePortalComponent* WithCompany = HomeWorldFirstLoopTest::MakeShrine(Scope.World, HomeLabel);
	TestTrue(TEXT("company returns home"), WithCompany && WithCompany->TryPortalTransit(Character));
	TestTrue(TEXT("the bull walk to the barn is set"), Character->IsWalkToBarn());
	TestFalse(TEXT("the ride ends on arrival"), Character->IsRidingBull());
	TestTrue(TEXT("the partner walk is set"), Character->IsPartnerWalkingHome());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FFamilyPlacesAndHintTest,
	"HomeWorld.T0.FL9.FamilyPlacesAndHint",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FFamilyPlacesAndHintTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL9 family"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	HomeWorldFirstLoopTest::AttachInventory(Scope.World);
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	TestEqual(TEXT("wake places the partner by the bed"), Character->GetPartnerPlace(), EHomeWorldFamilyPlace::ByBed);
	TestEqual(TEXT("wake places the child in the garden"), Character->GetChildPlace(), EHomeWorldFamilyPlace::InGarden);
	TestFalse(TEXT("no hint before tea"), Character->HasFamilyHintFired());

	Character->NotifyPartnerTaken();
	TestEqual(TEXT("the taken partner is away"), Character->GetPartnerPlace(), EHomeWorldFamilyPlace::Away);
	TestEqual(TEXT("after the taking the child waits by the bed"), Character->GetChildPlace(), EHomeWorldFamilyPlace::ByBed);

	TestTrue(TEXT("pick"), Character->TryPickGardenHerb());
	TestTrue(TEXT("tea"), Character->TryBrewNodeKettleTea());
	TestTrue(TEXT("one hint fires after tea"), Character->HasFamilyHintFired());
	TestEqual(TEXT("the hint points toward the edge"), Character->GetFamilyHint(), FString(TEXT("toward the edge")));

	TestTrue(TEXT("second pick"), Character->TryPickGardenHerb());
	TestTrue(TEXT("second tea"), Character->TryBrewNodeKettleTea());
	TestEqual(TEXT("the hint does not become a second line"), Character->GetFamilyHint(), FString(TEXT("toward the edge")));
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FNightFlightSpreadTest,
	"HomeWorld.T0.FL10.NightFlightSpreadsFertilizer",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FNightFlightSpreadTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("FL10 flight"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) ||
		!TestTrue(TEXT("night spirit glide"), HomeWorldFirstLoopTest::StartDescent(Scope.World, Character)))
	{
		return false;
	}

	TestTrue(TEXT("first wisp"), Character->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>()));
	TestTrue(TEXT("second wisp"), Character->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>()));
	TestFalse(TEXT("a third wisp is refused"),
		Character->CollectCloudWisp(Scope.World->SpawnActor<AHomeWorldCloudWisp>()));
	TestEqual(TEXT("cap stays two"), Character->GetCarriedCloudWisps(), 2);

	TestTrue(TEXT("one wisp heals the wound"), Character->TryGiveNightWispToWound());
	TestTrue(TEXT("dung"), Character->TryAddCarriedDung());
	TestTrue(TEXT("the other wisp mixes"), Character->TryMixHomesteadFertilizer());
	TestEqual(TEXT("one fertilizer"), Character->GetCarriedFertilizer(), 1);

	TestTrue(TEXT("the night flight spreads that mix"), Character->TrySpreadFertilizerOnNightFlight());
	TestEqual(TEXT("the fertilizer is consumed"), Character->GetCarriedFertilizer(), 0);

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	Character->SyncFormWithTimeOfDay();
	TestEqual(TEXT("dawn adds no herb pile"), Character->GetMorningHerbPiles(), 0);
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
