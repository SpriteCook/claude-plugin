---
name: spritecook-use-assets-in-godot
description: "Godot workflow for SpriteCook assets. Use when the user wants to turn SpriteCook spritesheet PNGs, animation assets, or character animation runs into Godot SpriteFrames resources and AnimatedSprite2D/AnimatedSprite3D animation nodes. Covers both manual spritesheet-to-Godot setup and the optional SpriteCook MCP Godot export endpoint."
---

# SpriteCook Use Assets In Godot

Use this skill when moving existing SpriteCook assets into Godot. Pair it with `spritecook-workflow-essentials` for safe downloads and asset manifests. Pair it with `spritecook-animate-assets` only when animations still need to be generated first.

Prefer the manual path first: most agents can create the Godot animation resource directly from SpriteCook spritesheets, which gives more freedom and avoids extra MCP server work. Use the MCP export endpoint second when the user wants SpriteCook to return a packaged set of files.

## Choose A Path

1. **Manual Godot setup, preferred:** Use SpriteCook animation spritesheets plus metadata to create a Godot `SpriteFrames` resource and an `AnimatedSprite2D` node yourself.
2. **MCP packaged export:** Call `export_godot_character_package` to get prebuilt text files and asset downloads, then materialize the returned manifest.

## Manual AnimatedSprite2D Setup

Use this path when the agent has downloaded SpriteCook animation outputs, has explicit animation asset IDs, or can access spritesheet URLs and frame metadata. The goal is only to make the spritesheets usable as a Godot animation component, not to build gameplay, controllers, playground scenes, or complete demo levels unless the user explicitly asks for those.

Required per animation:

- PNG spritesheet URL or local file.
- Animation name such as `idle`, `walk`, `attack`, `jump`, `fall`, `hurt`, or `death`.
- Frame width, frame height, frame count, and fps.
- Loop behavior. Loop locomotion/idles; usually do not loop `attack`, `hurt`, or `death`.

Important: use the output spritesheet frame size, not the original source asset size. Detailed animations may return larger frames because SpriteCook adds margin, for example a 512x512 source can produce 640x640 frames.

### File Layout

For a new package inside an existing Godot project, use a contained folder and avoid overwriting the user's existing scenes:

```text
SpriteCook/
  assets/
    player_idle.png
    player_walk.png
    player_attack.png
    player_frames.tres
```

If the user already has a scene, add or update only the `AnimatedSprite2D` node and its `sprite_frames` reference.

### Create SpriteFrames

Create a `.tres` `SpriteFrames` resource that references each spritesheet as a `Texture2D` ext_resource and creates one `AtlasTexture` sub_resource per frame.

For each frame `i`, use:

```gdresource
region = Rect2(i * frame_width, 0, frame_width, frame_height)
```

The resource shape is:

```gdresource
[gd_resource type="SpriteFrames" load_steps=<resource_count> format=3]

[ext_resource type="Texture2D" path="res://SpriteCook/assets/player_idle.png" id="idle_sheet"]

[sub_resource type="AtlasTexture" id="AtlasTexture_idle_0"]
atlas = ExtResource("idle_sheet")
region = Rect2(0, 0, 64, 64)

[resource]
animations = [{
"frames": [{"duration": 1.0, "texture": SubResource("AtlasTexture_idle_0")}],
"loop": true,
"name": &"idle",
"speed": 8.0
}]
```

Generate all frames, not only frame 0. If there are multiple animations, append each animation object to the `animations` array. Set `speed` to the SpriteCook `animation_fps`.

### Add AnimatedSprite2D

Add an `AnimatedSprite2D` node to the target scene, or create a minimal scene containing only the animation node when no target scene exists:

```gdscene
[gd_scene load_steps=2 format=3]

[ext_resource type="SpriteFrames" path="res://SpriteCook/assets/player_frames.tres" id="frames"]

[node name="AnimatedSprite2D" type="AnimatedSprite2D"]
sprite_frames = ExtResource("frames")
animation = &"idle"
autoplay = "idle"
```

If the user's scene already has a character/player node, attach the `AnimatedSprite2D` as a child and leave gameplay logic alone.

### Manual Verification

- Confirm every spritesheet path in `.tres` exists under `res://`.
- Confirm `frame_count * frame_width == spritesheet_width` for horizontal sheets.
- Confirm the target scene contains an `AnimatedSprite2D` and references the SpriteFrames resource.
- Open the project in Godot 4.x and check for missing ext_resource warnings.
- Preview the `AnimatedSprite2D` animations in Godot and verify frame slicing/playback.

## MCP Packaged Export

Use this path when the user wants SpriteCook to return a complete package manifest, or when a completed character animation `run_id` is available and state inference from presets is useful. Even when using the endpoint, focus on the returned SpriteFrames/AnimatedSprite setup unless the user asks for demo scenes.

Call `export_godot_character_package`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `run_id` | string | null | Completed character animation run ID. Prefer this when available because SpriteCook can infer animation states from presets |
| `animation_asset_ids` | string[] | null | Explicit animation asset IDs when no run ID is available |
| `character_name` | string | null | Optional name used in export metadata |
| `state_hints_by_asset_id` | object | null | Optional mapping from asset ID to animation state |

Valid state hints include `Idle`, `Walk`, `Run`, `Jump`, `Fall`, `IdleDown`, `IdleUp`, `IdleRight`, `WalkDown`, `WalkUp`, `WalkRight`, `RunDown`, `RunUp`, `RunRight`, `Attack`, `Hurt`, and `Death`.

The tool returns:

- `text_files`: write each `{ path, content }` exactly.
- `asset_downloads`: download each signed `url` to its `path`.
- `main_scene`: scene to open or run after Godot imports resources.
- `package_kind`: `character` for a playable setup, or `animation_preview` for a single animation.

Do not assume the MCP server wrote files locally. The agent must create the returned files in the user's Godot project.

Example arguments:

```json
{
  "animation_asset_ids": ["idle-id", "walk-id", "attack-id"],
  "character_name": "Player",
  "state_hints_by_asset_id": {
    "idle-id": "Idle",
    "walk-id": "Walk",
    "attack-id": "Attack"
  }
}
```

After materializing the package, use the same verification checklist as the manual path.
