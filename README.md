# Aura AI — Intentional Habit Architecture & Focus Suite

A high-performance personal growth operating system and productivity suite built with **FastAPI**, **LangChain**, and **Async SQLAlchemy 2.0**, featuring dual LLM orchestration (**Google Gemini** & **OpenAI**).

Designed with a **clean, agency-tier white theme**, time-block habit architecture, deep-work Pomodoro studio with synthesized binaural audio, 30-day activity heatmaps, live AI conversational mentoring, and automated weekly debriefs.

---

## ✨ Key Features

### 🖥️ High-End White Theme Web UI
- **Light/White Aesthetic**: Crisp white canvas, double-bezel card structure, subtle slate typography, and zero generic AI bloat.
- **Time-Block Routine Architecture**: Group habits into **Morning Rituals**, **Afternoon Deep Work**, and **Evening Wind-Down** with estimated durations and priority levels.
- **One-Click Rapid Completion**: Subtle synthesized audio chimes and instant check-ins.
- **30-Day Activity Heatmap**: Visual consistency grid mapping daily check-in intensity and streaks.

### ⏱️ Focus Studio & Audio Synthesizer
- **Interactive Timer**: 25m Focus, 50m Deep Work, and 5m Break presets with dynamic countdown animation.
- **Synthesized Ambient Soundscapes**: Pure Web Audio API generators for **40Hz Binaural Beats**, **Deep Brown Noise**, and **Gentle Rain Drone** with volume controls.
- **Session Logging & History**: Records actual focus minutes to the backend (`POST /api/v1/analytics/focus-session`).
- **AI Focus Strategy**: Customized priming sequences, anti-distraction psychological defense tips, and acoustic recommendations.

### 💬 AI Growth Mentor (Live Chat)
- **Real-Time Conversational Coaching (`/api/v1/coach/chat`)**: Context-aware AI mentor with access to your active routines, streaks, and focus metrics.
- **Quick-Prompt Shortcuts**: Unblock procrastination, optimize morning routines, and audit current habits.

### 📋 Habit Management & Calendar Sync
- **Full Habit Lifecycle**: Create, edit, and delete habits across categories (*Productivity, Health, Mindfulness, Fitness, Learning*).
- **Calendar & Spreadsheet Export**:
  - **iCalendar (`.ics`)**: One-click sync to Google Calendar, Apple Calendar, and Outlook.
  - **CSV Export**: Download complete habit logs as spreadsheets.

### 🎮 Gamification & Daily Quests
- **Leveling Engine**: Earn XP per habit check-in, focus session, and quest completion.
- **Dynamic Daily Quests (`/api/v1/gamification/quests`)**: Real-time quest tracking with claimable XP rewards.
- **Achievement Badges**: Milestone unlock system (*First Step*, *Consistency Champion*, *Habit Architect*, *Centurion*).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | **FastAPI** (Python 3.10–3.13) with Async Routes & Correlation IDs |
| **AI Orchestration** | **LangChain**, Prompt Templates, Output Parsers |
| **LLM Providers** | **Google Gemini** (`gemini-1.5-flash`) & **OpenAI** (`gpt-4o-mini`) |
| **Database & ORM** | **SQLite + Async SQLAlchemy 2.0** (`aiosqlite`) |
| **Authentication** | OAuth2 Bearer Tokens, **JWT**, Bcrypt Hashing |
| **Frontend UI** | **Tailwind CSS**, Phosphor Icons, Web Audio API, Vanilla ES6+ SPA |
| **Testing & CI/CD** | **Pytest** (36 automated tests), GitHub Actions matrix (3.10, 3.11, 3.12) |

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
| `POST` | `/api/v1/auth/register` | Register a new user account |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT access token |
| `GET` | `/api/v1/auth/me` | Retrieve profile of authenticated user |

### 📋 Habits & Exports (`/api/v1/habits`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/habits/` | List all habits for current user |
| `POST` | `/api/v1/habits/` | Create a new habit with time_of_day and duration |
| `GET` | `/api/v1/habits/{id}` | Get habit details and completion history |
| `PUT` | `/api/v1/habits/{id}` | Update habit title, category, or schedule |
| `DELETE` | `/api/v1/habits/{id}` | Delete a habit |
| `POST` | `/api/v1/habits/{id}/log` | Log habit completion with mood score (1-5) and notes |
| `GET` | `/api/v1/habits/export/ics` | Export habits as iCalendar (`.ics`) file |
| `GET` | `/api/v1/habits/export/csv` | Export habits as CSV spreadsheet |

### 💬 AI Conversational Mentor (`/api/v1/coach`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/coach/chat` | Context-aware conversational AI coach chat |

### 🧠 AI Growth Recommendations (`/api/v1/recommendations`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/recommendations/generate` | Generate AI growth recommendation via LangChain |
| `GET` | `/api/v1/recommendations/` | List previous recommendations |

### 📊 Analytics & Focus Sessions (`/api/v1/analytics`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/analytics/summary` | Get completion rates, total logs, and longest streak |
| `GET` | `/api/v1/analytics/mood-trends` | Category-by-category mood & energy impact metrics |
| `POST` | `/api/v1/analytics/focus-session` | Log completed focus timer session |
| `GET` | `/api/v1/analytics/focus-sessions` | Get user focus session logs and total focus minutes |
| `POST` | `/api/v1/analytics/focus-strategy` | Generate AI priming steps and distraction defense |
| `POST` | `/api/v1/analytics/generate-report` | Generate comprehensive AI productivity report |
| `GET` | `/api/v1/analytics/reports` | List past productivity reports |

### 🎯 AI Reviews & Motivation (`/api/v1/reviews`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/reviews/weekly` | Synthesize weekly progress into wins and SMART goals |
| `GET` | `/api/v1/reviews/quote` | Generate dynamic motivational reflection quote |

### 🏆 Gamification & Quests (`/api/v1/gamification`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/gamification/profile` | Get XP score, rank tier, level, and badge showcase |
| `GET` | `/api/v1/gamification/quests` | List active daily quests and completion status |
| `POST` | `/api/v1/gamification/quests/{id}/claim` | Claim quest reward and earn XP |

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
