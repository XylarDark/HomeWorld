// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCombatDreamTypes.h"

namespace HomeWorldCombatDream
{
	const TCHAR* GetMinigameLogTag(EHomeWorldMinigameKind Kind)
	{
		switch (Kind)
		{
		case EHomeWorldMinigameKind::Heal: return TEXT("MINIGAME:HEAL");
		case EHomeWorldMinigameKind::Nurture: return TEXT("MINIGAME:NURTURE");
		case EHomeWorldMinigameKind::Grow: return TEXT("MINIGAME:GROW");
		case EHomeWorldMinigameKind::Possess: return TEXT("MINIGAME:POSSESS");
		default: return TEXT("MINIGAME:UNKNOWN");
		}
	}

	bool IsPolishFirstMinigame(EHomeWorldMinigameKind Kind)
	{
		return Kind == EHomeWorldMinigameKind::Possess;
	}
}
