# Design Specification: AI-Driven Self-Improvement & Productivity Platform

## Overview
An AI-powered self-improvement platform backend built with FastAPI, SQLite (Async SQLAlchemy 2.0), and LangChain. The system provides user authentication, habit tracking, daily logging, AI growth recommendations, and LLM-driven productivity analytics using Google Gemini and OpenAI APIs.

---

## 1. System Architecture & Module Structure

```
.
├── app/
│   ├── main.py                  # FastAPI application entry point, CORS, exception handlers
│   ├── config.py                # Pydantic Settings (Environment, API Keys, JWT Config)
│   ├── database.py              # Async SQLAlchemy engine, session maker, DB initialization
│   ├── core/
│   │   ├── security.py          # Password hashing (bcrypt/passlib) & JWT token encoding/decoding
│   │   └── deps.py              # FastAPI dependencies (get_db, get_current_user)
│   ├── models/                  # SQLAlchemy ORM Models
│   │   ├── user.py              # User model
│   │   ├── habit.py             # Habit & HabitLog models
│   │   ├── recommendation.py    # AI Growth Recommendation model
│   │   └── analytics.py         # AI Analytics Report model
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── user.py              # UserRegister, UserLogin, UserOut, Token
│   │   ├── habit.py             # HabitCreate, HabitOut, HabitLogCreate, HabitLogOut
│   │   ├── recommendation.py    # RecommendationCreate, RecommendationOut
│   │   └── analytics.py         # AnalyticsSummaryOut, AIInsightOut
│   ├── services/                # Business logic layer
│   │   ├── habit_service.py     # Habit CRUD and logging operations
│   │   ├── recommendation_service.py # Recommendation management & LLM triggers
│   │   └── analytics_service.py # Statistics calculation & LLM insights triggers
│   ├── ai/                      # LangChain Integration Layer
│   │   ├── factory.py           # Multi-provider LLM Factory (Gemini & OpenAI with fallback)
│   │   ├── prompts.py           # Structured ChatPromptTemplates
│   │   ├── growth_chain.py      # LangChain workflow for personalized growth plans
│   │   └── analytics_chain.py   # LangChain workflow for productivity analytics
│   └── api/                     # FastAPI Route Controllers
│       ├── v1/
│       │   ├── auth.py          # Auth endpoints: /register, /login, /me
│       │   ├── habits.py        # Habit CRUD & habit logging endpoints
│       │   ├── recommendations.py # AI growth recommendation endpoints
│       │   └── analytics.py     # AI analytics & productivity report endpoints
│       └── router.py            # API V1 router aggregator
├── scripts/
│   └── seed_git_history.py      # Backdated Git commit timeline generator script
├── tests/                       # Test suite with mock LLM responses
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_habits.py
│   ├── test_recommendations.py
│   └── test_analytics.py
├── .env.example                 # Environment variables template
├── requirements.txt             # Python dependencies
└── README.md                    # Setup, architecture details, and API documentation
```

---

## 2. Database Models Schema (SQLite + Async SQLAlchemy 2.0)

### `User`
- `id`: String (UUID PK)
- `email`: String (Unique, Indexed)
- `hashed_password`: String
- `full_name`: String
- `created_at`: DateTime (UTC)

### `Habit`
- `id`: String (UUID PK)
- `user_id`: String (FK -> User.id)
- `title`: String
- `description`: String (Optional)
- `category`: String (e.g., Fitness, Learning, Mindfulness, Productivity)
- `frequency`: String (daily, weekly)
- `created_at`: DateTime (UTC)

### `HabitLog`
- `id`: String (UUID PK)
- `habit_id`: String (FK -> Habit.id)
- `user_id`: String (FK -> User.id)
- `completed_at`: DateTime (UTC)
- `notes`: Text (Optional)
- `mood_score`: Integer (1-5, Optional)

### `Recommendation`
- `id`: String (UUID PK)
- `user_id`: String (FK -> User.id)
- `title`: String
- `category`: String
- `action_items`: JSON list of strings
- `reasoning`: Text
- `llm_provider`: String ("gemini" or "openai")
- `created_at`: DateTime (UTC)

### `AnalyticsReport`
- `id`: String (UUID PK)
- `user_id`: String (FK -> User.id)
- `total_habits`: Integer
- `completion_rate`: Float
- `longest_streak`: Integer
- `ai_summary`: Text
- `key_takeaways`: JSON list of strings
- `created_at`: DateTime (UTC)

---

## 3. AI & LangChain Architecture

### Provider Strategy
- Supports `google-generativeai` (Gemini 1.5 Flash / Pro) and `openai` (GPT-4o / GPT-4o-mini).
- Configurable primary provider via environment variable `DEFAULT_LLM_PROVIDER` (`gemini` or `openai`).
- Graceful fallback: If primary provider fails or lacks API key, automatically routes to secondary provider. If neither API key is set, returns mock response in dev mode.

### Prompt Workflows
1. **Growth Recommendation Workflow**:
   - Context: User profile, current active habits, 14-day completion stats.
   - Prompt: System instructions with JSON schema requirements.
   - Output: Structured `RecommendationOut` schema via LangChain `PydanticOutputParser`.

2. **Productivity Analytics Workflow**:
   - Context: 30-day log history, completion rates, missed habits.
   - Prompt: Analysis instructions evaluating momentum, burnout risk, and habit consistency.
   - Output: Structured `AnalyticsReport` summary and actionable advice.

---

## 4. API Endpoints Specification

### Authentication (`/api/v1/auth`)
- `POST /register`: Create new user account.
- `POST /login`: Generate OAuth2 Bearer JWT access token.
- `GET /me`: Fetch authenticated user profile.

### Habit Management (`/api/v1/habits`)
- `GET /`: List all habits for current user.
- `POST /`: Create a new habit.
- `GET /{id}`: Retrieve habit details and logs.
- `PUT /{id}`: Update habit details.
- `DELETE /{id}`: Delete habit.
- `POST /{id}/log`: Record a daily completion entry.

### AI Growth Recommendations (`/api/v1/recommendations`)
- `POST /generate`: Trigger LangChain growth recommendation workflow and save report.
- `GET /`: Retrieve previous recommendations history.

### Analytics & Insights (`/api/v1/analytics`)
- `GET /summary`: Compute habit completion stats (total logs, rates, streaks).
- `POST /generate-report`: Trigger LangChain analytics workflow to create comprehensive AI insights report.
- `GET /reports`: List past analytics reports.

---

## 5. Backdated Git History Generator Strategy

A script (`scripts/seed_git_history.py`) will automate backdated commits across chronological milestones:
1. **Day -14**: Base FastAPI setup, Pydantic settings, DB initialization.
2. **Day -12**: User model, authentication security utils, JWT registration/login APIs.
3. **Day -10**: Habit and HabitLog database models, CRUD services, habit APIs.
4. **Day -7**: LangChain provider factory setup, OpenAI & Gemini LLM integrations.
5. **Day -5**: AI Growth Recommendation workflow and endpoints.
6. **Day -3**: AI Analytics & Productivity insights workflow and endpoints.
7. **Day -1**: Unit tests, README documentation, and final polish.

The script runs `git init`, configures author dates using `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`, creates commit snapshots step-by-step, and outputs instructions for pushing to GitHub.
