# FastMCP integration

Available with enable_mcp=true. Standalone FastMCP serves stateless Streamable HTTP on the same Uvicorn process, at /mcp/. Redis is not required.

## Connect a client

After starting the API, configure a compatible MCP client:

```json
{
  "mcpServers": {
    "backup-service": {
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

Client configuration formats differ. Use the trailing slash.

## Discover and call tools

Run this Python example in the generated environment:

```python
import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp/") as client:
        tools = await client.list_tools()
        print([tool.name for tool in tools])
        result = await client.call_tool("get_message_count", {})
        print(result.data)

asyncio.run(main())
```

The sample tool reads the actual SQLite message count.

## Add a tool

Register explicitly inside create_mcp_server in src/backup_service/mcp_server.py:

```python
@server.tool(annotations={"readOnlyHint": True})
def get_backup_status() -> str:
    """Return the last backup status."""
    return "completed"  # Replace with a domain query.
```

Synchronous tools run in FastMCP's thread pool. Use async functions for async I/O. Keep domain logic shared with HTTP routes and CLI commands.

Host and Origin validation is enabled. The default endpoint has no authentication and is intended only for loopback. Design authentication, TLS and host allowlists before remote access; never expose arbitrary shell execution or automatically publish every REST route.
