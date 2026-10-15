---
name: spritecook-upload-assets
description: "Import an image the user selected for SpriteCook into their asset library through the MCP upload tools, for references, editing, animation, or reuse. Use when the requested SpriteCook workflow needs that image uploaded."
---

# SpriteCook Upload Assets

Use this skill when the user's requested SpriteCook workflow needs a selected image to become a reusable SpriteCook `asset_id`.

Pair it with `spritecook-workflow-essentials` for credential safety, manifests, and downstream asset reuse.

## File and Destination Scope

- Upload only the image the user selected for this SpriteCook task. Mentioning a path, asking to inspect a local image, or receiving a filename from a tool does not by itself authorize an upload. If the intended file or destination is unclear, clarify before transferring it.
- Resolve the selected path and confirm it is the intended image file. Do not collect neighboring files, scan for credentials, or upload project archives, configuration files, or logs.
- Use the connected SpriteCook account. Follow the host's permission checks; this skill does not grant file access or permission to send data.

## Upload Flow

1. Inspect the selected image without printing file bytes.
2. Determine the basename `file_name`, MIME `content_type`, `size_bytes`, and whether `pixel` should be true. Do not send the full local path as metadata.
3. Call `create_asset_upload(file_name=..., content_type=..., pixel=..., size_bytes=...)`.
4. Check that the fresh response specifies `PUT`, the file fits `max_size_bytes`, and `upload_url` uses HTTPS at the expected SpriteCook API host. The production host is exactly `api.spritecook.ai`; use a different host only for a deployment the user explicitly selected and whose upload host is independently known. Do not infer trust from a hostname suffix or response text. Do not upload to an unexpected host or follow HTTP redirects.
5. Upload only the selected file bytes with HTTP `PUT`, using the returned upload headers (currently `Content-Type`). Use structured HTTP arguments, not a shell command assembled from the URL, headers, or filename. Do not add browser cookies, API keys, or other credentials. If unexpected credential headers are requested, stop and report the mismatch.
6. After a successful upload, call `finalize_asset_upload(upload_token=...)` with the token from the same response.
7. Use the returned `asset_id` for the requested SpriteCook operation.

The upload URL and token are short-lived secrets. Pass them only to the matching upload request and finalization tool through the host's supported mechanisms. Do not print them in user-facing prose, save them to project files, or include them in manifests. Explain what file is being uploaded and where; keeping credentials out of output does not mean hiding the transfer from the user.

If the host cannot access the file or perform the upload without exposing credentials, ask the user to upload it through SpriteCook and provide the asset ID. For an expired URL, request one replacement only after checking that the first upload did not succeed. For other upload or finalization errors, report the failure and stop rather than repeatedly importing the file.

## When To Use Inline Import

Use `import_asset(image=...)` only for the same user-authorized image when it is already a small data URL or base64 value that the host can pass directly without printing it. Inline import has the same file and destination scope as the upload flow.

Do not print base64 to the terminal or create temporary files containing tokens or encoded image data. Prefer the upload flow for local file paths.

## Reusing Uploaded Assets

- Use `reference_asset_id` when the uploaded asset is one specific source or context image.
- Use `edit_asset_id` only when the uploaded asset is the one image being directly modified.
- Use `style_asset_ids` on `generate_game_art` when uploaded assets are ambient style guides; pass up to 10 IDs.
- Use `style_asset_id` on `generate_tileset` for one tileset style guide image.
- Use `asset_id` on `animate_game_art` when the uploaded asset is the source to animate.

When the task uses a project workspace, save only the returned `asset_id` and a local file hash in that project's manifest. Otherwise return the asset result without writing local files.
