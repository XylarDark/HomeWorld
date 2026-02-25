// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldGameMode.h"
#include "HomeWorldCharacter.h"
#include "HomeWorldPlayerState.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"

AHomeWorldGameMode::AHomeWorldGameMode()
{
	DefaultPawnClass = AHomeWorldCharacter::StaticClass();
	PlayerStateClass = AHomeWorldPlayerState::StaticClass();
}

// #region agent log
void AHomeWorldGameMode::BeginPlay()
{
	Super::BeginPlay();
	const FString Path = FPaths::ProjectSavedDir() + TEXT("debug-e79282.log");
	const int64 Timestamp = FDateTime::UtcNow().ToUnixTimestamp() * 1000;
	const UClass* PawnClass = GetDefaultPawnClassForController(nullptr);
	const FString DataJson = FString::Printf(TEXT("{\"defaultPawnClass\":\"%s\"}"), PawnClass ? *PawnClass->GetName() : TEXT("null"));
	const FString Line = FString::Printf(TEXT("{\"sessionId\":\"e79282\",\"timestamp\":%lld,\"location\":\"HomeWorldGameMode.cpp:BeginPlay\",\"message\":\"GameMode BeginPlay\",\"data\":%s,\"hypothesisId\":\"H1\"}\n"),
		Timestamp, *DataJson);
	if (FArchive* Ar = IFileManager::Get().CreateFileWriter(*Path, 0x08))
	{
		FTCHARToUTF8 Utf8(*Line);
		Ar->Serialize(const_cast<char*>(Utf8.Get()), Utf8.Length());
		Ar->Close();
		delete Ar;
	}
}
// #endregion
