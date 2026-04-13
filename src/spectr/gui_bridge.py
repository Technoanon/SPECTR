# src/spectr/gui_bridge.py
from .app import SPECTRApp
from .xai_client import XAIClient

class SPECTRGuiBridge:
    """Bridge between your GUI and the clean SPECTR backend"""
    
    def __init__(self):
        self.client = XAIClient()
        self.app = SPECTRApp(self.client)

    def send_message(self, user_message: str) -> str:
        """Main method your GUI should call"""
        if user_message.startswith("Scope:"):
            self.app.set_scope(user_message[6:].strip())
            return f"[SPECTR] Scope updated → {self.app.current_scope}"
        
        if user_message.startswith("Phase:"):
            self.app.set_phase(user_message[6:].strip())
            return f"[SPECTR] Phase updated → {self.app.current_phase}"

        # Normal chat through the backend
        response = self.app.chat(user_message)
        return response

    def get_status(self) -> dict:
        """Return current status for GUI sidebar"""
        return {
            "scope": self.app.current_scope,
            "phase": self.app.current_phase,
            "messages_count": len(self.app.messages)
        }
