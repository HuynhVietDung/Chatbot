import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.page_functions import set_default_page, set_sidebar
from utils.crud import create_payment
from PIL import Image
import os
import time
from utils.connect import upload_image, get_data
from datetime import datetime
import string
import random

st.set_page_config(page_title="Use", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(
    ["Trang chủ", "Tư vấn", "Tìm kiếm", "Đặt hẹn", "Gói sản phẩm", "Hồ sơ", "Đăng xuất"], selected="Gói sản phẩm"
)

if "Package" not in st.session_state:
    st.switch_page("./pages/page1.py")

if navbar == "Đăng xuát":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Gói sản phẩm":
    placeholder = st.empty()
    with placeholder.form("Thông tin cá nhân mua hàng"):
        name = st.text_input(
            r"$\textsf{\normalsize Tên}$", type="default"
        )
        email = st.text_input(
            r"$\textsf{\normalsize Email}$", type="default"
        )
        phone = st.text_input(
            r"$\textsf{\normalsize Số điện thoại}$",
            type="default",
        )

        PackageID = st.session_state.Package

        gender = st.radio(r"$\textsf{\normalsize Giới tính}$", ("Nam", "Nữ", "Không tiết lộ"))
        
        Time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        uploaded_file = None
        image_link = ""

        try:
            uploaded_file = st.file_uploader(r"$\textsf{\normalsize Chọn ảnh}$", type=["jpg", "jpeg", "png"])
        except:
            st.error("Lỗi không tải được")

        if uploaded_file == None:
            image = ""
        else:
            saved_image = Image.open(uploaded_file)
            # Save the image using PIL
            image_path = f"{st.session_state.ID}-{Time}.png"
            if os.path.exists(image_path):
                os.remove(image_path)

            saved_image.save(image_path)
            file_id, web_view_link = upload_image(image_path, image_path, "image/jpg")
            image_link = f"https://drive.google.com/file/d/{file_id}/view"
            os.remove(image_path)


        if st.form_submit_button("Xác nhận"):
            if image_link != "" and email != "":
                characters = string.ascii_letters + string.digits
                ID = "".join(random.choice(characters) for i in range(8))
                create_payment(id= ID, PatientID= st.session_state.ID,  PackageID=PackageID, Email= email, Time= Time,link = image_link)
                # st.info(f"https://drive.google.com/file/d/{file_id}/view")
                st.info("Đang chờ xử lý đơn hàng")
                time.sleep(10)
                st.switch_page("./pages/page1.py")
            else: 
                st.error("Bạn phải điền đầy đủ các thông tin.")
else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

set_sidebar()
