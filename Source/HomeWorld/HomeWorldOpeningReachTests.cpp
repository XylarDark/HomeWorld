// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldInteractResolver.h"
#include "HomeWorldTestWorld.h"

struct FOpeningReachFlagParityAccess
{
	static bool LineOfSight(const AHomeWorldCharacter& Character, const AActor* Target)
	{
		return Character.HasOpeningLineOfSight(Target);
	}
};

namespace
{
	AActor* SpawnPropAt(UWorld* World, const FVector& Location)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		return World->SpawnActor<AStaticMeshActor>(Location, FRotator::ZeroRotator, Params);
	}

	AStaticMeshActor* SpawnVisibilityWall(UWorld* World, const FVector& Location)
	{
		FActorSpawnParameters Params;
		Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		AStaticMeshActor* Wall = World->SpawnActor<AStaticMeshActor>(Location, FRotator::ZeroRotator, Params);
		UStaticMesh* Cube = LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
		if (!Wall || !Cube)
		{
			return nullptr;
		}
		UStaticMeshComponent* Mesh = Wall->GetStaticMeshComponent();
		Mesh->SetMobility(EComponentMobility::Movable);
		Mesh->SetStaticMesh(Cube);
		Mesh->SetCollisionProfileName(UCollisionProfile::BlockAll_ProfileName);
		Wall->SetActorScale3D(FVector(0.25f, 4.f, 4.f));
		return Wall;
	}

	/** Pre-refactor inline reach and wall checks (test-only oracle). */
	bool OracleReachAndWall(
		const AHomeWorldCharacter* Character,
		HomeWorldInteract::EVerb Verb,
		const AActor* Target)
	{
		if (!Character || !Target)
		{
			return false;
		}
		if (FVector::Dist2D(Character->GetActorLocation(), Target->GetActorLocation())
			> HomeWorldInteract::ReachCm(Verb))
		{
			return false;
		}
		const HomeWorldInteract::FSpec* Spec = HomeWorldInteract::SpecFor(Verb);
		if (Spec && Spec->bWall && !FOpeningReachFlagParityAccess::LineOfSight(*Character, Target))
		{
			return false;
		}
		return true;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FOpeningReachFlagParityTest,
	"HomeWorld.Opening.ReachFlagParity",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FOpeningReachFlagParityTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("reach flag parity"));
	if (!Scope.Ok(this))
	{
		return false;
	}

	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("player"), Character))
	{
		return false;
	}

	const float Distances[] = { 100.f, 280.f, 281.f, 599.f, 600.f, 601.f };
	const HomeWorldInteract::EVerb Verbs[] = {
		HomeWorldInteract::EVerb::OpeningBed,
		HomeWorldInteract::EVerb::OpeningHotSpring,
	};
	int32 Mismatches = 0;
	for (HomeWorldInteract::EVerb Verb : Verbs)
	{
		for (float Dist : Distances)
		{
			for (bool bWall : { false, true })
			{
				Character->SetActorLocation(FVector::ZeroVector);
				Character->SetActorRotation(FRotator::ZeroRotator);
				AActor* Target = SpawnPropAt(Scope.World, FVector(Dist, 0.f, 0.f));
				if (!TestNotNull(TEXT("reach target"), Target))
				{
					return false;
				}
				AStaticMeshActor* Wall = nullptr;
				if (bWall)
				{
					Wall = SpawnVisibilityWall(Scope.World, FVector(Dist * 0.5f, 0.f, 0.f));
					if (!TestNotNull(TEXT("visibility wall"), Wall))
					{
						return false;
					}
				}
				const bool Oracle = OracleReachAndWall(Character, Verb, Target);
				const bool Helper = HomeWorldInteract::Admits(Character, Verb, Target, false);
				if (Oracle != Helper)
				{
					++Mismatches;
				}
				Target->Destroy();
				if (Wall)
				{
					Wall->Destroy();
				}
			}
		}
	}
	if (!TestEqual(TEXT("oracle matches helper"), Mismatches, 0))
	{
		return false;
	}

	Character->SetActorLocation(FVector::ZeroVector);
	Character->SetActorRotation(FRotator::ZeroRotator);
	AActor* Spring600 = SpawnPropAt(Scope.World, FVector(600.f, 0.f, 0.f));
	TestTrue(TEXT("spring accepts at 600"),
		Spring600 && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningHotSpring, Spring600, false));
	AActor* Spring601 = SpawnPropAt(Scope.World, FVector(601.f, 0.f, 0.f));
	TestFalse(TEXT("spring refuses at 601"),
		Spring601 && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningHotSpring, Spring601, false));

	AActor* Bed280 = SpawnPropAt(Scope.World, FVector(280.f, 0.f, 0.f));
	TestTrue(TEXT("bed fallback accepts at 280"),
		Bed280 && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningBed, Bed280, false));
	AActor* Bed281 = SpawnPropAt(Scope.World, FVector(281.f, 0.f, 0.f));
	TestFalse(TEXT("bed fallback refuses at 281"),
		Bed281 && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningBed, Bed281, false));

	AActor* InReach = SpawnPropAt(Scope.World, FVector(200.f, 0.f, 0.f));
	AStaticMeshActor* RefuseWall = SpawnVisibilityWall(Scope.World, FVector(100.f, 0.f, 0.f));
	if (!TestNotNull(TEXT("visibility wall for refuse asserts"), RefuseWall))
	{
		return false;
	}
	TestFalse(TEXT("wall refuses bed"),
		InReach && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningBed, InReach, false));
	TestFalse(TEXT("wall refuses spring"),
		InReach && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningHotSpring, InReach, false));
	RefuseWall->Destroy();

	Character->SetActorRotation(FRotator(0.f, 180.f, 0.f));
	AActor* BedLookAway = SpawnPropAt(Scope.World, FVector(280.f, 0.f, 0.f));
	TestTrue(TEXT("bed look-away still accepts"),
		BedLookAway && HomeWorldInteract::Admits(Character, HomeWorldInteract::EVerb::OpeningBed, BedLookAway, false));

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
