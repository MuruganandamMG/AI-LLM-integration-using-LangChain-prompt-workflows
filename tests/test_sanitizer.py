from app.core.sanitizer import InputSanitizer

def test_sanitizer_cleans_script():
    raw = "<script>alert('xss')</script>Hello World"
    cleaned = InputSanitizer.sanitize_text(raw)
    assert "<script>" not in cleaned
    assert "Hello World" in cleaned

def test_sanitizer_none():
    assert InputSanitizer.sanitize_text(None) is None
