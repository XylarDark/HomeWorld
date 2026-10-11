# ComfyUI

Look tool. Not a mesh tool. Not a second art bible. Sheets follow `Docs/art/STILL_GENERATION_STANDARD.md`. Meters are pasted from `Docs/art/SCALE.md`.

## This machine

Comfy Desktop is installed. The app is `C:\Users\User\AppData\Local\Programs\Comfy Desktop\Comfy Desktop.exe`. The instance checked on 2026-10-10 is ComfyUI v0.39.2 under `C:\Users\User\AppData\Local\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI`.

Desktop loads models from `C:\Users\User\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models`. Settings → Storage is that folder. Do not guess a second install.

The TripoSR player run is `Docs/art/PLAYER_TRIPOSR.md`. ComfyUI is only for holding the picture. It does not make the mesh.

## Where it sits

A text image generator draws the first mood or the first front. It has no kept picture to copy, so a new drawing is the right tool.

After that picture, score it with the rating in `Docs/art/GREYBOX_T0_CATALOG.md`. A job-gate miss is a new drawing of that view. One or two local drifts go to Kontext on this file, largest drift first, with the rest kept. Three local drifts are a new drawing. A generator pass on a kept subject invents a second design.

## The test

One image. The player, front, A-pose, flat light, plain light-gray ground. Same person as the attached still. Dark coat. Small shoulder spirit. No scarf. No weapon. No text. Head one sixth of height.

Attach one kept picture only:

`Docs/art/player/SM_Player_homestead_lookback.jpg`

Do not attach the expression sheet. The scarf in that sheet is the partner’s. Do not attach a homestead scene. The cottage scale is a different sheet.

Workflow, from the ComfyUI docs: Workflow → Browse Templates → Flux → Flux.1 Kontext Dev. Load the picture in Load Image. English prompt only. Queue. Copy the output into `Docs/art/player/` and add a row in `Docs/art/STILLS_LIBRARY.md` before a second file.

The template’s quality set, in the shared storage:

| File | Folder | Job |
|---|---|---|
| `flux1-dev-kontext_fp8_scaled.safetensors` | `models/diffusion_models/` | The Dev diffusion weight the template names. |
| `ae.safetensors` | `models/vae/` | The Flux VAE. |
| `clip_l.safetensors` | `models/text_encoders/` | The short text encoder. |
| `t5xxl_fp16.safetensors` | `models/text_encoders/` | The quality text encoder. Select this one in the CLIP loader. |

`t5xxl_fp8_e4m3fn_scaled.safetensors` stays beside it. Use that file only when a queue runs out of memory. The card is an 8 GB GPU, so the diffusion weight stays the template’s fp8 file.

## License

FLUX.1 Kontext Dev is the non-commercial weight. A test may use it to see if the face holds. A sheet that will be meshed for Steam does not. Kontext Pro and Max are the paid API edits. Do not copy a Dev output into `Content/`.

## What a pass proves

The face, coat, and shoulder spirit match the attached still. The pose is the A-pose. The ground is plain.

A pass does not prove 2 m. The card holds the meter. The picture holds the person. One change on the next file. A side view attaches this front. It does not start from text.
