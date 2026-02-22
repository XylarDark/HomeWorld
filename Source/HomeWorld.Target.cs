// Copyright HomeWorld. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class HomeWorldTarget : TargetRules
{
	public HomeWorldTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("HomeWorld");
	}
}
