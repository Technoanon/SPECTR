# src/spectr/memory.py - Enhanced with session map
from pathlib import Path
from datetime import datetime
from .config import SHORT_TERM_DIR, AUDIT_DIR

class MemoryManager:
    def __init__(self):
        self.short_term_file = SHORT_TERM_DIR / "current_session_context.md"
        self.session_map_file = SHORT_TERM_DIR / "spectr_session_map.md"
        self.audit_file = AUDIT_DIR / f"audit_{datetime.now().strftime('%Y%m%d')}.log"

    def save_context(self, scope: str, phase: str, last_user_input: str, last_response: str):
        """Save current session context"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save current context (overwrites)
        content = f"""# SPECTR Session Context - {timestamp}

**Scope:** {scope}
**Phase:** {phase}
**Last User Input:** {last_user_input}
**Last SPECTR Response:** {last_response[:500]}...

Last updated: {timestamp}
"""
        try:
            self.short_term_file.write_text(content, encoding="utf-8")
        except Exception as e:
            print(f"[Memory] Warning: Could not save context - {e}")
        
        # Update session map
        self.update_session_map(scope, phase, last_user_input, last_response)

    def update_session_map(self, scope: str, phase: str, last_user_input: str, last_response: str):
        """Update the tactical session map with latest activity"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%B %d, %Y")
        
        # Extract file operations if present
        file_ops = []
        if "[FILE OPERATIONS]" in last_response:
            ops_section = last_response.split("[FILE OPERATIONS]")[1].split("\n")
            for line in ops_section[:10]:
                if "SUCCESS:" in line or "ERROR:" in line:
                    file_ops.append(line.strip())
        
        # Build session entry
        session_entry = f"""
---
## SESSION UPDATE - {timestamp}

**Scope:** {scope}  
**Phase:** {phase}

**User:** {last_user_input[:200]}{'...' if len(last_user_input) > 200 else ''}

**File Operations:**
"""
        if file_ops:
            for op in file_ops:
                session_entry += f"- {op}\n"
        else:
            session_entry += "- None\n"
        
        session_entry += f"""
**Status:** Active  
**Next Action:** {self._extract_next_action(last_response)}

"""
        
        # Append to session map
        try:
            if self.session_map_file.exists():
                existing = self.session_map_file.read_text(encoding="utf-8")
            else:
                existing = f"""# SPECTR SESSION MAP
**Started:** {date_str}
**Target:** {scope}

---
"""
            
            updated = existing + session_entry
            
            # Keep only last 50 entries
            entries = updated.split("## SESSION UPDATE")
            if len(entries) > 51:
                updated = entries[0] + "## SESSION UPDATE".join(entries[-50:])
            
            self.session_map_file.write_text(updated, encoding="utf-8")
            print(f"[Memory] 💾 Session map updated")
            
        except Exception as e:
            print(f"[Memory] Warning: Could not update session map - {e}")
    
    def _extract_next_action(self, response: str) -> str:
        """Extract the next-action question from SPECTR's response"""
        lines = response.split('\n')
        for line in reversed(lines):
            if '?' in line and len(line) < 200:
                return line.strip()
        return "Awaiting next directive"

    def log_audit(self, message: str):
        """Log important actions to audit file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with self.audit_file.open("a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass

    def load_context(self) -> str:
        """Load previous session context if exists"""
        if self.short_term_file.exists():
            try:
                return self.short_term_file.read_text(encoding="utf-8")
            except:
                return ""
        return ""
