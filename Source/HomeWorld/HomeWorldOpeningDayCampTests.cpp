// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldOpeningDayCamp.h"
#include "HomeWorldOpeningSupply.h"
#include "HomeWorldTestWorld.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningDayCampTest,
	"HomeWorld.Opening.DayCamp",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningDayCampTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening day camp"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldOpeningDayCamp* Camp = Scope.World->SpawnActor<AHomeWorldOpeningDayCamp>(
		FVector::ZeroVector, FRotator::ZeroRotator);
	AHomeWorldCharacter* Empty = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldCharacter* Delivered = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldCharacter* Outside = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldCharacter* AtNight = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("camp"), Camp) || !TestNotNull(TEXT("empty arrival"), Empty)
		|| !TestNotNull(TEXT("delivered arrival"), Delivered) || !TestNotNull(TEXT("outside"), Outside)
		|| !TestNotNull(TEXT("night arrival"), AtNight))
	{
		return false;
	}

	Empty->SetActorLocation(FVector(200.f, 0.f, 0.f));
	Empty->SyncFormWithTimeOfDay();
	TestTrue(TEXT("walking in with no delivery takes the partner home"), Camp->TryArrive(Empty));
	TestTrue(TEXT("the eject latches"), Empty->IsDayCampEjectTriggered());
	TestEqual(TEXT("the partner is away"), Empty->GetPartnerPlace(), EHomeWorldFamilyPlace::Away);
	TestFalse(TEXT("the player stays in body"), Empty->GetIsSpiritForm());
	TestEqual(TEXT("no delivery was required"), Empty->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood), 0);
	TestEqual(TEXT("the phase stays day"), Scope.TimeOfDay->GetCurrentPhase(), EHomeWorldTimeOfDayPhase::Day);

	Delivered->SetActorLocation(FVector(100.f, 0.f, 0.f));
	Delivered->SyncFormWithTimeOfDay();
	Delivered->SeedOpeningHealedWisp();
	AActor* Wood = UHomeWorldOpeningSupply::SpawnDeliveryNode(
		Scope.World, HomeWorldOpeningMaterials::Wood, FVector(100.f, 40.f, 0.f));
	if (!TestNotNull(TEXT("wood node"), Wood) || !TestTrue(TEXT("a delivery is already in"), Delivered->TryDeliverOpeningNode(Wood)))
	{
		return false;
	}
	TestTrue(TEXT("walking in after a delivery still sends them home"), Camp->TryArrive(Delivered));
	TestEqual(TEXT("the delivery stays in the chest"), Delivered->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood), 10);
	TestEqual(TEXT("that partner is away too"), Delivered->GetPartnerPlace(), EHomeWorldFamilyPlace::Away);

	Outside->SetActorLocation(FVector(400.f, 0.f, 0.f));
	Outside->SyncFormWithTimeOfDay();
	TestFalse(TEXT("outside the reach does not arrive"), Camp->TryArrive(Outside));
	TestFalse(TEXT("outside does not eject"), Outside->IsDayCampEjectTriggered());
	TestEqual(TEXT("that partner stays by the bed"), Outside->GetPartnerPlace(), EHomeWorldFamilyPlace::ByBed);

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	AtNight->SetActorLocation(FVector(100.f, 0.f, 0.f));
	AtNight->SyncFormWithTimeOfDay();
	TestFalse(TEXT("night does not send them home"), Camp->TryArrive(AtNight));
	TestFalse(TEXT("night does not eject"), AtNight->IsDayCampEjectTriggered());
	return true;
}

#endif
