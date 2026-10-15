// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldVirtueTypes.h"

namespace HomeWorldVirtue
{
	TArray<float> PlaceholderChances()
	{
		return { 0.5f, 0.25f, 0.125f, 0.0625f, 0.03125f, 0.015625f, 0.0078125f };
	}

	bool ChancesAreNonIncreasing(const TArray<float>& Chances)
	{
		if (Chances.Num() != AxisCount)
		{
			return false;
		}
		for (int32 Index = 1; Index < Chances.Num(); ++Index)
		{
			if (Chances[Index] > Chances[Index - 1])
			{
				return false;
			}
		}
		return true;
	}

	bool TrySetHandPoles(TArray<EHomeWorldVirtuePole>& OutPoles, const TArray<EHomeWorldVirtuePole>& Hand, FString& OutError)
	{
		if (Hand.Num() > AxisCount)
		{
			OutError = TEXT("more than seven poles");
			return false;
		}
		TSet<int32> Axes;
		for (const EHomeWorldVirtuePole Pole : Hand)
		{
			const int32 Axis = AxisIndex(Pole);
			if (Axes.Contains(Axis))
			{
				OutError = TEXT("both poles of one axis");
				return false;
			}
			Axes.Add(Axis);
		}
		OutPoles = Hand;
		OutError.Reset();
		return true;
	}

	void RollPoles(TArray<EHomeWorldVirtuePole>& OutPoles, const TArray<float>& Chances, FRandomStream& Stream)
	{
		OutPoles.Reset();
		TArray<int32, TInlineAllocator<AxisCount>> OpenAxes;
		for (int32 Axis = 0; Axis < AxisCount; ++Axis)
		{
			OpenAxes.Add(Axis);
		}
		for (int32 Step = 0; Step < AxisCount; ++Step)
		{
			const float Chance = Chances.IsValidIndex(Step) ? Chances[Step] : 0.f;
			if (Stream.FRand() >= Chance || OpenAxes.Num() == 0)
			{
				break;
			}
			const int32 Pick = Stream.RandRange(0, OpenAxes.Num() - 1);
			const int32 Axis = OpenAxes[Pick];
			OpenAxes.RemoveAt(Pick);
			const int32 SinValue = Axis * 2;
			const int32 PoleValue = SinValue + Stream.RandRange(0, 1);
			OutPoles.Add(static_cast<EHomeWorldVirtuePole>(PoleValue));
		}
	}

	const TCHAR* PoleName(EHomeWorldVirtuePole Pole)
	{
		switch (Pole)
		{
		case EHomeWorldVirtuePole::Greed: return TEXT("Greed");
		case EHomeWorldVirtuePole::Generosity: return TEXT("Generosity");
		case EHomeWorldVirtuePole::Gluttony: return TEXT("Gluttony");
		case EHomeWorldVirtuePole::Abstinence: return TEXT("Abstinence");
		case EHomeWorldVirtuePole::Sloth: return TEXT("Sloth");
		case EHomeWorldVirtuePole::Productivity: return TEXT("Productivity");
		case EHomeWorldVirtuePole::Wrath: return TEXT("Wrath");
		case EHomeWorldVirtuePole::Grace: return TEXT("Grace");
		case EHomeWorldVirtuePole::Pride: return TEXT("Pride");
		case EHomeWorldVirtuePole::Humility: return TEXT("Humility");
		case EHomeWorldVirtuePole::Envy: return TEXT("Envy");
		case EHomeWorldVirtuePole::Fulfillment: return TEXT("Fulfillment");
		case EHomeWorldVirtuePole::Lust: return TEXT("Lust");
		case EHomeWorldVirtuePole::Love: return TEXT("Love");
		default: return TEXT("Unknown");
		}
	}

	FString FormatPoles(const TArray<EHomeWorldVirtuePole>& Poles)
	{
		if (Poles.Num() == 0)
		{
			return TEXT("(none)");
		}
		FString Text;
		for (int32 Index = 0; Index < Poles.Num(); ++Index)
		{
			if (Index > 0)
			{
				Text += TEXT(", ");
			}
			Text += PoleName(Poles[Index]);
		}
		return Text;
	}
}
