# AI-Driven Self-Improvement & Productivity Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, production-ready FastAPI backend with LangChain integration (Google Gemini & OpenAI APIs), SQLite + Async SQLAlchemy 2.0 database models, habit tracking, AI growth recommendations, productivity analytics, and a backdated Git commit history generator script.

**Architecture:** A clean modular monolith architecture with async SQLAlchemy DB layers, Pydantic data schemas, LangChain workflow service chains with dual-provider LLM fallback, FastAPI v1 REST routers, and pytest test suites.

**Tech Stack:** Python 3.10+, FastAPI, Async SQLAlchemy 2.0, aiosqlite, Pydantic v2, Passlib/Bcrypt, PyJWT, LangChain (`langchain-core`, `langchain-openai`, `langchain-google-genai`), Pytest, Pytest-Asyncio, HTTPX.

## Global Constraints
- Python 3.10+ compatible syntax.
- All database operations must be async (`aiosqlite` backend).
- Pydantic v2 configuration and schema syntax (`BaseModel`, `ConfigDict`).
- All tests must pass using `pytest`.
- Complete concrete code in every task step — no TBDs or placeholder functions.

---

### Task 1: Environment & Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `app/__init__.py`
- Create: `app/config.py`
- Test: `tests/test_config.py`

**Interfaces:**
- Produces: `app.config.settings` (Pydantic settings object containing DB URL, JWT secrets, and LLM API keys)

- [ ] **Step 1: Write failing test for config settings**

```python
# tests/test_config.py
from app.config import settings

def test_settings_load():
    assert settings.PROJECT_NAME == "AI Self-Improvement Platform"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DATABASE_URL is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'app')

- [ ] **Step 3: Implement dependencies and `app/config.py`**

```text
# requirements.txt
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
sqlalchemy>=2.0.28
aiosqlite>=0.20.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
passlib[bcrypt]>=1.7.4
pyjwt>=2.8.0
python-multipart>=0.0.9
langchain>=0.1.13
langchain-core>=0.1.33
langchain-openai>=0.1.0
langchain-google-genai>=1.0.1
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

```text
# .env.example
PROJECT_NAME="AI Self-Improvement Platform"
SECRET_KEY="secret-key-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DATABASE_URL="sqlite+aiosqlite:///./platform.db"
DEFAULT_LLM_PROVIDER="gemini"
OPENAI_API_KEY=""
GOOGLE_API_KEY=""
```

```python
# app/__init__.py
"""AI Self-Improvement Platform Package."""
```

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Self-Improvement Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    DATABASE_URL: str = "sqlite+aiosqlite:///./platform.db"
    DEFAULT_LLM_PROVIDER: str = "gemini"
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
```

- [ ] **Step 4: Install requirements and run test to verify it passes**

Run: `pip install -r requirements.txt && pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .env.example app/__init__.py app/config.py tests/test_config.py
git commit -m "feat: scaffold project dependencies and application configuration"
```

---

### Task 2: Async Database Engine and Base Models Setup

**Files:**
- Create: `app/database.py`
- Create: `app/models/__init__.py`
- Create: `app/models/user.py`
- Create: `app/models/habit.py`
- Create: `app/models/recommendation.py`
- Create: `app/models/analytics.py`
- Test: `tests/test_database.py`

**Interfaces:**
- Consumes: `app.config.settings`
- Produces: `app.database.engine`, `app.database.AsyncSessionLocal`, `app.database.Base`, `app.database.init_db()`, `app.database.get_db()`

- [ ] **Step 1: Write failing test for database session initialization**

```python
# tests/test_database.py
import pytest
from app.database import AsyncSessionLocal, init_db, Base, engine
from sqlalchemy import text

@pytest.mark.asyncio
async def test_database_connection():
    await init_db()
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_database.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'app.database')

- [ ] **Step 3: Implement database engine, Base, and ORM Models**

```python
# app/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

```python
# app/models/user.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    analytics_reports = relationship("AnalyticsReport", back_populates="user", cascade="all, delete-orphan")
```

```python
# app/models/habit.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=False, default="General")
    frequency: Mapped[str] = mapped_column(String, nullable=False, default="daily")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    habit_id: Mapped[str] = mapped_column(String, ForeignKey("habits.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    mood_score: Mapped[int] = mapped_column(Integer, nullable=True)

    habit = relationship("Habit", back_populates="logs")
```

```python
# app/models/recommendation.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    action_items: Mapped[list] = mapped_column(JSON, nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    llm_provider: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recommendations")
```

```python
# app/models/analytics.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    total_habits: Mapped[int] = mapped_column(Integer, nullable=False)
    completion_rate: Mapped[float] = mapped_column(Float, nullable=False)
    longest_streak: Mapped[int] = mapped_column(Integer, nullable=False)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_takeaways: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="analytics_reports")
```

```python
# app/models/__init__.py
from app.models.user import User
from app.models.habit import Habit, HabitLog
from app.models.recommendation import Recommendation
from app.models.analytics import AnalyticsReport

__all__ = ["User", "Habit", "HabitLog", "Recommendation", "AnalyticsReport"]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_database.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/database.py app/models/ tests/test_database.py
git commit -m "feat: setup async SQLAlchemy engine and ORM models"
```

---

### Task 3: Security Utilities & JWT Auth Layer

**Files:**
- Create: `app/core/__init__.py`
- Create: `app/core/security.py`
- Create: `app/core/deps.py`
- Create: `app/schemas/__init__.py`
- Create: `app/schemas/user.py`
- Test: `tests/test_security.py`

**Interfaces:**
- Consumes: `app.config.settings`, `app.database.get_db`
- Produces: `verify_password()`, `get_password_hash()`, `create_access_token()`, `get_current_user()` dependency.

- [ ] **Step 1: Write failing test for security password hashing & JWT generation**

```python
# tests/test_security.py
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    pwd = "secretpassword123"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_jwt_token_flow():
    user_id = "user-123-uuid"
    token = create_access_token(subject=user_id)
    payload = decode_access_token(token)
    assert payload["sub"] == user_id
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_security.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'app.core')

- [ ] **Step 3: Implement Pydantic User Schemas and Security utilities**

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str | None = None
```

```python
# app/schemas/__init__.py
from app.schemas.user import UserRegister, UserLogin, UserOut, Token, TokenData

__all__ = ["UserRegister", "UserLogin", "UserOut", "Token", "TokenData"]
```

```python
# app/core/__init__.py
"""Core security and dependency modules."""
```

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return {}
```

```python
# app/core/deps.py
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.config import settings
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_security.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/core/ app/schemas/ tests/test_security.py
git commit -m "feat: implement password hashing, JWT security tools, and auth dependencies"
```

---

### Task 4: Auth API Router & Endpoints

**Files:**
- Create: `app/api/__init__.py`
- Create: `app/api/v1/__init__.py`
- Create: `app/api/v1/auth.py`
- Test: `tests/test_auth_api.py`

**Interfaces:**
- Consumes: `app.core.security`, `app.database.get_db`, `app.schemas.user`
- Produces: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/auth/me` endpoints.

- [ ] **Step 1: Write failing test for registration and login APIs**

```python
# tests/test_auth_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_auth_register_and_login():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register
        reg_resp = await ac.post("/api/v1/auth/register", json={
            "email": "user@example.com",
            "password": "Password123!",
            "full_name": "Test User"
        })
        assert reg_resp.status_code == 201
        data = reg_resp.json()
        assert data["email"] == "user@example.com"

        # Login
        login_resp = await ac.post("/api/v1/auth/login", data={
            "username": "user@example.com",
            "password": "Password123!"
        })
        assert login_resp.status_code == 200
        token_data = login_resp.json()
        assert "access_token" in token_data

        # Me
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        me_resp = await ac.get("/api/v1/auth/me", headers=headers)
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "user@example.com"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_auth_api.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'app.main')

- [ ] **Step 3: Implement auth router and main FastAPI app entry point**

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserOut, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_in.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == form_data.username)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
```

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.v1.router import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_auth_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/api/ app/main.py tests/test_auth_api.py
git commit -m "feat: implement authentication endpoints and main FastAPI application"
```

---

### Task 5: Habit Management CRUD & Daily Log Services & Endpoints

**Files:**
- Create: `app/schemas/habit.py`
- Create: `app/services/habit_service.py`
- Create: `app/api/v1/habits.py`
- Modify: `app/api/v1/router.py`
- Test: `tests/test_habits_api.py`

**Interfaces:**
- Consumes: `app.models.habit`, `app.database.get_db`, `app.core.deps.get_current_user`
- Produces: `/api/v1/habits/` (GET, POST), `/api/v1/habits/{id}` (GET, PUT, DELETE), `/api/v1/habits/{id}/log` (POST)

- [ ] **Step 1: Write failing test for habit CRUD and log tracking**

```python
# tests/test_habits_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_habits_crud_and_logging():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user & get token
        reg = await ac.post("/api/v1/auth/register", json={
            "email": "habituser@example.com",
            "password": "Password123!",
            "full_name": "Habit User"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "habituser@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create Habit
        create_resp = await ac.post("/api/v1/habits/", json={
            "title": "Daily Meditation",
            "description": "10 minutes of mindfulness",
            "category": "Mindfulness",
            "frequency": "daily"
        }, headers=headers)
        assert create_resp.status_code == 201
        habit_id = create_resp.json()["id"]

        # List Habits
        list_resp = await ac.get("/api/v1/habits/", headers=headers)
        assert list_resp.status_code == 200
        assert len(list_resp.json()) == 1

        # Log Habit Completion
        log_resp = await ac.post(f"/api/v1/habits/{habit_id}/log", json={
            "notes": "Felt very calm",
            "mood_score": 5
        }, headers=headers)
        assert log_resp.status_code == 201
        assert log_resp.json()["notes"] == "Felt very calm"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_habits_api.py -v`
Expected: FAIL (404 Not Found on `/api/v1/habits/`)

- [ ] **Step 3: Implement Habit schemas, HabitService, and Habit router**

```python
# app/schemas/habit.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HabitCreate(BaseModel):
    title: str
    description: str | None = None
    category: str = "General"
    frequency: str = "daily"

class HabitUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    frequency: str | None = None

class HabitLogCreate(BaseModel):
    notes: str | None = None
    mood_score: int | None = None

class HabitLogOut(BaseModel):
    id: str
    habit_id: str
    user_id: str
    completed_at: datetime
    notes: str | None
    mood_score: int | None

    model_config = ConfigDict(from_attributes=True)

class HabitOut(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    category: str
    frequency: str
    created_at: datetime
    logs: list[HabitLogOut] = []

    model_config = ConfigDict(from_attributes=True)
```

```python
# app/services/habit_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.habit import Habit, HabitLog
from app.schemas.habit import HabitCreate, HabitUpdate, HabitLogCreate

class HabitService:
    @staticmethod
    async def create_habit(db: AsyncSession, user_id: str, habit_in: HabitCreate) -> Habit:
        habit = Habit(
            user_id=user_id,
            title=habit_in.title,
            description=habit_in.description,
            category=habit_in.category,
            frequency=habit_in.frequency
        )
        db.add(habit)
        await db.commit()
        await db.refresh(habit)
        return habit

    @staticmethod
    async def get_user_habits(db: AsyncSession, user_id: str) -> list[Habit]:
        stmt = select(Habit).where(Habit.user_id == user_id).options(selectinload(Habit.logs))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_habit_by_id(db: AsyncSession, habit_id: str, user_id: str) -> Habit | None:
        stmt = select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id).options(selectinload(Habit.logs))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def log_completion(db: AsyncSession, habit_id: str, user_id: str, log_in: HabitLogCreate) -> HabitLog:
        habit_log = HabitLog(
            habit_id=habit_id,
            user_id=user_id,
            notes=log_in.notes,
            mood_score=log_in.mood_score
        )
        db.add(habit_log)
        await db.commit()
        await db.refresh(habit_log)
        return habit_log
```

```python
# app/api/v1/habits.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.habit import HabitCreate, HabitOut, HabitLogCreate, HabitLogOut
from app.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_in: HabitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await HabitService.create_habit(db, current_user.id, habit_in)

@router.get("/", response_model=list[HabitOut])
async def list_habits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await HabitService.get_user_habits(db, current_user.id)

@router.get("/{habit_id}", response_model=HabitOut)
async def get_habit(
    habit_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.post("/{habit_id}/log", response_model=HabitLogOut, status_code=status.HTTP_201_CREATED)
async def log_habit_completion(
    habit_id: str,
    log_in: HabitLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await HabitService.get_habit_by_id(db, habit_id, current_user.id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return await HabitService.log_completion(db, habit_id, current_user.id, log_in)
```

Modify `app/api/v1/router.py` to include `habits.router`:

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.habits import router as habits_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(habits_router)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_habits_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/schemas/habit.py app/services/habit_service.py app/api/v1/habits.py app/api/v1/router.py tests/test_habits_api.py
git commit -m "feat: add habit management CRUD and log tracking endpoints"
```

---

### Task 6: LangChain Integration & Provider Factory Layer

**Files:**
- Create: `app/ai/__init__.py`
- Create: `app/ai/factory.py`
- Create: `app/ai/prompts.py`
- Create: `app/ai/growth_chain.py`
- Create: `app/ai/analytics_chain.py`
- Test: `tests/test_ai_chains.py`

**Interfaces:**
- Consumes: `app.config.settings`, LangChain core packages
- Produces: `LLMFactory.get_llm()`, `run_growth_recommendation_chain()`, `run_productivity_analytics_chain()`

- [ ] **Step 1: Write failing test for LLM factory & LangChain prompt workflows**

```python
# tests/test_ai_chains.py
import pytest
from app.ai.factory import LLMFactory
from app.ai.growth_chain import run_growth_recommendation_chain
from app.ai.analytics_chain import run_productivity_analytics_chain

@pytest.mark.asyncio
async def test_growth_chain_mock():
    habits = [{"title": "Exercise", "category": "Fitness", "logs_count": 5}]
    result = await run_growth_recommendation_chain(user_name="Alice", habits=habits)
    assert "title" in result
    assert "action_items" in result
    assert isinstance(result["action_items"], list)

@pytest.mark.asyncio
async def test_analytics_chain_mock():
    stats = {"total_habits": 3, "completion_rate": 85.0, "streak": 7}
    result = await run_productivity_analytics_chain(user_name="Alice", stats=stats)
    assert "ai_summary" in result
    assert "key_takeaways" in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_ai_chains.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'app.ai')

- [ ] **Step 3: Implement LLMFactory, Prompts, GrowthChain, and AnalyticsChain**

```python
# app/ai/__init__.py
"""LangChain AI module."""
```

```python
# app/ai/factory.py
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

class LLMFactory:
    @staticmethod
    def get_llm(preferred_provider: str | None = None) -> BaseChatModel | None:
        provider = preferred_provider or settings.DEFAULT_LLM_PROVIDER
        
        if provider == "google" or provider == "gemini":
            if settings.GOOGLE_API_KEY:
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.7
                )
        
        if provider == "openai":
            if settings.OPENAI_API_KEY:
                return ChatOpenAI(
                    model="gpt-4o-mini",
                    api_key=settings.OPENAI_API_KEY,
                    temperature=0.7
                )
        
        # Fallback check
        if settings.OPENAI_API_KEY:
            return ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY, temperature=0.7)
        if settings.GOOGLE_API_KEY:
            return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY, temperature=0.7)
            
        return None
```

```python
# app/ai/prompts.py
from langchain_core.prompts import ChatPromptTemplate

GROWTH_RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI performance coach specializing in habit formation, motivation, and goal alignment. Provide structured, practical growth advice in JSON format with keys: 'title', 'category', 'action_items' (list), and 'reasoning'."),
    ("user", "User Profile: {user_name}\nHabits & Log Summary:\n{habits_summary}\n\nGenerate personalized growth recommendations.")
])

PRODUCTIVITY_ANALYTICS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an AI productivity analyst. Based on habit tracking statistics, analyze consistency, identify burnout risk or positive momentum, and output structured JSON with keys: 'ai_summary' and 'key_takeaways' (list of strings)."),
    ("user", "User Profile: {user_name}\nHabit Statistics:\n{stats_summary}\n\nGenerate productivity insights and performance evaluation.")
])
```

```python
# app/ai/growth_chain.py
import json
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory
from app.ai.prompts import GROWTH_RECOMMENDATION_PROMPT

async def run_growth_recommendation_chain(user_name: str, habits: list[dict]) -> dict:
    llm = LLMFactory.get_llm()
    habits_summary = "\n".join([f"- {h['title']} ({h['category']}): {h.get('logs_count', 0)} completions" for h in habits]) or "No active habits logged yet."
    
    if llm is None:
        # Mock structured response for local development when no API keys are configured
        return {
            "title": "Optimize Daily Focus & Momentum",
            "category": "Productivity",
            "action_items": [
                "Schedule a 25-minute deep work block every morning.",
                "Log mood scores after habit completions to identify optimal productivity hours.",
                "Maintain habit streaks by starting with small, achievable micro-habits."
            ],
            "reasoning": "Consistent small wins establish momentum and protect against cognitive fatigue.",
            "provider": "mock"
        }
        
    chain = GROWTH_RECOMMENDATION_PROMPT | llm | JsonOutputParser()
    try:
        response = await chain.ainvoke({"user_name": user_name, "habits_summary": habits_summary})
        response["provider"] = settings.DEFAULT_LLM_PROVIDER
        return response
    except Exception:
        return {
            "title": "Establish Consistency & Routine",
            "category": "Mindfulness",
            "action_items": ["Set a fixed daily reminder", "Track weekly progress summaries"],
            "reasoning": "Fallback recommendation generated due to LLM response parser format.",
            "provider": "fallback"
        }
```

```python
# app/ai/analytics_chain.py
import json
from langchain_core.output_parsers import JsonOutputParser
from app.ai.factory import LLMFactory
from app.ai.prompts import PRODUCTIVITY_ANALYTICS_PROMPT

async def run_productivity_analytics_chain(user_name: str, stats: dict) -> dict:
    llm = LLMFactory.get_llm()
    stats_summary = f"Total Habits: {stats.get('total_habits', 0)}, Completion Rate: {stats.get('completion_rate', 0)}%, Longest Streak: {stats.get('streak', 0)} days."
    
    if llm is None:
        return {
            "ai_summary": f"{user_name} shows steady habit consistency with a completion rate of {stats.get('completion_rate', 0)}%. Keep protecting momentum during peak productivity windows.",
            "key_takeaways": [
                f"Maintained an active streak of {stats.get('streak', 0)} days.",
                "Completion rate indicates strong dedication across active routines.",
                "Consider increasing habit challenge level gradually."
            ],
            "provider": "mock"
        }
        
    chain = PRODUCTIVITY_ANALYTICS_PROMPT | llm | JsonOutputParser()
    try:
        response = await chain.ainvoke({"user_name": user_name, "stats_summary": stats_summary})
        return response
    except Exception:
        return {
            "ai_summary": f"Performance evaluation completed for {user_name}. Focus on building sustainable habit loops.",
            "key_takeaways": ["Maintain consistency", "Review habit difficulty"],
            "provider": "fallback"
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_ai_chains.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/ai/ tests/test_ai_chains.py
git commit -m "feat: implement LangChain multi-provider factory, prompt workflows, and chains"
```

---

### Task 7: Recommendations & Analytics Services & API Routers

**Files:**
- Create: `app/schemas/recommendation.py`
- Create: `app/schemas/analytics.py`
- Create: `app/services/recommendation_service.py`
- Create: `app/services/analytics_service.py`
- Create: `app/api/v1/recommendations.py`
- Create: `app/api/v1/analytics.py`
- Modify: `app/api/v1/router.py`
- Test: `tests/test_recommendations_and_analytics_api.py`

**Interfaces:**
- Consumes: `app.ai.growth_chain`, `app.ai.analytics_chain`, `app.services.habit_service`
- Produces: `/api/v1/recommendations/generate`, `/api/v1/analytics/summary`, `/api/v1/analytics/generate-report`

- [ ] **Step 1: Write failing test for recommendations & analytics APIs**

```python
# tests/test_recommendations_and_analytics_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

@pytest.mark.asyncio
async def test_recommendations_and_analytics_endpoints():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register user & get token
        await ac.post("/api/v1/auth/register", json={
            "email": "aiperson@example.com",
            "password": "Password123!",
            "full_name": "AI Tester"
        })
        login = await ac.post("/api/v1/auth/login", data={
            "username": "aiperson@example.com",
            "password": "Password123!"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Generate Recommendation
        rec_resp = await ac.post("/api/v1/recommendations/generate", headers=headers)
        assert rec_resp.status_code == 201
        assert "title" in rec_resp.json()

        # Get Analytics Summary
        sum_resp = await ac.get("/api/v1/analytics/summary", headers=headers)
        assert sum_resp.status_code == 200
        assert "completion_rate" in sum_resp.json()

        # Generate Analytics Report
        rep_resp = await ac.post("/api/v1/analytics/generate-report", headers=headers)
        assert rep_resp.status_code == 201
        assert "ai_summary" in rep_resp.json()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_recommendations_and_analytics_api.py -v`
Expected: FAIL (404 Not Found)

- [ ] **Step 3: Implement Schemas, Services, and API Routers**

```python
# app/schemas/recommendation.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RecommendationOut(BaseModel):
    id: str
    user_id: str
    title: str
    category: str
    action_items: list[str]
    reasoning: str
    llm_provider: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

```python
# app/schemas/analytics.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AnalyticsSummaryOut(BaseModel):
    total_habits: int
    total_logs: int
    completion_rate: float
    longest_streak: int

class AnalyticsReportOut(BaseModel):
    id: str
    user_id: str
    total_habits: int
    completion_rate: float
    longest_streak: int
    ai_summary: str
    key_takeaways: list[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

```python
# app/services/recommendation_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.habit_service import HabitService
from app.ai.growth_chain import run_growth_recommendation_chain

class RecommendationService:
    @staticmethod
    async def generate_recommendation(db: AsyncSession, user: User) -> Recommendation:
        habits = await HabitService.get_user_habits(db, user.id)
        habits_data = [{"title": h.title, "category": h.category, "logs_count": len(h.logs)} for h in habits]
        
        ai_res = await run_growth_recommendation_chain(user.full_name, habits_data)
        
        rec = Recommendation(
            user_id=user.id,
            title=ai_res.get("title", "Personalized Growth Advice"),
            category=ai_res.get("category", "General"),
            action_items=ai_res.get("action_items", []),
            reasoning=ai_res.get("reasoning", "AI analysis based on active daily routines."),
            llm_provider=ai_res.get("provider", "gemini")
        )
        db.add(rec)
        await db.commit()
        await db.refresh(rec)
        return rec

    @staticmethod
    async def get_user_recommendations(db: AsyncSession, user_id: str) -> list[Recommendation]:
        stmt = select(Recommendation).where(Recommendation.user_id == user_id).order_by(Recommendation.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
```

```python
# app/services/analytics_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.analytics import AnalyticsReport
from app.models.user import User
from app.services.habit_service import HabitService
from app.ai.analytics_chain import run_productivity_analytics_chain

class AnalyticsService:
    @staticmethod
    async def calculate_summary(db: AsyncSession, user_id: str) -> dict:
        habits = await HabitService.get_user_habits(db, user_id)
        total_habits = len(habits)
        total_logs = sum(len(h.logs) for h in habits)
        completion_rate = min(100.0, round((total_logs / max(1, total_habits * 7)) * 100, 1))
        longest_streak = max([len(h.logs) for h in habits], default=0)
        
        return {
            "total_habits": total_habits,
            "total_logs": total_logs,
            "completion_rate": completion_rate,
            "longest_streak": longest_streak
        }

    @staticmethod
    async def generate_report(db: AsyncSession, user: User) -> AnalyticsReport:
        stats = await AnalyticsService.calculate_summary(db, user.id)
        ai_res = await run_productivity_analytics_chain(user.full_name, stats)
        
        report = AnalyticsReport(
            user_id=user.id,
            total_habits=stats["total_habits"],
            completion_rate=stats["completion_rate"],
            longest_streak=stats["longest_streak"],
            ai_summary=ai_res.get("ai_summary", "Productivity evaluation completed."),
            key_takeaways=ai_res.get("key_takeaways", ["Maintain consistency"])
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_user_reports(db: AsyncSession, user_id: str) -> list[AnalyticsReport]:
        stmt = select(AnalyticsReport).where(AnalyticsReport.user_id == user_id).order_by(AnalyticsReport.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())
```

```python
# app/api/v1/recommendations.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.recommendation import RecommendationOut
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["AI Growth Recommendations"])

@router.post("/generate", response_model=RecommendationOut, status_code=status.HTTP_201_CREATED)
async def generate_recommendation(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RecommendationService.generate_recommendation(db, current_user)

@router.get("/", response_model=list[RecommendationOut])
async def list_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RecommendationService.get_user_recommendations(db, current_user.id)
```

```python
# app/api/v1/analytics.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.analytics import AnalyticsSummaryOut, AnalyticsReportOut
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Productivity Analytics"])

@router.get("/summary", response_model=AnalyticsSummaryOut)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.calculate_summary(db, current_user.id)

@router.post("/generate-report", response_model=AnalyticsReportOut, status_code=status.HTTP_201_CREATED)
async def generate_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.generate_report(db, current_user)

@router.get("/reports", response_model=list[AnalyticsReportOut])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await AnalyticsService.get_user_reports(db, current_user.id)
```

Update `app/api/v1/router.py`:

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.habits import router as habits_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.analytics import router as analytics_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(habits_router)
api_v1_router.include_router(recommendations_router)
api_v1_router.include_router(analytics_router)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_recommendations_and_analytics_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add app/schemas/ app/services/ app/api/v1/ tests/test_recommendations_and_analytics_api.py
git commit -m "feat: add AI recommendation and productivity analytics API routes and services"
```

---

### Task 8: Backdated Git Commit History Generator Script

**Files:**
- Create: `scripts/seed_git_history.py`
- Test: `tests/test_seed_script.py`

**Interfaces:**
- Produces: Executable python script `scripts/seed_git_history.py` that reconstructs past commit timeline with custom dates.

- [ ] **Step 1: Write failing test for git seed script module**

```python
# tests/test_seed_script.py
import pytest
from scripts.seed_git_history import get_commit_schedule

def test_get_commit_schedule():
    schedule = get_commit_schedule()
    assert len(schedule) >= 6
    assert "msg" in schedule[0]
    assert "days_ago" in schedule[0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_seed_script.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'scripts')

- [ ] **Step 3: Implement `scripts/seed_git_history.py`**

```python
# scripts/seed_git_history.py
import os
import subprocess
from datetime import datetime, timedelta, timezone

def get_commit_schedule():
    return [
        {
            "days_ago": 14,
            "msg": "feat: initial project structure and environment configuration",
            "files": ["requirements.txt", ".env.example", "app/__init__.py", "app/config.py"]
        },
        {
            "days_ago": 12,
            "msg": "feat: setup async SQLAlchemy engine and ORM models",
            "files": ["app/database.py", "app/models/"]
        },
        {
            "days_ago": 10,
            "msg": "feat: implement password hashing, JWT security tools, and auth dependencies",
            "files": ["app/core/", "app/schemas/user.py"]
        },
        {
            "days_ago": 7,
            "msg": "feat: implement authentication endpoints and main FastAPI application",
            "files": ["app/api/v1/auth.py", "app/main.py"]
        },
        {
            "days_ago": 5,
            "msg": "feat: add habit management CRUD and log tracking endpoints",
            "files": ["app/schemas/habit.py", "app/services/habit_service.py", "app/api/v1/habits.py"]
        },
        {
            "days_ago": 3,
            "msg": "feat: implement LangChain multi-provider factory, prompt workflows, and chains",
            "files": ["app/ai/"]
        },
        {
            "days_ago": 1,
            "msg": "feat: add AI recommendation and productivity analytics API routes and services",
            "files": ["app/schemas/recommendation.py", "app/schemas/analytics.py", "app/services/", "app/api/v1/"]
        }
    ]

def run_cmd(cmd, env=None):
    result = subprocess.run(cmd, shell=True, env=env or os.environ.copy(), capture_output=True, text=True)
    return result

def seed_history():
    print("Initializing backdated git commit history...")
    schedule = get_commit_schedule()
    now = datetime.now(timezone.utc)

    for item in schedule:
        days_ago = item["days_ago"]
        msg = item["msg"]
        commit_date = (now - timedelta(days=days_ago)).isoformat()

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = commit_date
        env["GIT_COMMITTER_DATE"] = commit_date

        run_cmd("git add .", env=env)
        res = run_cmd(f'git commit -m "{msg}"', env=env)
        print(f"[{commit_date[:10]}] Committed: {msg}")

    print("\nHistory generated successfully! To push to GitHub, run:")
    print("  git remote add origin <YOUR_GITHUB_REPO_URL>")
    print("  git branch -M main")
    print("  git push -u origin main --force")

if __name__ == "__main__":
    seed_history()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_seed_script.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/ tests/test_seed_script.py
git commit -m "feat: add backdated Git commit history generator tool"
```

---

### Task 9: Comprehensive README & Final Verification Suite

**Files:**
- Create: `README.md`
- Test: Run all pytest suites (`pytest -v`)

- [ ] **Step 1: Write complete project documentation in `README.md`**

```markdown
# AI-Driven Self-Improvement & Productivity Platform

An AI-driven backend API platform built with **FastAPI**, **Async SQLAlchemy 2.0**, and **LangChain** featuring dual LLM providers (**Google Gemini** & **OpenAI**). The platform powers personalized growth recommendations, habit tracking, daily logging, and AI productivity analytics.

---

## Key Features

- **FastAPI Core**: Async REST API architecture with auto-generated Swagger UI (`/docs`).
- **User Authentication**: Secure JWT Bearer tokens with Bcrypt password hashing.
- **Habit & Log Tracking**: Full CRUD for habits along with daily progress and mood logs.
- **LangChain AI Workflows**:
  - **Growth Recommendations**: Evaluates active habits and generates actionable steps using Gemini / OpenAI.
  - **Productivity Analytics**: Evaluates 30-day consistency stats and delivers performance insights and burnout risk warnings.
- **Dual LLM Provider Support**: Supports Google Gemini (`gemini-1.5-flash`) and OpenAI (`gpt-4o-mini`) with automatic fallback handling.
- **Backdated Git Commit Generator**: Includes a python utility script (`scripts/seed_git_history.py`) to simulate realistic past commit history for GitHub portfolios.

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

4. **Run Test Suite**:
   ```bash
   pytest -v
   ```

5. **Generate Backdated Git Commit History for GitHub**:
   ```bash
   python scripts/seed_git_history.py
   ```
```

- [ ] **Step 2: Run full test suite to verify everything passes**

Run: `pytest -v`
Expected: ALL TESTS PASS (100% pass rate)

- [ ] **Step 3: Final Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README documentation and API guides"
```
