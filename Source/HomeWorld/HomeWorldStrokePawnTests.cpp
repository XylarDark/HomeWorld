// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Engine/GameInstance.h"
#include "HomeWorldEasePad.h"
#include "HomeWorldInventorySubsystem.h"
#include "HomeWorldParadoxToy.h"
#include "HomeWorldStrokeCheck.h"
#include "HomeWorldTestWorld.h"
#include "HomeWorldTimeOfDaySubsystem.h"
#include "HomeWorldVirtueComponent.h"

namespace HomeWorldStrokePawnTest
{
	static FHomeWorldStrokeSample Sample(float X, float Y, float Time)
	{
		FHomeWorldStrokeSample Value;
		Value.Point = FVector2D(X, Y);
		Value.Time = Time;
		return Value;
	}

	static TArray<FHomeWorldStrokeSample> FromShape(const TArray<FVector2D>& Shape, float Time)
	{
		TArray<FHomeWorldStrokeSample> Stroke;
		for (const FVector2D& Point : Shape)
		{
			Stroke.Add(Sample(Point.X, Point.Y, Time));
		}
		return Stroke;
	}

	static EHomeWorldStrokeReport Play(AHomeWorldCharacter* Character, const TArray<FHomeWorldStrokeSample>& Stroke)
	{
		Character->BeginStrokeFromInput();
		for (const FHomeWorldStrokeSample& Point : Stroke)
		{
			Character->SampleStrokeFromInput(Point.Point, Point.Time);
		}
		return Character->EndStrokeFromInput();
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
		return World->GetGameInstance()->GetSubsystem<UHomeWorldInventorySubsystem>();
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokePawnInputRunsTheHold,
	"HomeWorld.Systems.Stroke.PawnInputRunsTheHold",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokePawnInputRunsTheHold::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("stroke pawn"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("pawn"), Character) || !TestNotNull(TEXT("stroke on the pawn"), Character->GetStrokeReport()))
	{
		return false;
	}

	Character->BeginStrokeFromInput();
	TestTrue(TEXT("hold starts from input"), Character->GetStrokeReport()->IsStrokeHeld());
	for (const FVector2D& Point : HomeWorldStroke::GraceShape())
	{
		Character->SampleStrokeFromInput(Point, 0.f);
	}
	TestEqual(TEXT("cursor samples are held"), Character->GetStrokeReport()->GetHeldStroke().Num(), 2);
	const EHomeWorldStrokeReport Matched = Character->EndStrokeFromInput();
	TestEqual(TEXT("release runs the stroke"), Matched, EHomeWorldStrokeReport::Matched);
	TestFalse(TEXT("release ends the hold"), Character->GetStrokeReport()->IsStrokeHeld());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeEasePadLadder,
	"HomeWorld.Systems.Stroke.EasePadLadder",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeEasePadLadder::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("ease pad"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("pawn"), Character))
	{
		return false;
	}

	TestEqual(TEXT("the first offer is Grace"), Pad->GetOfferedStep(), EHomeWorldStrokeStep::Grace);
	TestFalse(TEXT("a jump to paradox-first fails"), Pad->NoteMatch(EHomeWorldStrokeStep::Paradox));
	TestEqual(TEXT("a paradox miss is not the first offer"), Pad->GetOfferedStep(), EHomeWorldStrokeStep::Grace);

	Character->SetStrokePad(Pad);
	const FVector2D Through = Pad->GetExtraPoint();
	TestEqual(TEXT("Grace"), HomeWorldStrokePawnTest::Play(Character, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::GraceShape(), 0.f)), EHomeWorldStrokeReport::Matched);
	TestEqual(TEXT("Wrath is next"), Pad->GetOfferedStep(), EHomeWorldStrokeStep::Wrath);

	TestEqual(TEXT("Wrath"),
		HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.5f) }),
		EHomeWorldStrokeReport::Matched);
	TestEqual(TEXT("Paradox is next"), Pad->GetOfferedStep(), EHomeWorldStrokeStep::Paradox);

	const TArray<FHomeWorldStrokeSample> Paradox = {
		HomeWorldStrokePawnTest::Sample(0.f, 0.f, 0.4f),
		HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.4f),
		HomeWorldStrokePawnTest::Sample(1.f, 1.f, 0.4f)
	};
	TestEqual(TEXT("Paradox"), HomeWorldStrokePawnTest::Play(Character, Paradox), EHomeWorldStrokeReport::Matched);
	TestEqual(TEXT("the extra point is next"), Pad->GetOfferedStep(), EHomeWorldStrokeStep::ParadoxExtraPoint);

	TestEqual(TEXT("extra point"), HomeWorldStrokePawnTest::Play(Character, Paradox), EHomeWorldStrokeReport::Matched);
	TestTrue(TEXT("the four steps are done"), Pad->IsLadderComplete());
	TestFalse(TEXT("a fifth step fails"), Pad->NoteMatch(EHomeWorldStrokeStep::ParadoxExtraPoint));
	TestEqual(TEXT("the fifth step does not advance"), Pad->GetCompletedSteps(), 4);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeHerbSpendsOnMatch,
	"HomeWorld.Systems.Stroke.HerbSpendsOnMatch",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeHerbSpendsOnMatch::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("herb stroke"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	UHomeWorldInventorySubsystem* Inventory = HomeWorldStrokePawnTest::AttachInventory(Scope.World);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AActor* TargetActor = Scope.World->SpawnActor<AActor>(AActor::StaticClass(), FTransform::Identity, Params);
	UHomeWorldVirtueComponent* Target = TargetActor ? NewObject<UHomeWorldVirtueComponent>(TargetActor) : nullptr;
	if (!TestNotNull(TEXT("inventory"), Inventory) || !TestNotNull(TEXT("pawn"), Character) || !TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("target"), Target))
	{
		return false;
	}
	Target->RegisterComponent();
	Character->SetStrokePad(Pad);
	Character->SetStrokeHerb(EHomeWorldHerbVerb::Give, Target);

	TestTrue(TEXT("herb is stored"), Inventory->AddMarkedHerb({ EHomeWorldVirtuePole::Generosity }));
	TestEqual(TEXT("a match"),
		HomeWorldStrokePawnTest::Play(Character, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::GraceShape(), 0.f)),
		EHomeWorldStrokeReport::Matched);
	TestEqual(TEXT("a match spends one herb"), Inventory->GetMarkedHerbCount(), 0);
	TestTrue(TEXT("a match gives the pole"), Target->HasPole(EHomeWorldVirtuePole::Generosity));

	TestTrue(TEXT("another herb"), Inventory->AddMarkedHerb({ EHomeWorldVirtuePole::Generosity }));
	const EHomeWorldStrokeReport Weak = HomeWorldStrokePawnTest::Play(
		Character, { HomeWorldStrokePawnTest::Sample(0.f, 0.f, 5.f) });
	TestEqual(TEXT("a late wrath is a weak hit"), Weak, EHomeWorldStrokeReport::WeakHit);
	TestEqual(TEXT("a weak hit leaves the herb"), Inventory->GetMarkedHerbCount(), 1);

	const FVector2D Through = Pad->GetExtraPoint();
	HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.5f) });
	TArray<FHomeWorldStrokeSample> Late = HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::ParadoxShape(), 5.f);
	const EHomeWorldStrokeReport Bonk = HomeWorldStrokePawnTest::Play(Character, Late);
	TestEqual(TEXT("a late paradox bonks"), Bonk, EHomeWorldStrokeReport::Bonk);
	TestEqual(TEXT("a bonk leaves the herb"), Inventory->GetMarkedHerbCount(), 1);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeDawnRetiresParadoxToy,
	"HomeWorld.Systems.Stroke.DawnRetiresParadoxToy",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeDawnRetiresParadoxToy::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("dawn toy"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldParadoxToy* GraceToy = Scope.World->SpawnActor<AHomeWorldParadoxToy>(Params);
	AHomeWorldParadoxToy* ParadoxToy = Scope.World->SpawnActor<AHomeWorldParadoxToy>(Params);
	if (!TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("pawn"), Character) || !TestNotNull(TEXT("grace toy"), GraceToy) || !TestNotNull(TEXT("paradox toy"), ParadoxToy))
	{
		return false;
	}

	Character->SetStrokePad(Pad);
	Character->SetParadoxToy(GraceToy);
	TestEqual(TEXT("grace matches"),
		HomeWorldStrokePawnTest::Play(Character, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::GraceShape(), 0.f)),
		EHomeWorldStrokeReport::Matched);
	TestFalse(TEXT("a grace match does not arm the toy"), GraceToy->IsArmedForDawn());
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	TestTrue(TEXT("dawn leaves an unarmed toy up"), GraceToy->IsUp());

	Character->SetParadoxToy(ParadoxToy);
	const FVector2D Through = Pad->GetExtraPoint();
	HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.5f) });
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Night);
	const TArray<FHomeWorldStrokeSample> Paradox = {
		HomeWorldStrokePawnTest::Sample(0.f, 0.f, 0.4f),
		HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.4f),
		HomeWorldStrokePawnTest::Sample(1.f, 1.f, 0.4f)
	};
	TestEqual(TEXT("paradox matches"), HomeWorldStrokePawnTest::Play(Character, Paradox), EHomeWorldStrokeReport::Matched);
	TestTrue(TEXT("a paradox match arms the toy"), ParadoxToy->IsArmedForDawn());
	TestTrue(TEXT("the toy stays up through the night"), ParadoxToy->IsUp());
	Scope.TimeOfDay->SetPhase(EHomeWorldTimeOfDayPhase::Dawn);
	TestFalse(TEXT("the next dawn removes the armed toy"), ParadoxToy->IsUp());
	TestTrue(TEXT("dawn still leaves the grace toy up"), GraceToy->IsUp());
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokePixelDragMatchesGrace,
	"HomeWorld.Systems.Stroke.PixelDragMatchesGrace",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokePixelDragMatchesGrace::RunTest(const FString& Parameters)
{
	const FVector2D Viewport(1000.f, 1000.f);
	const FVector2D Top = HomeWorldStroke::StrokeUnitToScreen(FVector2D(0.f, 0.f), Viewport);
	const FVector2D Bottom = HomeWorldStroke::StrokeUnitToScreen(FVector2D(0.f, 1.f), Viewport);
	const FVector2D UnitTop = HomeWorldStroke::MapMouseToStrokeUnit(Top, Viewport);
	const FVector2D UnitBottom = HomeWorldStroke::MapMouseToStrokeUnit(Bottom, Viewport);
	TestTrue(TEXT("the top of the rect is unit 0,0"), UnitTop.Equals(FVector2D(0.f, 0.f), 0.001f));
	TestTrue(TEXT("the bottom of the rect is unit 0,1"), UnitBottom.Equals(FVector2D(0.f, 1.f), 0.001f));

	HomeWorldTestWorld::FScopedWorld Scope(TEXT("pixel grace"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("pawn"), Character))
	{
		return false;
	}
	const TArray<FHomeWorldStrokeSample> Drag = {
		HomeWorldStrokePawnTest::Sample(UnitTop.X, UnitTop.Y, 0.f),
		HomeWorldStrokePawnTest::Sample(UnitBottom.X, UnitBottom.Y, 0.f)
	};
	TestEqual(TEXT("a pixel-scale vertical drag matches Grace"),
		HomeWorldStrokePawnTest::Play(Character, Drag),
		EHomeWorldStrokeReport::Matched);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokePadClockWindow,
	"HomeWorld.Systems.Stroke.PadClockWindow",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokePadClockWindow::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("pad clock"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("pawn"), Character))
	{
		return false;
	}

	const float Inside = Pad->WindUpTimeAt(0.4f);
	const float Closed = Pad->WindUpTimeAt(1.5f);
	const float Wrapped = Pad->WindUpTimeAt(2.4f);
	TestTrue(TEXT("0.4s is inside the open half"), Inside >= Pad->GetWindowMin() && Inside <= Pad->GetWindowMax());
	TestTrue(TEXT("1.5s is in the closed half"), Closed > Pad->GetWindowMax());
	TestTrue(TEXT("the clock repeats into the open half"), Wrapped >= Pad->GetWindowMin() && Wrapped <= Pad->GetWindowMax());

	Character->SetStrokePad(Pad);
	TestTrue(TEXT("Grace is offered first"), Pad->NoteMatch(EHomeWorldStrokeStep::Grace));
	TestEqual(TEXT("a start inside the pad clock matches Wrath"),
		HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(0.f, 0.f, Inside) }),
		EHomeWorldStrokeReport::Matched);

	AHomeWorldEasePad* LatePad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* LateCharacter = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("late pad"), LatePad) || !TestNotNull(TEXT("late pawn"), LateCharacter))
	{
		return false;
	}
	LateCharacter->SetStrokePad(LatePad);
	TestTrue(TEXT("the late pad reaches Wrath"), LatePad->NoteMatch(EHomeWorldStrokeStep::Grace));
	TestEqual(TEXT("a start in the closed half is a weak hit on Wrath"),
		HomeWorldStrokePawnTest::Play(LateCharacter, { HomeWorldStrokePawnTest::Sample(0.f, 0.f, Closed) }),
		EHomeWorldStrokeReport::WeakHit);

	TestTrue(TEXT("the late pad reaches the paradox"), LatePad->NoteMatch(EHomeWorldStrokeStep::Wrath));
	TestEqual(TEXT("a start in the closed half bonks on the paradox"),
		HomeWorldStrokePawnTest::Play(LateCharacter, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::ParadoxShape(), Closed)),
		EHomeWorldStrokeReport::Bonk);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeCarriedPointInUnitRect,
	"HomeWorld.Systems.Stroke.CarriedPointInUnitRect",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeCarriedPointInUnitRect::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("carried point"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	if (!TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("pawn"), Character))
	{
		return false;
	}
	Character->SetStrokePad(Pad);
	TestEqual(TEXT("Grace matches"),
		HomeWorldStrokePawnTest::Play(Character, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::GraceShape(), 0.f)),
		EHomeWorldStrokeReport::Matched);
	const FVector2D Carried = Character->GetStrokeReport()->GetCarriedPoint();
	TestTrue(TEXT("the match leaves the extra point in hand"), Character->GetStrokeReport()->HasCarriedPoint());
	TestEqual(TEXT("the carried point is the pad's unit point"), Carried, Pad->GetExtraPoint());

	TestEqual(TEXT("a stroke that misses the point does not match"),
		HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(0.f, 0.f, 0.4f) }),
		EHomeWorldStrokeReport::WeakHit);
	TestEqual(TEXT("the miss keeps the point"), Character->GetStrokeReport()->GetCarriedPoint(), Carried);
	TestEqual(TEXT("a stroke through the point matches"),
		HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(Carried.X, Carried.Y, 0.4f) }),
		EHomeWorldStrokeReport::Matched);
	return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FStrokeParadoxToyDiscovered,
	"HomeWorld.Systems.Stroke.ParadoxToyDiscovered",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FStrokeParadoxToyDiscovered::RunTest(const FString& Parameters)
{
	HomeWorldTestWorld::FScopedWorld Scope(TEXT("discovered toy"));
	if (!Scope.Ok(this))
	{
		return false;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AHomeWorldEasePad* Pad = Scope.World->SpawnActor<AHomeWorldEasePad>(Params);
	AHomeWorldCharacter* Character = HomeWorldTestWorld::SpawnCharacter(Scope.World);
	AHomeWorldParadoxToy* Toy = Scope.World->SpawnActor<AHomeWorldParadoxToy>(Params);
	if (!TestNotNull(TEXT("pad"), Pad) || !TestNotNull(TEXT("pawn"), Character) || !TestNotNull(TEXT("toy"), Toy))
	{
		return false;
	}
	Character->SetStrokePad(Pad);
	// Intentionally NOT calling SetParadoxToy: the pawn must discover it from the world.

	const FVector2D Through = Pad->GetExtraPoint();
	HomeWorldStrokePawnTest::Play(Character, HomeWorldStrokePawnTest::FromShape(HomeWorldStroke::GraceShape(), 0.f));
	HomeWorldStrokePawnTest::Play(Character, { HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.5f) });
	const TArray<FHomeWorldStrokeSample> Paradox = {
		HomeWorldStrokePawnTest::Sample(0.f, 0.f, 0.4f),
		HomeWorldStrokePawnTest::Sample(Through.X, Through.Y, 0.4f),
		HomeWorldStrokePawnTest::Sample(1.f, 1.f, 0.4f)
	};
	TestEqual(TEXT("paradox matches"), HomeWorldStrokePawnTest::Play(Character, Paradox), EHomeWorldStrokeReport::Matched);
	TestTrue(TEXT("discovery armed the toy"), Toy->IsArmedForDawn());
	return true;
}
#endif
