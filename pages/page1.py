import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import  create_credentials
from utils.page_functions import home, search_drugs, appointment, profile, set_sidebar
from utils.chat import chatbot
from utils.payment import payment, upgrade_account
st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

create_credentials()
if "default_page" not in st.session_state:
    st.switch_page("main.py")

if "ID" not in st.session_state:
    st.switch_page("main.py")

navbar = st_navbar(
    ["Trang chủ", "Tư vấn", "Tìm kiếm", "Đặt hẹn", "Gói sản phẩm", "Hồ sơ", "Đăng xuất"],
    selected=st.session_state.default_page,
)

if navbar == "Trang chủ":
    home()

elif navbar == "Tư vấn":
    upgrade_account(st.session_state.ID)
    chatbot()
    
elif navbar == "Tìm kiếm":
    search_drugs()

elif navbar == "Đặt hẹn":
    appointment()

elif navbar == "Hồ sơ":
    profile()

elif navbar == "Gói sản phẩm":
    payment()
    
elif navbar == "Đăng xuất":
    st.session_state.clear()
    st.switch_page("main.py")

set_sidebar()
