# OpenRegister MCP Server

A unofficial Model Context Protocol (MCP) server for accessing the [OpenRegister API](https://openregister.de/), providing tools to search and retrieve company information from the German company register.

## Features

- Search for companies based on various criteria (name, register number, type, etc.)
- Get detailed company information including history, financials, and documents
- Retrieve company shareholders information

## Requirements

- Python 3.9+
- uv
- OpenRegister API key (which you can get from https://openregister.de after you have created an account)
- Claude Desktop (or another MCP client that understands MCP)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Syndicats/openregister-mcp.git
   cd openregister-mcp
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install "mcp[cli]" httpx dotenv
   ```

3. Create a `.env` file based on the example:
   ```bash
   cp env.example .env
   ```

4. Add your OpenRegister API key to the `.env` file:
   ```
   OPENREGISTER_API_KEY=your_api_key_here
   OPENREGISTER_API_URL=https://api.openregister.de/v0
   ```

## Usage as MCP Server

Run the server within Claude Desktop, e.g. by editing the `claude_desktop_config.json` from Claude Desktop

```json
{
    "mcpServers": {
        "openregister": {
            "command": "uv",
            "args": [
                "--directory",
                "<Absolute Path to openregister-mcp>/openregister-mcp",
                "run",
                "server.py"
            ]
        }
    }
}
```

Restart Claude Desktop so that the changes take effect.

#### Caution
Sometimes it is necessary to use the absolute path for uv. Then the JSON needs to be changed accordingly.

### Available Tools

The server provides the following MCP tools:

1. **search_companies** - Search for companies based on various criteria
   - Parameters:
     - `query`: Text search query to find companies by name
     - `register_number`: Company register number for exact matching
     - `register_type`: Type of register to filter results (e.g., "HRB", "HRA", "PR", "GnR", "VR")
     - `register_court`: Court where the company is registered
     - `active`: Filter for active or inactive companies (default: true)
     - `legal_form`: Legal form of the company (e.g., "gmbh", "ag", "ug")

2. **get_company_info** - Get detailed information about a company using its unique ID
   - Parameters:
     - `company_id`: Unique company identifier (e.g., "DE-HRB-F1103-267645")
     - `history`: Include historical company data (default: true)
     - `financials`: Include financial data (default: true)
     - `documents`: Include document metadata (default: true)

3. **get_company_shareholders** - Retrieve the shareholders of a company
   - Parameters:
     - `company_id`: Unique company identifier (e.g., "DE-HRB-F1103-267645")
   - Note: Currently only supports companies with the legal form GmbH

## License

[MIT](LICENSE)