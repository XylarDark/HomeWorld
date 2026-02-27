// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldWalletSubsystem.h"

void UHomeWorldWalletSubsystem::SetConnectedAddress(const FString& Address)
{
	ConnectedAddress = Address;
}

void UHomeWorldWalletSubsystem::ClearConnectedAddress()
{
	ConnectedAddress.Empty();
}

bool UHomeWorldWalletSubsystem::IsConnected() const
{
	return !ConnectedAddress.IsEmpty();
}
