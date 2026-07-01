"""
JavaMentor AI — MCP Server
Exposes JavaMentor tools as an MCP (Model Context Protocol) server.
Can be used standalone or connected via MCPToolset.

Run standalone: uv run python -m java_mentor.mcp_server
"""

from fastmcp import FastMCP
from java_mentor.tools import (
    execute_java_code,
    get_java_version_features,
    get_available_java_runtimes,
)

mcp = FastMCP(
    name="JavaMentor Tools",
    instructions="""
    JavaMentor MCP Server — provides tools for Java learning:
    - execute_java_code: Run Java code via Piston API (free, no key)
    - get_java_version_features: Get accurate Java version release notes
    - get_available_java_runtimes: Check available Java versions on Piston
    """,
)

# Register tools
mcp.tool(execute_java_code)
mcp.tool(get_java_version_features)
mcp.tool(get_available_java_runtimes)

if __name__ == "__main__":
    mcp.run()
