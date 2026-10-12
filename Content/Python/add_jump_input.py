"""Put Space on the mapping list Unreal 5.8 actually reads."""

import unreal

PATH = "/Game/HomeWorld/Input"
action = unreal.EditorAssetLibrary.load_asset(PATH + "/IA_Jump")
context = unreal.EditorAssetLibrary.load_asset(PATH + "/IMC_Default")
data = context.get_editor_property("default_key_mappings")
text = data.export_text()
if "IA_Jump" in text and "SpaceBar" in text:
    unreal.log("jump input: Space already in default_key_mappings")
else:
    key = unreal.Key()
    key.set_editor_property("key_name", unreal.Name("SpaceBar"))
    mapping = unreal.EnhancedActionKeyMapping()
    mapping.set_editor_property("action", action)
    mapping.set_editor_property("key", key)
    rows = list(data.get_editor_property("mappings") or [])
    rows.append(mapping)
    data.set_editor_property("mappings", rows)
    context.set_editor_property("default_key_mappings", data)
    unreal.EditorAssetLibrary.save_loaded_asset(context)
    saved = context.get_editor_property("default_key_mappings").export_text()
    unreal.log("jump input: space stored %s" % ("IA_Jump" in saved and "SpaceBar" in saved))
