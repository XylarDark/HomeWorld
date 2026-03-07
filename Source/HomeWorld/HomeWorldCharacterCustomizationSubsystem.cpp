// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldCharacterCustomizationSubsystem.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/MorphTarget.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

void UHomeWorldCharacterCustomizationSubsystem::SetCustomizationTarget(USkeletalMeshComponent* MeshComponent)
{
	CustomizationTarget = MeshComponent;
	CachedMorphValues.Empty();
}

TArray<FName> UHomeWorldCharacterCustomizationSubsystem::GetMorphTargetNames() const
{
	TArray<FName> Out;
	if (!CustomizationTarget || !CustomizationTarget->GetSkeletalMeshAsset())
	{
		return Out;
	}
	USkeletalMesh* Mesh = CustomizationTarget->GetSkeletalMeshAsset();
	for (UMorphTarget* Morph : Mesh->GetMorphTargets())
	{
		if (Morph)
		{
			Out.Add(Morph->GetFName());
		}
	}
	return Out;
}

void UHomeWorldCharacterCustomizationSubsystem::SetMorphTargetValue(FName MorphName, float Value)
{
	if (!CustomizationTarget)
	{
		return;
	}
	CustomizationTarget->SetMorphTarget(MorphName, Value);
	CachedMorphValues.FindOrAdd(MorphName) = Value;
}

void UHomeWorldCharacterCustomizationSubsystem::SaveCustomizationToProfile()
{
	const FString Path = GetProfilePath();
	TSharedPtr<FJsonObject> Root = MakeShareable(new FJsonObject());
	for (const auto& Pair : CachedMorphValues)
	{
		Root->SetNumberField(Pair.Key.ToString(), Pair.Value);
	}
	FString Json;
	TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&Json);
	FJsonSerializer::Serialize(Root.ToSharedRef(), Writer);
	FFileHelper::SaveStringToFile(Json, *Path);
}

bool UHomeWorldCharacterCustomizationSubsystem::LoadCustomizationFromProfile()
{
	const FString Path = GetProfilePath();
	FString Json;
	if (!FFileHelper::LoadFileToString(Json, *Path))
	{
		return false;
	}
	TSharedPtr<FJsonObject> Root;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Json);
	if (!FJsonSerializer::Deserialize(Reader, Root) || !Root.IsValid())
	{
		return false;
	}
	TMap<FName, float> Values;
	for (const auto& Pair : Root->Values)
	{
		if (Pair.Value->Type == EJson::Number)
		{
			Values.Add(FName(*Pair.Key), static_cast<float>(Pair.Value->AsNumber()));
		}
	}
	ApplyMorphValues(Values);
	CachedMorphValues = Values;
	return true;
}

void UHomeWorldCharacterCustomizationSubsystem::ApplyMorphValues(const TMap<FName, float>& Values)
{
	if (!CustomizationTarget)
	{
		return;
	}
	for (const auto& Pair : Values)
	{
		CustomizationTarget->SetMorphTarget(Pair.Key, Pair.Value);
	}
	CachedMorphValues = Values;
}

FString UHomeWorldCharacterCustomizationSubsystem::GetProfilePath()
{
	return FPaths::ProjectSavedDir() / TEXT("CharacterCustomization.json");
}
