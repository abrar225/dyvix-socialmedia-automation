#!/usr/bin/env python3
"""
Project-Scoped n8n MCP Client Bridge
Securely calls n8n MCP server using local environment configuration.
"""
import os
import sys
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

# Load project-local .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

MCP_URL = os.getenv("N8N_MCP_URL", "https://flow.dyvix.net/mcp-server/http")
API_KEY = os.getenv("N8N_API_KEY")

if not API_KEY:
    print(json.dumps({"error": "N8N_API_KEY is not defined in .env"}), file=sys.stderr)
    sys.exit(1)

def call_mcp(method: str, params: dict = None, req_id: int = 1):
    if params is None:
        params = {}
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(MCP_URL, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8")
            # Parse text/event-stream or application/json
            for line in raw.split("\n"):
                if line.startswith("data:"):
                    json_str = line[len("data:"):].strip()
                    if json_str:
                        return json.loads(json_str)
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {err_msg}"}
    except Exception as e:
        return {"error": str(e)}

def call_tool(tool_name: str, arguments: dict = None):
    return call_mcp("tools/call", {"name": tool_name, "arguments": arguments or {}})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 n8n_mcp_client.py list-tools")
        print("  python3 n8n_mcp_client.py call-tool <tool_name> '<json_arguments>'")
        print("  python3 n8n_mcp_client.py search-workflows '<query>'")
        sys.exit(0)
        
    cmd = sys.argv[1]
    if cmd == "list-tools":
        res = call_mcp("tools/list")
        print(json.dumps(res, indent=2))
    elif cmd == "call-tool":
        tool = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        res = call_tool(tool, args)
        print(json.dumps(res, indent=2))
    elif cmd == "search-workflows":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        res = call_tool("search_workflows", {"query": query, "limit": 20})
        print(json.dumps(res, indent=2))
