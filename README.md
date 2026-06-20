# Vibe Design Guide MCP Server

This Model Context Protocol (MCP) server exposes **The Vibe Coder's Web Design Guide** directly as tools for AI agents. With this server connected, your AI assistant (e.g. Claude Desktop, Cursor, windsurf, or custom agents) can look up UI design patterns, CSS/JS code snippets, design theories, and compose optimized front-end prompts matching the guide's formula.

---

## Exposed Tools

1. `list_design_elements`: Lists all design aesthetics, layouts, animations, navigation patterns, typography, and components available in the guide.
2. `get_element_details`: Retrieves comprehensive definitions, CSS instructions, code templates, study sites, and prompt rules for a specific element (e.g. `glassmorphism`, `bento_grid`).
3. `search_guide`: Searches keywords across all definitions, instructions, and prompt templates in the guide.
4. `compose_design_prompt`: Automatically structures and generates a optimized prompt using the guide's core formula: `Aesthetic + Layout + Animation + specific colors/fonts + custom request`.

---

## Installation

Make sure you have Python installed and the standard Model Context Protocol SDK package (`mcp`) available.

### 1. Install Dependencies
Run the following command in your terminal to install the MCP package:
```bash
pip install -r requirements.txt
```
*(Or simply run `pip install mcp`)*

### 2. Verify Server Manually
To check if the server runs properly, you can start it from your terminal:
```bash
python server.py
```
*(It will run in standard I/O mode, listening for JSON-RPC messages on stdin. Press `Ctrl+C` to exit.)*

---

## Integration Setup

### A. Claude Desktop Integration

To add this server to Claude Desktop on Windows:

1. Open your Claude Desktop configuration file. The default path on Windows is:
   `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the server under the `mcpServers` block. Replace the absolute path to point to your `server.py` file:

```json
{
  "mcpServers": {
    "vibe-design-guide": {
      "command": "python",
      "args": [
        "d:/Enginner Yatharth/WebDesigningMCP/server.py"
      ]
    }
  }
}
```

3. Save the file and restart Claude Desktop. You should now see a plug/tool icon in your chat box!

---

### B. Cursor Integration

To add this server to Cursor:

1. Open Cursor and go to **Settings** -> **Features** -> **MCP**.
2. Click on **+ Add New MCP Server**.
3. Fill in the following details:
   - **Name**: `vibe-design-guide`
   - **Type**: `command`
   - **Command**: `python -u "d:/Enginner Yatharth/WebDesigningMCP/server.py"`
4. Click **Save**. The server status indicator should turn green showing it is successfully connected.

---

### C. Developer Tooling (Debugging)
To test and inspect the MCP server tools in real-time, you can use the MCP Inspector:
```bash
npx @modelcontextprotocol/inspector python d:/Enginner Yatharth/WebDesigningMCP/server.py
```
This launches a local web interface at `http://localhost:5173` where you can manually invoke and test each tool.
