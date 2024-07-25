import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import get_data
from utils.page_functions import set_default_page, set_sidebar
from utils.crud import update_appointment
import datetime
import time

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

if "default_page" not in st.session_state or "ID" not in st.session_state:
    st.switch_page("main.py")

navbar = st_navbar(
    ["Trang chủ", "Tư vấn", "Tìm kiếm", "Đặt hẹn", "Gói sản phẩm", "Hồ sơ", "Đăng xuất"], selected="Hồ sơ"
)

if navbar == "Đăng xuất":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Hồ sơ":
    placeholder = st.empty()
    with placeholder.form("Chỉnh sửa lịch hẹn"):
        st.title("Chỉnh sửa lịch hẹn")

        date = st.date_input(
            r"$\textsf{\normalsize Chọn ngày khám}$:red[$\textsf{\normalsize *}$]",
            min_value=datetime.date.today(),
        )

        # Determine available slots by excluding unavailable ones
        df = get_data("Doctor")
        doctor_info = df[df["ID"] == st.session_state["app_doctor_id"]]
        unavailable_slots = []

        all_slots = doctor_info["TimeSlots"].values[0].split(",")
        available_slots = [slot for slot in all_slots if slot not in unavailable_slots]

        # Maintain consistency with unavailable slots and session state
        selected_time = st.selectbox(
            r"$\textsf{\normalsize Thời gian khám}$:red[$\textsf{\normalsize *}$]",
            available_slots,
            index=(
                available_slots.index(st.session_state["selected_time"])
                if st.session_state["selected_time"] in available_slots
                else 0
            ),
        )

        symptoms = st.text_area(
            r"$\textsf{\normalsize Triệu chứng}$",
            placeholder="Nhập triệu chứng của bạn",
            height=300,
        )

        notes = st.text_area(
            r"$\textsf{\normalsize  Ghi chú}$",
            placeholder="Ghi chú thêm dành cho bác sĩ",
            height=200,
        )

        if st.form_submit_button("Xác nhận"):
            Time = str(date) + " " + selected_time
            Description = f"Triệu chứng: {symptoms}. Ghi chú: {notes}"

            update_appointment(
                id=st.session_state.app_id, Time=Time, Description=Description
            )
            st.success("Thay đổi lịch hẹn thành công")
            time.sleep(1)
            st.switch_page("./pages/page1.py")
else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

set_sidebar()
