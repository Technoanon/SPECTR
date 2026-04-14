# SPECTR
### Security Pen-testing Exploitation Collaborative Tactical Resource

![SPECTR UI](assets/SPECTR_UI.jpg)

SPECTR is a locally-run, autonomous AI assistant built for offensive security workflows.
No pleasantries. No filler. Tactical responses, persistent memory, and autonomous file 
operations — purpose-built for penetration testers and bug bounty hunters.

---

## What SPECTR Does

- **Autonomous file operations** — creates directories, moves files, organizes workspaces on command
- **Persistent session memory** — tracks context across sessions, auto-updates session map
- **Tactical personality** — military strict, task-focused, no chat
- **GUI interface** — clean Flet-based UI with password authentication
- **Modular architecture** — swap AI providers, extend handlers, build on top

---

## Requirements

- Python 3.10+
- API key for your chosen provider (xAI Grok or Google Gemini)

```bash
pip install -r requirements.txt

Setup
1. Clone the repo

bash
git clone https://github.com/Technoanon/SPECTR.git
cd SPECTR
2. Create your .env file

bash
cp src/spectr/.env.example .env
Edit .env and add your API key:

text
XAI_API_KEY=your_key_here
# OR
GEMINI_API_KEY=your_key_here
3. Set your password

Edit src/spectr/auth.py and replace the dummy hash with your own:

python
import bcrypt
# Run this once to generate your hash:
# python3 -c "import bcrypt; print(bcrypt.hashpw(b'yourpassword', bcrypt.gensalt()))"
self.password_hash = b'your_generated_hash_here'
4. Run SPECTR

bash
python3 gui_flet.py
File Operations
SPECTR can autonomously manage your workspace:

text
# Create directories
REQUEST_MKDIR: recon/nmap

# Move files
REQUEST_MV: findings.md TO: reports/findings.md

# Read files
REQUEST_READ: scope.md

# Write files
REQUEST_WRITE: notes.md
CONTENT:
[content here]
All operations execute relative to data/memory/short_term/.

Session Memory
Every interaction updates two files automatically:

data/memory/short_term/current_session_context.md — live session snapshot
data/memory/short_term/spectr_session_map.md — rolling interaction log
Context persists across sessions. SPECTR knows what you were doing last time.

Project Structure
text
SPECTR/
├── src/spectr/
│   ├── app.py          # Core loop
│   ├── handlers.py     # File operation execution
│   ├── memory.py       # Session persistence
│   ├── prompts.py      # SPECTR personality + rules
│   ├── auth.py         # Authentication
│   ├── config.py       # Configuration
│   └── xai_client.py   # AI provider client
├── gui_flet.py         # GUI entry point
├── data/memory/        # Workspace (gitignored)
└── assets/             # UI assets
Philosophy
"You do not chat. You do not speculate."

SPECTR is not a general-purpose assistant. She is a force multiplier for security
professionals who know what they're doing and need a tool that keeps up.

Built for:

Bug bounty hunting
Penetration testing workflows
CTF research
Offensive security tooling
License
MIT License — see LICENSE for details.

Author
Built by @Technoanon
"Military strict, doesn't chat, but really good."
