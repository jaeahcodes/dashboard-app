import streamlit as st

from utils.state_manager import (
    initialize_state, 
    load_user,
    set_page_title
)
from utils.forms import user_registration_form
from utils.database import initialize_database

# App Initialization
initialize_state()

st.set_page_config(
    page_title = set_page_title("dashboard"),
    page_icon = '🪴',
    layout = "centered"
)

# Functions
def home_page():
    st.title = set_page_title("dashboard")
    with st.container(border = True, horizontal_alignment = "center"):
        # TODO: fetch a random affirmation from variables/affirmations.json and write it into the container
        st.write(f"today's affirmation for {st.session_state.user['name']}")


# Logic
initialize_database()

if st.session_state.no_user:
    user_registration_form()
elif st.session_state.user is None:
    # TODO: user_greeting_form()
    pass
else:
    home_page()