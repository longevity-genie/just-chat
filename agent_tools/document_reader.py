from pathlib import Path
import re

def read_file(file_path: Path) -> str:
    """Read content from a single file, use this function to get additional information. NEVER CALL this function without getting available files with list_files first!!!"""
    print("FUNCTION CALLED: read_file", file_path)
    file_path = Path(file_path)
    content = file_path.read_text(encoding='utf-8')
    print("CONTENT: ", content)
    return content

def list_files():
    """List all text files (*.txt and *.md) in the data directory"""
    print("FUNCTION CALLED: list_files")
    return list(Path("/data").glob("*.[tm][dx][t]"))