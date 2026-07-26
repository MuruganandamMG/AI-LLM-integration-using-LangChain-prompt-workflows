from pydantic import BaseModel

class LLMGenerationConfig(BaseModel):
    temperature: float = 0.7
    max_output_tokens: int = 1024
    top_p: float = 0.95
