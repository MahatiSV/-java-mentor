"""
JavaMentor AI — Tool Functions
All tools available to the sub-agents. Using direct Python functions
(google-adk auto-wraps them as FunctionTools).
"""
import json
import httpx
from java_mentor.config import PISTON_API_URL, PISTON_TIMEOUT, JAVA_VERSION_FEATURES


# ─────────────────────────────────────────────────────────────────────────────
# Tool 1: Execute Java Code via Piston API (free, no API key required)
# ─────────────────────────────────────────────────────────────────────────────

def execute_java_code(code: str) -> str:
    """
    Execute Java source code using the Piston API (free, open-source, no API key).
    Supports Java 21. Returns stdout, stderr, and compilation errors.

    Args:
        code: Complete Java source code to execute (must include a class with main method)

    Returns:
        JSON string with fields: success (bool), output (str), stderr (str), error (str|null)
    """
    try:
        payload = {
            "language": "java",
            "version": "*",  # latest available
            "files": [{"content": code}],
            "stdin": "",
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 5000,
        }
        response = httpx.post(
            PISTON_API_URL,
            json=payload,
            timeout=PISTON_TIMEOUT,
        )
        response.raise_for_status()
        result = response.json()

        compile_info = result.get("compile", {})
        run_info = result.get("run", {})
        language_version = result.get("language", "java") + " " + result.get("version", "")

        # Compilation error
        compile_stderr = compile_info.get("stderr", "") if compile_info else ""
        compile_stdout = compile_info.get("stdout", "") if compile_info else ""
        if compile_stderr and not run_info.get("stdout"):
            return json.dumps({
                "success": False,
                "output": compile_stdout,
                "stderr": compile_stderr,
                "error": "Compilation failed",
                "runtime_version": language_version.strip(),
            })

        run_stdout = run_info.get("stdout", "")
        run_stderr = run_info.get("stderr", "")

        return json.dumps({
            "success": True,
            "output": run_stdout,
            "stderr": run_stderr,
            "error": None,
            "runtime_version": language_version.strip(),
        })

    except httpx.TimeoutException:
        return json.dumps({
            "success": False,
            "output": "",
            "stderr": "Execution timed out after 15 seconds.",
            "error": "Timeout",
            "runtime_version": "unknown",
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "output": "",
            "stderr": str(e),
            "error": f"Execution service error: {str(e)}",
            "runtime_version": "unknown",
        })


# ─────────────────────────────────────────────────────────────────────────────
# Tool 2: Get Java Version Features (grounded knowledge base)
# ─────────────────────────────────────────────────────────────────────────────

def get_java_version_features(version: str) -> str:
    """
    Retrieve accurate, versioned features for a specific Java release.
    Use this to ground your answers about Java versions — never hallucinate.

    Args:
        version: Java version number as string, e.g. '8', '11', '17', '21', '22', '23', '24'

    Returns:
        JSON string with: release date, lts status, features list, JEPs, and code example
    """
    key = str(version).strip().lstrip("0") or "8"
    if key in JAVA_VERSION_FEATURES:
        return json.dumps(JAVA_VERSION_FEATURES[key])
    else:
        available = list(JAVA_VERSION_FEATURES.keys())
        return json.dumps({
            "error": f"Version '{version}' not in knowledge base.",
            "available_versions": available,
            "tip": f"Available: {available}. For very recent releases check https://openjdk.org/projects/jdk/",
        })


# ─────────────────────────────────────────────────────────────────────────────
# Tool 3: Get Piston Runtime Info (what Java version is available)
# ─────────────────────────────────────────────────────────────────────────────

def get_available_java_runtimes() -> str:
    """
    Check which Java runtimes are available on the Piston code execution service.

    Returns:
        JSON string listing available Java versions on Piston API
    """
    try:
        response = httpx.get("https://emkc.org/api/v2/piston/runtimes", timeout=10.0)
        runtimes = response.json()
        java_runtimes = [r for r in runtimes if r.get("language") == "java"]
        return json.dumps({
            "java_runtimes": java_runtimes,
            "note": "These are the Java versions available for code execution via Piston API"
        })
    except Exception as e:
        return json.dumps({"error": str(e), "java_runtimes": []})
