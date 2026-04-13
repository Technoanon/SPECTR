# SPECTR
**S**ecurity **P**entesting **E**xploitation **C**ollaborative **T**actical **R**esource

SPECTR is a custom-built, highly tactical AI assistant architecture designed for ethical hacking and deep-work workflows. It prioritizes function over form, operating with strict precision and zero conversational filler.

## Core Capabilities

* **Autonomous File Operations:** SPECTR does not just output text. It processes batch operations (`REQUEST_MKDIR`, `REQUEST_MV`) to autonomously build workspace directories and organize scattered files based on conversational context.
* **Persistent Session Memory:** Maintains a rolling, auto-updating `spectr_session_map.md` that acts as a tactical log of all file operations, scope changes, and next actions. Memory persists across sessions.
* **Strict Prompting Engine:** Designed to end every interaction with a forward-moving action question. "You do not chat. You do not speculate."

## Setup
1. Clone the repository.
2. Copy `.env.example` to `.env` and add your Gemini API key.
3. Review `src/spectr/auth.py` for default credentials.
4. Run `python3 gui_flet.py` to initiate the session.
