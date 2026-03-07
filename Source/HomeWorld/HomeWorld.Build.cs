// Copyright HomeWorld. All Rights Reserved.

using UnrealBuildTool;

public class HomeWorld : ModuleRules
{
	public HomeWorld(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"AIModule",
			"Core",
			"CoreUObject",
			"Engine",
			"HTTP",
			"InputCore",
			"EnhancedInput",
			"Json",
			"JsonUtilities",
			"GameplayAbilities",
			"GameplayTags",
			"GameplayTasks",
			"SmartObjectsModule",
			"UMG",
			"Slate",
			"SlateCore",
		});
	}
}
