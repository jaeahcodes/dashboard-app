import streamlit as st

from utils.state_manager import load_user, edit_user
from utils.forms import edit_user_form

# Everything in this script call functions to create the journal page.

# Initialize all states
st.session_state.user, st.session_state.no_user = load_user()

# Set page config

st.set_page_config(
    page_title = "settings",
    page_icon = "⚙️",
    layout = "centered"
)

edit_user_form()