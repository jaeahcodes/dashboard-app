import csv
import streamlit as st
import pandas as pd
import sqlite3
import json
import os
from pathlib import  Path
from datetime import date

import utils.database as database
from utils.db_repository import add_entry

# Files and paths
script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parent.parent if script_dir.parent.name == "utils" else script_dir.parent
var_dir = base_dir / "variables"
data_dir = base_dir / "data"

DATABASE_FILE = str(data_dir / "app_db.db")
USER_FILE = str(var_dir / "user.json")

# App Initialization
# ------------------------------------------------------------
def initialize_state():
    if "user" not in st.session_state:
        st.session_state.users, st.session_state.no_user = load_user()

def set_page_title(page_name: str):
    user = st.session_state.get("user", {})

    if user and user[0].get('name'):
        page_title = f"{user['name']}'s {page_name}"
    else:
        page_title = page_name
    return page_title

# User Management
# ------------------------------------------------------------
@st.cache_data
def load_user():
    """Load user information from a JSON file into Streamlit session state."""
    user_file = Path(USER_FILE)
    if not user_file.exists():
        return [], True

    try:
        with user_file.open('r', encoding = 'utf-8') as f:
            data = json.load(f)
        if data:
            return data, False
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading user data: {e}")
    return [], True

def search_user(name):
    with open(USER_FILE, 'r') as f:
        user_data = json.load(f)
    user_df = pd.DataFrame(user_data)

    if name.strip():
        final_df = user_df[
            user_df['name'].str.contains(
                name.strip(),
                case = False,
                na = False
            )
        ]
    return final_df

def edit_user(name, new_name = None, birthday = None, pic = None):
    with open(USER_FILE, 'r') as f:
        user_data = json.load(f)

    for user in user_data:
        if user['name'] == name:
            if new_name:
                user['name'] = new_name
            if birthday is not None:
                user['birthday'] = birthday
            if pic is not None:
                user['main pic'] = str(pic)
            break

    with open(USER_FILE, 'w') as f:
        json.dump(user_data, f, indent = 2)

    load_user.clear()

def register_user():
    """Save user info from Streamlit session state to a JSON file."""
    with open(USER_FILE, "w") as f:
        json.dump(st.session_state.user, f, indent = 2)
    st.session_state.no_user = False
    load_user.clear()

# Journal Management
# ------------------------------------------------------------
def save_journal_entry(name, datetime, entry):
    entry_data = {
        "title": name,
        "timestamp": datetime.isoformat(),
        "entry": entry
    }

    add_entry(**entry_data)
    st.rerun()

def submit_new_journal_entry():
    name = st.session_state.new_journal_entry
    datetime = st.session_state.new_journal_entry_datetime
    entry = st.session_state.new_journal_entry_content

    conn = database.get_connection()
    cursor = conn.cursor()
    prev_dates = cursor.execute("""
        SELECT
            DISTINCT date(timestamp)
        FROM journal
    """)

    if name and datetime and entry:
        if date(datetime) in prev_dates:
            msg = "duplicate"
        else:
            save_journal_entry(name, datetime, entry)
            msg = "journal entry saved."
    elif not name:
        st.warning("please provide a name for this entry.")
        return
    elif not entry:
        st.warning("please submit a non-empty entry.")
        return
    st.session_state.entry_created_message = msg
    












