---
name: spritecook-generate-sprites
description: "Still-image generation guide for SpriteCook. Use with spritecook-workflow-essentials when generating pixel art or detailed/HD assets, choosing models, and keeping style consistency with reference assets."
---

# SpriteCook Generate Sprites

Use this skill for still-image generation. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and shared defaults.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Tool

### `generate_game_art`

Generate game art assets from a text prompt. Supports both pixel art and detailed/HD styles. Waits up to 90s for the result and returns download URLs.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string (required) | - | What to generate. Be specific about subject, pose, and view angle |
| `width` | int | 64 | Width in pixels (16-512) |
| `height` | int | 64 | Height in pixels (16-512) |
| `variations` | int | 1 | Number of variations (1-4) |
| `pixel` | bool | true | True for pixel art, false for detailed/HD art |
| `bg_mode` | string | "transparent" | "transparent", "white", or "include" |
| `theme` | string | null | Art theme context, e.g. "dark fantasy medieval" |
| `style` | string | null | Style direction, e.g. "16-bit SNES style" |
| `aspect_ratio` | string | "1:1" | "1:1", "16:9", or "9:16" |
| `smart_crop` | bool | true | Auto-crop to content bounds |
| `smart_crop_mode` | string | "tightest" | Use `"tightest"` by default. Use `"power_of_2"` only when explicitly requested |
| `model` | string | null | Optional generation model. Call `list_generation_models` for current options and costs. |
| `mode` | string | "assets" | "assets", "texture", or "ui" |
| `resolution` | string | "1K" | "1K", "2K", or "4K" |
| `quality` | string | "medium" | GPT-Image-2 quality tier: "low", "medium", or "high". Higher quality costs more credits. |
| `colors` | string[] | null | Hex color palette, max 8 |
| `reference_asset_id` | string | null | Asset ID from a previous generation to use as style reference |
| `edit_asset_id` | string | null | Asset ID to edit/modify with the new prompt |

`reference_asset_id` and `edit_asset_id` are mutually exclusive. The referenced asset must belong to your account.

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

Generate a base pixel-art character with SpriteCook's recommended character settings: 64x64, transparent background, 1K square, tight smart crop, and the perspective-specific character prompt rewrite. Returns a job response; when complete, the first generated asset is the `character_id`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string (required) | - | Character description |
| `perspective` | string (required) | - | `platformer`, `isometric`, or `topdown` |
| `model` | string | null | Optional generation model. Call `list_generation_models` for current options and costs. |
| `quality` | string | "medium" | GPT-Image-2 quality tier: "low", "medium", or "high" |

### `generate_character_animations`

Generate preset and/or custom animations for a base character asset.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `character_id` | string (required) | - | Base character asset id returned by `generate_character` |
| `perspective` | string (required) | - | Same perspective used for the base character |
| `animation_ids` | string[] | perspective defaults | Preset ids from `list_character_workflows` |
| `custom_animations` | object[] | null | Custom animations with `{ id, label, prompt, source_view, output_frames }` |
| `bg_removal_provider` | string | "basic" | `basic` or `photoroom` |

Custom animations use the custom prompt as the final animation prompt and skip preset prompt enhancement. `source_view` defaults to `front_idle`; if another source view needs prep, SpriteCook uses the matching workflow prep dependency for that perspective.

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

Check a guided character animation run by id. Returns run status, item statuses, generated asset ids, prep state, failures, and credits.

## Working Style

- Be specific about subject, pose, camera/view angle, and key materials.
- Call `list_generation_models` when current model names, pixel-art support, quality options, or credit costs matter.
- Use `list_character_workflows`, `generate_character`, and `generate_character_animations` when the user wants a directly usable animated character set.
- Default to pixel art unless the user asks for HD, detailed, smooth, realistic, or high-res output.
- When the user wants the same character or item in multiple outputs, generate one canonical still asset first and reuse that asset ID.
- Use `reference_asset_id` for follow-up generations that should keep the same character or visual style.
- Use `edit_asset_id` only when modifying an existing SpriteCook asset.
- Do not generate multiple independent still variations when the real goal is one consistent character plus later animations.
- Prefer `smart_crop_mode="tightest"` unless the user explicitly asks for `"power_of_2"`.

## Consistency Rules

- For a motion set like idle, walk, attack, or hurt: generate the base character once, then animate that exact `asset_id` separately for each motion.
- For asset variations that should stay recognizably the same design, prefer `edit_asset_id` or `reference_asset_id` over a brand-new unreferenced generation.
- Only skip a reference when the user explicitly wants different designs to explore.

## Pixel Art vs Detailed Art

**Pixel art** (`pixel: true`, default):
- Crisp hard edges, no anti-aliasing, visible pixel grid
- Automatic pixel-perfect post-processing for clean grid alignment
- Best for retro games, indie games, and 8-bit/16-bit projects

**Detailed/HD art** (`pixel: false`):
- Smooth gradients, fine detail, anti-aliased edges
- Higher fidelity output without pixel grid constraints
- Best for HD 2D games, concept art, and marketing assets

Choose based on the game's art direction. When the user does not specify, default to pixel art.
