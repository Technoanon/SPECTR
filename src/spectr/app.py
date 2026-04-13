# src/spectr/app.py - COMPLETE DEBUG VERSION
from .xai_client import XAIClient
from .prompts import SPECTR_SUPER_PROMPT
from .handlers import handle_file_request
from .memory import MemoryManager
from .config import SHORT_TERM_DIR

class SPECTRApp:
    def __init__(self, client: XAIClient):
        self.client = client
        self.current_scope = "General ethical hacking"
        self.current_phase = "Idle"
        self.memory = MemoryManager()
        self.messages = [{"role": "system", "content": SPECTR_SUPER_PROMPT}]
        self.current_dir = SHORT_TERM_DIR

    def set_scope(self, scope: str):
        self.current_scope = scope
        print(f"[DEBUG] Scope set to: {scope}")

    def set_phase(self, phase: str):
        self.current_phase = phase
        print(f"[DEBUG] Phase set to: {phase}")

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        context = f"Current Scope: {self.current_scope}\nCurrent Phase: {self.current_phase}"
        full_messages = self.messages.copy()
        full_messages[-1]["content"] = context + "\n\n" + user_input

        response = self.client.chat(full_messages, temperature=0.3)

        # COMPLETE DEBUG OUTPUT
        print(f"\n{'='*60}")
        print(f"[DEBUG] Raw SPECTR response length: {len(response)}")
        print(f"[DEBUG] Contains REQUEST_READ: {'REQUEST_READ' in response}")
        print(f"[DEBUG] Contains REQUEST_WRITE: {'REQUEST_WRITE' in response}")
        print(f"[DEBUG] Contains REQUEST_MKDIR: {'REQUEST_MKDIR' in response}")
        print(f"[DEBUG] Contains REQUEST_MV: {'REQUEST_MV' in response}")
        
        # Show first 500 chars of response
        print(f"\n[DEBUG] Response preview:")
        print(response[:500])
        print(f"{'='*60}\n")

        # Execute file operations
        file_result = handle_file_request(response, self.current_dir)
        
        if file_result:
            print(f"[DEBUG] ✅ Handler executed and returned:")
            print(file_result)
            print()
        else:
            print(f"[DEBUG] ❌ Handler returned nothing")
            print()

        # Add results to conversation
        if file_result:
            self.messages.append({"role": "assistant", "content": response})
            self.messages.append({"role": "user", "content": f"File operation result:\n{file_result}"})
            response = response + "\n\n[FILE OPERATIONS]\n" + file_result
        else:
            self.messages.append({"role": "assistant", "content": response})

        self.memory.save_context(self.current_scope, self.current_phase, user_input, response)

        return response


# Simple test
if __name__ == "__main__":
    from .xai_client import XAIClient
    client = XAIClient()
    app = SPECTRApp(client)
    print("Debug app started")
