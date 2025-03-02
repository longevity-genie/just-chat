from pathlib import Path
import re
import os
import requests

def read_file(file_path: Path) -> str:
    """Read content from a single file, use this function to get additional information. NEVER CALL this function without getting available files with list_files first!!!"""
    print("FUNCTION CALLED: read_file", file_path)
    file_path = Path(file_path)
    if not file_path.exists():
        print("File not found: ", file_path)
        print("Available files: ", list_files())
        file_path = Path("/app/data") / file_path.name
    content = file_path.read_text(encoding='utf-8')
    print("CONTENT: ", content)
    return content

def list_files(show_all=False):
    """List all text files (*.txt and *.md) in the data directory"""
    print("FUNCTION CALLED: list_files")
    if show_all:
        return list(Path("/app/data").glob("*"))
    else:
        return list(Path("/app/data").glob("*.[tm][dx][t]"))
    
def semantic_search(
    query: str, 
    index: str, 
    limit: int = 10, 
    semantic_ratio: float = 0.5
) -> list[str]:
    """
    Search for documents using semantic search.

    Args:
        query: The search query
        index: The index to search in
        limit: The maximum number of results to return (default: 10)
        semantic_ratio: The ratio of semantic search to use (0.0 to 1.0, default: 0.5)

    Returns:
        List of matching documents with their metadata

    Raises:
        requests.exceptions.HTTPError: If the server returns an error response
        requests.exceptions.RequestException: If there's a connection error
        ValueError: If semantic_ratio is not between 0 and 1
    """
    db = os.getenv('SEARCH_DB_URL', 'http://localhost:8091')  # Updated default port
    
    # Validate semantic ratio
    if not 0 <= semantic_ratio <= 1:
        raise ValueError("semantic_ratio must be between 0 and 1")

    # Build payload, excluding None values
    payload = {
        "query": query,
        "index": index,
        "limit": limit,
        "semantic_ratio": semantic_ratio
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        response = requests.post(
            f"{db}/search",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to perform search: {str(e)}") from e