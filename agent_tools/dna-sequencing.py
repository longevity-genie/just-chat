import sqlite3
from pathlib import Path


PATH_TO_DNA_SEQUENCING_DB = Path("data", "genetics", "dna_sequencing.txt")

def sequencing_info() -> str:
    """Function to get the sequencing information from the database."""
    with open(PATH_TO_DNA_SEQUENCING_DB) as f:
        info = f.readlines()
    return info