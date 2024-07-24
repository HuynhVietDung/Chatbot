import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from utils.connect import get_data, get_all_data
from utils.page_functions import set_default_page, set_sidebar
from utils.crud import update_account, hash_pass, check_pass
import time

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

if "default_page" not in st.session_state or "ID" not in st.session_state or "update_data" not in st.session_state:
    st.switch_page("main.py")

if st.session_state.update_data == 1:
    get_all_data()
    st.session_state.update_data = 0

navbar = st_navbar(
    ["Trang chủ", "Tư vấn", "Tìm kiếm", "Đặt hẹn", "Gói sản phẩm", "Hồ sơ", "Đăng xuất"], selected="Hồ sơ"
)

if navbar == "Trang chủ":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Hồ sơ":
    df = get_data("Account")
    user_pw = df[df["ID"] == st.session_state.ID].iloc[0]["Password"]

    placeholder = st.empty()
    with placeholder.form("Đổi mật khẩu"):
        st.markdown("### Đổi mật khẩu")
        old_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu cũ}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        new_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu mới}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu mới}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        if password != new_pass:
            st.warning("Mật khẩu không khớp.")

        if st.form_submit_button("Xác nhận"):
            if check_pass(old_pass, user_pw) and password == new_pass:
                password = hash_pass(password)
                update_account(id=st.session_state.ID, password=password)
                st.success("Thay đổi mật khẩu thành công")
                time.sleep(1)
                st.switch_page("./pages/page1.py")
            else:
                st.error("Mật khẩu mới/cũ không khớp.")

else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

set_sidebar()
