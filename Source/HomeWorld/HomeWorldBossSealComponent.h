// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HomeWorldBossSealComponent.generated.h"

class AHomeWorldCharacter;

/** CD-A optional boss seal stub interact — logs BOSS:SEAL (no AI, no kill). */
UCLASS(ClassGroup = (HomeWorld), meta = (BlueprintSpawnableComponent))
class HOMEWORLD_API UHomeWorldBossSealComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHomeWorldBossSealComponent();

	UFUNCTION(BlueprintCallable, Category = "CD|Boss")
	bool TrySealStub(AHomeWorldCharacter* Character);

protected:
	virtual void BeginPlay() override;

	UPROPERTY(Transient)
	bool bSealUsed = false;
};
