// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldFamilySubsystem.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Actor.h"
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
	Out->bSavedPartnerOut = bPartnerOut;
	Out->bSavedChildOut = bChildOut;
}

void UHomeWorldFamilySubsystem::DeserializeFromSaveGame(const UHomeWorldSaveGame* In)
{
	if (!In) return;
	RoleBySpawnIndex.Reset();
	for (uint8 B : In->SavedRoleBySpawnIndex)
	{
		RoleBySpawnIndex.Add(static_cast<EHomeWorldFamilyRole>(B));
	}
	bPartnerOut = In->bSavedPartnerOut;
	bChildOut = In->bSavedChildOut;
}

EHomeWorldPartySetup UHomeWorldFamilySubsystem::GetPartySetup() const
{
	if (bPartnerOut && bChildOut)
	{
		return EHomeWorldPartySetup::AllThree;
	}
	if (bPartnerOut)
	{
		return EHomeWorldPartySetup::Partner;
	}
	if (bChildOut)
	{
		return EHomeWorldPartySetup::Child;
	}
	return EHomeWorldPartySetup::Solo;
}

void UHomeWorldFamilySubsystem::SetRescueComplete(bool bComplete)
{
	bRescueComplete = bComplete;
	if (!bRescueComplete)
	{
		bPartnerOut = false;
		bChildOut = false;
	}
}

bool UHomeWorldFamilySubsystem::TryInvitePartner(bool bNightOrDefend, bool bSpiritForm, bool bAtCamp, UWorld* World)
{
	if (!bRescueComplete || bNightOrDefend || bSpiritForm || bAtCamp)
	{
		return false;
	}
	RememberTaggedHome(World, TEXT("NPC_PARTNER"), PartnerHome, bHasPartnerHome);
	bPartnerOut = true;
	return true;
}

bool UHomeWorldFamilySubsystem::TryInviteChild(bool bNightOrDefend, bool bSpiritForm, bool bAtCave, UWorld* World)
{
	if (!bRescueComplete || bNightOrDefend || bSpiritForm || bAtCave)
	{
		return false;
	}
	RememberTaggedHome(World, TEXT("NPC_CHILD"), ChildHome, bHasChildHome);
	bChildOut = true;
	return true;
}

EHomeWorldPartyToggle UHomeWorldFamilySubsystem::ToggleMemberAtHome(AActor* Target, bool bAtHome, bool bNightOrDefend, bool bSpiritForm, UWorld* World)
{
	if (!Target)
	{
		return EHomeWorldPartyToggle::Refused;
	}
	const bool bPartner = Target->ActorHasTag(TEXT("NPC_PARTNER"));
	const bool bChild = Target->ActorHasTag(TEXT("NPC_CHILD"));
	if (!bPartner && !bChild)
	{
		return EHomeWorldPartyToggle::Refused;
	}
	if (!bAtHome || !bRescueComplete || bNightOrDefend || bSpiritForm)
	{
		return EHomeWorldPartyToggle::Refused;
	}
	if (bPartner && bPartnerOut)
	{
		bPartnerOut = false;
		PlaceMemberHome(World, true);
		return EHomeWorldPartyToggle::SentHome;
	}
	if (bChild && bChildOut)
	{
		bChildOut = false;
		PlaceMemberHome(World, false);
		return EHomeWorldPartyToggle::SentHome;
	}
	const bool bInvited = bPartner
		? TryInvitePartner(false, false, false, World)
		: TryInviteChild(false, false, false, World);
	return bInvited ? EHomeWorldPartyToggle::Invited : EHomeWorldPartyToggle::Refused;
}

void UHomeWorldFamilySubsystem::RememberPartnerHome(const FVector& Location)
{
	PartnerHome = Location;
	bHasPartnerHome = true;
}

void UHomeWorldFamilySubsystem::RememberChildHome(const FVector& Location)
{
	ChildHome = Location;
	bHasChildHome = true;
}

void UHomeWorldFamilySubsystem::ApplyLoadForces(bool bRescueDone, bool bNightOrSpirit, UWorld* World)
{
	const bool bWasPartner = bPartnerOut;
	const bool bWasChild = bChildOut;
	bRescueComplete = bRescueDone;
	if (!bRescueDone || bNightOrSpirit)
	{
		bPartnerOut = false;
		bChildOut = false;
		if (bWasPartner)
		{
			PlaceMemberHome(World, true);
		}
		if (bWasChild)
		{
			PlaceMemberHome(World, false);
		}
	}
}

void UHomeWorldFamilySubsystem::EndOuting(EHomeWorldPartyAbsence Reason, UWorld* World)
{
	if (!bPartnerOut && !bChildOut)
	{
		return;
	}
	const bool bWasPartner = bPartnerOut;
	const bool bWasChild = bChildOut;
	bPartnerOut = false;
	bChildOut = false;
	if (bWasPartner)
	{
		PlaceMemberHome(World, true);
	}
	if (bWasChild)
	{
		PlaceMemberHome(World, false);
	}
	UE_LOG(LogTemp, Log, TEXT("party: outing ended reason=%d partner=%d child=%d"),
		static_cast<int32>(Reason), bWasPartner ? 1 : 0, bWasChild ? 1 : 0);
}

bool UHomeWorldFamilySubsystem::IsActorOut(const AActor* Actor) const
{
	if (!Actor)
	{
		return false;
	}
	if (bPartnerOut && Actor->ActorHasTag(TEXT("NPC_PARTNER")))
	{
		return true;
	}
	if (bChildOut && Actor->ActorHasTag(TEXT("NPC_CHILD")))
	{
		return true;
	}
	return false;
}

void UHomeWorldFamilySubsystem::RememberTaggedHome(UWorld* World, FName Tag, FVector& OutHome, bool& bOutHasHome)
{
	if (!World)
	{
		if (UGameInstance* GameInstance = GetGameInstance())
		{
			World = GameInstance->GetWorld();
		}
	}
	if (!World)
	{
		return;
	}
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(Tag))
		{
			OutHome = It->GetActorLocation();
			bOutHasHome = true;
			return;
		}
	}
}

void UHomeWorldFamilySubsystem::PlaceMemberHome(UWorld* World, bool bPartner) const
{
	if (!World)
	{
		return;
	}
	const bool bHasHome = bPartner ? bHasPartnerHome : bHasChildHome;
	if (!bHasHome)
	{
		return;
	}
	const FVector Home = bPartner ? PartnerHome : ChildHome;
	const FName Tag = bPartner ? TEXT("NPC_PARTNER") : TEXT("NPC_CHILD");
	for (TActorIterator<AActor> It(World); It; ++It)
	{
		if (It->ActorHasTag(Tag))
		{
			It->SetActorLocation(Home);
			break;
		}
	}
}
