// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HomeWorldWalletSubsystem.generated.h"

/**
 * Game instance subsystem for wallet connect (Milady pipeline).
 * Store connected wallet address; actual connect flow uses Web3/Wallet plugin (Phase 2.1).
 * Stub: SetConnectedAddress can be called from Blueprint/plugin integration.
 */
UCLASS(BlueprintType)
class HOMEWORLD_API UHomeWorldWalletSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()

public:
	/** Currently connected wallet address (empty if not connected). */
	UPROPERTY(BlueprintReadOnly, Category = "Wallet")
	FString ConnectedAddress;

	/** Set the connected wallet address (call from plugin ConnectWallet callback or Blueprint). */
	UFUNCTION(BlueprintCallable, Category = "Wallet", meta = (DisplayName = "Set Connected Address"))
	void SetConnectedAddress(const FString& Address);

	/** Clear connection (e.g. on disconnect). */
	UFUNCTION(BlueprintCallable, Category = "Wallet", meta = (DisplayName = "Clear Connected Address"))
	void ClearConnectedAddress();

	/** True if a wallet is connected. */
	UFUNCTION(BlueprintCallable, Category = "Wallet", meta = (DisplayName = "Is Connected"))
	bool IsConnected() const;
};
