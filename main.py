import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import create_credentials
from utils.page_functions import (
    home,
    search_drugs,
    login,
    register,
    reset_password,
    set_sessionID,
    set_flag,
    set_default_page,
    set_sidebar
)

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")
set_default_page()

navbar = st_navbar(["Home", "Chat", "Search", "Appointment", "Login"])
set_sessionID()

create_credentials()

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

    if st.session_state.is_login:
        login()
        
        if st.button("Quên mật khẩu"):
            st.session_state.is_login = False
            st.session_state.is_forgotten = True
            st.rerun()

        st.write("Chưa có tài khoản.")
        if st.button("Đăng ký ngay"):
            st.session_state.is_login = False
            st.rerun()
        
    elif st.session_state.is_forgotten:
        reset_password()
        if st.button("Quay lại"):
            st.session_state.is_login = True
            st.session_state.is_forgotten = False
            st.rerun()

    else:
        register()
        st.write("Đã có tài khoản.")
        if st.button("Đăng nhập ngay"):
            st.session_state.is_login = True
            st.session_state.is_forgotten = False
            st.rerun()

set_sidebar()
