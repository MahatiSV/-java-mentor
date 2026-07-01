"""
JavaMentor AI — Shared Type Definitions
Pydantic models and type aliases shared across the application.
"""
from pydantic import BaseModel
from typing import Literal

# ── Shared Types ──────────────────────────────────────────────────────────────

UserLevel = Literal["Beginner", "Intermediate", "Advanced"]

AgentName = Literal[
    "JavaMentorOrchestrator",
    "tutor_agent",
    "quiz_agent",
    "code_agent",
    "interview_agent",
    "news_agent",
    "learning_path_agent",
]


class JavaTopic(BaseModel):
    id: str
    label: str
    subtopics: list[str] = []


class UserSession(BaseModel):
    session_id: str
    user_id: str
    level: UserLevel = "Beginner"
    current_topic: str | None = None
    progress: dict[str, int] = {}  # topic_id -> completion percentage
