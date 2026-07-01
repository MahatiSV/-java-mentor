# JavaMentor AI — Competition Submission Writeup

**Google × Kaggle ADK Vibe Coding Intensive 2026**

---

## 1. Problem Statement

Java remains one of the most in-demand programming languages globally, yet learners
face a fragmented ecosystem: scattered tutorials, outdated Stack Overflow answers
about deprecated APIs, no adaptive feedback, and disconnected interview prep resources.

JavaMentor AI solves this with a single, adaptive, multi-agent platform that meets
learners wherever they are — from first-timers writing Hello World to senior engineers
prepping for FAANG interviews.

---

## 2. Solution Overview

JavaMentor AI is a **production-grade, multi-agent Java learning platform** built
entirely on Google ADK. It provides:

- **Adaptive tutoring** that adjusts depth based on user level (Beginner/Intermediate/Advanced)
- **Live Java code execution** via Piston API (free, open-source, no API key)
- **Grounded knowledge base** covering Java 8 through Java 24+ (anti-hallucination)
- **Mock technical interviews** for Core Java, Spring, and Spring Boot
- **Adaptive quizzes** with scoring and study recommendations
- **Personalized learning roadmaps** with free resources
- **Beautiful glassmorphism UI** with Mermaid diagram rendering and syntax highlighting

---

## 3. Technical Architecture

### Multi-Agent Design (Google ADK 2.3.0)

```
root_agent: JavaMentorOrchestrator (LlmAgent)
├── tutor_agent        — adapts explanations by level, generates Mermaid diagrams
├── quiz_agent         — creates MCQ/code-tracing quizzes, tracks score
├── code_agent         — live execution via Piston API, code review, debugging
├── interview_agent    — mock interviews with per-answer feedback
├── news_agent         — Java version features (grounded, versioned KB)
└── learning_path_agent— personalized roadmaps, progress tracking
```

The orchestrator routes messages based on user intent, injecting the user's skill
level tag (`[User Level: Beginner]`) into every message for downstream adaptation.

### Tools
| Tool | Description | Cost |
|------|-------------|------|
| `execute_java_code` | Piston REST API — runs Java 21 | Free |
| `get_java_version_features` | In-process KB — Java 8–24 | Free |
| `get_available_java_runtimes` | Piston runtime info | Free |

### Anti-Hallucination Strategy
1. **Grounded knowledge base** — Java version features hardcoded from official JEPs
2. **Live execution as ground truth** — agent cannot hallucinate runtime output
3. **System prompt constraints** — agents instructed to cite versions and acknowledge uncertainty
4. **Source attribution** — news agent labels all facts with "As of Java [version]..."

---

## 4. User Experience

### Adaptive Learning
The level selector (Beginner/Intermediate/Advanced) changes:
- Vocabulary used (analogies for beginners vs. JMM for advanced)
- Code complexity (basic syntax vs. generics + concurrency)
- Quiz difficulty (syntax MCQ vs. concurrency edge cases)
- Interview depth (OOP basics vs. JVM internals)

### Beautiful UI
- Dark glassmorphism design with purple/blue gradient palette
- Three-column layout: Topic Navigator | Chat | Live Code Editor
- Mermaid.js rendering for class hierarchies and flowcharts
- Highlight.js for Java syntax highlighting in chat
- Progress ring tracking session engagement
- Mode tabs: Learn / Quiz / Interview / Code Review

### Code Execution Flow
1. User writes or pastes Java code in the right panel
2. Clicks ▶ Run → FastAPI backend calls Piston API
3. Real stdout/stderr displayed in the output console
4. Alternatively, chat responses include "Run in Playground" buttons
   that auto-load code into the editor

---

## 5. Technology Stack (100% Free)

| Layer | Technology | Why |
|-------|-----------|-----|
| Agent framework | Google ADK 2.3.0 | Competition requirement; multi-agent orchestration |
| LLM | Gemini 2.5 Flash | Free AI Studio tier; best quality/quota ratio |
| Backend | FastAPI + Uvicorn | Async, lightweight, easy to deploy |
| MCP server | fastmcp | ADK-native tool protocol |
| Code execution | Piston API | Free, open-source, supports Java 21 |
| Frontend | Vanilla HTML/CSS/JS | Zero build step; runs anywhere |
| Diagram rendering | Mermaid.js (CDN) | Beautiful flowcharts and class diagrams |
| Syntax highlighting | Highlight.js (CDN) | Java-aware code highlighting |
| Markdown | marked.js (CDN) | Full markdown in chat responses |

**Total infrastructure cost: $0/month**

---

## 6. Java Coverage

### Core Java
Variables, Types, OOP, Interfaces, Generics, Collections Framework,
Streams & Lambdas, Exceptions, I/O, Serialization, Reflection, Annotations

### Modern Java (17–24+)
Records, Sealed Classes, Pattern Matching for switch, Text Blocks,
Virtual Threads (Project Loom), Record Patterns, Sequenced Collections,
Stream Gatherers, Unnamed Variables, Foreign Function & Memory API

### Concurrency
Thread lifecycle, synchronized, volatile, atomic classes, ExecutorService,
CompletableFuture, ForkJoinPool, Virtual Threads, Structured Concurrency

### Spring Ecosystem
Spring IoC/DI, AOP, Spring MVC, Spring Security, Spring Data JPA,
Spring Boot auto-configuration, Actuator, testing (@SpringBootTest)

---

## 7. Competition Alignment

| Criterion | How JavaMentor AI Qualifies |
|-----------|---------------------------|
| Uses Google ADK | Core framework — multi-agent with LlmAgent + sub_agents |
| Multi-agent | 1 orchestrator + 6 specialist agents |
| MCP integration | mcp_server.py with fastmcp, 3 MCP tools |
| Practical impact | Directly addresses Java learning fragmentation |
| Free-tier | 100% free APIs (AI Studio + Piston) |
| Code quality | Unit tests, typed Python, structured architecture |

---

## 8. Future Work

- Persistent user profiles (PostgreSQL or Firestore)
- GitHub integration — review actual user repositories
- Video/animation explanations for complex concepts
- Community features — share learning paths, compare quiz scores
- Mobile-responsive UI
- Voice interaction mode
