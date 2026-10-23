// Copyright HomeWorld. All Rights Reserved.

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "HAL/FileManager.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

/**
 * Refactor item 6: every test world comes from HomeWorldTestWorld. A copied
 * CreateWorld fixture leaked once and failed a later, unrelated test, so the only
 * place a test world is created, torn down, or a tagged prop is spawned for the
 * resolver is HomeWorldTestWorld.h. This reads the test sources and says which file
 * still builds its own.
 */
namespace HomeWorldTestWorldScan
{
	bool IsCommentLine(const FString& Line)
	{
		const FString Trimmed = Line.TrimStart();
		return Trimmed.StartsWith(TEXT("*")) || Trimmed.StartsWith(TEXT("//")) || Trimmed.StartsWith(TEXT("/*"));
	}

	/** "File.cpp:line" for each code line in *Tests.cpp that contains Needle. */
	TArray<FString> FindInTests(const FString& Dir, const FString& Needle)
	{
		TArray<FString> Hits;
		TArray<FString> Files;
		IFileManager::Get().FindFiles(Files, *(Dir / TEXT("*Tests.cpp")), true, false);
		Files.Sort();
		for (const FString& File : Files)
		{
			TArray<FString> Lines;
			if (!FFileHelper::LoadFileToStringArray(Lines, *(Dir / File)))
			{
				Hits.Add(FString::Printf(TEXT("%s:unreadable"), *File));
				continue;
			}
			for (int32 Index = 0; Index < Lines.Num(); ++Index)
			{
				if (!IsCommentLine(Lines[Index]) && Lines[Index].Contains(Needle))
				{
					Hits.Add(FString::Printf(TEXT("%s:%d"), *File, Index + 1));
				}
			}
		}
		return Hits;
	}
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FTestWorldOneFixtureTest,
	"HomeWorld.TestWorld.OneFixture",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FTestWorldOneFixtureTest::RunTest(const FString& Parameters)
{
	(void)Parameters;
	const FString Dir = FPaths::ConvertRelativePathToFull(FPaths::ProjectDir() / TEXT("Source/HomeWorld"));
	const FString Fixture = Dir / TEXT("HomeWorldTestWorld.h");
	FString FixtureText;
	if (!TestTrue(*FString::Printf(TEXT("fixture readable at %s"), *Fixture), FFileHelper::LoadFileToString(FixtureText, *Fixture)))
	{
		return false;
	}
	TArray<FString> TestFiles;
	IFileManager::Get().FindFiles(TestFiles, *(Dir / TEXT("*Tests.cpp")), true, false);
	if (!TestTrue(TEXT("test sources found"), TestFiles.Num() > 0))
	{
		return false;
	}

	// The needles are split so this file does not match itself.
	const FString CreateWorld = FString(TEXT("UWorld::")) + TEXT("CreateWorld(");
	const FString OwnFixture = FString(TEXT("struct ")) + TEXT("FScopedWorld");
	const FString OwnTaggedSpawn = FString(TEXT("AActor* ")) + TEXT("SpawnTagged(");

	const TArray<FString> Creates = HomeWorldTestWorldScan::FindInTests(Dir, CreateWorld);
	const TArray<FString> Fixtures = HomeWorldTestWorldScan::FindInTests(Dir, OwnFixture);
	const TArray<FString> TaggedSpawns = HomeWorldTestWorldScan::FindInTests(Dir, OwnTaggedSpawn);

	TestEqual(*FString::Printf(TEXT("test files that create their own world [%s]"), *FString::Join(Creates, TEXT(", "))), Creates.Num(), 0);
	TestEqual(*FString::Printf(TEXT("test files with their own FScopedWorld [%s]"), *FString::Join(Fixtures, TEXT(", "))), Fixtures.Num(), 0);
	TestEqual(*FString::Printf(TEXT("test files with their own tagged spawn [%s]"), *FString::Join(TaggedSpawns, TEXT(", "))), TaggedSpawns.Num(), 0);
	TestTrue(TEXT("fixture owns the world"), FixtureText.Contains(CreateWorld) && FixtureText.Contains(OwnFixture));
	TestTrue(TEXT("fixture owns the tagged spawn"), FixtureText.Contains(OwnTaggedSpawn));
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
