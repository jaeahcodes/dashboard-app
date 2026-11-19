import pandas as pd
import streamlit as st
import utils.database as database

"""
Anything to do with pushing to and pulling from the database file.
"""

# Journal 
# ------------------------------------------------------------
def add_entry(name, timestamp, entry):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO journal
            (
                title,
                timestamp,
                entry
            )
        VALUES (?, ?, ?)
    """, (name, timestamp, entry))

    conn.commit()
    conn.close()