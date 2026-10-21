// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/GameInstance.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldInventoryTypes.h"
#include "HomeWorldOpeningSupply.h"
#include "HomeWorldTestWorld.h"

namespace
{
	static AActor* SpawnGlideStart(UWorld* World)
	{
		FActorSpawnParameters Params;
		Params.Name = FName(TEXT("GP_GlideStart"));
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		return World->SpawnActor<AActor>(FVector::ZeroVector, FRotator::ZeroRotator, Params);
	}

	static UHomeWorldInventorySubsystem* AttachInventory(UWorld* World)
	{
		if (!World)
		{
			return nullptr;
		}
		if (!World->GetGameInstance())
		{
			UGameInstance* GameInstance = NewObject<UGameInstance>(World);
			GameInstance->Init();
			World->SetGameInstance(GameInstance);
		}
		UGameInstance* GameInstance = World->GetGameInstance();
		return GameInstance ? GameInstance->GetSubsystem<UHomeWorldInventorySubsystem>() : nullptr;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningGliderCraftTest,
	"HomeWorld.Opening.GliderCraft",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningGliderCraftTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening glider craft"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) || !TestNotNull(TEXT("glide start"), SpawnGlideStart(Scope.World)))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();

	TestFalse(TEXT("an empty chest refuses the descent"), Character->TryStartCloudDescent());
	TestFalse(TEXT("an empty chest refuses the craft"), Character->TryCraftOpeningGlider());

	Character->StockOpeningDawnChest();
	TestEqual(TEXT("dawn wood"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Wood), 1);
	TestEqual(TEXT("dawn silk"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Silk), 1);
	TestEqual(TEXT("dawn metal"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Metal), 1);
	TestFalse(TEXT("stocking the chest is not the craft"), Character->IsOpeningGliderCrafted());

	TestTrue(TEXT("the armory craft spends the chest"), Character->TryCraftOpeningGlider());
	TestEqual(TEXT("wood spent"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Wood), 0);
	TestEqual(TEXT("silk spent"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Silk), 0);
	TestEqual(TEXT("metal spent"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Metal), 0);
	TestTrue(TEXT("the glider is crafted"), Character->IsOpeningGliderCrafted());
	TestFalse(TEXT("a second craft is refused"), Character->TryCraftOpeningGlider());

	Character->StockOpeningDawnChest();
	TestEqual(TEXT("a crafted glider does not restock wood"), Character->GetOpeningDawnCountForTest(HomeWorldOpeningMaterials::Wood), 0);

	TestTrue(TEXT("the crafted glider may launch"), Character->TryStartCloudDescent());
	TestTrue(TEXT("the descent is active"), Character->IsCloudDescentActive());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningDeliveryTest,
	"HomeWorld.Opening.Delivery",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningDeliveryTest::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("opening delivery"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Day);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	UHomeWorldInventorySubsystem* Inventory = AttachInventory(Scope.World);
	if (!TestNotNull(TEXT("character"), Character) || !TestNotNull(TEXT("inventory"), Inventory))
	{
		return false;
	}
	Character->SyncFormWithTimeOfDay();
	Character->SeedOpeningHealedWisp();

	const int32 Followers = Character->GetOpeningWispFollowerCountForTest();
	const int32 Carried = Inventory->GetTotalPhysicalGoods();
	TestEqual(TEXT("one healed follower"), Followers, 1);
	TestEqual(TEXT("the heal timer was not started"), Character->GetOpeningWispHealTimerCountForTest(), 0);
	TestEqual(TEXT("the player is not carrying a pile"), Carried, 0);

	AActor* Silk = UHomeWorldOpeningSupply::SpawnDeliveryNode(
		Scope.World, HomeWorldOpeningMaterials::Silk, FVector(300.f, 0.f, 0.f));
	AActor* Wood = UHomeWorldOpeningSupply::SpawnDeliveryNode(
		Scope.World, HomeWorldOpeningMaterials::Wood, FVector(100.f, 0.f, 0.f));
	AActor* Stone = UHomeWorldOpeningSupply::SpawnDeliveryNode(
		Scope.World, HomeWorldOpeningMaterials::Stone, FVector(-100.f, 0.f, 0.f));
	if (!TestNotNull(TEXT("silk node"), Silk) || !TestNotNull(TEXT("wood node"), Wood) || !TestNotNull(TEXT("stone node"), Stone))
	{
		return false;
	}

	TestFalse(TEXT("silk stays off the field"), Character->TryDeliverOpeningNode(Silk));
	TestEqual(TEXT("silk credited nothing"), Character->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Silk), 0);

	TestTrue(TEXT("the wood node delivers once"), Character->TryDeliverOpeningNode(Wood));
	TestEqual(TEXT("the wood chest holds 10"), Character->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood), 10);
	TestFalse(TEXT("a second wood fill is refused"), Character->TryDeliverOpeningNode(Wood));
	TestEqual(TEXT("the wood chest stays at 10"), Character->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood), 10);

	TestTrue(TEXT("the stone node delivers to its own chest"), Character->TryDeliverOpeningNode(Stone));
	TestEqual(TEXT("the stone chest holds 10"), Character->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Stone), 10);
	TestEqual(TEXT("stone did not fill the wood chest"), Character->GetOpeningDeliveryCountForTest(HomeWorldOpeningMaterials::Wood), 10);

	TestEqual(TEXT("the follower is back at the legs"), Character->GetOpeningWispFollowerCountForTest(), Followers);
	TestEqual(TEXT("the healed count is unchanged"), Character->GetOpeningWispsHealedForTest(), 1);
	TestEqual(TEXT("the heal timer is still untouched"), Character->GetOpeningWispHealTimerCountForTest(), 0);
	TestEqual(TEXT("the player still is not carrying the pile"), Inventory->GetTotalPhysicalGoods(), Carried);
	TestEqual(TEXT("the carry has no wood"), Inventory->GetResource(HomeWorldInventory::RES_WOOD), 0);
	return true;
}

#endif
