// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldFamilySubsystem.h"
#include "HomeWorldSaveGame.h"

void UHomeWorldFamilySubsystem::SetRoleForIndex(int32 SpawnIndex, EHomeWorldFamilyRole Role)
{
	if (SpawnIndex < 0) return;
	while (RoleBySpawnIndex.Num() <= SpawnIndex)
	{
		RoleBySpawnIndex.Add(EHomeWorldFamilyRole::Gatherer);
	}
	RoleBySpawnIndex[SpawnIndex] = Role;
}

EHomeWorldFamilyRole UHomeWorldFamilySubsystem::GetRoleForIndex(int32 SpawnIndex) const
{
	if (SpawnIndex < 0 || SpawnIndex >= RoleBySpawnIndex.Num())
	{
		return EHomeWorldFamilyRole::Gatherer;
	}
	return RoleBySpawnIndex[SpawnIndex];
}

int32 UHomeWorldFamilySubsystem::GetMemberCount() const
{
	return RoleBySpawnIndex.Num();
}

void UHomeWorldFamilySubsystem::SerializeToSaveGame(UHomeWorldSaveGame* Out) const
{
	if (!Out) return;
	Out->SavedRoleBySpawnIndex.Reset();
	for (EHomeWorldFamilyRole R : RoleBySpawnIndex)
	{
		Out->SavedRoleBySpawnIndex.Add(static_cast<uint8>(R));
	}
}

void UHomeWorldFamilySubsystem::DeserializeFromSaveGame(const UHomeWorldSaveGame* In)
{
	if (!In) return;
	RoleBySpawnIndex.Reset();
	for (uint8 B : In->SavedRoleBySpawnIndex)
	{
		RoleBySpawnIndex.Add(static_cast<EHomeWorldFamilyRole>(B));
	}
}
