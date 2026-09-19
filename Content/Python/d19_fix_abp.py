import unreal, os
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n"); unreal.log(str(m))

bp_path = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
cls = unreal.EditorAssetLibrary.load_blueprint_class(bp_path)
w("cls="+str(cls))
cdo = unreal.get_default_object(cls)
w("cdo="+str(cdo))
# list interesting props
for name in ("mesh","Mesh","CharacterMesh0","skeletal_mesh_component"):
  try:
    v=cdo.get_editor_property(name)
    w("prop %s=%s"%(name,v))
  except Exception as e:
    w("prop %s err %s"%(name,e))
# components
try:
  mesh = cdo.mesh
  w("cdo.mesh="+str(mesh))
  w("anim_class="+str(mesh.get_editor_property("anim_class")))
  w("skel="+str(mesh.get_editor_property("skeletal_mesh_asset") if hasattr(mesh,"skeletal_mesh_asset") else mesh.skeletal_mesh))
except Exception as e:
  w("mesh access "+str(e))

abp = unreal.EditorAssetLibrary.load_blueprint_class("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed")
mesh_asset = unreal.EditorAssetLibrary.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
w("abp="+str(abp)+" mesh_asset="+str(mesh_asset))
if mesh and abp:
  try:
    mesh.set_editor_property("anim_class", abp)
    w("set anim ok")
  except Exception as e:
    w("set anim "+str(e))
  try:
    mesh.set_skeletal_mesh_asset(mesh_asset)
    w("set mesh ok")
  except Exception as e:
    try:
      mesh.set_editor_property("skeletal_mesh_asset", mesh_asset)
      w("set mesh prop ok")
    except Exception as e2:
      w("set mesh "+str(e)+" / "+str(e2))
  unreal.EditorAssetLibrary.save_asset(bp_path)
  w("saved")
# compile
try:
  unreal.BlueprintEditorLibrary.compile_blueprint(unreal.EditorAssetLibrary.load_asset(bp_path))
  w("compiled")
except Exception as e:
  w("compile "+str(e))
