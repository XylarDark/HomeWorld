// Copyright HomeWorld. All Rights Reserved.

using UnrealBuildTool;

public class HomeWorldEditor : ModuleRules
{
	public HomeWorldEditor(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
			"CoreUObject",
			"Engine",
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"UnrealEd",
			"AssetTools",
			"AssetRegistry",
			"MassSpawner",
			"MassRepresentation",
			"PCG",
		});
	}
}
