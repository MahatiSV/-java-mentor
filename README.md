# JavaMentor AI ☕

> **Your adaptive Java learning companion** — from "Hello World" to Virtual Threads,
> Spring Boot to interview prep. Built with Google ADK for the Google × Kaggle 2026 competition.

![JavaMentor AI — Multi-agent Java learning platform](./assets/cover_page_banner.png)

---

## ✨ Problem & Solution

JavaMentor AI addresses the fragmented nature of Java learning by combining adaptive tutoring, deterministic code execution, and specialized AI agents into a single learning platform.

| Feature | Description |
|---------|-------------|
| 🎓 **Adaptive Tutoring** | Explains any Java concept with examples, analogies, and Mermaid diagrams |
| ▶️ **Live Code Execution** | Runs Java code in-browser via Piston API (free, no setup) |
| 🎯 **Adaptive Quizzes** | MCQ, code tracing, spot-the-bug — adjusts to your level |
| 💼 **Mock Interviews** | Core Java, Spring Boot, concurrency — with detailed feedback |
| 🚀 **Java Version News** | Grounded, versioned coverage of Java 8 → 24+ features |
| 🗺️ **Learning Paths** | Personalized roadmaps with free resources |

---

## 🏗️ Architecture

```
JavaMentorOrchestrator (root_agent)
    ├── tutor_agent         — concepts, analogies, Mermaid diagrams
    ├── quiz_agent          — adaptive MCQ, code tracing, scoring
    ├── code_agent          — live execution (Piston API), review, debug
    ├── interview_agent     — mock interviews + feedback
    ├── news_agent          — Java release notes (grounded KB)
    └── learning_path_agent — personalized roadmaps
```
### High-Level Architecture

```
                ┌──────────────────────┐
                │     Frontend UI      │
                │ (Markdown + Mermaid) │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │   FastAPI Backend    │
                └─────────┬────────────┘
                          │
                          ▼
        ┌──────────────────────────────────┐
        │ JavaMentor Orchestrator (ADK)    │
        └──────────────────────────────────┘
              │     │      │      │
              ▼     ▼      ▼      ▼
        Tutor  Quiz  Code  Interview  Learning
         Agent  Agent Agent   Agent      Path
              │
              ▼
        News / Knowledge Agent
              │
              ▼
        MCP Tool Layer
              │
     ┌────────┴─────────┐
     ▼                  ▼
Piston API        Java Knowledge Base
```
The system separates:

- **Reasoning** → Gemini-powered agents through Google ADK
- **Orchestration** → Root agent routing and coordination
- **Execution** → MCP tools and external capabilities
- **Verification** → Runtime results and structured knowledge sources

This allows JavaMentor AI to combine AI reasoning with deterministic execution where correctness matters.

---

Built with Google ADK + Gemini 2.5 Flash (AI Studio tier).
Code execution is powered by **Piston API**, providing sandboxed Java runtime execution without requiring a separate setup.

---

## 🚀 Quick Start

### Prerequisites
```bash
python --version   # >= 3.11
uv --version       # any recent version
```

### 1. Clone & Install
```bash
git clone <your-repo>
cd java-mentor
uv sync
```

### 2. Configure API Key
Create your env file from the template:

```bash
cp .env.example .env
```

Then edit `.env`:
```
GOOGLE_API_KEY=your_gemini_key_from_aistudio
```
Get a free key at https://aistudio.google.com/apikey

### 3. Run the Application
```bash
# Option A: Beautiful custom UI (recommended)
uv run uvicorn java_mentor.fast_api_app:app --host 127.0.0.1 --port 8090 --reload
# Open: http://127.0.0.1:8090

# Option B: ADK Dev Playground
uv run adk web java_mentor --host 127.0.0.1 --port 18081 --reload_agents
# Open: http://127.0.0.1:18081
```

### 4. Run Tests
```bash
uv run pytest tests/unit/ -v
```

---

## 💡 Example Interactions

**Explain a concept:**
> "Explain Java Streams with a real-world analogy for a beginner"

**Run code:**
> "Run this code: `System.out.println("Hello".repeat(3));`"

**Quiz mode:**
> "Quiz me on Java Collections — intermediate level"

**Interview prep:**
> "Start a Spring Boot mock interview"

**Latest Java:**
> "What are the key features in Java 21?"

**Learning path:**
> "I know Python, where should I start with Java?"

---

## 📦 Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Agent framework | Google ADK | Free |
| LLM | Gemini 2.5 Flash | Free (AI Studio) |
| Backend | FastAPI + Uvicorn | Free |
| MCP server | fastmcp | Free |
| Code execution | Piston API | Free |
| Frontend | Vanilla HTML/CSS/JS | Free |
| Diagrams | Mermaid.js (CDN) | Free |
| Syntax highlight | Highlight.js (CDN) | Free |

**Total cost: $0** ☕

---

## 📁 Project Structure

```
java-mentor/
├── java_mentor/
│   ├── agent.py          # Root orchestrator + specialist agents
│   ├── tools.py          # Code execution + knowledge base tools
│   ├── config.py         # Model config + Java version knowledge base
│   ├── mcp_server.py     # MCP server (fastmcp)
│   ├── fast_api_app.py   # FastAPI backend + frontend serving
│   └── app_utils/        # Logging, types
├── frontend/
│   └── index.html        # Beautiful standalone UI
├── tests/
│   ├── unit/             # Unit + mock tests (no API quota used)
│   └── eval/             # Eval tests (skipped by default)
└── .env                  # API key (not committed)
```

## 🧠 Engineering Highlights

### Multi-Agent over Monolithic Chat

Instead of a single general-purpose chatbot, JavaMentor AI uses specialized agents:

- Tutor Agent → explanations and visual learning
- Quiz Agent → assessment and adaptive practice
- Code Agent → execution, debugging, and validation
- Interview Agent → technical interview simulation
- Learning Path Agent → personalized progression
- News Agent → Java version-aware updates

Each agent has a focused responsibility, making the system modular and extensible.

---

### Grounded Learning Experience

JavaMentor AI reduces unreliable AI responses by combining:

- Versioned Java feature knowledge base
- Real Java execution through Piston API
- Tool-based information retrieval
- Structured agent responsibilities

For code-related questions, the system executes programs instead of only predicting outputs.

---

## 🚀 Future Enhancements

The current system provides the foundation for a larger adaptive learning platform.

Planned improvements:

- **Persistent learner memory**
  - Maintain progress, strengths, and learning gaps across sessions

- **Agent Skills framework**
  - Modular capability packages that can be loaded when required

- **Trajectory evaluation**
  - Measure learning progress and evaluate reasoning paths

- **Enhanced documentation grounding**
  - RAG-based retrieval from official Java and Spring documentation

- **GitHub learning assistant**
  - Analyze repositories and provide personalized improvement guidance

- **Voice-based learning mode**
  - Conversational Java mentoring experience

The long-term vision is to evolve JavaMentor AI from an adaptive assistant into a complete AI-powered Java learning ecosystem.

---

## 🎥 Demo

A complete end-to-end demonstration is available in the submitted demo video.

The demo showcases:

- Adaptive Java concept explanation
- Mermaid-based visual learning
- Agent-driven response generation
- Java code execution workflow
- Tool integration through MCP

---

## 🏆 Competition

Built for the **Google × Kaggle ADK Vibe Coding Intensive 2026**.

Key differentiators:
- ✅ Full multi-agent ADK architecture with 6 specialist agents
- ✅ Anti-hallucination: versioned knowledge base + live code execution as ground truth
- ✅ Zero-cost deployment (all free APIs)
- ✅ Production-quality adaptive UI with Mermaid, syntax highlighting
- ✅ Spring/Spring Boot coverage (industry-relevant)

---

## Push to GitHub

1. Create a new repo at https://github.com/new
    - Name: `java-mentor`
    - Visibility: Public or Private
    - Do not initialize with README

2. In your terminal, run:

```bash
git add .
git commit -m "feat: bootstrap JavaMentor ADK project"
git branch -M main
git remote add origin https://github.com/MahatiSV/java-mentor.git
git push -u origin main
```

3. Tag the submission snapshot:

```bash
git tag -a kaggle-2026-final -m "Kaggle submission snapshot"
git push origin kaggle-2026-final
```

---

## Final Public-Release Checklist

- [ ] No API keys committed
- [ ] `.env` is ignored
- [ ] `.env.example` exists
- [ ] No personal/local temp files
- [ ] README setup works from a clean clone
- [ ] Demo video completed
- [ ] Final tests executed
