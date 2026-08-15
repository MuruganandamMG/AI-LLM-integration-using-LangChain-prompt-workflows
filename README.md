# AI-Driven Self-Improvement & Productivity Platform

An AI-driven backend API platform built with **FastAPI**, **Async SQLAlchemy 2.0**, and **LangChain** featuring dual LLM providers (**Google Gemini** & **OpenAI**). The platform powers personalized growth recommendations, habit tracking, daily logging, AI productivity analytics, gamification leveling, and AI weekly coaching reviews.

---

## Key Features

- **FastAPI Core**: Async REST API architecture with auto-generated Swagger UI (`/docs`) and correlation ID tracking.
- **User Authentication**: Secure JWT Bearer tokens with password hashing.
- **Habit & Log Tracking**: Full CRUD for habits along with daily progress and mood logs.
- **Gamification Engine**: XP leveling tiers (Bronze, Silver, Gold, Diamond) and milestone badges.
- **LangChain AI Workflows**:
  - **Growth Recommendations**: Evaluates active habits and generates actionable steps using Gemini / OpenAI.
  - **Productivity Analytics**: Evaluates 30-day consistency stats and delivers performance insights and burnout risk warnings.
  - **Weekly Coaching Reviews**: Executive AI debrief generating weekly performance assessments and next week's SMART goals.
- **Dual LLM Provider Support**: Supports Google Gemini (`gemini-1.5-flash`) and OpenAI (`gpt-4o-mini`) with automatic fallback handling.
- **CI/CD & Docker**: Automated GitHub Actions testing matrix and multi-stage Docker containerization.

---

## API Endpoints Overview

### Auth Router (`/api/v1/auth`)
- `POST /register`: Register user account.
- `POST /login`: Generate OAuth2 JWT access token.
- `GET /me`: Get authenticated user details.

### Habits Router (`/api/v1/habits`)
- `POST /`: Create habit.
- `GET /`: List user habits.
- `GET /{id}`: Retrieve habit details & logs.
- `POST /{id}/log`: Log daily habit completion and mood score.

### AI Recommendations (`/api/v1/recommendations`)
- `POST /generate`: Trigger LangChain growth recommendation workflow.
- `GET /`: List previous growth recommendations.

### Analytics Router (`/api/v1/analytics`)
- `GET /summary`: Get completion stats and streaks.
- `POST /generate-report`: Trigger LangChain analytics workflow.
- `GET /reports`: List past analytics reports.

### Gamification Router (`/api/v1/gamification`)
- `GET /profile`: Get user level, XP score, tier status, and unlocked badges.

### AI Weekly Reviews (`/api/v1/reviews`)
- `POST /weekly`: Generate an AI weekly debrief with SMART goals.

---

## Setup & Local Installation

1. **Clone repository & install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and add your LLM API keys:
   ```env
   OPENAI_API_KEY="your-openai-key"
   GOOGLE_API_KEY="your-google-gemini-key"
   ```

3. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Access API documentation at `http://127.0.0.1:8000/docs`.

4. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

5. **Run Test Suite**:
   ```bash
   pytest -v
   ```

6. **Export OpenAPI Schema**:
   ```bash
   python scripts/export_openapi.py
   ```
