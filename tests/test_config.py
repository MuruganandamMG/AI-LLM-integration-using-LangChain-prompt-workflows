from app.config import settings

def test_settings_load():
    assert settings.PROJECT_NAME == "AI Self-Improvement Platform"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DATABASE_URL is not None
