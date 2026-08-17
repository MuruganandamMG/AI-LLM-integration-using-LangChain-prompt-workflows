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
