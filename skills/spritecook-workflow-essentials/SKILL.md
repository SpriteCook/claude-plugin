---
name: spritecook-workflow-essentials
description: "Shared workflow rules for SpriteCook. Use together with spritecook-generate-sprites or spritecook-animate-assets for credits, downloads, asset manifests, safe auth handling, and recommended defaults."
---

# SpriteCook Workflow Essentials

Use this alongside the SpriteCook image or animation skill whenever SpriteCook MCP tools are available.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Preflight Checklist

1. Check credits first with `get_credit_balance` before starting a batch or multi-asset workflow.
2. Prefer presigned download URLs over authenticated asset endpoints.
3. Save important `asset_id` values in a local manifest whenever there is a writable workspace, unless the user explicitly wants a throwaway result.
4. When a workflow involves follow-up generations or animations for the same subject, identify and reuse the canonical `asset_id` instead of generating from scratch again.

## Credential Safety

- Never ask the user to paste a SpriteCook API key into chat, prompts, code blocks, shell commands, or generated files.
- Never print, persist, echo, or inline API keys or `Authorization` headers in agent output.
- Prefer SpriteCook MCP tools, presigned URLs, or a preconfigured local connector/helper that handles authentication outside the prompt.
- If a raw API call is required and no authenticated helper exists, stop and ask the user to configure one.

## Defaults

- Prefer `smart_crop_mode="tightest"` for the best default results. Use `"power_of_2"` only when the user explicitly asks for it.
- Model guidance:
  - `gemini-2.5-flash-image`: cheapest
  - `gemini-3.1-flash-image-preview`: recommended default
  - `gemini-3-pro-image-preview`: most expensive

## Asset Manifest

- Treat `asset_id` as the primary stable identifier.
- Store a 12-character SHA-256 prefix (`sha12`) for saved local files.
- Use a minimal manifest entry shape:
  - `asset_id`
  - `sha12`
  - optional `label`
- Prefer a simple machine-readable file such as `spritecook-assets.json` unless the project already has an asset manifest.
- Before generating a new reference asset or asking the user for an asset id, check the local manifest first.
- Before reusing a local file, compute its `sha12` and match it against the manifest to recover the correct `asset_id`.

## Downloading Assets

- Prefer `_presigned_pixel_url` when saving the pixel PNG.
- Prefer `_presigned_url` when saving the raw/original image.
- Avoid direct authenticated download endpoints in skill-driven workflows unless a helper handles auth out of band.
