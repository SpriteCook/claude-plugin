---
name: spritecook-workflow-essentials
description: "Shared workflow rules for SpriteCook. Use together with SpriteCook generation, UI-kit building, animation, import, background-removal, and asset-organization workflows for credits, downloads, asset manifests, safe auth handling, and recommended defaults."
---

# SpriteCook Workflow Essentials

Use this alongside the SpriteCook image or animation skill whenever SpriteCook MCP tools are available.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Preflight Checklist

1. Check credits first with `get_credit_balance` before starting a batch or multi-asset workflow.
2. Use each asset's `sprite_url` as the canonical downloadable image URL. Use `spritesheet_url` only when it is present and specifically needed.
3. Save important `asset_id` values in a local manifest whenever there is a writable workspace, unless the user explicitly wants a throwaway result.
4. When a workflow involves follow-up generations or animations for the same subject, reuse the canonical design. For animation, reuse its `asset_id` when the starting pose fits; otherwise prepare a referenced or edited pose first, as explained in `spritecook-animate-assets`.
5. If the agent loses track of generated asset IDs, recover them with `list_recent_assets(limit=...)` before failing.
6. `get_credit_balance` also returns `account_handle` and a masked `account_email`. Use them to confirm which SpriteCook account the connection acts as, especially before saving presets or when an asset ID returns a no-access error (it may belong to a different account).

## Credential Safety

- Never ask the user to paste a SpriteCook API key into chat, prompts, code blocks, shell commands, or generated files.
- Never print, persist, echo, or inline API keys or `Authorization` headers in agent output.
- Prefer SpriteCook MCP tools, presigned URLs, or a preconfigured local connector/helper that handles authentication outside the prompt.
- If a raw API call is required and no authenticated helper exists, stop and ask the user to configure one.

## Async Operations

- Treat `generate_game_art`, `generate_tileset`, `remove_background`, `generate_character`, `generate_character_animations`, and `animate_game_art` as asynchronous operations.
- Follow the returned `poll.tool` with its exact `poll.arguments`. Do not invent a polling endpoint or search arbitrary response fields.
- Use `operation_id` as the generic identifier while retaining the returned `job_id` or `run_id` for the matching poll tool.
- Pass `wait_seconds` only when the tool exposes it and an explicit bounded wait is useful; the normal default is immediate return.
- On a terminal success, consume canonical `assets`. If the response contains `warning.code="asset_output_unavailable"`, execute its supplied `warning.recovery` tool call.

## Asset Library Tools

- Inspect generated assets before delivery or reuse. For broken outlines, faint edges, halos, or background debris, use `spritecook-polish-sprites`: read `get_asset_metadata.alpha_editing`, compare the preserved source locally, then save a selected cutoff with `set_asset_alpha_cutoff`. This adjustment costs no credits and avoids a new background-removal job.
- Use `spritecook-upload-assets` plus `create_asset_upload` and `finalize_asset_upload` when a local file path needs to become a SpriteCook asset before animation, editing, reference, or tileset-style reuse.
- Use `import_asset(image=..., pixel=..., display_name=..., file_name=...)` only when the image is already a small data URL or raw base64 value that can be passed without printing it.
- Use `remove_background(asset_id=...)` for owned SpriteCook assets that need a transparent cutout. Use `remove_background(image=...)` only when the user supplies local image data and does not need a reusable imported asset first. Poll the returned job contract for the cleaned asset.
- Use `update_asset_label(asset_id=..., label=...)` after generation, import, or cleanup when a clearer asset name will help the project manifest or future agent steps.
- Do not tell the user to use the SpriteCook HTTP API or API keys for local image import when the SpriteCook MCP tools are available. Prefer the upload bridge for file paths.

## UI Kit Tools

- Use `spritecook-build-ui-kits` for complete UI screens and cohesive systems. Build or select one concept first, then generate sheets and extract components from that shared visual source.
- If the UI-kit MCP tools are missing, refresh or reconnect the SpriteCook integration. Do not silently substitute several unrelated `generate_game_art(mode="ui")` calls for a full screen.
- Pass an existing owned concept to `create_ui_kit(concept_asset_id=...)` when the user or agent already has a suitable SpriteCook asset. Do not regenerate it merely to enter the UI-kit workflow.
- Keep `generate_game_art(mode="ui")` for a single isolated UI asset such as an icon, badge, control, divider, or decoration.
- Treat UI-kit concept and sheet generation as multi-asset work: check credits first, preserve the kit ID, and poll with `get_ui_kit` until queued jobs settle.
- Recommend GPT Image 2.5 Sunburst (`gpt-image-2.5-sunburst`) for UI-kit component sheets. The server selects the sheet model independently; the kit's `model` controls concepts, which default to GPT Image 2.5 Flare (`gpt-image-2.5-flare`). Gemini concepts require an account that independently supports 2K generation.
- Inspect extraction `quality_summary` before finalization and follow `spritecook-build-ui-kits` when it requires corrections.

## Preset Tools

- When the user says to use one of their saved presets, call `list_presets(query=...)` first and identify the best matching preset by title, mode, and status.
- Then call `get_preset_settings(preset_id=...)` and apply the returned settings as guidance for the next SpriteCook MCP generation or edit tool.
- Treat presets as saved settings and reference guidance, not as a separate generation path.
- Private draft presets can return owned reference asset IDs in `settings.reference.styleAssetIds`, `contextAssetId`, and `editAssetId`.
- For still-image generation, map `settings.reference.styleAssetIds` to `style_asset_ids` on `generate_game_art`; use up to 10 IDs.
- Treat style guide images as ambient style context for new related assets; agents do not need to restate them in the prompt unless calling out a specific visual trait.
- Map `settings.reference.contextAssetId` to `reference_asset_id` when the preset provides one specific visual/context reference asset.
- Use `reference_asset_id` when a prompt refers to one specific source or context asset, such as a particular building, character, prop, or part.
- Use `edit_asset_id` only for the one asset being directly modified.
- Published presets can return frozen preset media URLs in `settings.reference.styleUploadUrls`, `contextUploadUrl`, and `editUploadUrl`; use these only when the target MCP tool supports upload URL references.
- Use `save_private_preset(...)` only when the user explicitly asks to save a private preset. It creates a private draft preset only and does not publish, share, or submit anything for moderation.

## Defaults

- For several related props, items, or decorations, or when aiming for smaller pixel art, follow the grid-generation guidance in `spritecook-generate-sprites`: generate a 3×3 or 4×4 sheet, set pixel-art dimensions for each piece, then slice and animate individual assets as needed.
- Prefer `smart_crop_mode="tightest"` for the best default results. Use `"power_of_2"` only when the user explicitly asks for it.
- Use Nano Banana 2.1 (`model="gemini-nano-banana-2.1"`) as the recommended default for new pixel-art sprites and base characters. Use `pixel=true` for `generate_game_art`; `generate_character` already uses pixel-art settings.
- Preserve an explicit user model choice, a saved preset's model, or an edit workflow's inherited model. Nano Banana 2 (`gemini-3.1-flash-image`) is an older option, not the default for new pixel art.
- Call `list_generation_models` for current availability, pixel-art support, resolution limits, and credit costs. If NB2.1 is unavailable, choose an available pixel-art model from that response; do not guess a replacement model ID.
- NB2.1 supports 1K, 2K, and 4K source generation. Its base per-image price is 12 / 18 / 30 credits respectively, the same as NB2 at release; existing background-removal or workflow charges can still apply. Prefer 1K for ordinary pixel-art sprites, and verify current costs before a larger run.
- Focused workflow defaults override this general guidance. UI-kit concepts default to GPT Image 2.5 Flare (`gpt-image-2.5-flare`), while component sheets use GPT Image 2.5 Sunburst (`gpt-image-2.5-sunburst`). Follow `spritecook-build-ui-kits` for these separate stages.

## Asset Manifest

- Treat `asset_id` as the primary stable identifier.
- Store a 12-character SHA-256 prefix (`sha12`) for saved local files.
- Use a minimal manifest entry shape:
  - `asset_id`
  - `sha12`
  - optional `label`
- Prefer a simple machine-readable file such as `spritecook-assets.json` unless the project already has an asset manifest.
- Before generating a new reference asset or asking the user for an asset id, check the local manifest first.
- Before reusing a local file, compute its `sha12` and match it against the manifest to recover the correct `asset_id`.

## Downloading Assets

- For recent-asset recovery flows, prefer `list_recent_assets(limit=...)`.
- Treat `sprite_url` as the single primary asset URL to inspect, save, or hand off to downstream tools.
- Treat `spritesheet_url` as an optional secondary artifact. Use it only when present and only when you specifically need a spritesheet export.
- For single-asset inspection flows, `get_asset_metadata(asset_id)` also exposes canonical `asset_id`, `sprite_url`, and optional `spritesheet_url` fields.
- Treat `url`, `pixel_url`, and `raw_url` as compatibility aliases rather than the primary contract.
- Avoid relying on low-level internal fields such as `_presigned_pixel_url`, `_presigned_url`, `_presignRawUrl`, or `_presignPixelUrl` in agent-facing workflows unless no higher-level field is available.
- Avoid direct authenticated download endpoints in skill-driven workflows unless a helper handles auth out of band.
