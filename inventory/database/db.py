from __future__ import annotations

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "inventory.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)
