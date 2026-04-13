# src/spectr/main.py
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .config import PROJECT_ROOT
from .prompts import SPECTR_BASE_PROMPT, SPECTR_SUPER_PROMPT
from .xai_client import XAIClient
from .app import SPECTRApp

def main():
    print("=== SPECTR Tactical Machine v2.3 Loaded ===\n")
    print(SPECTR_BASE_PROMPT.strip())
    print("\n" + "=" * 80)
    print("Super Prompt loaded successfully.")
    print("\n=== SPECTR Tactical Machine Ready ===")
    print("Type 'exit' to quit.")
    print("Commands: 'Scope: ...' or 'Phase: ...'\n")

    client = XAIClient()
    app = SPECTRApp(client)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Session ended. Goodbye.")
                break

            if user_input.startswith("Scope:"):
                app.set_scope(user_input[6:].strip())
                continue
            if user_input.startswith("Phase:"):
                app.set_phase(user_input[6:].strip())
                continue

            response = app.chat(user_input)
            print("\nSPECTR:", response)
        except KeyboardInterrupt:
            print("\nSession terminated.")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
