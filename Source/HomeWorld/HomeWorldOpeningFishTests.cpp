// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HomeWorldOpeningFish.h"
#include "HomeWorldTestWorld.h"
#include "Components/SceneComponent.h"

namespace
{
	AActor* SpawnNamed(UWorld* World, const TCHAR* Name)
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
		Actor->SetActorLabel(Name);
		return Actor;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningFishPondParityTest,
	"HomeWorld.Opening.FishPondParity",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningFishPondParityTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("fish pond parity"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AActor* Decoy = SpawnNamed(Scope.World, TEXT("Water_PondSide"));
	AActor* Pond = SpawnNamed(Scope.World, TEXT("Water_Pond"));
	if (!TestNotNull(TEXT("decoy"), Decoy) || !TestNotNull(TEXT("pond"), Pond))
	{
		return false;
	}
	AActor* OldPick = HomeWorldOpeningFish::FindPondByWorldScan(Scope.World);
	AActor* NewPick = HomeWorldOpeningFish::FindPond(Scope.World);
	TestEqual(*FString::Printf(TEXT("old and new pond (old %s new %s)"), *GetNameSafe(OldPick), *GetNameSafe(NewPick)), NewPick, OldPick);
	TestEqual(TEXT("Water_Pond"), NewPick, Pond);
	TestTrue(TEXT("decoy is not the pond"), NewPick != Decoy);
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
