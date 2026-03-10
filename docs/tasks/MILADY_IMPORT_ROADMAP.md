# Milady Character Import Pipeline – Development Roadmap

**Scope:** HomeWorld tiny chibi Milady protagonists (from Milady Maker NFTs). Flow: Wallet connect → Verify NFT (Remilia Collective) → Fetch 2D PNG from IPFS → Auto-rig to 3D chibi VRM/GLB → Import to UE5 → Retarget animations → Spawn at 0.1x scale with bouncy movement.

**Project alignment:** HomeWorld targets **UE 5.7** (not 5.4); programmatic-by-default (C++ for systems, Blueprint for content). Content paths per [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md); add `/Game/HomeWorld/Milady/` (or `/Game/HomeWorld/Characters/Milady/`) for imported VRM/GLB, materials, and Milady-specific Blueprints.

**Contract reference:** Remilia Collective (mainnet); `balanceOf(wallet)`, `tokenURI(tokenId)` → metadata → IPFS image URL.

**Performance:** Editor-time import for prototype; runtime async load + LODs for shipping.

---

## Phase 1: Plugin & Dependency Setup

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 1.1 | Add VRM4U plugin | **Manual** | None | Medium (3–6h) | Install [VRM4U](https://github.com/ruyo/VRM4U) (GitHub, free): clone or download release into `Plugins/VRM4U`, enable in Editor (Edit > Plugins), add to `HomeWorld.uproject` under Plugins. Verify UE 5.7 compatibility (check plugin's supported engine version). Restart Editor. | Editor startup |
| 1.2 | Add Meshy-for-Unreal plugin | **Manual** | None | Low (1–2h) | Install official Meshy-for-Unreal plugin (Marketplace or Meshy.ai docs). Enable in project; configure Meshy API key in project settings or plugin UI. Document key storage in `.env.example` (no secrets in repo). | Editor/runtime (API calls) |
| 1.3 | Add Web3 / Wallet plugin | **Manual** | None | Medium (3–6h) | Choose and install Web3/Wallet plugin: e.g. **Web3.UE** or **MetaMask Embedded Wallets SDK** (or equivalent). Enable in Editor; add to `.uproject`. Verify UE 5.7 and that it supports Ethereum mainnet, `eth_call` (for `balanceOf`, `tokenURI`). | Runtime (wallet + RPC) |
| 1.4 | Document plugins and paths | **Programmatic** | 1.1–1.3 | Low (1–2h) | Update [SETUP.md](../SETUP.md) with Milady pipeline plugins (VRM4U, Meshy, Web3). Add `/Game/HomeWorld/Milady/` (or subfolder under Characters) to [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md). Add [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md) with one-time setup: API keys, plugin order, known issues. | — |
| 1.5 | Create Milady content folders (Python) | **Programmatic** | 1.4 | Low (1–2h) | Idempotent script in `Content/Python/` (e.g. `ensure_milady_folders.py`): ensure `/Game/HomeWorld/Milady/Meshes`, `/Game/HomeWorld/Milady/Materials`, `/Game/HomeWorld/Milady/Animations`, `/Game/HomeWorld/Milady/Blueprints` exist via `unreal.EditorAssetLibrary.make_directory()`. Call from bootstrap or run via MCP. | Editor |

---

## Phase 2: Wallet Connect & NFT Verification

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 2.1 | Wallet connect UI / flow | **Programmatic** or **Manual** | 1.3 | Medium (3–6h) | **Programmatic:** C++ or Blueprint: call plugin API to connect wallet (e.g. connect button → plugin's ConnectWallet). Store returned address in `UHomeWorldSessionSubsystem` or new `UHomeWorldWalletSubsystem` (C++). **Manual:** If plugin provides a sample UI, place and wire in level/UMG. Expose "Connected address" for Phase 2.2. | Runtime |
| 2.2 | Remilia Collective ABI and RPC | **Programmatic** | 2.1 | Medium (3–6h) | **Programmatic:** Add minimal ABI for Remilia Collective: `balanceOf(address)` (view), `tokenURI(uint256)` (view). Add config (e.g. `DefaultGame.ini` or Blueprint) for RPC URL (e.g. Infura/Alchemy mainnet). C++: `UHomeWorldNFTSubsystem` or Blueprint: call `eth_call` via Web3 plugin with contract `0x5e5a...` (full address in config), function selectors for `balanceOf` and `tokenURI`. No private key in code; read-only. | Runtime (RPC latency) |
| 2.3 | Verify ownership (balanceOf) | **Programmatic** | 2.2 | Low (1–2h) | Given wallet address, call `balanceOf(wallet)`. If > 0, wallet owns at least one Milady. Optional: enumerate token IDs (e.g. events or tokenOfOwnerByIndex if ERC721Enumerable). Stub: `bool VerifyMiladyOwnership(FString WalletAddress)` returning true when balance > 0. | Runtime |
| 2.4 | Resolve tokenId → metadata (tokenURI) | **Programmatic** | 2.2 | Medium (3–6h) | Call `tokenURI(tokenId)`; parse returned URI (typically `ipfs://...` or `https://...`). If IPFS, resolve via gateway (e.g. `https://ipfs.io/ipfs/<cid>` or project-configured gateway). HTTP GET metadata JSON; parse `image` (or equivalent) field to get PNG URL. C++ HTTP module or Blueprint HTTP node; store result in struct `FMiladyTokenMetadata { FString ImageURI; ... }`. | Runtime (HTTP + IPFS gateway) |

---

## Phase 3: Fetch Milady PNG from IPFS

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 3.1 | Download PNG from metadata image URL | **Programmatic** | 2.4 | Medium (3–6h) | Given `ImageURI` (IPFS or HTTPS), download binary PNG. Use UE `FHttpModule` / `IHttpRequest` (C++) or Blueprint HTTP. Save to transient or project dir (e.g. `Saved/MiladyCache/<tokenId>.png` or under Content if importing). Handle timeouts and failures; optional retry. | Runtime (network) |
| 3.2 | Optional: IPFS gateway config | **Programmatic** | 3.1 | Low (1–2h) | Make gateway configurable (e.g. `IPFS_GATEWAY=https://ipfs.io/ipfs/`). Replace `ipfs://` scheme with gateway base + CID in 3.1. | Runtime |
| 3.3 | Pass PNG to Meshy pipeline | **Programmatic** | 3.1, Phase 4 | Low (1–2h) | Once Meshy plugin is integrated (Phase 4): pass local PNG path or in-memory buffer to Meshy "image to 3D" API (plugin's API). Interface: e.g. `StartMiladyImageTo3D(FString LocalPNGPath, FOnMeshyComplete Callback)`. | Runtime/Editor |

---

## Phase 4: 2D PNG to 3D Model Conversion (Meshy.ai)

**Image-to-3D (Milady) — feasible via Meshy or Tripo; full pipeline deferred to post–Steam Demo (or next asset sprint). Manual path: PNG → Meshy/Tripo → GLB → VRM4U import.** See [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 for tools (Meshy, Tripo/TripoSR, Luma) and when to defer full pipeline; manual upload → GLB → VRM4U is a valid short-term path.

**When resuming (Phase 2 step 2.3):** For a clear "when resuming" checklist (what to implement, where to document no-access), see [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 *When resuming the image-to-3D pipeline*. Implement Phase 4 (Meshy from UE) or add a Tripo/TripoSR path; document any variables or options automation cannot set in `docs/MILADY_VARIABLES_NO_ACCESS.md` (create when needed), [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md), or [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 4.1 | Meshy API key and plugin config | **Manual** | 1.2 | Low (1–2h) | In Editor (or plugin settings): set Meshy API key. Prefer env var or encrypted config; document in MILADY_IMPORT_SETUP. Confirm plugin can call "image to 3D" (GLB/VRM output). | — |
| 4.2 | Call Meshy image-to-3D from UE | **Programmatic** | 4.1, 3.3 | High (1+ day) | Use Meshy-for-Unreal plugin to submit PNG and request GLB/VRM. If plugin exposes Blueprint nodes: create Blueprint or C++ wrapper that (1) uploads PNG or sends URL, (2) polls or receives callback when job completes, (3) downloads result to `Saved/` or Content. Stub: `RequestMeshyImageTo3D(FString PNGPath, FOnMeshyResult ResultCallback)`. Handle async and errors. | Runtime/Editor (API latency) |
| 4.3 | Save output GLB/VRM to project path | **Programmatic** | 4.2 | Low (1–2h) | On success, save Meshy output to e.g. `Content/HomeWorld/Milady/Generated/<tokenId>.glb` (or .vrm). Use `IPlatformFile` or plugin's save API. Idempotent: if file exists, optionally skip or overwrite per config. | Editor/disk |

---

## Phase 5: 3D Model Import & Rigging (VRM4U / GLB)

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 5.1 | Import GLB/VRM via VRM4U | **Programmatic** or **Manual** | 1.1, 4.3 | Medium (3–6h) | **Manual (first):** Use VRM4U "Import VRM" from Content Browser on a sample GLB/VRM; confirm skeleton and mesh appear. **Programmatic:** If VRM4U exposes import API (e.g. `VRM4UImportLibrary::ImportVRM(FString Path)`), call from C++ or Python; place imported assets under `/Game/HomeWorld/Milady/Meshes/<TokenId>_SK` (or similar). Document in PCG_VARIABLES_NO_ACCESS style any required options automation cannot set. | Editor (import time) |
| 5.2 | Auto-rig and skeleton mapping | **Manual** + **Programmatic** | 5.1 | Medium (3–6h) | VRM4U typically auto-rigs. Verify skeleton matches UE mannequin or project's chibi skeleton (e.g. `/Game/Man/` or dedicated chibi skeleton). If retargeting (Phase 6) requires a specific skeleton, document "source skeleton" and "target skeleton". Programmatic: store skeleton asset path in config; Blueprint or C++ can reference. | Editor |
| 5.3 | Scale and LOD for chibi (0.1x) | **Programmatic** | 5.1 | Low (1–2h) | On import or in a post-import step, scale skeleton/mesh to 0.1x (chibi). Option: VRM4U import option "Scale" or Blueprint/C++ that sets SkeletalMeshComponent scale to 0.1. Document in CONTENT_LAYOUT; optional LOD setup for shipping. | Editor/runtime |
| 5.4 | Master material (Milady Pastel) | **Programmatic** | 1.5 | Low (1–2h) | Create master material (or material instance) using Milady Pastel palette: e.g. `#FFB3D1` (bubblegum), `#E0BBE4` (lilac), `#A8E6CF` (mint). Use as base for imported Milady materials; C++ or Blueprint can set vector params if needed. | Editor |

---

## Phase 6: Animation Retargeting & Customization

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 6.1 | Retargeter setup (VRM4U IK Retargeter) | **Manual** + **Programmatic** | 5.2 | Medium (3–6h) | Use VRM4U IK Retargeter (or UE retargeting) to map source animations (e.g. from `/Game/Man/Demo/Animations/` or new chibi pack) to Milady skeleton. **Manual:** Create retarget asset, set source/target skeletons. **Programmatic:** If API exists, create retarget asset via script; document any "no access" options per automation-standards. | Editor |
| 6.2 | Bouncy walk and idle (Control Rig) | **Programmatic** or **Manual** | 6.1 | High (1+ day) | Add bouncy, kawaii motion: Control Rig or Animation Blueprint. Option A: Control Rig that adds vertical bounce to root or pelvis. Option B: AnimBP with additive layer or custom blend. Stub: `UHomeWorldChibiAnimInstance` (C++) with `BouncePhase`, `BounceScale`; drive from Speed or curve. Reference: [CHARACTER_ANIMATION.md](CHARACTER_ANIMATION.md) for AnimBP pattern. | Runtime |
| 6.3 | Emotes and optional gestures | **Programmatic** | 6.2 | Medium (3–6h) | Add emote animations (wave, sit, etc.): import or create sequences; expose as GAS abilities or simple Play Animation in Blueprint. Optional: gesture layer in AnimBP. | Runtime |

---

## Phase 7: Player Character Integration & Testing

| # | Task | Type | Dependencies | Effort | Description | Perf |
|---|------|------|--------------|--------|-------------|------|
| 7.1 | Swap default pawn to Milady (Blueprint) | **Programmatic** | 5.3, 6.1 | Low (1–2h) | Create `BP_MiladyCharacter` (child of `AHomeWorldCharacter`). Set SkeletalMesh to imported Milady mesh; AnimBP to retargeted chibi AnimBP; scale 0.1. Set as GameMode's DefaultPawnClass (or use a subsystem to swap at runtime after wallet + import). Per 09-mcp-workflow: inherited C++ components may need Python for mesh/AnimBP assignment if MCP cannot set them. | Runtime |
| 7.2 | End-to-end: Wallet → Import → Spawn | **Programmatic** | 2.1–2.4, 3.1–3.3, 4.2–4.3, 5.1–5.3, 6.1, 7.1 | High (1+ day) | Orchestrate full flow: Connect wallet → Verify ownership → Choose tokenId → Fetch PNG → Meshy 2D→3D → Import VRM/GLB → Retarget → Spawn as pawn (or load existing if already imported). Use Blueprint or C++ subsystem (e.g. `UHomeWorldMiladyImportSubsystem`) with async steps and progress/error delegates. Optional: simple UI (Connect, Select Token, Import, Play). | Runtime (first time); cached thereafter |
| 7.3 | PIE test and demo capture | **Manual** | 7.2 | Low (1–2h) | Run PIE: connect (or mock wallet), run import for one token, confirm 0.1x chibi spawns with movement and bouncy animation. Record short demo video. Add optional `pie_test_runner.py` check for "Milady mesh present" if useful. | — |

---

## Milestones

- **Milestone 1 – Manual import working:** VRM4U + Meshy plugins installed; one Milady PNG manually converted to GLB, imported via VRM4U, scaled to 0.1x, and set as default pawn. Movement and basic animation work. **Demo:** Short video of chibi moving in level.
- **Milestone 2 – Wallet + verified import:** Wallet connect works; ownership verified for one wallet; tokenId → metadata → IPFS PNG fetch automated; Meshy conversion and VRM4U import run from one button/flow. **Demo:** Connect wallet → Import my Milady → Spawn in level.
- **Milestone 3 – Playable slice (1–2 day goal):** Full pipeline: Wallet connect → Select Milady by tokenId → Fetch PNG → 2D→3D → Import → Retarget → Spawn at 0.1x with bouncy movement. **Demo:** End-to-end playable slice video.

---

## References and Conventions

- **Engine:** UE 5.7 ([AGENTS.md](../../AGENTS.md), [STACK_PLAN.md](../STACK_PLAN.md)). Verify VRM4U/Meshy/Web3 plugin compatibility with 5.7.
- **Code:** C++ in `Source/HomeWorld/`; new subsystems (Wallet, NFT, Milady Import) in C++ with Blueprint-callable APIs where needed. Blueprint for UI and content wiring.
- **Automation:** Follow automation-standards: document any "variables with no access" for VRM4U/Meshy (e.g. import options, retargeter settings) in `docs/MILADY_VARIABLES_NO_ACCESS.md` or [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).
- **Content:** Use [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) paths; add Milady folders and reference from scripts/bootstrap.
- **Session:** Log progress and any plugin/API issues in [SESSION_LOG.md](../SESSION_LOG.md); record errors in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).

---

## Programmatic work completed

The following has been implemented and is ready to use (no plugins required for metadata/PNG path):

- **C++:** `UHomeWorldWalletSubsystem` (store connected address), `UHomeWorldNFTSubsystem` (config, `FetchMetadataFromURL`, `DownloadMiladyPNG`, IPFS gateway, `VerifyMiladyOwnership` stub), `UHomeWorldMiladyImportSubsystem` (`ImportMiladyFromMetadataURL` runs metadata → PNG; Meshy/VRM4U stubbed), `FMiladyTokenMetadata` ([MiladyTypes.h](../../Source/HomeWorld/MiladyTypes.h)), `UHomeWorldChibiAnimInstance` (BouncePhase, BounceScale, BounceOffset for bouncy motion).
- **Config:** [Config/DefaultGame.ini](../../Config/DefaultGame.ini) `[Milady]` RemiliaContractAddress, EthereumRPCURL, IPFSGateway.
- **Python:** [ensure_milady_folders.py](../../Content/Python/ensure_milady_folders.py), [create_milady_pastel_material.py](../../Content/Python/create_milady_pastel_material.py) (creates M_MiladyPastel; add base color in Editor).
- **Flow:** From Blueprint or C++, call `ImportMiladyFromMetadataURL(MetadataURL, TokenId)` with a known metadata URL (e.g. from Web3 `tokenURI` or test); PNG is saved to `Saved/MiladyCache/TokenId.png`. Web3 plugin still required for `tokenURI(tokenId)` and wallet connect.

---

## Manual steps required

Complete these in order. Check off as done.

### Phase 1 – Plugins and one-time setup

- [ ] **1.1** Install VRM4U: clone or download from [GitHub ruyo/VRM4U](https://github.com/ruyo/VRM4U) into `Plugins/VRM4U`. Enable in Edit > Plugins, add to `HomeWorld.uproject`. Restart Editor. Verify UE 5.7 compatibility.
- [ ] **1.2** Install Meshy-for-Unreal (Marketplace or Meshy.ai). Enable in project. Set Meshy API key in project settings or plugin UI (do not commit; use `.env.example`).
- [ ] **1.3** Install Web3/Wallet plugin (e.g. Web3.UE or MetaMask Embedded Wallets SDK). Enable; verify Ethereum mainnet and `eth_call` support.
- [ ] Run `Content/Python/ensure_milady_folders.py` in Editor (Tools > Execute Python Script or MCP). Optionally run `create_milady_pastel_material.py`; then open M_MiladyPastel and add Base Color / VectorParameter for bubblegum (#FFB3D1), lilac (#E0BBE4), mint (#A8E6CF) if desired.

### Phase 2 – Wallet and contract

- [ ] **2.1** Wire wallet connect: call plugin’s ConnectWallet from UI or Blueprint; on success call `UHomeWorldWalletSubsystem::SetConnectedAddress(Address)`.
- [ ] **2.2** Fill `Config/DefaultGame.ini` [Milady]: RemiliaContractAddress (full mainnet address), EthereumRPCURL (e.g. Infura/Alchemy). Implement `tokenURI(tokenId)` via Web3 plugin and pass result to `UHomeWorldNFTSubsystem::FetchMetadataFromURL` or `UHomeWorldMiladyImportSubsystem::ImportMiladyFromMetadataURL`.
- [ ] **2.3–2.4** Implement `VerifyMiladyOwnership` and tokenId → tokenURI in C++ or Blueprint using Web3 plugin (eth_call). Stub in code returns false until then.

### Phase 4 – Meshy

- [ ] **4.1** Confirm Meshy API key is set and plugin can run “image to 3D” (GLB/VRM output).
- [ ] **4.2–4.3** In C++ or Blueprint: when Meshy job completes, save GLB/VRM to e.g. `Content/HomeWorld/Milady/Generated/<tokenId>.glb`. Wire `LastDownloadedPNGPath` from Milady Import subsystem into Meshy plugin input (path or upload).

### Phase 5 – VRM4U import and scale

- [ ] **5.1** Manually import one sample GLB/VRM via VRM4U (Content Browser) to confirm skeleton/mesh. If plugin exposes import API, call from C++/Python to place under `/Game/HomeWorld/Milady/Meshes/<TokenId>_SK`.
- [ ] **5.2** Confirm auto-rig and document source/target skeleton for retargeting.
- [ ] **5.3** Set scale to 0.1x on import or on SkeletalMeshComponent (Blueprint/C++).
- [ ] **5.4** Apply M_MiladyPastel (or instances) to imported Milady materials as needed.

### Phase 6 – Animation

- [ ] **6.1** Create retarget asset (VRM4U IK Retargeter or UE retargeting): source = project/Man skeleton (or chibi), target = Milady skeleton. Map walk/idle from `/Game/Man/Demo/Animations/` or chibi pack.
- [ ] **6.2** Create or reparent AnimBP for chibi to `UHomeWorldChibiAnimInstance`; use BounceOffset (or BouncePhase/BounceScale) in AnimGraph for vertical bounce. Optionally add Control Rig for extra kawaii motion.
- [ ] **6.3** Add emote animations (wave, sit) and expose via GAS or Play Animation.

### Phase 7 – Player and testing

- [ ] **7.1** Create Blueprint `BP_MiladyCharacter` (parent `AHomeWorldCharacter`). Assign imported Milady Skeletal Mesh, chibi AnimBP (with UHomeWorldChibiAnimInstance), scale 0.1. Set as Default Pawn Class or swap at runtime after import. (If MCP cannot set inherited C++ component props, use Python or set in Editor.)
- [ ] **7.2** Wire full flow: Connect wallet → Get tokenURI(tokenId) (Web3) → ImportMiladyFromMetadataURL or ImportMiladyByTokenId (once Web3 returns URL) → when PNG ready, trigger Meshy → on GLB/VRM, trigger VRM4U import → retarget → spawn BP_MiladyCharacter. Optional: simple UI (Connect, Select Token, Import, Play).
- [ ] **7.3** PIE test: connect (or mock), import one token, confirm 0.1x chibi spawns with movement and bouncy animation. Record demo video.

---

**See also:** [workflow/README.md](../workflow/README.md), [MILADY_IMPORT_SETUP.md](../MILADY_IMPORT_SETUP.md).
