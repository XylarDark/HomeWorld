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

	/** Spring arm length (distance from character to camera). Tune in Editor. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "100.0", ClampMax = "2000.0"))
	float TargetArmLength = 400.0f;

	/** Follow camera field of view (degrees). */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "60.0", ClampMax = "120.0"))
	float CameraFOV = 90.0f;

	/** Minimum camera pitch (degrees). Prevents camera from going below horizon. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "-89.0", ClampMax = "0.0"))
	float MinPitch = -70.0f;

	/** Maximum camera pitch (degrees). Prevents camera from flipping over the top. */
	UPROPERTY(EditDefaultsOnly, Category = "Camera", meta = (ClampMin = "0.0", ClampMax = "89.0"))
	float MaxPitch = 20.0f;

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

	/** Yaw rotation rate (deg/s) when orienting to movement. Tune in Editor for snappier or smoother turning. */
	UPROPERTY(EditDefaultsOnly, Category = "Movement", meta = (ClampMin = "1.0", ClampMax = "1440.0"))
	float RotationRateYaw = 720.0f;

	/** Offset (degrees) applied to the mesh relative rotation so mesh forward matches movement direction. Use e.g. 90 or -90 if the mesh faces the wrong way. */
	UPROPERTY(EditDefaultsOnly, Category = "Mesh", meta = (ClampMin = "-180.0", ClampMax = "180.0"))
	float MeshForwardYawOffset = 0.0f;

	virtual void BeginPlay() override;

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
};
