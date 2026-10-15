// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldVirtueComponent.h"
#include "HomeWorldVirtueSpawnTable.h"

bool UHomeWorldVirtueComponent::HasPole(EHomeWorldVirtuePole Pole) const
{
	return Poles.Contains(Pole);
}

bool UHomeWorldVirtueComponent::HasAxis(EHomeWorldVirtuePole Pole) const
{
	const int32 Axis = HomeWorldVirtue::AxisIndex(Pole);
	for (const EHomeWorldVirtuePole Held : Poles)
	{
		if (HomeWorldVirtue::AxisIndex(Held) == Axis)
		{
			return true;
		}
	}
	return false;
}

void UHomeWorldVirtueComponent::ClearPoles()
{
	Poles.Reset();
}

bool UHomeWorldVirtueComponent::TryGivePole(EHomeWorldVirtuePole Pole)
{
	if (HasAxis(Pole) || Poles.Num() >= HomeWorldVirtue::AxisCount)
	{
		return false;
	}
	Poles.Add(Pole);
	return true;
}

bool UHomeWorldVirtueComponent::TryTakePole(EHomeWorldVirtuePole Pole)
{
	const int32 Removed = Poles.Remove(Pole);
	return Removed > 0;
}

bool UHomeWorldVirtueComponent::TrySwapAxis(EHomeWorldVirtuePole Pole)
{
	const int32 Axis = HomeWorldVirtue::AxisIndex(Pole);
	for (EHomeWorldVirtuePole& Held : Poles)
	{
		if (HomeWorldVirtue::AxisIndex(Held) == Axis)
		{
			Held = HomeWorldVirtue::Opposite(Held);
			return true;
		}
	}
	return false;
}

bool UHomeWorldVirtueComponent::TrySetHandPoles(const TArray<EHomeWorldVirtuePole>& Hand, FString& OutError)
{
	TArray<EHomeWorldVirtuePole> Next;
	if (!HomeWorldVirtue::TrySetHandPoles(Next, Hand, OutError))
	{
		return false;
	}
	bHandAuthored = true;
	HandPoles = Next;
	Poles = Next;
	return true;
}

void UHomeWorldVirtueComponent::Roll(const TArray<float>& Chances, FRandomStream& Stream)
{
	HomeWorldVirtue::RollPoles(Poles, Chances, Stream);
	bHandAuthored = false;
}

void UHomeWorldVirtueComponent::BeginPlay()
{
	Super::BeginPlay();
	if (bHandAuthored)
	{
		FString Error;
		if (!HomeWorldVirtue::TrySetHandPoles(Poles, HandPoles, Error))
		{
			UE_LOG(LogTemp, Warning, TEXT("Virtue hand set rejected on %s: %s"), *GetNameSafe(GetOwner()), *Error);
			Poles.Reset();
		}
		return;
	}
	const TArray<float> Fallback = HomeWorldVirtue::PlaceholderChances();
	const TArray<float>* Chances = &Fallback;
	if (SpawnTable)
	{
		Chances = bCollectible ? &SpawnTable->CollectibleChances : &SpawnTable->CharacterChances;
	}
	FRandomStream Stream(FMath::Rand());
	HomeWorldVirtue::RollPoles(Poles, *Chances, Stream);
}
