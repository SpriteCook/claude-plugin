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
| `model` | string | null | "gemini-2.5-flash-image" (cheapest), "gemini-3.1-flash-image-preview" (recommended default), or "gemini-3-pro-image-preview" (most expensive) |
| `mode` | string | "assets" | "assets", "texture", or "ui" |
| `resolution` | string | "1K" | "1K", "2K", or "4K" |
| `colors` | string[] | null | Hex color palette, max 8 |
| `reference_asset_id` | string | null | Asset ID from a previous generation to use as style reference |
| `edit_asset_id` | string | null | Asset ID to edit/modify with the new prompt |

`reference_asset_id` and `edit_asset_id` are mutually exclusive. The referenced asset must belong to your account.

## Working Style

- Be specific about subject, pose, camera/view angle, and key materials.
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
