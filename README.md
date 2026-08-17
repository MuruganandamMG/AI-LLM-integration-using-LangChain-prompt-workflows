# Aura AI — Intelligent Self-Improvement & Habit Coaching Platform

An intelligent self-improvement platform and productivity suite built with **FastAPI**, **LangChain**, and **Async SQLAlchemy 2.0**, featuring dual LLM orchestration (**Google Gemini** & **OpenAI**). 

The platform combines a **modern interactive Web UI**, habit tracking, deep-work Pomodoro timers, 30-day consistency heatmaps, calendar exports, gamification milestones, and automated AI weekly coaching debriefs.

---

## ✨ Key Features

### 🖥️ Interactive Web UI Dashboard
- **Single Page Application (SPA)**: Served directly from `/` with light/dark theme toggle, smooth micro-interactions, and instant **1-Click Demo Login**.
- **Daily AI Motivational Quote**: Dynamically generated coaching reflections and prompts tailored to user goals and streaks.
- **30-Day Activity Heatmap**: GitHub-style consistency grid visualizing daily check-in intensity and streaks.

### ⏱️ AI Focus Mode & Pomodoro Timer
- **Interactive Timer**: 25m Focus, 50m Deep Work, and 5m Break presets with dynamic countdown animation.
- **AI Focus Strategy Assistant**: Generates customized priming sequences, anti-distraction psychological defense tips, and acoustic soundscape recommendations for any given task.

### 📋 Habit Management & Calendar Sync
- **Full Habit CRUD**: Create, view, edit, and delete habits across categories (*Productivity, Health, Mindfulness, Fitness, Learning*).
- **Daily Reflection & Mood Logging**: Record completions with 1–5 mood score and notes.
- **Calendar & Spreadsheet Export**:
  - **iCalendar (`.ics`)**: One-click sync to Google Calendar, Apple Calendar, and Outlook.
  - **CSV Export**: Download complete habit logs as spreadsheets.

### 🤖 LangChain AI Workflows & Dual LLM Orchestration
- **Growth Recommendations (`growth_chain.py`)**: Analyzes habits and generates structured action protocols and scientific reasoning.
- **Productivity Analytics (`analytics_chain.py`)**: Synthesizes 30-day metrics, detects consistency bottlenecks, and flags burnout risks.
- **Weekly Coaching Reviews (`weekly_review_chain.py`)**: AI debrief generating overall sentiment, key wins, focus areas, and next week's SMART goals.
- **Motivational Reflections (`quote_chain.py`)**: Context-aware daily inspiration.
- **Dual LLM Provider with Auto-Fallback**: Seamlessly toggles between Google Gemini (`gemini-1.5-flash`) and OpenAI (`gpt-4o-mini`).

### 🎮 Gamification & XP System
- **Leveling Engine**: Earn +10 XP per habit completion and +25 XP per focus session.
- **Tiers**: Progress from *Bronze Explorer* to *Silver*, *Gold*, and *Diamond*.
- **Achievement Badges**: Unlock consistency milestones (e.g. *Streak Starter*, *Mindful Master*, *Centurion*).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | **FastAPI** (Python 3.10–3.13) with Async Routes & Correlation IDs |
| **AI Orchestration** | **LangChain**, Prompt Templates, JSON Output Parsers |
| **LLM Providers** | **Google Gemini** (`gemini-1.5-flash`) & **OpenAI** (`gpt-4o-mini`) |
| **Database & ORM** | **SQLite + Async SQLAlchemy 2.0** (`aiosqlite`) |
| **Authentication** | OAuth2 Bearer Tokens, **JWT**, Bcrypt Hashing |
| **Frontend UI** | **Tailwind CSS**, Phosphor Icons, Vanilla ES6+ SPA |
| **Testing & CI/CD** | **Pytest** (32 automated tests), GitHub Actions matrix (3.10, 3.11, 3.12) |

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/MuruganandamMG/AI-LLM-integration-using-LangChain-prompt-workflows.git
cd AI-LLM-integration-using-LangChain-prompt-workflows
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and configure your API keys (optional for mock mode):
```env
OPENAI_API_KEY="your-openai-api-key"
GOOGLE_API_KEY="your-google-gemini-api-key"
DEFAULT_LLM_PROVIDER="gemini"
SECRET_KEY="your-super-secret-jwt-key"
```

### 3. Start the Server
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Web Dashboard**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check**: [http://127.0.0.1:8000/healthcheck](http://127.0.0.1:8000/healthcheck)

---

## 📡 API Endpoints Reference

### 🔐 Authentication (`/api/v1/auth`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT access token |
| `GET` | `/api/v1/auth/me` | Retrieve profile of authenticated user |

### 📋 Habits & Exports (`/api/v1/habits`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/habits/` | List all habits for current user |
| `POST` | `/api/v1/habits/` | Create a new habit |
| `GET` | `/api/v1/habits/{id}` | Get habit details and completion history |
| `PUT` | `/api/v1/habits/{id}` | Update habit title, category, or schedule |
| `DELETE` | `/api/v1/habits/{id}` | Delete a habit |
| `POST` | `/api/v1/habits/{id}/log` | Log habit completion with mood score (1-5) and notes |
| `GET` | `/api/v1/habits/export/ics` | Export habits as iCalendar (`.ics`) file |
| `GET` | `/api/v1/habits/export/csv` | Export habits as CSV spreadsheet |

### 🧠 AI Growth Coach (`/api/v1/recommendations`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/recommendations/generate` | Generate AI growth recommendation via LangChain |
| `GET` | `/api/v1/recommendations/` | List previous recommendations |

### 📊 Analytics & Focus Mode (`/api/v1/analytics`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/analytics/summary` | Get completion rates, total logs, and longest streak |
| `POST` | `/api/v1/analytics/generate-report` | Generate comprehensive AI productivity report |
| `GET` | `/api/v1/analytics/reports` | List past productivity reports |
| `POST` | `/api/v1/analytics/focus-strategy` | Generate AI priming steps and distraction defense |

### 🎯 AI Reviews & Motivation (`/api/v1/reviews`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/reviews/weekly` | Synthesize weekly progress into wins and SMART goals |
| `GET` | `/api/v1/reviews/quote` | Generate dynamic motivational reflection quote |

### 🏆 Gamification (`/api/v1/gamification`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/gamification/profile` | Get XP score, rank tier, level, and badge showcase |

---

## 🧪 Testing

Run the full automated test suite:
```bash
pytest -v
```

---

## 🐳 Docker Deployment

Run with Docker Compose:
```bash
docker-compose up --build
```
