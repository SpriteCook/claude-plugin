---
name: spritecook-build-ui-kits
description: "Concept-first UI system and kit-building guide for SpriteCook. Use with spritecook-workflow-essentials when creating a complete game UI screen, menu, HUD, dialog, inventory, settings screen, overlay, or cohesive UI system; generating or selecting a concept before extracting reusable components; continuing from an existing SpriteCook concept asset ID; or producing named controls, states, and 9-slice metadata through SpriteCook UI-kit MCP tools. Prefer this over generate_game_art mode='ui' for complete screens or systems."
---

# SpriteCook Build UI Kits

Use this skill for complete screens and cohesive UI systems. Pair it with `spritecook-workflow-essentials` for credits, manifests, safe downloads, and shared defaults.

**Requires:** SpriteCook MCP server connected to your editor. Set up with `npx spritecook-mcp setup` or see [spritecook.ai](https://spritecook.ai).

## Choose the Right Workflow

- Use the UI-kit workflow for menus, HUDs, inventories, dialogs, settings, overlays, shops, character screens, and other compositions whose parts must share one visual language.
- Use `generate_game_art(mode="ui")` only for one isolated icon, badge, button, control, divider, frame, or decoration.
- For a new screen, always establish one coherent concept first, then extract production components from that concept. Do not generate unrelated controls independently and try to assemble a visual system afterward.

## Default Workflow

1. Confirm the UI-kit tools are present, then call `get_credit_balance` before starting the multi-image workflow. If the tools are missing, refresh or reconnect the SpriteCook MCP integration; do not fall back to independently generating a full screen with `mode="ui"`.
2. Create the kit with `create_ui_kit` and preserve its `id`. Keep the default `model="gpt-image-2"` unless the user specifically requests Gemini and their account supports 2K Gemini generation.
3. Establish the concept:
   - If the user or agent already has a suitable owned SpriteCook asset ID, pass it as `concept_asset_id`. This selects it immediately and skips concept generation.
   - If the concept is a local file, use `spritecook-upload-assets` first, then pass the returned ID as `concept_asset_id`.
   - Otherwise call `generate_ui_kit_concepts`, follow progress with `get_ui_kit`, inspect the returned concept assets, and call `select_ui_kit_concept` with the strongest option.
4. Call `generate_ui_kit_component_sheets`. Omit `sheet_count` to let SpriteCook plan one to three sheets from the concept.
5. Follow progress with `get_ui_kit` until `status` is `sheet_review` and component-sheet assets are present.
6. Call `extract_ui_kit_components` without `sheet_asset_ids` to process every sheet from the selected or latest successful attempt.
7. Inspect `quality_summary` and the returned component draft programmatically. Confirm names are distinct, each rectangle represents one useful element, state families are sensible, and scalable components are marked correctly. If `requires_review` is true, resolve every relevant warning before finalizing.
8. Call `finalize_ui_kit` with no `components` argument only when the saved draft is sensible and `quality_summary.requires_review` is false. Otherwise supply a corrected component list with fixed names, groups, states, rectangles, scalability, or 9-slice borders.
9. Preserve the UI-kit ID, finalized component asset IDs, and manifest in the project asset manifest.

Continue through extraction and finalization by default. The returned `review_url` is an optional quality-control surface, not a required handoff. Use it when detection is ambiguous, the user asks to inspect the work, or scalable borders need visual tuning.

## Creating the Kit

Give `create_ui_kit` the screen intent, platform, aspect ratio, game description, visual direction, and screen-specific instructions. Use `style_asset_ids` only for owned images that define the broader art direction.

For UI kits, use `gpt-image-2` by default. The accepted canonical alternatives are `gemini-3.1-flash-image` and `gemini-3-pro-image`, but UI-kit concepts are 2K and those Gemini models require a plan that independently allows 2K generation. If the server returns `ui_kit_model_resolution_limit`, retry by creating or updating the kit with `model="gpt-image-2"`; no generation credits were spent on that validation error. Do not use legacy `-preview` model IDs.

Use `state_mode="visible-only"` when the user needs only what appears in the concept. Use `state_mode="complete-states"` for production control families that should include normal, hover/focus, pressed, disabled, checked, or selected variants.

Set the state mode when creating the kit. Omit `state_mode` from `generate_ui_kit_component_sheets` to preserve that stored choice; pass it there only when intentionally overriding the kit for this sheet attempt.

An existing `concept_asset_id` is the specific screen concept being decomposed. It is different from `style_asset_ids`, which provide ambient visual guidance.

## Refining Results

- Regenerate concepts with `revision_notes` to explore a fresh batch.
- Refine one concept with `edit_source_asset_id` and `edit_notes`.
- Use `focus_notes` when only a subset such as buttons, inventory slots, or HUD meters is needed. A focused request uses one sheet.
- Use `supplemental_notes` for missing pieces without replacing accepted sheets.
- Refine one component sheet with `edit_source_asset_id` and `edit_notes`.
- Request `high_resolution=true` only when the user's plan supports 4K and larger source components materially help.

Paid concept and sheet tools return job IDs immediately. Do not treat submission as completion; call `get_ui_kit` until the workflow reaches the expected review status.

## Extraction and 9-Slice Rules

`extract_ui_kit_components` defaults to connected-alpha threshold `1`, minimum area `24`, merge distance `1`, and padding `0`. Keep these defaults unless the sheet visibly fragments or merges components incorrectly.

Always audit the returned `quality_summary` before finalization:

- A sheet with `at_component_limit=true` reached the 100-detection ceiling. Check whether small components were omitted or merged.
- Inspect `possible_merged` and split an obvious multi-object rectangle into separate corrected rectangles, or omit it when its contents already exist separately.
- Fix duplicate or vague names and correct controls misclassified as panels or decorations.
- Give obvious interaction families one stable `group` and distinct `state` values such as normal, hover, pressed, disabled, on/off, selected/unselected, or checked/unchecked.
- Treat fallback classification as a reason to review all names and types.
- Keep at most 100 finalized components per source sheet, at most three sheets, and at most 300 components total. If splitting a merged rectangle would exceed 100 on a sheet, remove low-value duplicates or combine corrections before finalizing.

Automatic extraction initializes all 9-slice borders to zero. Zero is correct for fixed-size icons and decorations. For scalable panels, buttons, inputs, tooltips, tracks, and frames, set non-zero `left`, `top`, `right`, and `bottom` borders only when the protected edges can be identified confidently. Use the optional browser review for precise visual placement.

Finalization returns reusable private component assets plus a manifest containing type, state group, state, dimensions, scalability, and 9-slice metadata. Unity, Godot, and web archive downloads remain available from the browser review page; MCP supplies the assets and manifest directly.

## Recovery

- Use `list_ui_kits` if the kit ID is lost, then continue with `get_ui_kit`.
- Use `cancel_ui_kit` to stop active concept or component-sheet jobs for the kit.
- Keep the returned `review_url`; it opens the same durable kit in SpriteCook without making review mandatory.
- Surface brief, user-friendly errors. Preserve successful concepts or sheets after partial failures and continue from them when possible.
