import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.page_functions import set_default_page, set_sidebar
from utils.crud import update_patient_record
from utils.connect import upload_image
from PIL import Image
import os
import time

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

if "default_page" not in st.session_state or "ID" not in st.session_state or "update_data" not in st.session_state:
    st.switch_page("main.py")

navbar = st_navbar(
    ["Trang chủ", "Tư vấn", "Tìm kiếm", "Đặt hẹn", "Gói sản phẩm", "Hồ sơ", "Đăng xuất"], selected="Hồ sơ"
)

if navbar == "Đăng xuát":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Hồ sơ":
    placeholder = st.empty()
    with placeholder.form("Chỉnh sửa thông tin cá nhân"):
        name = st.text_input(
            r"$\textsf{\normalsize Tên}$", type="default"
        )
        age = st.text_input(
            r"$\textsf{\normalsize Tuổi}$", type="default"
        )
        phone = st.text_input(
            r"$\textsf{\normalsize Số điện thoại}$",
            type="default",
        )
        gender = st.radio(r"$\textsf{\normalsize Giới tính}$", ("Nam", "Nữ", "Không tiết lộ"))

        uploaded_file = None
        try:
            uploaded_file = st.file_uploader(r"$\textsf{\normalsize Chọn ảnh}$", type=["jpg", "jpeg", "png"])
        except:
            st.error("Lỗi không tải được")

        if uploaded_file == None:
            image = ""
        else:
            saved_image = Image.open(uploaded_file)
            # Save the image using PIL
            image_path = f"{st.session_state.ID}.png"
            if os.path.exists(image_path):
                os.remove(image_path)

            saved_image.save(image_path)
            file_id, web_view_link = upload_image(image_path, image_path, "image/jpg", type = "info")
            image = f"https://drive.google.com/uc?export=view&id={file_id}"
            os.remove(image_path)

        if st.form_submit_button("Xác nhận"):
            update_patient_record(
                id=st.session_state.ID,
                name=name,
                age=age,
                phone=phone,
                gender=gender,
                image=image,
            )
            st.success("Thay đổi thông tin thành công")
            time.sleep(1)
            st.switch_page("./pages/page1.py")
else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

set_sidebar()
