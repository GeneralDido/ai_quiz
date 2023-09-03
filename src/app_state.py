import streamlit as st
from helper.functions import generate_session_id

def initialize_session_state():
    default_state = {
        "app_state": "generation",
        "student": {},
        "questions": [],
        "user_answers": {},
        "questions_data": {},
        "app_rating": 0,
        "user_feedback": "",
        "saved_data_to_airtable": False,
        "saved_user_feedback": False,
        "session_id": generate_session_id()
    }
    
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value
