"""
Unit tests for JavaMentor AI agents and tools.
Run: uv run pytest tests/ -v
"""
import json
import pytest
from unittest.mock import patch, MagicMock

from java_mentor.tools import (
    execute_java_code,
    get_java_version_features,
    get_available_java_runtimes,
)
from java_mentor.config import JAVA_VERSION_FEATURES


# ─── Tool Tests ───────────────────────────────────────────────────────────────

class TestGetJavaVersionFeatures:
    """Tests for the Java version knowledge base tool."""

    def test_returns_known_version_java_8(self):
        result = json.loads(get_java_version_features("8"))
        assert "features" in result
        assert "release" in result
        assert result["lts"] is True
        assert any("Lambda" in f for f in result["features"])

    def test_returns_known_version_java_21(self):
        result = json.loads(get_java_version_features("21"))
        assert "features" in result
        assert result["lts"] is True
        assert any("Virtual Thread" in f for f in result["features"])

    def test_returns_known_version_java_17(self):
        result = json.loads(get_java_version_features("17"))
        assert "features" in result
        assert any("Record" in f for f in result["features"])
        assert any("Sealed" in f for f in result["features"])

    def test_returns_error_for_unknown_version(self):
        result = json.loads(get_java_version_features("99"))
        assert "error" in result
        assert "available_versions" in result

    def test_all_known_versions_have_required_fields(self):
        required_fields = ["release", "lts", "features", "jeps"]
        for version in JAVA_VERSION_FEATURES:
            result = json.loads(get_java_version_features(version))
            for field in required_fields:
                assert field in result, f"Version {version} missing field: {field}"

    def test_all_versions_have_nonempty_features(self):
        for version in JAVA_VERSION_FEATURES:
            result = json.loads(get_java_version_features(version))
            assert len(result["features"]) > 0, f"Version {version} has no features"

    def test_version_with_leading_zero(self):
        """Version strings like '08' should still resolve correctly."""
        result = json.loads(get_java_version_features("08"))
        assert "features" in result


class TestExecuteJavaCode:
    """Tests for the Piston API code execution tool."""

    @patch("java_mentor.tools.httpx.post")
    def test_successful_execution(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "language": "java",
            "version": "21.0.1",
            "run": {"stdout": "Hello World\n", "stderr": ""},
            "compile": {"stderr": "", "stdout": ""},
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = json.loads(execute_java_code('public class Main { public static void main(String[] args) { System.out.println("Hello World"); } }'))
        assert result["success"] is True
        assert "Hello World" in result["output"]
        assert result["error"] is None

    @patch("java_mentor.tools.httpx.post")
    def test_compilation_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "language": "java",
            "version": "21.0.1",
            "run": {"stdout": "", "stderr": ""},
            "compile": {"stderr": "error: ';' expected", "stdout": ""},
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = json.loads(execute_java_code("public class Main { broken"))
        assert result["success"] is False
        assert "error" in result
        assert "Compilation" in result["error"]

    @patch("java_mentor.tools.httpx.post")
    def test_timeout_returns_error(self, mock_post):
        import httpx
        mock_post.side_effect = httpx.TimeoutException("timeout")

        result = json.loads(execute_java_code("public class Main { public static void main(String[] args) {} }"))
        assert result["success"] is False
        assert "Timeout" in result["error"]

    @patch("java_mentor.tools.httpx.post")
    def test_returns_valid_json(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "language": "java", "version": "21",
            "run": {"stdout": "42", "stderr": ""}, "compile": {},
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result_str = execute_java_code("public class Main {}")
        # Should be valid JSON
        result = json.loads(result_str)
        assert isinstance(result, dict)

    def test_result_has_required_fields(self):
        """Even on error, result must have all required fields."""
        with patch("java_mentor.tools.httpx.post") as mock_post:
            import httpx
            mock_post.side_effect = Exception("network error")
            result = json.loads(execute_java_code("code"))
            assert "success" in result
            assert "output" in result
            assert "stderr" in result
            assert "error" in result


# ─── Agent Config Tests ───────────────────────────────────────────────────────

class TestAgentConfiguration:
    """Tests that agents are configured correctly."""

    def test_root_agent_exists(self):
        from java_mentor.agent import root_agent
        assert root_agent is not None
        assert root_agent.name == "JavaMentorOrchestrator"

    def test_root_agent_has_sub_agents(self):
        from java_mentor.agent import root_agent
        assert hasattr(root_agent, 'sub_agents')
        assert root_agent.sub_agents is not None
        assert len(root_agent.sub_agents) == 6

    def test_all_sub_agents_have_names(self):
        from java_mentor.agent import (
            tutor_agent, quiz_agent, code_agent,
            interview_agent, news_agent, learning_path_agent
        )
        agents = [tutor_agent, quiz_agent, code_agent, interview_agent, news_agent, learning_path_agent]
        for agent in agents:
            assert agent.name, f"Agent has no name: {agent}"

    def test_all_sub_agents_have_descriptions(self):
        from java_mentor.agent import (
            tutor_agent, quiz_agent, code_agent,
            interview_agent, news_agent, learning_path_agent
        )
        agents = [tutor_agent, quiz_agent, code_agent, interview_agent, news_agent, learning_path_agent]
        for agent in agents:
            assert agent.description, f"Agent '{agent.name}' has no description"

    def test_code_agent_has_execute_tool(self):
        from java_mentor.agent import code_agent
        tool_names = [t.__name__ if callable(t) else str(t) for t in code_agent.tools]
        assert any("execute" in name.lower() for name in tool_names)

    def test_news_agent_has_version_tool(self):
        from java_mentor.agent import news_agent
        tool_names = [t.__name__ if callable(t) else str(t) for t in news_agent.tools]
        assert any("version" in name.lower() or "java" in name.lower() for name in tool_names)

    def test_config_model_is_set(self):
        from java_mentor.config import GEMINI_MODEL
        assert GEMINI_MODEL
        assert "gemini" in GEMINI_MODEL.lower()


# ─── Knowledge Base Integrity Tests ──────────────────────────────────────────

class TestJavaKnowledgeBase:
    """Verify the Java version knowledge base is accurate and complete."""

    def test_java_8_has_lambda(self):
        features = JAVA_VERSION_FEATURES["8"]["features"]
        assert any("Lambda" in f for f in features)

    def test_java_11_has_http_client(self):
        features = JAVA_VERSION_FEATURES["11"]["features"]
        assert any("HTTP" in f for f in features)

    def test_java_17_is_lts(self):
        assert JAVA_VERSION_FEATURES["17"]["lts"] is True

    def test_java_21_has_virtual_threads(self):
        features = JAVA_VERSION_FEATURES["21"]["features"]
        assert any("Virtual Thread" in f for f in features)

    def test_java_21_is_lts(self):
        assert JAVA_VERSION_FEATURES["21"]["lts"] is True

    def test_java_22_is_not_lts(self):
        assert JAVA_VERSION_FEATURES["22"]["lts"] is False

    def test_all_versions_have_code_examples(self):
        for version, data in JAVA_VERSION_FEATURES.items():
            assert "example" in data, f"Java {version} has no code example"
            assert len(data["example"]) > 10, f"Java {version} example too short"
