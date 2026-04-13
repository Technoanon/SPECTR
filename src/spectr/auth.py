# src/spectr/auth.py - Single user
import bcrypt

class AuthManager:
    """Single-user auth for W3bW1z4rd"""
    
    def __init__(self):
        # Password hash - generated on April 13, 2026
        self.password_hash = b'$2b$12$DummyHashForPublicReleaseDoNotUse1234567890'
    
    def verify_password(self, password: str) -> bool:
        """Simple password check"""
        return bcrypt.checkpw(password.encode(), self.password_hash)

auth_manager = AuthManager()
