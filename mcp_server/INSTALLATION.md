# MCP Server Installation Guide

Quick guide to get the Legal Evolution MCP Server running.

## Step 1: Install Dependencies

```bash
pip install mcp anthropic-mcp-sdk
```

## Step 2: Install Repository

```bash
cd /home/user/webapp/legal-evolution-unified
pip install -e .
```

## Step 3: Configure Claude Desktop

### Mac/Linux

Edit `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "legal-evolution-unified": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.core.server"
      ],
      "cwd": "/path/to/legal-evolution-unified",
      "env": {
        "PYTHONPATH": "/path/to/legal-evolution-unified"
      }
    }
  }
}
```

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json` with the same content.

## Step 4: Restart Claude Desktop

Close and reopen Claude Desktop completely.

## Step 5: Verify Installation

In Claude, check MCP tools menu. You should see 13 tools from "legal-evolution-unified".

## Step 6: Test

Try a simple tool:

```
Use the calculate_cli_score tool with these components:
- text_vagueness: 0.75
- judicial_activism: 0.95
- treaty_hierarchy: 0.88
- precedent_weight: 0.85
- amendment_difficulty: 0.70

What's the result?
```

Expected: CLI ≈ 0.842, classification "Lock-in"

## Troubleshooting

### Server not appearing

1. Check config file location
2. Verify paths in config
3. Check Claude logs: `~/.config/Claude/logs/`

### Import errors

```bash
export PYTHONPATH="/path/to/legal-evolution-unified:$PYTHONPATH"
python -m mcp_server.core.server
```

Should start without errors.

## Advanced: Custom Configuration

Create `mcp_config.json`:

```json
{
  "name": "legal-evolution-unified",
  "version": "1.0.0",
  "cache_enabled": true,
  "cache_ttl": 3600,
  "logging_level": "INFO",
  "tools_enabled": [
    "cli_calculator",
    "jurisrank",
    "egt_framework",
    "workflows"
  ]
}
```

Run with:

```bash
python -m mcp_server.core.server --config mcp_config.json
```

## Done! 🎉

Your MCP server is ready. See [README.md](README.md) for usage examples.
