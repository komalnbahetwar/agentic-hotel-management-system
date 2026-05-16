# Agentic Hotel Management System

AI-powered hotel management assistant built using LangGraph, FastAPI, Streamlit, and OpenAI models.

This project demonstrates:
- Agentic AI workflows
- Tool calling
- Hotel room booking
- Food ordering
- Conversational memory
- FastAPI backend
- Streamlit frontend

---

# Tech Stack

- Python
- LangGraph
- LangChain
- FastAPI
- Streamlit
- OpenAI
- Uvicorn
- uv (Python package manager)

---

# Project Structure

```text
agentic-hotel-management-system/
│
├── app/
│   ├── main.py
│   ├── agents/
│   ├── tools/
│   └── services/
│
├── streamlit_app.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Prerequisites

Install:

- Python 3.11+
- uv

Install uv:

## Mac/Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Verify Installation

```bash
uv --version
```

---

# Clone Repository

```bash
git clone git@github.com:<your-username>/agentic-hotel-management-system.git
```

```bash
cd agentic-hotel-management-system
```

---

# Setup Environment

Create virtual environment and sync dependencies:

```bash
uv sync
```

This automatically:
- creates `.venv`
- installs dependencies
- prepares the project environment

---

# Install Additional Dependencies

If using requirements.txt:

```bash
uv pip install -r requirements.txt
```

---

# Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

# Run Backend (FastAPI)

Start backend server:

```bash
uv run uvicorn app.main:app --reload
```

Backend will start at:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

---

# Run Frontend (Streamlit)

Open another terminal and run:

```bash
uv run streamlit run streamlit_app.py
```

Frontend will start at:

```text
http://localhost:8501
```

---

# Example User Queries

Try asking:

```text
What rooms are available?
```

```text
Book room 105
```

```text
Book room 103 for Srikanth
```

```text
What south indian food is available?
```

```text
Order 2 servings of Pasta to room 105
```

```text
I want food bill for 105
```

---

# Development Commands

## Add New Package

```bash
uv add package_name
```

Example:

```bash
uv add langgraph
```

---

## Run Python File

```bash
uv run python app/main.py
```

---

## View Installed Packages

```bash
uv pip list
```

---

# Features

- Conversational hotel assistant
- Room booking workflow
- Food ordering workflow
- Multi-step reasoning
- Tool execution
- Memory-aware conversations
- Agent orchestration using LangGraph

---

# Future Enhancements

- Multi-agent architecture
- PostgreSQL integration
- Authentication & authorization
- Payment integration
- Vector database memory
- Voice assistant support
- WhatsApp integration
- Admin dashboard
- Kubernetes deployment

---

# Learning Objectives

This project is designed to help learn:
- LangGraph fundamentals
- Agentic AI systems
- AI workflow orchestration
- Tool calling
- FastAPI backend development
- Streamlit frontend integration
- Modern Python dependency management using uv

---

# Stop Applications

Press:

```text
CTRL + C
```

in terminal to stop running services.

---

# References

- LangGraph
- LangChain
- FastAPI
- Streamlit
- OpenAI
- uv
