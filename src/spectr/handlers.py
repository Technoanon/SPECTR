# src/spectr/handlers.py - Handle MULTIPLE operations
import os
from pathlib import Path
from .config import SHORT_TERM_DIR

def handle_file_request(response: str, current_dir: Path = None) -> str:
    """Handle ALL file operations in response (READ, WRITE, MKDIR, MV)"""
    if not response:
        return ""

    results = []
    base_dir = current_dir or SHORT_TERM_DIR

    # Split response into lines for multi-operation support
    lines = response.split('\n')

    # READ - process all occurrences
    for line in lines:
        if "REQUEST_READ:" in line:
            try:
                filename = line.split("REQUEST_READ:", 1)[1].strip().split()[0]
                safe_filename = os.path.basename(filename)
                file_path = base_dir / safe_filename

                if file_path.exists():
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    results.append(f"READ_SUCCESS: {safe_filename}\n\n{content}")
                else:
                    results.append(f"READ_ERROR: File '{safe_filename}' not found.")
            except Exception as e:
                results.append(f"READ_ERROR: {str(e)}")

    # WRITE - process all occurrences
    if "REQUEST_WRITE:" in response:
        try:
            parts = response.split("REQUEST_WRITE:", 1)[1]
            if "CONTENT:" in parts:
                filename_part, content = parts.split("CONTENT:", 1)
                filename = filename_part.strip().splitlines()[0].strip()
                safe_filename = os.path.basename(filename)

                file_path = base_dir / safe_filename
                file_path.write_text(content.strip(), encoding="utf-8")
                results.append(f"WRITE_SUCCESS: {safe_filename} written successfully.")
        except Exception as e:
            results.append(f"WRITE_ERROR: {str(e)}")

    # MKDIR - process all occurrences
    for line in lines:
        if "REQUEST_MKDIR:" in line:
            try:
                dirname = line.split("REQUEST_MKDIR:", 1)[1].strip()
                safe_dirname = dirname.replace("..", "").strip("/")
                
                dir_path = base_dir / safe_dirname
                dir_path.mkdir(parents=True, exist_ok=True)
                results.append(f"MKDIR_SUCCESS: Directory '{safe_dirname}' created.")
            except Exception as e:
                results.append(f"MKDIR_ERROR: {str(e)}")

    # MV - process all occurrences
    for line in lines:
        if "REQUEST_MV:" in line and "TO:" in line:
            try:
                parts = line.split("REQUEST_MV:", 1)[1]
                if "TO:" in parts:
                    source_part, dest_part = parts.split("TO:", 1)
                    source = source_part.strip()
                    dest = dest_part.strip()
                    
                    # Keep relative paths but prevent directory traversal
                    safe_source = source.replace("..", "").strip("/")
                    safe_dest = dest.replace("..", "").strip("/")
                    
                    source_path = base_dir / safe_source
                    dest_path = base_dir / safe_dest
                    
                    if source_path.exists():
                        # Create destination directory if needed
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        source_path.rename(dest_path)
                        results.append(f"MV_SUCCESS: Moved '{safe_source}' to '{safe_dest}'")
                    else:
                        results.append(f"MV_ERROR: Source file '{safe_source}' not found.")
            except Exception as e:
                results.append(f"MV_ERROR: {str(e)}")

    return "\n".join(results) if results else ""
