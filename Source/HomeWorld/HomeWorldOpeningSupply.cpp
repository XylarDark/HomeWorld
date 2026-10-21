// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningSupply.h"

#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"

namespace
{
	const FName DeliveryNodeTag(TEXT("NODE_OPENING_DELIVERY"));
	constexpr int32 DeliveryPile = 10;
}

UHomeWorldOpeningDeliveryNode::UHomeWorldOpeningDeliveryNode()
{
	PrimaryComponentTick.bCanEverTick = false;
}

UHomeWorldOpeningSupply::UHomeWorldOpeningSupply()
{
	PrimaryComponentTick.bCanEverTick = false;
}

bool UHomeWorldOpeningSupply::IsDeliveryMaterial(FName Material)
{
	return Material == HomeWorldOpeningMaterials::Wood
		|| Material == HomeWorldOpeningMaterials::Herb
		|| Material == HomeWorldOpeningMaterials::Stone;
}

AActor* UHomeWorldOpeningSupply::SpawnDeliveryNode(UWorld* World, FName Material, const FVector& Location)
{
	if (!World)
	{
		return nullptr;
	}
	FActorSpawnParameters Params;
	Params.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	AStaticMeshActor* Actor = World->SpawnActor<AStaticMeshActor>(Location, FRotator::ZeroRotator, Params);
	if (!Actor)
	{
		return nullptr;
	}
	Actor->Tags.Add(DeliveryNodeTag);
	UHomeWorldOpeningDeliveryNode* Node = NewObject<UHomeWorldOpeningDeliveryNode>(Actor, TEXT("Delivery"));
	Actor->AddInstanceComponent(Node);
	Node->SetMaterial(Material);
	Node->RegisterComponent();
	return Actor;
}

void UHomeWorldOpeningSupply::StockDawnChest()
{
	if (bGliderCrafted)
	{
		return;
	}
	DawnWood = 1;
	DawnSilk = 1;
	DawnMetal = 1;
	UE_LOG(LogTemp, Log, TEXT("opening_glider: dawn chest holds wood 1, silk 1, metal 1"));
}

bool UHomeWorldOpeningSupply::HasDawnStock() const
{
	return DawnWood >= 1 && DawnSilk >= 1 && DawnMetal >= 1;
}

int32 UHomeWorldOpeningSupply::GetDawnCount(FName Material) const
{
	if (Material == HomeWorldOpeningMaterials::Wood)
	{
		return DawnWood;
	}
	if (Material == HomeWorldOpeningMaterials::Silk)
	{
		return DawnSilk;
	}
	if (Material == HomeWorldOpeningMaterials::Metal)
	{
		return DawnMetal;
	}
	return 0;
}

bool UHomeWorldOpeningSupply::TryCraftGlider()
{
	if (bGliderCrafted || !HasDawnStock())
	{
		return false;
	}
	--DawnWood;
	--DawnSilk;
	--DawnMetal;
	bGliderCrafted = true;
	UE_LOG(LogTemp, Log, TEXT("opening_glider: crafted (wood %d, silk %d, metal %d)"), DawnWood, DawnSilk, DawnMetal);
	return true;
}

int32 UHomeWorldOpeningSupply::GetDeliveryCount(FName Material) const
{
	if (Material == HomeWorldOpeningMaterials::Wood)
	{
		return DeliveryWood;
	}
	if (Material == HomeWorldOpeningMaterials::Herb)
	{
		return DeliveryHerb;
	}
	if (Material == HomeWorldOpeningMaterials::Stone)
	{
		return DeliveryStone;
	}
	return 0;
}

bool UHomeWorldOpeningSupply::TryDeliver(UHomeWorldOpeningDeliveryNode* Node)
{
	if (!Node || Node->IsDelivered() || !IsDeliveryMaterial(Node->GetMaterial()))
	{
		return false;
	}
	const FName Material = Node->GetMaterial();
	if (Material == HomeWorldOpeningMaterials::Wood)
	{
		DeliveryWood += DeliveryPile;
	}
	else if (Material == HomeWorldOpeningMaterials::Herb)
	{
		DeliveryHerb += DeliveryPile;
	}
	else
	{
		DeliveryStone += DeliveryPile;
	}
	Node->MarkDelivered();
	UE_LOG(LogTemp, Log, TEXT("opening_delivery: %s pile %d in the matching chest"),
		*Material.ToString(), GetDeliveryCount(Material));
	return true;
}
