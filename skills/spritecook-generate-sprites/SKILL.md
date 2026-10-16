---
name: spritecook-generate-sprites
description: "Still-image generation guide for SpriteCook. Use with spritecook-workflow-essentials when generating pixel art or detailed/HD assets, choosing models, and keeping style consistency with reference assets."
---

# SpriteCook Generate Sprites

Use this skill for still-image generation. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and shared defaults.

**Requires:** A connected SpriteCook MCP server. If disconnected, explain that connection is needed and use the host's native connection flow when authorized. Do not install software or change authentication settings as part of an art task.

For a complete UI screen or cohesive UI system, stop and use `spritecook-build-ui-kits` instead. The UI-kit workflow creates one coherent concept before extracting reusable controls and states. Keep `generate_game_art(mode="ui")` for one isolated icon, badge, button, control, divider, frame, or decoration.

## Pixel-Art Model Default

- For new pixel-art sprites, use `generate_game_art` with `model="gemini-nano-banana-2.1"`, `pixel=true`, and `resolution="1K"` unless the user requests different settings. For a new base character, use `generate_character(model="gemini-nano-banana-2.1", ...)`.
- Keep explicit user choices and saved preset models. For edits, preserve the source model inherited by the tool unless the user requests a model change.
- Check `list_generation_models` for current availability and prices. Nano Banana 2.1 retains NB2's base 12 / 18 / 30 credits at 1K / 2K / 4K at release. Source resolution is separate from the requested pixel-art dimensions and does not guarantee an exact final canvas size.
- For transparent sprites, continue using `background="transparent"`; SpriteCook removes the background after generation. NB2.1 does not produce native alpha transparency.
- Keep the reference limits: `generate_game_art` accepts up to 14 reference images in total across `style_asset_ids` plus a `reference_asset_id` or `edit_asset_id`. The selected model's own limit can be lower; `list_generation_models` reports it.
- Complete UI kits follow `spritecook-build-ui-kits` and its own model default.

## Exact-Size Sprites: Pixel Engine Image

Use Pixel Engine Image (`model="pixel-engine-image-v1"`) when one sprite or UI piece must come back at an exact small size, such as a 32×32 item icon or a 16×16 pickup.

- It draws exactly `width` × `height`. Sides are 16 to 128 px, the longest side at most 4× the shortest, and both sides even once the longest passes 64 px. Larger requests are scaled down to fit. `resolved_parameters.size_behavior` is `"exact"` for this model instead of `"hint"`.
- The background comes back already removed, so there is no separate removal step or charge. `smart_crop` is ignored and `resolution` is always `1K`.
- It is text only. Do not pass `style_asset_ids`, `reference_asset_id`, or `edit_asset_id`: requests with any reference image are rejected. It cannot match an existing collection through references, so put the shared look in `theme` and `style` and reuse the same wording for every sprite in the set. When the result must match existing art closely, use Nano Banana 2.1 or Pro with style references instead.
- Pixel art only: use `pixel=true` and `mode="assets"` or `mode="ui"`. It is not available for textures, tilesets, or UI kits. Character animation preps on a Pixel Engine Image sprite run on the default model.
- It draws one subject per image. Do not ask it for 3×3 sheets; call it once per sprite, or use `variations` for alternatives of the same sprite.
- Editing a Pixel Engine Image asset needs another model, because this one takes no input image. Pass the edit model explicitly with `edit_asset_id`.
- Check `list_generation_models` for its current price; its entry includes `exact_output_size`.

## Generating Multiple Assets in a Grid

Generating assets together in a 3×3 or 4×4 grid is generally recommended when you need several related props, items, or decorations, or when you want to achieve smaller pixel art. This produces multiple assets in one generation, which can save the user credits compared with generating every asset separately, and helps keep the collection visually consistent.

### Recommended Settings

- Prefer Nano Banana 2.1 (`gemini-nano-banana-2.1`) or Nano Banana Pro (`gemini-3-pro-image`) for multi-object generations. Respect explicit user choices and saved presets, and check `list_generation_models` for current availability and costs.
- Use `pixel=true` and `mode="assets"`.
- Set the pixel-art width and height to the desired size of **each piece**. For example, when aiming for approximately 32×32 sprites, use `width=32` and `height=32`, rather than increasing them to 256×256 to represent the whole sheet. This works well as generation guidance; inspect the extracted sprites rather than assuming exact dimensions.
- The `resolution` setting (`1K`, `2K`, or `4K`) controls source-image resolution separately. Start with `1K` for this workflow.
- Describe the 3×3 or 4×4 grid in the prompt. `variations` controls the number of generated sheets, not the number of objects within a sheet.
- Recommend Pro background removal for the best results when extracting individual sprites, especially around fine details and object edges. Account for its additional credit cost when estimating the batch. Select Pro where the workflow exposes that setting; do not invent a Pro parameter on `generate_game_art` or `remove_background` when the connected tool does not expose one. Background removal is a workflow setting, not an image-prompt instruction.

### Prompting the Sheet

- List the objects in row order, with one complete object per cell.
- Request generous empty spacing, no overlaps, no labels, and no visible grid lines.
- Specify consistent perspective, palette, lighting, outlines, and pixel scale across all objects.
- Use existing assets as style references when matching a collection.

Example prompt:

> Nine medieval tavern props in a regular 3×3 grid. Row 1: barrel, wooden crate, sack. Row 2: mug, bottle, candle. Row 3: stool, bucket, cooking pot. One complete object centered in each cell, generous empty spacing, consistent three-quarter view and scale. Low-resolution pixel art suitable for approximately 32×32 sprites, readable silhouettes, limited warm palette, crisp edges, consistent upper-left lighting. No text, labels, grid lines, overlaps, or scene background.

Pair this prompt with 32×32 pixel-art dimensions, 1K source resolution, Nano Banana 2.1 or Pro, and Pro background removal where available.

### Slice First, Animate Afterward

- Before slicing or animating, inspect outlines and transparency with `spritecook-polish-sprites`. If cleanup has removed edge pixels, compare the preserved alpha source locally and save the best cutoff before making derivatives.
- Inspect the generated sheet before slicing; grid placement may be uneven.
- If relying on regular grid boundaries, use `smart_crop=false` to preserve the outer layout, then verify the actual cell boundaries.
- Slice into separate PNGs using available image-processing tools and check each sprite for complete boundaries, clean transparency, consistent scale, and readability at its intended size.
- `auto_slice_asset` splits an owned sheet into owned assets by connected alpha. It works well for compact objects (raise `merge_distance` slightly for sprites with small gaps). Objects with detached parts, such as separate wing tips or sparkles, can split into extra pieces; slice those by grid cell locally instead.
- Cells can come back at different sizes even within one sheet. Normalize the set to one shared canvas locally when sizes must match.
- If resizing is needed, use nearest-neighbor sampling and recheck the result; prefer integer scaling where possible.
- Keep the original sheet and record which crop produced each named asset.
- If an extracted sprite needs animation, upload that individual PNG through `spritecook-upload-assets`, then animate its returned `asset_id` using `spritecook-animate-assets`.
- Reuse the same extracted source asset for motions with a suitable starting pose. For a different starting state, prepare a referenced or edited pose first, following `spritecook-animate-assets`.

Use individual generation when an asset needs dedicated control, and keep using the specialized character, tileset, and UI-kit workflows where relevant.

## Tool

### `generate_game_art`

Generate game art assets from a text prompt. Supports both pixel art and detailed/HD styles. Returns a job immediately by default; follow the returned `poll.tool` and `poll.arguments` until the assets are ready. Pass `wait_seconds` only when an explicit bounded wait is useful.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string (required) | - | What to generate. Be specific about subject, pose, and view angle |
| `width` | int | 64 | Width hint in pixels (16-512); exact (16-128) with `pixel-engine-image-v1`. See Output Size below |
| `height` | int | 64 | Height hint in pixels (16-512); exact (16-128) with `pixel-engine-image-v1`. See Output Size below |
| `variations` | int | 1 | Number of variations (1-4) |
| `pixel` | bool | true | True for pixel art, false for detailed/HD art |
| `bg_mode` | string | "transparent" | "transparent", "white", or "include" |
| `theme` | string | null | Art theme context, e.g. "dark fantasy medieval" |
| `style` | string | null | Style direction, e.g. "16-bit SNES style" |
| `aspect_ratio` | string | "1:1" | "1:1", "16:9", or "9:16" |
| `smart_crop` | bool | true | Auto-crop to content bounds |
| `smart_crop_mode` | string | "tightest" | Use `"tightest"` by default. Use `"power_of_2"` only when explicitly requested |
| `model` | string | null | Optional generation model. Call `list_generation_models` for current options and costs. |
| `mode` | string | "assets" | "assets", "texture", or "ui". Use `"ui"` only for one isolated UI asset; use `spritecook-build-ui-kits` for screens or systems. |
| `resolution` | string | "1K" | "1K", "2K", or "4K" |
| `quality` | string | "medium" | GPT-Image-2 quality tier: "low", "medium", or "high". Higher quality costs more credits. |
| `colors` | string[] | null | Hex palette guidance, max 64. Guides the colors; the output is not an indexed palette |
| `style_asset_ids` | string[] | null | Owned asset IDs to use as ambient style guide images; up to 14 references in total, model limits apply |
| `project_id` | string | null | Owned project to place the new assets in |
| `reference_asset_id` | string | null | Asset ID to use as one specific visual/context reference |
| `edit_asset_id` | string | null | Asset ID to edit/modify with the new prompt |
| `wait_seconds` | int | 0 | Optional bounded wait from 0-90 seconds before returning the polling contract |

Referenced assets must belong to the user's account. `style_asset_ids` can be combined with either `reference_asset_id` or `edit_asset_id`. Do not combine `reference_asset_id` and `edit_asset_id`.

If the user provides local image file paths for these references, use `spritecook-upload-assets` first and pass the returned asset IDs into the appropriate reference field.

## Reference Roles

- Use `style_asset_ids` for style guide images: ambient style, palette, proportions, rendering, and art-direction context. This is the normal choice when generating a new related asset that should match an existing collection, such as giving three existing buildings as style guides before asking for a new building type. SpriteCook already treats these images as style references; mention them in the prompt only when the user wants a specific trait called out.
- Use `reference_asset_id` when one specific asset is the source or context for the prompt, such as `make a building in a similar style to this one`, `give me just the door sprite`, or `use this character as the visual reference`.
- Use `edit_asset_id` when the user wants a direct modification of one existing asset, such as `make this roof red`, `remove the sign`, or `change the helmet color`.
- A reference also carries over its flaws, such as noise or stray pixels. Clean a reference before reusing it.
- `reference_asset_id` copies the reference's pixel size closely, and several variations of a close reference can return near copies of it. Use `variations=1` or `2` for a reference redraw and say in the prompt what must change.

## Output Size

`width` and `height` are hints (`size_behavior: "hint"` in `resolved_parameters`), not a hard canvas size. The one exception is Pixel Engine Image (`pixel-engine-image-v1`), which returns exactly the requested size; see Exact-Size Sprites above. In pixel mode the final canvas follows the detected pixel grid and the content crop, so it can differ a lot from the request. Variations from one job can also come back at different sizes.

- Read `resolved_parameters.output_dimensions` or each asset's `width`/`height` before planning a layout. Do not assume the requested size.
- Small requests usually land larger: a 16-48 px request for a detailed subject commonly returns 40-90 px. Describe the size in the prompt too, for example "tiny low-resolution sprite, about 32 pixels tall".
- `aspect_ratio` and `smart_crop` do not guarantee the canvas shape. A transparent subject can come back square with empty bands; trim locally when the exact box matters.
- Edits can change the size. A model switch on `edit_asset_id` can put a 44 px sprite on a different grid. Keep the source's model for small pixel edits and check the size afterward.
- `generate_character` aims for about 64 px but often returns 56-170 px canvases depending on model and subject.

To get a sprite at a specific small size:

- If no reference image is needed, use Pixel Engine Image (`model="pixel-engine-image-v1"`) and set `width` and `height` to the target size. The output is exactly that size.
- When the sprite must follow a reference or match existing art, use this redraw route instead:

1. Generate at the model's natural size and pick the best design.
2. Downscale it locally with nearest-neighbor to the target size (for example by half), then upload it through `spritecook-upload-assets`.
3. Call `generate_game_art` with the upload as `reference_asset_id`, `variations=1` or `2`, and a prompt like "a clean redraw of this exact low-resolution sprite at the same chunky pixel size, same design and palette". The redraw keeps the reference's pixel size and cleans up the downscale.

To match the pixel scale of an existing collection, pass that collection as `style_asset_ids`. Style references carry pixel density well; a new prop or creature matches the established scale far more reliably than a size hint alone.

## Proven Recipes

**Consistent families.** For a set of icons, badges, tiers, or items, generate the whole set as one 3×3 or 4×4 sheet in one call. One sheet gives the same size, outline weight, and lighting across the set, and beats a chain of edits or separate calls. Reuse the finished sheet as `style_asset_ids` for the next set.

**Objects at a scene's exact scale and position.** To cut props out of a generated scene, edit the scene with `edit_asset_id` and a prompt like "Keep only the torches, chest, and banner exactly where they are, at the same size. Fill everything else with flat pure magenta #FF00FF." Key out the magenta locally. This keeps each object at the scene's pixel scale and position. A reference generation of a single prop does not.

**Clean background plates.** "Remove the X" edits on a full scene keep the rest of the composition almost pixel for pixel. Use them for background plates and for masks (original minus plate). They are more reliable than "keep only X on solid green".

**Tiny pixel edits.** For a 1-2 px detail such as a string, eye, or trim, ask to change what exists: "Recolor the existing thin dark bowstring line to light cream. Change nothing else." Prompts like "make" or "draw" a detail can erase the original instead.

**Palette.** `colors` steers the palette, but pixel outputs still contain hundreds or thousands of near-duplicate shades. When the user needs a strict indexed palette (for example 4 or 16 colors), quantize the downloaded sprite locally with nearest-color mapping and no dithering.

**White parts with transparent backgrounds.** `bg_mode="transparent"` can cut out large white areas inside a subject, such as a blank label. Ask for an off-white or colored fill, or use `bg_mode="white"` and remove the background separately.

**A single composed UI screen.** `generate_game_art(mode="ui")` also works for one composed screen or HUD image for a mockup, thumbnail, or marketing art, where reusable parts are not needed. GPT image models render readable UI text more reliably than Gemini at this size. For reusable parts, use `spritecook-build-ui-kits`.

### `list_generation_models`

List available still-image generation models, pixel-art support, reference-image limits, supported quality options, and SpriteCook credit costs per image. Call this when choosing a model or when the user asks what models/costs are currently available.

### `list_character_workflows`

List guided pixel-art character perspectives, default animation ids, source-view/prep requirements, frame counts, and credit estimates.

Perspectives and preset animations:

| Perspective | Defaults | Presets |
|-------------|----------|---------|
| `platformer` | `idle`, `walk`, `jump` | `idle`, `walk`, `jump`, `run`, `attack`, `hurt`, `death` |
| `isometric` | `idle`, `walk_down`, `walk_right` | `idle`, `idle_back`, `walk_down`, `walk_right`, `jump_back`, `jump_front`, `run_down`, `run_right`, `attack`, `hurt`, `death` |
| `topdown` | `idle`, `walk_up`, `walk_right`, `walk_down` | `idle`, `idle_back`, `idle_right`, `walk_up`, `walk_down`, `walk_right`, `attack`, `hurt`, `death` |

### `generate_character`

Generate a base pixel-art character with SpriteCook's recommended character settings: a 64x64 size hint, transparent background, 1K square, tight smart crop, and the perspective-specific character prompt rewrite. The final canvas is often 56-170 px, so check the returned size. Returns a job immediately by default; when complete, the first generated asset is the `character_id`. This tool has no `project_id`; move the result with `assign_assets_to_project` when it belongs in a project.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string (required) | - | Character description |
| `perspective` | string (required) | - | `platformer`, `isometric`, or `topdown` |
| `model` | string | null | Optional generation model. Call `list_generation_models` for current options and costs. |
| `quality` | string | "medium" | GPT-Image-2 quality tier: "low", "medium", or "high" |
| `wait_seconds` | int | 0 | Optional bounded wait from 0-90 seconds before returning the polling contract |

### `generate_character_animations`

Generate preset and/or custom animations for a base character asset. Returns a character-animation run immediately by default; follow the returned polling contract until canonical `assets` entries are ready.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `character_id` | string (required) | - | Base character asset id: a `generate_character` result or any owned character still, including an edited, uploaded, or sliced sprite |
| `perspective` | string (required) | - | Same perspective used for the base character |
| `animation_ids` | string[] | perspective defaults | Preset ids from `list_character_workflows` |
| `custom_animations` | object[] | null | Custom animations with `{ id, label, prompt, source_view, output_frames }` |
| `bg_removal_provider` | string | "basic" | `basic` or `photoroom` |
| `wait_seconds` | int | 0 | Optional bounded wait from 0-90 seconds before returning the polling contract |

Character animation runs use `pixel-engine-v1.1`; this tool has no `model` argument. For `pixel-engine-v1.5`, animate each motion separately with `animate_game_art` on the same still (see `spritecook-animate-assets`). Run outputs use their own canvas, which is usually larger than the base still and not aligned to it; match frame 0 against the still locally when the hand-off must not jump. Fast jumps and overhead swings can touch the canvas edge, so check those frames. Two identical calls sent together can return the same run; send one call per take you want.

Passing any owned still as `character_id` is often the best way to animate a character that matches an existing art style. Give uploaded or sliced assets a descriptive label first with `update_asset_label`, because the label can feed the automatic animation prompt.

Custom animations use the custom prompt as the final animation prompt and skip preset prompt enhancement. `source_view` defaults to `front_idle`; if another source view needs prep, SpriteCook uses the matching workflow prep dependency for that perspective. A `source_view` selects a supported workflow input, not an arbitrary new state such as curled-up sleep. For a custom state that needs a different starting pose, prepare the still with `generate_game_art` first, then use `animate_game_art` on that prepared asset.

Example custom animation:

```json
{
  "label": "Spin Attack",
  "prompt": "Spin in place with a quick sword slash, looping cleanly.",
  "source_view": "right_walk",
  "output_frames": 8
}
```

### `check_character_animation_run`

Check a guided character animation run by id. Returns run status, item statuses, canonical generated `assets`, prep state, failures, and credits.

## Async Result Contract

- Follow the returned `poll.tool` with its exact `poll.arguments`; use `check_job_status` for jobs and `check_character_animation_run` for character-animation runs.
- Treat `operation_id` as the generic operation identifier while retaining `job_id` or `run_id` for the matching poll tool.
- On success, use each asset's `asset_id` and `sprite_url`. Use `spritesheet_url` only when an animation also provides a spritesheet.
- If a successful response contains `warning.code="asset_output_unavailable"`, execute the supplied `warning.recovery` tool call instead of searching arbitrary nested URL fields.

## Working Style

- After generation, inspect the result at native size and nearest-neighbor zoom. Use `spritecook-polish-sprites` for broken outlines, missing edge pixels, halos, or background debris before delivery or reuse; keep clean results unchanged.
- Be specific about subject, pose, camera/view angle, and key materials.
- Call `list_generation_models` when current model names, pixel-art support, quality options, or credit costs matter.
- When the user asks to use a saved preset, use `list_presets` and `get_preset_settings` first, then map the returned prompt, style, model, size, color, and reference guidance into `generate_game_art`.
- Use `list_character_workflows`, `generate_character`, and `generate_character_animations` when the user wants a directly usable animated character set.
- Route menus, HUDs, inventories, dialogs, settings screens, overlays, and other complete UI compositions to `spritecook-build-ui-kits`.
- Default to pixel art unless the user asks for HD, detailed, smooth, realistic, or high-res output.
- When the user wants the same character or item in multiple outputs, establish one canonical design and reuse it as the source or reference. For animation, prepare a different starting pose when needed, following `spritecook-animate-assets`.
- Use `style_asset_ids` for follow-up generations that should keep the same visual style, especially when a preset returns `settings.reference.styleAssetIds`.
- Use `reference_asset_id` when the prompt depends on one specific visual/context reference asset.
- Use `edit_asset_id` when directly modifying one existing SpriteCook asset.
- Do not generate multiple independent still variations when the real goal is one consistent character plus later animations.
- Prefer `smart_crop_mode="tightest"` unless the user explicitly asks for `"power_of_2"`.

## Consistency Rules

- For a motion set, establish the base character once. Animate the same `asset_id` when its starting pose fits; otherwise create a referenced or edited still in the required starting pose, inspect it, and animate that new asset. For example, prepare a sleeping still before generating a sleeping loop.
- For asset variations that should stay recognizably the same design, prefer `edit_asset_id` for direct modification or `style_asset_ids` for style guidance over a brand-new unreferenced generation.
- Only skip a reference when the user explicitly wants different designs to explore.

## Pixel Art vs Detailed Art

**Pixel art** (`pixel: true`, default):
- Crisp hard edges, no anti-aliasing, visible pixel grid
- Automatic pixel-perfect post-processing for clean grid alignment
- Best for retro games, indie games, and 8-bit/16-bit projects
- Gemini models are highly recommended, in particular Nano Banana 2.1 (`gemini-nano-banana-2.1`), Nano Banana Pro (`gemini-3-pro-image`), or newer Gemini image models

**Detailed/HD art** (`pixel: false`):
- Smooth gradients, fine detail, anti-aliased edges
- Higher fidelity output without pixel grid constraints
- Best for HD 2D games, concept art, and marketing assets
- GPT image models are generally a bit stronger for complex detailed art, but Gemini and GPT models both work well here

Choose based on the game's art direction. When the user does not specify, default to pixel art.
