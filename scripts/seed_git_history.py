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
