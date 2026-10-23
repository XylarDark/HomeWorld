// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldSpiritRosterSubsystem.h"
#include "HomeWorldSaveGame.h"
#include "HomeWorldSaveSlices.h"
#include "Serialization/MemoryReader.h"
#include "Serialization/MemoryWriter.h"

void UHomeWorldSpiritRosterSubsystem::AddSpirit(FName SpiritId)
{
	if (SpiritId.IsNone()) return;
	if (SpiritIds.Contains(SpiritId)) return;
	SpiritIds.Add(SpiritId);
	UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spirit added to roster: %s (count=%d)"), *SpiritId.ToString(), SpiritIds.Num());
}

TArray<FName> UHomeWorldSpiritRosterSubsystem::GetSpirits() const
{
	return SpiritIds;
}

bool UHomeWorldSpiritRosterSubsystem::RemoveSpirit(FName SpiritId)
{
	int32 Removed = SpiritIds.Remove(SpiritId);
	if (Removed > 0)
	{
		UE_LOG(LogTemp, Log, TEXT("HomeWorld: Spirit removed from roster: %s"), *SpiritId.ToString());
		return true;
	}
	return false;
}

int32 UHomeWorldSpiritRosterSubsystem::GetSpiritCount() const
{
	return SpiritIds.Num();
}

void UHomeWorldSpiritRosterSubsystem::SerializeToSaveGame(UHomeWorldSaveGame* Out) const
{
	if (!Out) return;
	Out->SavedSpiritIds = SpiritIds;
}

void UHomeWorldSpiritRosterSubsystem::DeserializeFromSaveGame(const UHomeWorldSaveGame* In)
{
	if (!In) return;
	SpiritIds = In->SavedSpiritIds;
}

void UHomeWorldSpiritRosterSubsystem::WriteSaveSlice(TArray<uint8>& OutBytes) const
{
	OutBytes.Reset();
	FMemoryWriter Ar(OutBytes);
	TArray<FName> Ids = SpiritIds;
	HomeWorldSaveSlices::SerializeNames(Ar, Ids);
}

bool UHomeWorldSpiritRosterSubsystem::ReadSaveSlice(const TArray<uint8>& InBytes)
{
	FMemoryReader Ar(InBytes);
	TArray<FName> Ids;
	HomeWorldSaveSlices::SerializeNames(Ar, Ids);
	if (Ar.IsError())
	{
		return false;
	}
	SpiritIds = MoveTemp(Ids);
	return true;
}
