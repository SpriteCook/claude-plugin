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
4. When a workflow involves follow-up generations or animations for the same subject, identify and reuse the canonical `asset_id` instead of generating from scratch again.
5. If the agent loses track of generated asset IDs, recover them with `list_recent_assets(limit=...)` before failing.

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
- Keep `gpt-image-2` as the UI-kit model default. Gemini UI-kit concepts require an account that independently supports 2K generation.
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

- Prefer `smart_crop_mode="tightest"` for the best default results. Use `"power_of_2"` only when the user explicitly asks for it.
- Model guidance:
  - `gemini-2.5-flash-image`: cheapest
  - `gemini-3.1-flash-image`: recommended default for ordinary still-image generation
  - `gemini-3-pro-image`: most expensive
- Focused workflow defaults override this general guidance. In particular, UI kits default to `gpt-image-2` because their concept and sheet pipeline uses 2K output.

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
- Avoid relying on low-level internal fields such as `_presigned_pixel_url` or `_presigned_url` in agent-facing workflows unless no higher-level field is available.
- Avoid direct authenticated download endpoints in skill-driven workflows unless a helper handles auth out of band.
