---
name: spritecook-animate-assets
description: "Animation guide for SpriteCook. Use with spritecook-workflow-essentials when importing source images, writing stronger motion prompts, and animating existing assets."
---

# SpriteCook Animate Assets

Use this skill for animation workflows. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and shared defaults.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Tool

### `animate_game_art`

Animate an existing SpriteCook asset into a short pixel-art or detailed animation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_id` | string (required) | - | Existing SpriteCook asset ID to animate |
| `prompt` | string (required) | - | Describe the exact motion over time. If `auto_enhance_prompt=true`, simple prompts like "Idle" or "Attack" are acceptable |
| `auto_enhance_prompt` | bool | true | Inspect the source asset and expand short prompts into a fuller animation prompt |
| `edge_margin` | int | 6 | Adds spacing on all sides before animation framing |
| `pixel` | bool | null | Optional mode override. If omitted, SpriteCook infers the mode from the asset |
| `output_frames` | int | 8 | Even frame count. Pixel supports 2-16, detailed supports 2-24 |
| `output_format` | string | "webp" | "webp", "gif", or "spritesheet" |
| `negative_prompt` | string | null | Optional motion/content exclusions |
| `matte_color` | string | "#808080" | Hex matte color used before processing transparency |
| `removebg` | string | "Basic" | "None", "Basic", or "Pro" |
| `colors` | int | 24 | Pixel palette size. Only valid when `pixel=true` |

## Workflow

1. If the user already has a SpriteCook asset, pass its `asset_id` directly to `animate_game_art`.
2. If the user only has a local image file or data URL, import it through an authenticated helper that returns an `asset_id`.
3. Use the returned `asset_id` in `animate_game_art`.
4. Keep `pixel` omitted unless you need to force a mode.

The import step is where the source image enters SpriteCook. It is not the animation call itself.

## Consistency Rules

- Always animate the exact source asset that represents the intended character or object.
- If the user asks for multiple motions for one character, run separate animation jobs against the same `asset_id` for `Idle`, `Walk`, `Attack`, and so on.
- Do not create a new still image for each motion unless the user explicitly wants different character designs.

## Source Rules

- Pixel animation is the correct choice for assets up to `256x256`.
- Detailed animation is the correct choice for assets between `256x256` and `2048x2048`.
- Do not force a sub-256 source into detailed mode.
- Keep `edge_margin=6` by default. It helps prevent pixel art from crowding the canvas edge.

## Prompt Writing

- Inspect the actual source character before writing the prompt.
- For pixel art, upscale the source with nearest-neighbor to about `1024x1024` for inspection only.
- Identify visible character details first: silhouette, armor, visor, weapon, shield, pose, and facing.
- Only mention details that are actually visible in the source image.
- Write one short paragraph in plain prose, not a label or keyword list.
- Describe what moves, how it moves, what stays stable, and how visible props or weapons are used.
- Keep the motion grounded in the existing character rather than inventing new equipment or effects.
- Avoid generic prompts like `idle animation` unless `auto_enhance_prompt=true`.

Example idle prompt:
`The armored soldier in purple tactical gear stands in a steady combat stance, subtly bobbing up and down in a rhythmic breathing idle. His yellow visor catches the light while his rifle shifts slightly in his grip, maintaining a high state of readiness.`

Example attack prompt:
`The armored soldier in purple tactical gear raises his rifle and fires several shots, with yellow muzzle flashes appearing at the tip of the barrel. His body recoils with each shot while his head and visor remain focused forward, maintaining a steady combat stance throughout the firing sequence.`

If `auto_enhance_prompt=true`, simple prompts like `Idle`, `Attack`, or `Walk` are valid because SpriteCook can inspect the source asset and expand them automatically.

### `check_job_status`

Use `check_job_status(job_id=...)` for long-running animations instead of blocking when the client can continue work in the background.
