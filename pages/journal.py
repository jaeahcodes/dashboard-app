import streamlit as st

from utils.state_manager import set_page_title, load_user, submit_new_journal_entry

# Everything in this script call functions to create the journal page.

# Initialize all states
st.session_state.user, st.session_state.no_user = load_user()

# Set page config
journal_title = set_page_title(page_name = 'journal')

st.set_page_config(
    page_title = journal_title,
    page_icon = "✒️",
    layout = "centered"
)

# TODO: sm.load_journal_entries()

# Functions
def write_journal_entry(tab):
    # Button for creating new journal entry.
    with tab:
        st.text_input("entry title", key = "new_journal_entry")
        st.datetime_input("entry date and time", key = "new_journal_entry_datetime", value = "now")
        st.text_area("entry", "write your entry here...", key = "new_journal_entry_content")

        st.button("submit entry", on_click = submit_new_journal_entry)

        # Entry created message
        if "entry_created_message" in st.session_state:
            msg = st.session_state.entry_created_message
            if msg == "duplicate":
                st.warning(
                    f"an entry for this day already exists."
                )
            else: 
                st.toast(msg, icon = "✅", duration = "short")
            del st.session_state.entry_created_message

# Base structure of the journal page.
# Header
if 'name' not in st.session_state.user:
    st.header("woah there!")
    st.text("head over to the dashboard/home page and introduce yourself. then I can load this page!")
else:
    st.header(journal_title)
    st.caption("click the buttons below to write a new journal entry, view previous journal entries, delete a journal entry, or reflect on journal entries.")

    tab1, tab2, tab3, tab4 = st.tabs(["write journal entry", "view journal entries", "delete journal entry", "reflect"])

    # Initialize session state variables
    if "show_journal_entries" not in st.session_state:
        st.session_state.show_journal_entries = False

    if "new_journal_entry" not in st.session_state:
        st.session_state.new_journal_entry = ""

    if "reflect" not in st.session_state:
        st.session_state.reflect = False

    # Helper function calls
    write_journal_entry(tab1)
    # TODO: view_journal_entries_bt(tab2)
    # TODO: delete_journal_entry_bt(tab3)
    # TODO: reflect(tab4)

