// Copyright HomeWorld. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "AbilitySystemInterface.h"
#include "GameFramework/Character.h"
#include "InputActionValue.h"
#include "HomeWorldCharacter.generated.h"

class UAbilitySystemComponent;
class UAttributeSet;
class USpringArmComponent;
class UCameraComponent;
class UInputAction;
class UInputMappingContext;

UCLASS(Blueprintable)
class HOMEWORLD_API AHomeWorldCharacter : public ACharacter, public IAbilitySystemInterface
{
	GENERATED_BODY()

public:
	AHomeWorldCharacter(const FObjectInitializer& ObjectInitializer);

	virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override;
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

protected:
	virtual void PossessedBy(AController* NewController) override;

	/** Ability system; used for GAS combat and attributes. */
	UPROPERTY(VisibleAnywhere, Category = "Abilities")
	TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

	/** Default attribute set (e.g. Health, Stamina). Subclass or add more in Blueprint. */
	UPROPERTY(VisibleAnywhere, Category = "Abilities")
	TObjectPtr<UAttributeSet> AttributeSet;

	/** Spring arm attached to capsule; camera follows controller rotation. */
	UPROPERTY(VisibleAnywhere, Category = "Camera")
	TObjectPtr<USpringArmComponent> CameraBoom;

	/** Follow camera attached to spring arm. */
	UPROPERTY(VisibleAnywhere, Category = "Camera")
	TObjectPtr<UCameraComponent> FollowCamera;

	/** Move input action (Axis2D: X = strafe, Y = forward/back). Assign in Editor or Blueprint defaults. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> MoveAction;

	/** Look input action (Axis2D: mouse delta). Assign in Editor or Blueprint defaults. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputAction> LookAction;

	/** Default mapping context (WASD + Mouse). Assign in Editor or Blueprint defaults. */
	UPROPERTY(EditDefaultsOnly, Category = "Input")
	TObjectPtr<UInputMappingContext> DefaultMappingContext;

	/** Scale applied to look input (mouse sensitivity). */
	UPROPERTY(EditDefaultsOnly, Category = "Input", meta = (ClampMin = "0.01", ClampMax = "10.0"))
	float LookSensitivity = 1.0f;

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
};
