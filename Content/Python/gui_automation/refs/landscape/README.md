# Landscape (minimal) — ref images for GUI automation

Used by [landscape_apply_basic.py](../../landscape_apply_basic.py) to open Landscape mode and optionally focus the Sculpt tool. **Full terrain sculpting** (canyons, erosion, noise, spires) is not practical via ref-based automation; use [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §8 for real terrain work. This ref set supports only "focus Landscape" and optionally "click Sculpt."

## Capture

From project root with a level open that has a **Landscape** (e.g. Planetoid_Pride):

```text
py Content/Python/gui_automation/capture_landscape_refs.py
```

Capture: Modes panel with Landscape selected, and optionally the Sculpt tool. Crop to the relevant control.

## Ref images

| Filename | Description | When to capture |
|----------|-------------|-----------------|
| `landscape_mode.png` | Modes panel with "Landscape" selected (or Landscape mode indicator). | With level open, Modes panel visible. |
| `sculpt_tool.png` | Sculpt tool button or icon in Landscape toolbar. | With Landscape mode active, Sculpt tool visible. |

If a ref is missing, the script skips that step. See [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md) §4.7 and [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §8.
