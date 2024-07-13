import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import create_credentials
from utils.page_functions import (
    home,
    search_drugs,
    login,
    register,
    set_sessionID,
    set_flag,
    set_default_page,
)

create_credentials()
set_default_page()
st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(["Home", "Chat", "Search", "Appointment", "Login"])
set_sessionID()


if navbar == "Home":
    home()

elif navbar == "Chat":
    st.warning("Đăng nhập để sử dụng tính năng này")

elif navbar == "Search":
    search_drugs()

elif navbar == "Appointment":
    st.warning("Đăng nhập để sử dụng tính năng này")

elif navbar == "Login":
    set_flag()
    flag = st.session_state.is_login

    if flag:
        login()
        if st.button("Chưa có tài khoản. Đăng ký ngay"):
            st.session_state.is_login = False
            st.rerun()
    
    else:
        register()
        if st.button("Đã có tài khoản. Đăng nhập ngay"):
            st.session_state.is_login = True
            st.rerun()



st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
