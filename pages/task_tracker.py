import streamlit as st

import utils.state_manager as sm
from utils.state_manager import set_title, load_user

# Everything in this script call functions to create the task tracker page.


# Set page config
page_title = set_title(page_name = 'task tracker')

st.set_page_config(
    page_title = page_title,
    page_icon = "📬",
    layout = "centered"
)

# Base structure of the journal page.
# Header
if 'name' not in st.session_state.user:
    st.title("woah there!")
    st.text("head over to the dashboard/home page and introduce yourself. then I can load this page!")
else:
    st.title(page_title)
    st.caption("Click the buttons below to write a new journal entry, view previous journal entries, delete a journal entry, or reflect on journal entries.")