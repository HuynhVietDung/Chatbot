import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from utils.connect import  create_credentials
from utils.page_functions import home, search_drugs, appointment, profile, set_sidebar
from utils.chat import chatbot


create_credentials()
if "default_page" not in st.session_state:
    st.switch_page("main.py")
if "ID" not in st.session_state:
    st.switch_page("main.py")

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

navbar = st_navbar(
    ["Home", "Chat", "Search", "Appointment", "Profile", "Logout"],
    selected=st.session_state.default_page,
)

if navbar == "Home":
    home()

elif navbar == "Chat":
    chatbot()
    
elif navbar == "Search":
    search_drugs()

elif navbar == "Appointment":
    appointment()

elif navbar == "Logout":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Profile":
    profile()

set_sidebar()
