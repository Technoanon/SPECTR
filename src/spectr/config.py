# src/spectr/config.py
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_DIR = DATA_DIR / "memory"
AUDIT_DIR = MEMORY_DIR / "audit"
LONG_TERM_DIR = MEMORY_DIR / "long_term"
SHORT_TERM_DIR = MEMORY_DIR / "short_term"

# Ensure directories exist
for directory in [AUDIT_DIR, LONG_TERM_DIR, SHORT_TERM_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default settings
DEFAULT_MODEL = "grok-3"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2048
