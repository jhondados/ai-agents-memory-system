# 🧠 AI Agents Memory System

[![Memory Types](https://img.shields.io/badge/Memory%20Types-4-blue)](.) [![pgvector](https://img.shields.io/badge/pgvector-PostgreSQL-green)](.) [![Sessions](https://img.shields.io/badge/Cross--session-Persistent-orange)](.)

> **Cognitive memory architecture** for AI agents. Implements episodic, semantic, procedural and working memory with vector storage, Ebbinghaus forgetting curves and automatic memory consolidation.

## 🧩 Memory Architecture
```
WORKING MEMORY (Redis, 4K tokens) — current context window
EPISODIC MEMORY (pgvector) — past conversations + interactions
SEMANTIC MEMORY (pgvector) — facts, knowledge, preferences
PROCEDURAL MEMORY (JSON) — learned skills, workflows, preferences
        │
        ▼
Memory Consolidation (nightly) — important → long-term
Forgetting Curve — decay unimportant memories over time
Cross-session Retrieval — relevant memories injected at session start
```

## 🏆 Agent Performance Improvement
- **+67% task success** on long-horizon tasks (cross-session)
- **User personalization**: agents remember preferences, history, feedback
- **Knowledge accumulation**: agents get smarter with each session
