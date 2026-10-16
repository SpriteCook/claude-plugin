[![Listed on ClaudePluginHub](https://www.claudepluginhub.com/badge/spritecook-spritecook)](https://www.claudepluginhub.com/plugins/spritecook-spritecook?ref=badge)

# SpriteCook Claude Plugin

Generate sprites, cohesive UI kits, textures, tilesets, and short animations from Claude Code or the Claude desktop app.

SpriteCook gives Claude access to a hosted MCP server for game-art workflows. You can ask Claude to create pixel art, HD game assets, character animation sheets, autotile tilesets, and Godot-ready asset packages while it works inside your project.

## What You Can Do

- Generate pixel-art sprites, items, UI elements, textures, and HD game assets.
- Build complete menus, HUDs, inventories, dialogs, and other cohesive UI systems from one shared concept.
- Create tilesets for top-down, platformer, and isometric projects.
- Animate existing SpriteCook assets into short looping sprite sheets.
- Check generation jobs, credit balance, and recent assets.
- Export generated character animations into Godot-friendly files.

## Install

### Claude Code

Clone this repo, then load the plugin from the checkout:

```bash
git clone https://github.com/SpriteCook/claude-plugin.git
cd claude-plugin
claude --plugin-dir .
```

Then inside Claude Code:

- Run `/reload-plugins` after editing plugin files.
- Run `/plugin validate` to check the manifest and components.
- Start `claude --debug` if you want plugin load details.

### Claude Desktop

Install the plugin locally from inside the app:

```text
/plugin install /path/to/claude-plugin
```

Use the path to your local checkout. Restart the app once, then complete the SpriteCook sign-in flow the first time you call a SpriteCook tool.

### Updates

Claude doesn't auto-update plugins from third-party marketplaces unless you turn it on. If you installed SpriteCook from the marketplace, run `/plugin`, open **Marketplaces**, select **spritecook** and choose **Enable auto-update**. To update right away, run `claude plugin update spritecook@spritecook`, then `/reload-plugins`.

## Try It

Ask Claude:

```text
Use SpriteCook to generate a 64x64 transparent pixel-art slime enemy and save the result in my project.
```

Other useful prompts:

- `Use SpriteCook to list my current image generation models and credit costs.`
- `Use SpriteCook to generate a top-down mossy dungeon floor tileset.`
- `Use SpriteCook to design an inventory-screen concept, extract reusable components, and finalize the UI kit.`
- `Use SpriteCook to list my recent assets and inspect the newest one.`
- `Use SpriteCook to check my credit balance.`
- `Use SpriteCook to package my completed character animation run for Godot.`

## What's Included

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) - plugin manifest
- [`.mcp.json`](.mcp.json) - hosted SpriteCook MCP server configuration
- [`skills/`](skills) - bundled SpriteCook workflow skills:
  - `spritecook-workflow-essentials`
  - `spritecook-build-ui-kits`
  - `spritecook-generate-sprites`
  - `spritecook-polish-sprites`
  - `spritecook-generate-tilesets`
  - `spritecook-animate-assets`
  - `spritecook-upload-assets`
  - `spritecook-use-presets`
  - `spritecook-use-assets-in-godot`
  - `spritecook-use-dual-grid-tilesets`
- [`assets/`](assets) - plugin icon and branding

## Authentication

The plugin connects to the hosted SpriteCook MCP endpoint:

- `https://mcp.spritecook.ai/mcp/claude`

Claude handles authentication through SpriteCook OAuth on first protected use. Do not paste SpriteCook API keys, OAuth tokens, cookies, or other secrets into Claude chat.

## Known Limitations

- Generation and animation tools spend SpriteCook credits.
- Long-running jobs may return a queued or active status before completion; ask Claude to check the job status again.
- Animation tools require an existing SpriteCook `asset_id`. Local images must be uploaded or imported through SpriteCook before animation.
- Signed download URLs expire and can be refreshed by asking Claude to check the asset or job again.

## Privacy and Support

- Privacy policy: https://www.spritecook.ai/privacy
- Plugin and MCP support: kimo@spritecook.ai
- Privacy requests: privacy@spritecook.ai

## License

MIT

## Skill source of truth

Bundled workflow skills come from [SpriteCook/skills](https://github.com/SpriteCook/skills). Update that repository first, then sync its committed skills into `skills/`. [skills-source.json](skills-source.json) records the exact bundled source revision.

Bundled skills now match the current SpriteCook tools on reference limits, size hints, tileset edges and animation engines, and include tested steps for small sprites, scene cutouts, tiny edits and two-surface tilesets. Version checks run when you ask about updates or compatibility. No new plugin environment variables or database migrations are required.
