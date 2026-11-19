import json
import os
import pandas as pd
import streamlit as st
import utils.database as database
from utils.state_manager import register_user, search_user, edit_user
from datetime import date
from pathlib import Path
from uuid import uuid4

"""
About: Everything in this script are form elements that physically show up on pages.
"""

# User Management
# ------------------------------------------------------------
# User Registration
def user_registration_form():
    with st.form("user_name_form", enter_to_submit = False):
        st.subheader("hello! nice to meet you.")
        st.caption("enter your name and details in the form below to start creating your dashboard.")

        user_name = st.text_input("your name")
        user_birthday = st.date_input("your birthday", value = date.today(), min_value = date(1900, 1, 1), max_value = date(2120, 12, 31))
        picture = st.file_uploader(
            "choose a photo of your choice. this will go on your dashboard.",
            type = ['png', 'jpg', 'jpeg']
        )

        submitted = st.form_submit_button("submit")

        if submitted:
            if not user_name:
                st.warning("please provide a name for your dashboard.")
                return
            if not user_birthday:
                st.warning("please provide a birthday! it's an important date.")
                return

            picture_path = None
            if picture is not None:
                upload_dir = Path("data/dashboard_pictures")
                upload_dir.mkdir(parents = True, exist_ok = True)

                suffix = Path(picture.name).suffix.lower()
                picture_path = upload_dir / f"{uuid4().hex}{suffix}"
                picture_path.write_bytes(picture.getvalue())

            st.session_state.user = {
                "name": user_name,
                "birthday": user_birthday.isoformat(),
                "main pic": str(picture_path) if picture_path else None,
            }

            register_user()
            st.write("registration completed.")
            st.rerun()

# Edit User
def edit_user_form():
    st.subheader("edit user info")
    st.caption("enter a name to find the user you want to edit.")

    user_name = st.text_input("user name", key = "search_user_name")

    if user_name.strip():
        results = search_user(user_name)

        event = st.dataframe(
            results,
            use_container_width = True,
            on_select = "rerun",
            selection_mode = "single-row",
            key = "user_selection"
        )

        selected_row = event.selection.rows
        if selected_row:
            selected_user = results.iloc[selected_row[0]]
            st.session_state.selected_user = selected_user.todict()

    if "selected_user" in st.session_state:
        user = st.session_state.selected_user

        st.divider()
        st.subheader(f"edit {user['name']}")

        with st.form("user_edit_form", enter_to_submit = False):
            new_name = st.text_input(
                "corrected name",
                value = user['name'] or ""
            )
            new_birthday = st.date_input(
                "corrected_birthday",
                value = user['birthday'] or ""
            )
            picture = st.file_uploader(
                'new profile picture',
                type = ['png', 'jpg', 'jpeg']
            )

            submitted = st.form_submit_button('save changes')

            if submitted:
                updated_name = new_name.strip() or user['name']
                updated_birthday = new_birthday or user['birthday']
                picture_path = user.get('main pic')

                if picture is not None:
                    upload_dir = Path('data/dashboard_pictures')
                    upload_dir.mkdir(parents = True, exist_ok = True)

                    suffix = Path(picture.name).suffix.lower()
                    picture_path = upload_dir / f"{uuid4().hex}{suffix}"
                    picture_path.write_bytes(picture.getvalue())

                st.session_state.user = {
                    **user,
                    "name": updated_name,
                    "birthday": updated_birthday,
                    "main pic": picture_path
                }

                edit_user(selected_user, updated_name, updated_birthday, picture_path)
                st.session_state.pop('selected_user', None)

                st.success("user information updated!")
                st.rerun()