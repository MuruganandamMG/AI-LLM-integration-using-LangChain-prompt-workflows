# Architecture & Technical Design

## Architecture Overview
The platform implements an asynchronous modular monolith built on FastAPI, LangChain, and SQLAlchemy 2.0.

```
Client (HTTP/REST)
   ↓
Middleware (CORS, RequestID, Correlation)
   ↓
API Routers (/auth, /habits, /recommendations, /analytics, /gamification, /reviews)
   ↓
Service Layer (HabitService, RecommendationService, AnalyticsService, GamificationService)
   ↓
AI Engine (LangChain LLM Factory: Gemini 1.5 Flash / OpenAI GPT-4o-mini)
   ↓
Database (Async SQLAlchemy 2.0 + SQLite WAL Mode)
```
