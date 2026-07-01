"""
JavaMentor AI — FastAPI Backend
Wraps the ADK multi-agent system with a REST API.
Also serves the beautiful frontend at GET /

Run: uv run uvicorn java_mentor.fast_api_app:app --host 127.0.0.1 --port 8090 --reload
Then open: http://127.0.0.1:8090
"""

import uuid
import json
import httpx
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from java_mentor.agent import root_agent
from java_mentor.config import APP_NAME, APP_HOST, APP_PORT, PISTON_API_URL, PISTON_TIMEOUT
from java_mentor.app_utils.telemetry import setup_telemetry

# ─── Session Service (in-memory for demo) ─────────────────────────────────────
session_service = InMemorySessionService()
runner: Runner | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize runner on startup."""
    global runner
    setup_telemetry()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    print(f"[OK] JavaMentor AI started -- open http://{APP_HOST}:{APP_PORT}")
    yield
    print("[BYE] JavaMentor AI shutting down...")


# ─── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="JavaMentor AI",
    description="Multi-agent Java learning platform powered by Google ADK",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ─────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str = "default_user"
    level: str = "Beginner"  # Beginner | Intermediate | Advanced


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_used: str = "unknown"


class ExecuteRequest(BaseModel):
    code: str


class ExecuteResponse(BaseModel):
    success: bool
    output: str
    stderr: str
    error: str | None
    runtime_version: str


# ─── API Routes ────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Liveness probe."""
    return {"status": "ok", "app": APP_NAME, "version": "0.1.0"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the JavaMentor multi-agent system."""
    if runner is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id

    # Ensure session exists.
    try:
        session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
    except Exception:
        session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )


    # Prefix message with level context so agents can adapt
    full_message = f"[User Level: {request.level}] {request.message}"

    content = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=full_message)],
    )

    final_response = ""
    agent_used = "JavaMentorOrchestrator"

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = "".join(
                        part.text
                        for part in event.content.parts
                        if hasattr(part, "text")
                    )
                if hasattr(event, "author") and event.author:
                    agent_used = event.author
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    if not final_response:
        final_response = "I'm sorry, I couldn't generate a response. Please try again."

    return ChatResponse(
        response=final_response,
        session_id=session_id,
        agent_used=agent_used,
    )


@app.post("/api/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    """
    Execute Java code via Piston API (free, no API key required).
    Proxied through the backend to keep API calls server-side.
    """
    try:
        payload = {
            "language": "java",
            "version": "*",
            "files": [{"content": request.code}],
            "stdin": "",
            "args": [],
            "compile_timeout": 10000,
            "run_timeout": 5000,
        }
        async with httpx.AsyncClient(timeout=PISTON_TIMEOUT) as client:
            response = await client.post(PISTON_API_URL, json=payload)
            response.raise_for_status()
            result = response.json()

        compile_info = result.get("compile", {}) or {}
        run_info = result.get("run", {}) or {}
        lang_version = f"{result.get('language', 'java')} {result.get('version', '')}".strip()

        compile_stderr = compile_info.get("stderr", "")
        run_stdout = run_info.get("stdout", "")
        run_stderr = run_info.get("stderr", "")

        if compile_stderr and not run_stdout:
            return ExecuteResponse(
                success=False,
                output="",
                stderr=compile_stderr,
                error="Compilation failed",
                runtime_version=lang_version,
            )

        return ExecuteResponse(
            success=True,
            output=run_stdout,
            stderr=run_stderr,
            error=None,
            runtime_version=lang_version,
        )

    except httpx.TimeoutException:
        return ExecuteResponse(
            success=False,
            output="",
            stderr="Execution timed out.",
            error="Timeout",
            runtime_version="unknown",
        )
    except Exception as e:
        return ExecuteResponse(
            success=False,
            output="",
            stderr=str(e),
            error=str(e),
            runtime_version="unknown",
        )


@app.get("/api/topics")
async def get_topics():
    """Return the Java topic tree for the sidebar navigation."""
    return {
        "topics": [
            {"id": "basics", "label": "☕ Java Basics", "subtopics": ["Variables & Types", "Control Flow", "Arrays", "Methods"]},
            {"id": "oop", "label": "🏗️ OOP", "subtopics": ["Classes & Objects", "Inheritance", "Polymorphism", "Encapsulation", "Interfaces"]},
            {"id": "collections", "label": "📦 Collections", "subtopics": ["ArrayList", "HashMap", "HashSet", "LinkedList", "TreeMap", "PriorityQueue"]},
            {"id": "streams", "label": "🌊 Streams & Lambdas", "subtopics": ["Lambda Basics", "Stream Pipeline", "map/filter/reduce", "Collectors", "Optional"]},
            {"id": "generics", "label": "🧬 Generics", "subtopics": ["Type Parameters", "Wildcards", "Bounded Types", "Type Erasure"]},
            {"id": "concurrency", "label": "⚡ Concurrency", "subtopics": ["Threads", "ExecutorService", "CompletableFuture", "Virtual Threads (21+)", "Locks & Atomic"]},
            {"id": "modern", "label": "🚀 Modern Java", "subtopics": ["Records (17+)", "Sealed Classes (17+)", "Pattern Matching (21+)", "Text Blocks", "var"]},
            {"id": "spring", "label": "🌱 Spring", "subtopics": ["IoC & DI", "AOP", "Spring MVC", "Spring Security", "Testing"]},
            {"id": "springboot", "label": "🥾 Spring Boot", "subtopics": ["Auto-Configuration", "Starters", "Actuator", "Spring Data JPA", "REST APIs"]},
            {"id": "interview", "label": "💼 Interview Prep", "subtopics": ["Core Java Questions", "Collections Questions", "Concurrency Questions", "Spring Questions"]},
        ]
    }


# ─── Serve Frontend ────────────────────────────────────────────────────────────
_frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.isdir(_frontend_dir):
    app.mount("/static", StaticFiles(directory=_frontend_dir), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(_frontend_dir, "index.html"))
else:
    @app.get("/")
    async def no_frontend():
        return JSONResponse({"message": "JavaMentor AI API running. Frontend not found.", "docs": "/docs"})


# ─── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("java_mentor.fast_api_app:app", host=APP_HOST, port=APP_PORT, reload=True)
