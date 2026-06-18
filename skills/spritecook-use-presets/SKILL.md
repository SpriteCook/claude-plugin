---
name: spritecook-use-presets
description: "Use SpriteCook saved presets through MCP. Use when the user explicitly asks to use a preset, refers to one of their saved SpriteCook presets, asks for the same style/settings as a saved preset, or asks to save a private preset for future consistent asset generation."
---

# SpriteCook Use Presets

Use this skill with `spritecook-workflow-essentials` and the relevant generation skill.

Presets are saved SpriteCook settings and prompt recipes. Their purpose is to help the user get consistent, similar output later, especially when they need a collection of related assets with the same style, model, prompt structure, dimensions, color guidance, and reference images. Users can fine-tune and save presets in the SpriteCook app, then ask an agent to use those presets through MCP.

## When To Use Presets

- Use presets when the user explicitly says `use my preset`, names a saved preset, or asks for assets matching a saved SpriteCook setup.
- Use presets when the user implies continuity with a named saved style or workflow, such as `use my character preset for this`.
- Do not browse presets by default for ordinary generation requests. If the user does not mention or imply a preset, use the normal SpriteCook generation workflow.
- Use `save_private_preset` only when the user asks to save a preset or preserve these settings for future use.

## Fetch And Apply

1. Call `list_presets(query=...)` with the user's preset name or intent.
2. Pick the best match by title first, then mode, status, description, and settings.
3. If multiple plausible presets remain, ask a concise clarification before generating.
4. Call `get_preset_settings(preset_id=...)` for the selected preset.
5. Map returned settings into the relevant MCP tool:
   - `prompt` -> base prompt or prompt guidance.
   - `themeText` -> `theme`.
   - `styleText` -> `style`.
   - `width`, `height`, `pixel`, `bgMode`, `aspectRatio`, `smartCropEnabled`, `smartCropMode`, `detailedModel`, `resolution`, `quality`, and `colors` -> matching generation arguments when the target tool supports them.
   - `settings.reference.styleAssetIds` -> `style_asset_ids` for `generate_game_art`, up to 10 asset IDs.
   - `settings.reference.contextAssetId` -> `reference_asset_id` for `generate_game_art`.
   - `settings.reference.editAssetId` -> `edit_asset_id` for `generate_game_art` only when the user is modifying that specific image.
   - `tilesetPerspective`, `tilesetPieceSet`, and `tilesetElevation` -> `generate_tileset` settings.
6. Preserve the user's requested subject or change. The preset should guide style/settings; it should not override the user's new intent unless the user asks for an exact repeat.

## Reference Images

- Private draft presets can return owned asset IDs:
  - `settings.reference.styleAssetIds`
  - `settings.reference.contextAssetId`
  - `settings.reference.editAssetId`
- Published presets can return frozen preset media URLs:
  - `settings.reference.styleUploadUrls`
  - `settings.reference.contextUploadUrl`
  - `settings.reference.editUploadUrl`
- Use `style_asset_ids` directly for `settings.reference.styleAssetIds` when calling `generate_game_art`; pass at most 10 IDs.
- Use `reference_asset_id` for `settings.reference.contextAssetId` when the preset provides one specific visual/context reference.
- Use `edit_asset_id` only for `settings.reference.editAssetId`, when the user is modifying that specific image.
- Treat style asset IDs as ambient style guide images: they establish style, palette, proportions, and rendering for new related assets. The prompt does not need to restate that they are style references unless the user asks to emphasize a specific detail.
- If a preset returns multiple style asset IDs but the target tool only accepts one, prefer the first style asset unless the user asks to choose differently.
- If a preset returns upload URLs that the target MCP generation tool cannot consume, still use the text/model/size/color settings and mention that the media reference could not be applied through that tool.

## Saving Presets

- Use `save_private_preset(...)` only after the user asks to save a preset.
- Save presets as private drafts only. Do not publish, share, or submit anything for moderation.
- Include the settings that matter for repeatability: prompt pattern, theme, style, model, size, pixel mode, background mode, smart crop, quality, colors, and supported reference/edit/style images.
- Use `style_references`, `reference_image`, `edit_image`, and preview asset IDs when the user wants the saved preset to include those images.
- If saving fails because of the private preset limit or unavailable reference assets, explain the user-facing problem briefly and do not retry with missing references unless the user asks.

## Practical Pattern

When the user says `Use my character preset for a blue wizard idle sprite`:

1. `list_presets(query="character")`
2. Select the likely character preset.
3. `get_preset_settings(preset_id="...")`
4. Generate with the preset's style/settings plus the new subject: `blue wizard idle sprite`.
