# SpriteCook Claude Plugin

SpriteCook brings game art generation into Claude Code and the Claude desktop app with a hosted MCP server and bundled skills for sprite generation, animation workflows, and asset handling.

## What's included

- [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) — plugin manifest
- [`.mcp.json`](.mcp.json) — SpriteCook hosted MCP server
- [`skills/`](skills) — bundled SpriteCook workflow skills:
  - `spritecook-workflow-essentials`
  - `spritecook-generate-sprites`
  - `spritecook-animate-assets`
- [`assets/`](assets) — plugin icons and branding

## Local testing

The same plugin works for both Claude Code (CLI) and the Claude desktop app.

### Claude Code (CLI)

Load the plugin directly from this folder:

```bash
claude --plugin-dir "/path/to/claude-plugin"
```

Then inside the session:

- Run `/reload-plugins` after editing any plugin file.
- Run `/plugin validate` to check the manifest and components.
- Start `claude --debug` if you want to see plugin load details.

The SpriteCook MCP tools and the three `spritecook-*` skills should appear once the plugin loads.

### Claude desktop app

Install the plugin locally from inside the app:

```
/plugin install ./
```

Run that command with this folder as the working directory, or pass the absolute path. Restart the app once, then complete the SpriteCook OAuth flow the first time you call a SpriteCook tool.

## Authentication

The plugin points Claude at the hosted SpriteCook MCP endpoint:

- `https://api.spritecook.ai/mcp/claude`

Claude handles authentication through the SpriteCook OAuth flow on first protected use.

## Skill source of truth

Skills are maintained separately in:

- `/path/to/spritecook-skills`

When those skills change, sync the updated `SKILL.md` files into [`skills/`](skills) and bump the version in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) so Claude refreshes its installed cache.

## License

MIT
