import sys
from pathlib import Path

# Add backend/src to Python's import search path.
# This allows tests to import modules directly, for example:
# from app import create_app
# from store import NoteStore

# __file__ = this conftest.py file
# .resolve() = get its absolute path
# .parent = get the backend/ directory
# / "src" = build the path to backend/src/
# str() = convert the Path object into a string

# Insert the src directory at position 0 so Python searches it first.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))