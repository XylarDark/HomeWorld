// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldOpeningHover.h"
#include "HomeWorldTestWorld.h"
#include "Components/SceneComponent.h"

namespace
{
	struct FCenterLookScope
	{
		FCenterLookScope()
		{
			HomeWorldOpeningHover::SetCenterLookForTest(true);
		}
		~FCenterLookScope()
		{
			HomeWorldOpeningHover::SetCenterLookForTest(false);
		}
	};

	AActor* SpawnNamed(UWorld* World, const FVector& Location, const TCHAR* Name, FName Tag)
	{
		FActorSpawnParameters Params;
		Params.Name = FName(Name);
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AActor* Actor = World->SpawnActor<AActor>(AActor::StaticClass(), FVector::ZeroVector, FRotator::ZeroRotator, Params);
		if (!Actor)
		{
			return nullptr;
		}
		USceneComponent* Root = NewObject<USceneComponent>(Actor, TEXT("Root"));
		Actor->SetRootComponent(Root);
		Root->RegisterComponent();
		Actor->SetActorLocation(Location);
		Actor->Tags.Add(Tag);
		return Actor;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningHoverParityTest,
	"HomeWorld.Opening.HoverParity",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningHoverParityTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("hover parity"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("player"), Character))
	{
		return false;
	}
	AActor* Child = SpawnNamed(Scope.World, FVector(80.f, 0.f, 0.f), TEXT("NPC_ChildProp"), FName(TEXT("NPC_CHILD")));
	AActor* Far = SpawnNamed(Scope.World, FVector(400.f, 0.f, 0.f), TEXT("SM_FarArmor"), FName(TEXT("NODE_ARMOR_TABLE")));
	AActor* Table = SpawnNamed(Scope.World, FVector(150.f, 0.f, 0.f), TEXT("SM_Size_ArmorTable"), FName(TEXT("NODE_ARMOR_TABLE")));
	if (!TestNotNull(TEXT("child"), Child) || !TestNotNull(TEXT("far table"), Far) || !TestNotNull(TEXT("armory table"), Table))
	{
		return false;
	}

	const FCenterLookScope Look;
	AActor* OldPick = HomeWorldOpeningHover::PickByWorldScan(Character);
	AActor* NewPick = HomeWorldOpeningHover::PickByRegistry(Character);
	TestEqual(*FString::Printf(TEXT("old and new hover target (old %s new %s)"), *GetNameSafe(OldPick), *GetNameSafe(NewPick)), NewPick, OldPick);
	TestEqual(*FString::Printf(TEXT("glider armory table (pick %s)"), *GetNameSafe(NewPick)), NewPick, Table);
	TestTrue(TEXT("child is not the hover"), NewPick != Child);
	TestTrue(TEXT("far table is not the hover"), NewPick != Far);
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
