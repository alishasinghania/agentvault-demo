# AgentVault — Intelligent Knowledge Assistant for Modern Enterprises

> **⚠️ SECURITY RESEARCH TARGET — INTENTIONALLY VULNERABLE**
> AgentVault is a deliberately insecure application built for security education and CTF-style demos.
> It contains **14 real, working vulnerabilities** in agentic AI systems.
> **Do not deploy in production. Do not use real credentials. All "Meridian Corp" credentials are fictional.**
> See [`VULNERABILITIES.md`](VULNERABILITIES.md) for the full presenter answer key.

---

> **Meridian Corp Internal AI Platform** — Empowering employees with instant access to company knowledge, code assistance, and intelligent research capabilities.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-0.0.131-1C3C3C?logo=chainlink)
![Anthropic](https://img.shields.io/badge/Claude-Haiku-D97706?logo=anthropic)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.22-FF6B35)
![CrewAI](https://img.shields.io/badge/CrewAI-0.1.0-4A90D9)

---

## ✨ Features

- 📚 **Policy & Knowledge RAG** — Instant answers from company policy documents, the employee handbook, and IT security guides using retrieval-augmented generation
- 🖥️ **Code Assistant** — Ask AgentVault to write, debug, or run Python calculations directly in the chat
- 🔬 **Research Crew** — Kick off a multi-agent CrewAI research task to synthesize information from multiple sources
- 🗄️ **Database Queries** — Natural language interface to the Meridian Corp employee and project database
- 📧 **Smart Email Drafting** — Let AgentVault draft and send internal emails on your behalf
- 💬 **Streaming Chat** — Real-time WebSocket streaming for a responsive chat experience
- 🧠 **Persistent Memory** — Conversation history maintained across your session for coherent multi-turn dialogue

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph UI["Frontend"]
        A[Browser Chat UI]
    end

    subgraph Gateway["API Gateway"]
        B[FastAPI HTTP/WebSocket]
    end

    subgraph Orchestration["Agent Orchestration Layer — LangGraph"]
        C[Primary Agent\nAnthropic Claude]
        D[Code Agent\nPythonREPL]
        E[Research Crew\nCrewAI]
        F[Memory Agent\nConversationBuffer]
    end

    subgraph RAGPipeline["RAG Pipeline"]
        G[LlamaIndex Ingestor]
        H[HuggingFace Embedder\nall-MiniLM-L6-v2]
        I[ChromaDB Vector Store]
        J[LangChain RetrievalQA]
    end

    subgraph Tools["Tool Layer"]
        K[Email Tool\nSMTP]
        L[Database Tool\nSQLite]
        M[Utils\nIntent Classifier]
    end

    subgraph MCPServers["MCP Servers"]
        N[Filesystem Server\n@modelcontextprotocol]
        O[SQLite Server\n@modelcontextprotocol]
        P[Web Search Server\nCustom]
    end

    subgraph KnowledgeBase["Knowledge Base"]
        Q[company_policy.txt]
        R[employee_handbook.txt]
        S[it_security_guide.txt]
    end

    A -- user_query --> B
    B -- user_query --> C
    C -- tool_call --> D
    C -- crew_task --> E
    C -- history --> F
    C -- retrieval_request --> J
    J -- user_query --> I
    I -- embeddings --> H
    G -- file_content --> H
    G -- documents --> I
    Q & R & S --> G
    C -- tool_call --> K
    C -- nl_query --> L
    C -- search_query --> P
    C -- file_request --> N
    L -- sql_result --> C
    N -- file_content --> C
    O -- db_result --> C
    P -- search_result --> C
    E -- crew_output --> C
    J -- retrieved_docs --> C
    F -- conversation_history --> C
    B -- llm_output --> A
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- An Anthropic API key

### 1. Clone and configure
```bash
git clone https://github.com/meridian-corp/agentvault.git
cd agentvault
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Launch with Docker Compose
```bash
docker-compose up --build
```

### 3. Seed the knowledge base
```bash
docker-compose exec agentvault python scripts/seed_vectorstore.py
```

### 4. Open the chat interface
Navigate to [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Configuration

All configuration is managed through environment variables. See [`.env.example`](.env.example) for the full list.

| Variable | Description | Default |
|---|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | — |
| `OPENAI_API_KEY` | OpenAI API key for auxiliary classification | — |
| `APP_ENV` | Deployment environment | `production` |
| `CHROMA_PERSIST_DIR` | ChromaDB persistence directory | `./data/chroma` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| API Gateway | FastAPI + Uvicorn |
| LLM | Anthropic Claude (claude-3-haiku) |
| Agent Orchestration | LangGraph |
| Sub-agent Crew | CrewAI |
| RAG Chains | LangChain RetrievalQA |
| Document Ingestion | LlamaIndex |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace sentence-transformers |
| Code Execution | LangChain PythonREPL |
| MCP Integration | @modelcontextprotocol servers |
| Frontend | Vanilla HTML/JS + WebSockets |

---

## 📂 Project Structure

```
agentvault/
├── app/
│   ├── main.py              # FastAPI application and routes
│   ├── orchestrator.py      # LangGraph agent graph
│   ├── config.py            # Configuration management
│   ├── agents/              # Agent implementations
│   ├── rag/                 # RAG pipeline
│   ├── tools/               # LangChain tools
│   └── mcp/                 # Custom MCP servers
├── knowledge-base/          # Source documents for RAG
├── frontend/                # Web chat interface
├── scripts/                 # Utility scripts
└── docker-compose.yml
```

---

## 🤝 Contributing

Internal tool — please submit changes via Meridian Corp GitLab. See the IT Security Guide for data handling requirements before submitting PRs that touch PII or credentials.

---

*AgentVault is an internal Meridian Corp product. For support, contact the Platform Engineering team on Slack: #agentvault-support*
