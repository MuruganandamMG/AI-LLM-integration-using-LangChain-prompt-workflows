import time
from app.core.logger import logger

class AITelemetry:
    @staticmethod
    def record_call(provider: str, chain_name: str, duration_ms: float, success: bool = True):
        logger.info(f"[AI-TELEMETRY] Provider={provider} Chain={chain_name} Duration={duration_ms:.1f}ms Success={success}")
