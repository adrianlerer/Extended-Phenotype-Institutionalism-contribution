#!/bin/bash
# Legal Evolution MCP Server - Installation Script
# Auto-configures Claude Desktop to use this MCP server

set -e

echo "================================================"
echo "Legal Evolution MCP Server - Installation"
echo "================================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
    OS="Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
    OS="Windows"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Detected OS: $OS"
echo "Config path: $CONFIG_PATH"
echo ""

# Get absolute path to server.py
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_PATH="$SCRIPT_DIR/server.py"

echo "Server path: $SERVER_PATH"
echo ""

# Check if server.py exists
if [ ! -f "$SERVER_PATH" ]; then
    echo "❌ Error: server.py not found at $SERVER_PATH"
    exit 1
fi

echo "✓ Server file found"

# Check if Python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python not found. Please install Python 3.11+"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
echo "✓ Python found: $PYTHON_CMD"

# Check if MCP is installed
if ! $PYTHON_CMD -c "import mcp" &> /dev/null; then
    echo "⚠️  MCP SDK not installed"
    echo "Installing MCP SDK..."
    $PYTHON_CMD -m pip install mcp --quiet
    echo "✓ MCP SDK installed"
else
    echo "✓ MCP SDK already installed"
fi

# Test that server imports work
echo ""
echo "Testing server imports..."
if ! $PYTHON_CMD -c "import sys; sys.path.insert(0, '$SCRIPT_DIR/..'); from mcp_server.server import server; print('OK')" &> /dev/null; then
    echo "❌ Error: Server imports failed"
    echo "   Make sure you're in the legal-evolution-unified directory"
    exit 1
fi
echo "✓ Server imports OK"

# Create config directory if it doesn't exist
CONFIG_DIR=$(dirname "$CONFIG_PATH")
if [ ! -d "$CONFIG_DIR" ]; then
    echo ""
    echo "Creating config directory: $CONFIG_DIR"
    mkdir -p "$CONFIG_DIR"
fi

# Backup existing config
if [ -f "$CONFIG_PATH" ]; then
    echo ""
    echo "Backing up existing config..."
    cp "$CONFIG_PATH" "$CONFIG_PATH.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✓ Backup created"
fi

# Read existing config or create new
if [ -f "$CONFIG_PATH" ]; then
    echo ""
    echo "Reading existing config..."
    EXISTING_CONFIG=$(cat "$CONFIG_PATH")
else
    echo ""
    echo "Creating new config..."
    EXISTING_CONFIG="{}"
fi

# Check if legal-evolution server already exists
if echo "$EXISTING_CONFIG" | grep -q "legal-evolution"; then
    echo ""
    echo "⚠️  legal-evolution server already configured"
    echo ""
    read -p "Overwrite? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 0
    fi
fi

# Generate new config
echo ""
echo "Generating config..."

# Use Python to properly merge JSON
$PYTHON_CMD << EOF
import json
import sys

try:
    config = json.loads('''$EXISTING_CONFIG''')
except:
    config = {}

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['legal-evolution'] = {
    'command': '$PYTHON_CMD',
    'args': ['$SERVER_PATH']
}

with open('$CONFIG_PATH', 'w') as f:
    json.dump(config, f, indent=2)

print('✓ Config updated')
EOF

echo ""
echo "================================================"
echo "✅ Installation Complete!"
echo "================================================"
echo ""
echo "Configuration saved to:"
echo "  $CONFIG_PATH"
echo ""
echo "MCP Server: legal-evolution"
echo "Command: $PYTHON_CMD"
echo "Args: $SERVER_PATH"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Desktop (completely quit and reopen)"
echo "  2. Look for the 🔌 icon indicating MCP server is connected"
echo "  3. Try: 'Analyze Argentina's institutional configuration'"
echo ""
echo "Tools available:"
echo "  - calculate_cli"
echo "  - analyze_jurisdiction"
echo "  - compare_jurisdictions_batch"
echo "  - calculate_hv_ratio"
echo ""
echo "For troubleshooting, see: mcp_server/README.md"
echo ""
