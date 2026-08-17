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
