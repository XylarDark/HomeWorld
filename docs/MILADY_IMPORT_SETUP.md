# Milady Character Import Pipeline – One-Time Setup

One-time setup for the Milady chibi protagonist import pipeline. For the full task roadmap see [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md).

---

## Plugins (install order)

1. **VRM4U** – [GitHub: ruyo/VRM4U](https://github.com/ruyo/VRM4U)  
   - Clone or download release into `Plugins/VRM4U` (project root).  
   - Enable in Editor: **Edit > Plugins** → search VRM4U → Enable.  
   - Add to `HomeWorld.uproject` under `Plugins` if not auto-added.  
   - Verify UE 5.7 compatibility (check plugin’s supported engine version).  
   - Restart Editor after enable.

2. **Meshy-for-Unreal** – Marketplace or Meshy.ai docs  
   - Install per Meshy’s instructions. Enable in project.  
   - Configure **Meshy API key** in project settings or plugin UI (see [API keys](#api-keys) below).

3. **Web3 / Wallet** – e.g. Web3.UE or MetaMask Embedded Wallets SDK  
   - Install and enable; add to `.uproject`.  
   - Verify UE 5.7 and support for Ethereum mainnet and `eth_call` (for `balanceOf`, `tokenURI`).

---

## API keys

- **Meshy:** Set in Editor (plugin settings) or via environment variable. Do not commit keys; document in `.env.example` with a placeholder (e.g. `MESHY_API_KEY=`). See [02-security.mdc](.cursor/rules/02-security.mdc).
- **Ethereum RPC (optional):** For NFT verification, use Infura/Alchemy mainnet URL. Store in config (e.g. `DefaultGame.ini` section or Blueprint) or env; never commit secrets.

---

## Content paths

After setup, ensure Milady content folders exist. Run from Editor:

- **Tools → Execute Python Script** → `Content/Python/ensure_milady_folders.py`  
  or run via MCP: `execute_python_script("ensure_milady_folders.py")`.

Paths created (per [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md)):

- `/Game/HomeWorld/Milady/Meshes`
- `/Game/HomeWorld/Milady/Materials`
- `/Game/HomeWorld/Milady/Animations`
- `/Game/HomeWorld/Milady/Blueprints`

Generated imports (e.g. from Meshy) can go under `Milady/Generated` or `Milady/Meshes/<TokenId>_SK` as decided in the roadmap.

---

## Known issues and plugin order

- **VRM4U:** If import fails on a given GLB/VRM, check plugin’s issue tracker for UE 5.7-specific fixes. Document any “variables with no access” (import options automation cannot set) in `docs/MILADY_VARIABLES_NO_ACCESS.md` or [KNOWN_ERRORS.md](KNOWN_ERRORS.md) per [automation-standards.mdc](.cursor/rules/automation-standards.mdc).
- **Meshy:** Confirm plugin supports “image to 3D” with GLB/VRM output. Async job completion and download path may require project-specific wiring.
- **Web3:** Read-only contract calls (`balanceOf`, `tokenURI`) do not require a private key; wallet connect is for address only.

---

## Contract reference (Remilia Collective)

- Mainnet contract (use full address in config): Remilia Collective.  
- Calls: `balanceOf(address)` → ownership check; `tokenURI(uint256)` → metadata URI (often IPFS).  
- Resolve IPFS via configurable gateway (e.g. `https://ipfs.io/ipfs/<cid>`).

---

**See also:** [SETUP.md](SETUP.md), [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md), [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md).
