// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldFamilySubsystem.h"

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
