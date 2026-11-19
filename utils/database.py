import sqlite3
import streamlit as st
from contextlib import closing
from pathlib import Path

# Files and paths
script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parent.parent if script_dir.parent.name == "utils" else script_dir.parent
var_dir = base_dir / "variables"
data_dir = base_dir / "data"

DATABASE_FILE = str(data_dir / "app_db.db")
USER_FILE = str(var_dir / "user.json")

def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

@st.cache_data
def initialize_database():
    """Create necessary tables if they don't exist."""
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()

            # Create journal table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    title TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    entry TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wellbeing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    date TEXT NOT NULL,
                    last_edited TEXT NOT NULL,
                    headache TEXT NOT NULL,
                    pain TEXT NOT NULL, -- list
                    period TEXT NOT NULL,
                    medications TEXT NOT NULL, -- list
                    appetite INTEGER NOT NULL,
                    amount_eaten INTEGER NOT NULL,
                    food_eaten TEXT NOT NULL, -- list
                    steps INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    exercise TEXT NOT NULL, -- list
                    cpap TEXT NOT NULL, 
                    sleep_quality INTEGER NOT NULL,
                    sleep_hours INTEGER NOT NULL,
                    energy INTEGER NOT NULL,
                    productivity INTEGER NOT NULL,
                    anger INTEGER NOT NULL,
                    anger_desc TEXT NOT NULL, -- list
                    fear INTEGER NOT NULL,
                    fear_desc TEXT NOT NULL, -- list
                    love INTEGER NOT NULL,
                    love_desc TEXT NOT NULL, -- list
                    joy INTEGER NOT NULL,
                    joy_desc TEXT NOT NULL, -- list
                    sadness INTEGER NOT NULL,
                    sadness_desc TEXT NOT NULL -- list
                )
            """)

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT NOT NULL,
                        date TEXT NOT NULL,
                        last_edited TEXT NOT NULL,
                        category TEXT NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        urgency TEXT NOT NULL,
                        importance TEXT NOT NULL,
                        status TEXT NOT NULL,
                        date_completed TEXT NOT NULL
                    )
                """)

    return True

