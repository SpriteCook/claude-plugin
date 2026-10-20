---
name: spritecook-animate-assets
description: "Animation guide for SpriteCook. Use with spritecook-workflow-essentials when importing source images, writing stronger motion prompts, and animating existing assets."
---

# SpriteCook Animate Assets

Use this skill for animation workflows. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and shared defaults.

**Requires:** A connected SpriteCook MCP server. If disconnected, explain that connection is needed and use the host's native connection flow when authorized. Do not install software or change authentication settings as part of an art task.

## Tool

Before animation, inspect the source outline and transparency. Use `spritecook-polish-sprites` to recover edge pixels from a preserved alpha source when useful, then animate the polished asset ID. Inspect completed animations for edge flicker; the polishing workflow can compare one cutoff across all frames of a supported animation.

### `animate_game_art`

Animate an existing SpriteCook asset into a short pixel-art or detailed animation. The tool returns a job immediately; follow its `poll.tool` and `poll.arguments` instead of holding the request open.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_id` | string (required) | - | Existing SpriteCook asset ID to animate |
| `prompt` | string (required) | - | Describe the exact motion over time. If `auto_enhance_prompt=true`, simple prompts like "Idle" or "Attack" are acceptable |
| `auto_enhance_prompt` | bool | true | Inspect the source asset and expand short prompts into a fuller animation prompt |
| `edge_margin` | int | 6 | Spacing added before animation framing. Pixel art stands on the bottom edge as a ground line, so the margin goes on the sides and top |
| `vertical_align` | string | null | Pixel art only. `"center"` for flying, floating or bouncing subjects, so `edge_margin` also leaves room below. Omit to keep the ground line |
| `pixel` | bool | null | Optional mode override. If omitted, SpriteCook infers the mode from the asset |
| `model` | string | mode default | `pixel-engine-v1.1`, `frame-engine-v1.1`, or `pixel-engine-v1.5`. Omit for the v1.1 default |
| `output_frames` | int | 8 | v1.1 uses even counts (pixel 2-16, detailed 2-24); v1.5 accepts 3-16 whole-number frames |
| `output_format` | string | "webp" | "webp", "gif", or "spritesheet" |
| `negative_prompt` | string | null | Optional motion/content exclusions. Not supported by `pixel-engine-v1.5`; do not send it there |
| `matte_color` | string | "#808080" | Hex matte color used before processing transparency |
| `removebg` | string | "Basic" | "None", "Basic", or "Pro". Pro adds a per-frame cost |
| `colors` | int | 24 | Pixel palette size, enforced on the output. Only valid when `pixel=true` |

Animations take about 1-5 minutes. Pass a bounded `wait_seconds` only if the tool's schema lists it; otherwise space `check_job_status` calls accordingly. `animate_game_art` takes no `project_id`; move results with `assign_assets_to_project` when needed.

## Prepare the Starting Frame

The animation model animates the input image. Treat that image as the starting frame: it should already show the pose, state, and facing needed at the start of the requested motion. A motion prompt or `auto_enhance_prompt` does not replace preparing the right source image.

- Inspect the source before animating. Reuse it when its starting pose fits the motion.
- When the requested state needs a different pose, first use `generate_game_art` with `edit_asset_id` to prepare that pose, or `reference_asset_id` to generate it from the established character. Preserve the character's design, palette, proportions, and art style.
- Inspect the prepared still, then pass its returned `asset_id` to `animate_game_art`.

### Example: Sleeping Loop vs. Falling Asleep

The following illustrates how to choose a starting frame for different motions of the same character:

- For a **sleeping loop**, first create a still of the same character lying down or curled up, eyes closed. Then animate gentle breathing while keeping that sleeping pose. Do not use a standing, awake idle sprite as the input for this loop.
- For a **falling-asleep transition**, an awake starting pose can be appropriate because lying down and closing the eyes are part of the requested motion. Choose the source for the beginning of the action, not its final state.

Example: edit the idle bunny into “the same bunny curled up asleep, eyes closed, preserving its design and pixel-art style.” Inspect that still, then animate the new asset with “The sleeping bunny stays curled up with eyes closed, breathing gently in a seamless loop.”

### Example: Continuous Walk Cycle

For a looping walk animation, first edit or reference the idle sprite into a mid-walk pose with the same character design and facing. Inspect that still, then animate its returned asset ID. Starting mid-stride helps keep the first frame part of the walking motion, avoiding an awkward standing idle pose each time the cycle repeats. An idle source can still be appropriate for a separate transition from standing to walking.

Example still prompt: "The same character mid-stride, one leg forward and the other back, arms in a natural walking swing, preserving the original facing, proportions, palette, and pixel-art style." Then animate with "A continuous walk cycle in place, maintaining the same facing and a steady rhythm, looping smoothly through the starting stride without stopping or returning to a standing idle pose." Inspect the loop boundary to check that the motion stays continuous.

## Workflow

1. If the user already has a SpriteCook asset, inspect its starting pose. Use it directly only when that pose fits the requested motion; otherwise prepare the starting frame as described above.
2. If the user only has a local image file path, use `spritecook-upload-assets` to call `create_asset_upload`, upload the bytes, then call `finalize_asset_upload`.
3. If the user supplies a small data URL or raw base64 value, call `import_asset` first and use the returned `asset_id`.
4. Check the uploaded/imported image against the starting-frame guidance too. Prepare a different pose when needed, then use that prepared still's `asset_id` in `animate_game_art`.
5. Keep `pixel` omitted unless you need to force a mode.

The upload/import step is where the source image enters SpriteCook. It is not the animation call itself. Use MCP asset upload tools when they are available.

## Consistency Rules

- Preserve one established character design across motions.
- Reuse the same `asset_id` for motions that share a suitable starting pose. Prepare a referenced or edited still when a motion needs a different starting state, pose, or facing, then animate that still separately.
- Keep the original character asset and record prepared pose asset IDs for reuse; avoid unrelated, unreferenced character generations.

## Source Rules

- Pixel animation is the correct choice for small sources: v1.1 pixel animation accepts assets up to `256x256`; v1.5 pixel animation accepts assets up to `320x320`.
- Detailed animation is the correct choice for assets between `256x256` and `2048x2048`.
- Do not force a sub-256 source into detailed mode.
- Source aspect ratio must be between 1:2 and 2:1.
- Keep `edge_margin=6` by default. It helps prevent pixel art from crowding the canvas edge. It is a percentage, so very small sprites gain only a pixel or two; raise it for motions that reach outward, such as a lid opening or a wide swing. For a subject that leaves the ground, such as a flying bat or a bouncing slime, pass `vertical_align="center"` and raise `edge_margin` for big stretches or jumps.

## Choosing an Engine

- `pixel-engine-v1.1` (default) suits loops, walk cycles, and idles.
- `pixel-engine-v1.5` suits precise or unusual motion and isolated subjects. It also tends to give calmer, more faithful motion on a single transparent character or prop.
- Results vary per subject. When quality matters, try both engines on the same still and keep the better one.
- Guided character runs (`generate_character_animations`) use v1.1 only. For v1.5, animate each motion with `animate_game_art` on the same still.

## Output Canvas

- The output frame is usually square and padded. A non-square source is centered in a square frame (a 180x320 source returns 320x320 frames), and small sprites can be rescaled slightly. The response does not report the offset.
- To put an animation back in a scene or line it up with its still, match frame 0 against the source locally to find the offset, and check the scale.
- Frame sizes differ between jobs. For a set that must share one ground line, compute a shared frame box locally and re-place every frame.
- Frame counts can occasionally differ by one from `output_frames`; read `frame_count` from the result metadata before assuming a loop length.
- With `output_format="spritesheet"`, `sprite_url` is still the animated WebP; the PNG strip is `spritesheet_url`.

## Quality Checks

- Clean the still before animating: stray pixels on outlines, background trapped between parts, and noise get redrawn into every frame. Use `spritecook-polish-sprites` first.
- Below about 32 px, outlines can soften and small features such as eyes can drift between frames. Keep faces simple at that size and inspect every frame.
- Idles can flicker: isolated pixels change for one frame and change back. A calm prompt with `auto_enhance_prompt=false` reduces overall motion. Fix the remaining one-frame flips locally by restoring a pixel when the frames before and after it agree.
- Say what must stay still ("feet stay planted", "the face does not change") and check that it held; the engine does not always respect it.
- Check for grey or off-color specks near glows and at the feet, and for loops that don't close (compare the last frame with the first).

## Animating Part of a Scene

Animating a full scene redraws the whole frame: static areas such as sky and stone shift between frames and the loop rarely closes. Animate the moving part on its own instead:

1. Edit the scene with `generate_game_art(edit_asset_id=<scene>, prompt="Remove the X ...")` to get a clean background plate.
2. Cut X out locally as the difference between the original and the plate, upload it, and animate that asset alone.
3. Composite the frames back onto the plate at the matched offset.

For effects that belong to the background, such as a waterfall, animate a crop of the plate with `removebg="None"` and `edge_margin=0`, then blend the moving region back with a motion mask.

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

Use the `job_id` from `animate_game_art` with `check_job_status`. On success, use `asset_id` plus the canonical `sprite_url`; use `spritesheet_url` only when present. If the response reports `warning.code="asset_output_unavailable"`, execute the supplied `warning.recovery` tool call.
