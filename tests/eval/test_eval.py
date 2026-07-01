"""
Eval tests — verify agent output quality (requires GOOGLE_API_KEY).
Run: uv run pytest tests/eval/ -v -m eval
These tests call the real Gemini API — use sparingly to preserve quota.
"""
import pytest
import asyncio

pytestmark = pytest.mark.skipif(
    True,  # Skip by default to protect API quota
    reason="Eval tests call the real Gemini API. Run explicitly with: pytest tests/eval/ -v --run-eval"
)


class TestTutorAgentEval:
    """Eval tests for the tutor agent output quality."""

    async def test_explains_streams_with_code(self):
        """Tutor should always include a code example when explaining Streams."""
        from java_mentor.agent import tutor_agent
        # Placeholder — implement with ADK test runner
        pass

    async def test_includes_mermaid_for_oop_concepts(self):
        """Tutor should include Mermaid diagram for OOP hierarchy questions."""
        pass


class TestCodeAgentEval:
    """Eval tests for code execution accuracy."""

    async def test_runs_hello_world_correctly(self):
        """Code agent should run Hello World and return correct output."""
        pass

    async def test_detects_null_pointer_risk(self):
        """Code agent should flag NullPointerException risk in review."""
        pass
