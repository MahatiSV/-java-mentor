.PHONY: run playground stop install test lint

# Install dependencies
install:
	uv sync

# Run the FastAPI server (custom UI at http://127.0.0.1:8090)
run:
	uv run uvicorn java_mentor.fast_api_app:app --host 127.0.0.1 --port 8090 --reload

# Run the ADK Dev Playground (http://127.0.0.1:18081)
# NOTE: On Windows, run this command directly instead of 'make playground':
#   uv run adk web java_mentor --host 127.0.0.1 --port 18081 --reload_agents
playground:
	uv run adk web java_mentor --host 127.0.0.1 --port 18081 --reload_agents

# Run the MCP server standalone
mcp:
	uv run python -m java_mentor.mcp_server

# Run tests
test:
	uv run pytest tests/ -v

# Stop any running servers (Windows)
stop:
	-powershell -Command "Get-Process -Id (Get-NetTCPConnection -LocalPort 8090,18081 -ErrorAction SilentlyContinue).OwningProcess | Stop-Process -Force"
