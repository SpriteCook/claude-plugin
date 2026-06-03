---
name: spritecook-generate-tilesets
description: "Tileset generation guide for SpriteCook. Use with spritecook-workflow-essentials when generating autotile tilesets through SpriteCook MCP/API, choosing tile sizes, using reference/edit/style asset IDs, and saving generated tileset asset IDs."
---

# SpriteCook Generate Tilesets

Use this skill for SpriteCook tileset generation. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and asset tracking.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Tools

### `list_tileset_options`

Call this when you need current supported perspectives, piece sets, tile sizes, elevations, edge modes, output dimensions, or defaults.

### `generate_tileset`

Generate a game-ready tileset. The tool waits up to 90 seconds and returns a job response with generated asset IDs and download URLs when complete.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Terrain/material request, e.g. `mossy dungeon floor` |
| `style_mode` | string | `pixel` | `pixel` or `detailed` |
| `perspective` | string | `topdown` | `topdown` or `platformer` |
| `piece_set` | string | registry default | `15-piece`, `17-piece-base`, or `autotile-16-set` |
| `tile_size` | int | registry default | Final tile size in pixels |
| `elevation` | string | registry default | `no-elevation` or `minimal` where supported |
| `edges` | string | `transparent` | `transparent` or `two_surfaces`; `two_surfaces` only works for 15-piece top-down |
| `variations` | int | `1` | Number of variations, 1-4 |
| `model` | string | null | Optional model override. Omit to use SpriteCook's tileset default |
| `colors` | string[] | null | Optional hex color guidance, max 8 |
| `force_enabled` | bool | `false` | Force the output toward `force_colors` |
| `force_colors` | string[] | null | Optional forced hex palette, max 8 |
| `reference_asset_id` | string | null | Existing tileset asset to use as source/reference; tileset settings are inherited |
| `edit_asset_id` | string | null | Existing tileset asset to edit; tileset settings are inherited |
| `style_asset_id` | string | null | Existing asset to use as visual style guide only |

`reference_asset_id` and `edit_asset_id` are mutually exclusive. The referenced asset must belong to the SpriteCook account.

## Recommended Defaults

- For top-down pixel autotiles, start with `style_mode="pixel"`, `perspective="topdown"`, `piece_set="15-piece"`, `tile_size=32`, `edges="transparent"`.
- For top-down inner-corner base tiles, use `piece_set="17-piece-base"` and keep `edges="transparent"`.
- For side-view platformers, use `perspective="platformer"`, `piece_set="autotile-16-set"`, `edges="transparent"`.
- For detailed top-down tilesets, use `style_mode="detailed"` and call `list_tileset_options` before choosing size/elevation.
- Use `model` only when the user explicitly wants to compare models.

## Reference Workflow

- If the user has a local image, first import it with the HTTP API endpoint `POST /v1/api/assets/import`, then pass the returned asset ID.
- Use `reference_asset_id` when the existing tileset should guide a new generation while preserving its tile size/layout.
- Use `edit_asset_id` when the user wants a direct change to an existing tileset.
- Use `style_asset_id` when the image should affect only visual style, not tileset layout.
- When referencing or editing a tileset, do not change `style_mode`, `perspective`, `piece_set`, `tile_size`, or `elevation`; SpriteCook inherits and locks those settings.

## Prompting

- Keep prompts short and material-focused: `snowy stone path`, `muddy swamp grass`, `volcanic rock`, `clean wooden floor`.
- For single-surface tilesets, name one main material.
- For `two_surfaces`, name both surfaces clearly: `grass and water`, `volcanic rock and lava`.
- Avoid asking for labels, UI, characters, props, or scene composition inside the tileset.

## Output Handling

- Save the returned `asset_id` in the project manifest or task notes.
- Use the returned `pixel_url` for pixel-art tilesets when available.
- Use the returned `raw_url` when the user asks for the original generated asset variant.
