// Copyright HomeWorld. All Rights Reserved.

#include "HomeWorldOpeningWalker.h"
#include "HomeWorldAIController.h"

#include "Animation/AnimSequence.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"

AHomeWorldOpeningWalker::AHomeWorldOpeningWalker()
{
	PrimaryActorTick.bCanEverTick = true;
	bUseControllerRotationYaw = false;
	AutoPossessAI = EAutoPossessAI::Disabled;
	if (UCharacterMovementComponent* Movement = GetCharacterMovement())
	{
		Movement->bOrientRotationToMovement = true;
		Movement->bRunPhysicsWithNoController = true;
		Movement->RotationRate = FRotator(0.f, 720.f, 0.f);
		Movement->MaxWalkSpeed = 450.f;
	}
	if (UCapsuleComponent* Capsule = GetCapsuleComponent())
	{
		Capsule->SetCapsuleSize(42.f, 100.f);
		Capsule->SetCollisionProfileName(FName("Pawn"));
		Capsule->SetCollisionResponseToChannel(ECC_Visibility, ECR_Ignore);
	}
	if (USkeletalMeshComponent* Body = GetMesh())
	{
		Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

void AHomeWorldOpeningWalker::CopyAppearance(AActor* Source)
{
	if (!Source)
	{
		return;
	}
	Tags = Source->Tags;
	USkeletalMeshComponent* SourceBody = Source->FindComponentByClass<USkeletalMeshComponent>();
	USkeletalMeshComponent* Body = GetMesh();
	if (!SourceBody || !Body)
	{
		return;
	}
	Body->SetSkeletalMeshAsset(SourceBody->GetSkeletalMeshAsset());
	Body->SetAnimInstanceClass(nullptr);
	Body->SetAnimationMode(EAnimationMode::AnimationSingleNode);
}

void AHomeWorldOpeningWalker::SetMoveSpeed(float CentimetersPerSecond)
{
	if (UCharacterMovementComponent* Movement = GetCharacterMovement())
	{
		Movement->MaxWalkSpeed = FMath::Max(1.f, CentimetersPerSecond);
	}
}

bool AHomeWorldOpeningWalker::WalkToward(const FVector& Goal, float AcceptCm)
{
	const FVector From = GetActorLocation();
	if (FVector::Dist2D(From, Goal) <= AcceptCm)
	{
		return true;
	}
	const FVector Dir(Goal.X - From.X, Goal.Y - From.Y, 0.f);
	AddMovementInput(Dir.GetSafeNormal(), 1.f);
	return false;
}

void AHomeWorldOpeningWalker::BeginPlay()
{
	Super::BeginPlay();
	if (USkeletalMeshComponent* Body = GetMesh())
	{
		const float Half = GetCapsuleComponent() ? GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight() : 100.f;
		Body->SetRelativeLocation(FVector(0.f, 0.f, -Half));
		Body->SetRelativeRotation(FRotator(0.f, 90.f, 0.f));
		Body->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	}
}

void AHomeWorldOpeningWalker::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	AHomeWorldAIController::DriveUnpossessedFollow(this);
	USkeletalMeshComponent* Body = GetMesh();
	if (!Body)
	{
		return;
	}
	const bool bMoving = GetVelocity().SizeSquared2D() > 100.f;
	if (bMoving == bWalkPlaying)
	{
		return;
	}
	bWalkPlaying = bMoving;
	Body->SetEnableAnimation(true);
	Body->SetAnimationMode(EAnimationMode::AnimationSingleNode);
	if (!bMoving)
	{
		Body->Stop();
		return;
	}
	if (UAnimSequence* Walk = LoadObject<UAnimSequence>(nullptr, TEXT("/Game/HomeWorld/Meshes/SizeTest/SK_Player_Female_Anim.SK_Player_Female_Anim")))
	{
		Body->PlayAnimation(Walk, true);
		if (UAnimSingleNodeInstance* Node = Body->GetSingleNodeInstance())
		{
			Node->SetRootMotionMode(ERootMotionMode::IgnoreRootMotion);
		}
	}
}
