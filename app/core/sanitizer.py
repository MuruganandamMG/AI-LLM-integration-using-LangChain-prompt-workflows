import html
import re

class InputSanitizer:
    @staticmethod
    def sanitize_text(text: str | None) -> str | None:
        if text is None:
            return None
        cleaned = re.sub(r'<[^>]*?>', '', text)
        return html.escape(cleaned.strip())
