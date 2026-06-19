---
name: spritecook-upload-assets
description: "Upload local image files into SpriteCook through MCP without API keys or base64 logs. Use when the user provides a local file path that should become a SpriteCook asset for generation references, style guides, tilesets, animation, background removal, presets, or asset organization."
---

# SpriteCook Upload Assets

Use this skill when a local image file should become a reusable SpriteCook `asset_id`.

Pair it with `spritecook-workflow-essentials` for credential safety, manifests, and downstream asset reuse.

## Preferred Flow

1. Inspect the local file path without printing file bytes.
2. Determine `file_name`, MIME `content_type`, optional `size_bytes`, and whether `pixel` should be true.
3. Call `create_asset_upload(file_name=..., content_type=..., pixel=..., size_bytes=...)`.
4. Upload the file bytes to the returned `upload_url` with HTTP `PUT` and the returned headers.
5. Call `finalize_asset_upload(upload_token=...)`.
6. Use the returned `asset_id` in the next SpriteCook tool.

The upload URL and token are short-lived secrets. Do not print them in user-facing prose, save them to project files, or include them in manifests.

## PowerShell Pattern

On Windows, upload without printing bytes:

```powershell
Invoke-WebRequest -Method Put -Uri $uploadUrl -InFile $path -ContentType $contentType | Out-Null
```

Use variables for `$uploadUrl`, `$path`, and `$contentType`; do not echo them if they include the upload token.

## When To Use Inline Import

Use `import_asset(image=...)` only when the image is already a small data URL or base64 value that can be passed directly without logging it.

Do not use shell commands that print base64 to the terminal. If encoding is necessary, store the value in memory or a private variable and pass it directly to the MCP tool.

## Reusing Uploaded Assets

- Use `reference_asset_id` when the uploaded asset is one specific source or context image.
- Use `edit_asset_id` only when the uploaded asset is the one image being directly modified.
- Use `style_asset_ids` on `generate_game_art` when uploaded assets are ambient style guides; pass up to 10 IDs.
- Use `style_asset_id` on `generate_tileset` for one tileset style guide image.
- Use `asset_id` on `animate_game_art` when the uploaded asset is the source to animate.

Save the returned `asset_id` and a local file hash in the project manifest when the workspace is writable.
