// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldPlacementConstants.h"

#include "Dom/JsonObject.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

namespace HomeWorldPlacement
{
	static const TSharedPtr<FJsonObject>* ObjectField(const TSharedPtr<FJsonObject>& Root, const TCHAR* Name)
	{
		if (!Root.IsValid())
		{
			return nullptr;
		}
		const TSharedPtr<FJsonObject>* Out = nullptr;
		if (!Root->TryGetObjectField(Name, Out) || Out == nullptr || !Out->IsValid())
		{
			return nullptr;
		}
		return Out;
	}

	static void ReadNumber(const TSharedPtr<FJsonObject>& Obj, const TCHAR* Name, float& Out)
	{
		if (!Obj.IsValid())
		{
			return;
		}
		float Value = Out;
		if (Obj->TryGetNumberField(Name, Value))
		{
			Out = Value;
		}
	}

	static void ReadString(const TSharedPtr<FJsonObject>& Obj, const TCHAR* Name, FString& Out)
	{
		if (!Obj.IsValid())
		{
			return;
		}
		FString Value;
		if (Obj->TryGetStringField(Name, Value) && !Value.IsEmpty())
		{
			Out = Value;
		}
	}

	static FConstants Load()
	{
		FConstants Constants;
		const FString Path = FPaths::ProjectContentDir() / TEXT("Python/placement_constants.json");
		FString Json;
		if (!FFileHelper::LoadFileToString(Json, *Path))
		{
			return Constants;
		}
		TSharedPtr<FJsonObject> Root;
		const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Json);
		if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
		{
			return Constants;
		}
		if (const TSharedPtr<FJsonObject>* Counter = ObjectField(Root, TEXT("counter")))
		{
			ReadNumber(*Counter, TEXT("height_cm"), Constants.CounterHeightCm);
			ReadNumber(*Counter, TEXT("depth_cm"), Constants.CounterDepthCm);
			ReadNumber(*Counter, TEXT("length_cm"), Constants.CounterLengthCm);
			ReadNumber(*Counter, TEXT("reveal_x"), Constants.RevealCounterX);
			ReadNumber(*Counter, TEXT("reveal_y"), Constants.RevealCounterY);
		}
		if (const TSharedPtr<FJsonObject>* Standoff = ObjectField(Root, TEXT("standoff_cm")))
		{
			ReadNumber(*Standoff, TEXT("partner"), Constants.PartnerStandoffCm);
			ReadNumber(*Standoff, TEXT("pond"), Constants.PondStandoffCm);
		}
		if (const TSharedPtr<FJsonObject>* Tags = ObjectField(Root, TEXT("tags")))
		{
			ReadString(*Tags, TEXT("kettle"), Constants.TagKettle);
			ReadString(*Tags, TEXT("kettle_counter"), Constants.TagKettleCounter);
			ReadString(*Tags, TEXT("consumable_station"), Constants.TagConsumableStation);
			ReadString(*Tags, TEXT("armor_table"), Constants.TagArmorTable);
			ReadString(*Tags, TEXT("partner"), Constants.TagPartner);
			ReadString(*Tags, TEXT("opening_dog"), Constants.TagOpeningDog);
		}
		Constants.bLoaded = true;
		return Constants;
	}

	const FConstants& Get()
	{
		static const FConstants Constants = Load();
		return Constants;
	}
}
