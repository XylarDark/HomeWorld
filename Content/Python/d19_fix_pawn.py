import unreal, os
p=r"C:\dev\HomeWorld\Saved\d19_probe.txt"
open(p,"w").close()
def w(m):
  open(p,"a",encoding="utf-8").write(str(m)+"\n"); unreal.log(str(m))
# Load BP character and clear broken ABP on mesh if possible
path="/Game/HomeWorld/Characters/BP_HomeWorldCharacter.BP_HomeWorldCharacter"
bp = unreal.EditorAssetLibrary.load_blueprint_class(path.replace(".BP_HomeWorldCharacter","")) 
# better load asset
asset = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Characters/BP_HomeWorldCharacter")
w("asset="+str(asset))
# Game mode default pawn
gm = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Core/BP_HomeWorldGameMode")
w("gm="+str(gm))
# Try set CDO mesh anim class to None via SubobjectData or simple: use console
# List skeleton assets
regs = unreal.AssetRegistryHelpers.get_asset_registry()
ars = regs.get_assets_by_path("/Game/Characters", recursive=True)
w("chars count try")
found=[]
for a in regs.get_assets_by_path("/Game", recursive=True)[:5000]:
  n=str(a.asset_name)
  if "ABP" in n or "Manny" in n or "Unarmed" in n:
    found.append(str(a.package_name)+"/"+n)
w("found="+str(found[:40]))
