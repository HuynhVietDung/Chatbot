import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import  create_credentials
from utils.page_functions import set_sidebar, add_package_form, delete_package_form, add_admin, add_doctor
from utils.connect import get_data

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

create_credentials()
navbar = st_navbar(
    ["Home", "Update", "Logout"]
)

if navbar == "Home":
    st.title("Wellcome back Admin.")
    
    package = get_data("Package")

    col = st.columns(2)
    with col[0]:
        st.title("Gói sản phẩm.")
        st.dataframe(package)


    st.title("Dashboard")

    doctor = get_data("Danh sách bác sĩ")
    patient = get_data("Danh sách bệnh nhân")
    appointment = get_data("Danh sách lịch hẹn")
    account = get_data("Danh sách tài khoản")

    new_appointment = appointment.join(doctor, how= "inner").join(patient, how= "inner")

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.header("Patient")
            st.dataframe(patient)
        with st.container():
            st.header("Doctor")
            st.dataframe(doctor)

    with col2:
        with st.container():
            st.header("Appointment")
            st.dataframe(new_appointment)
        with st.container():
            st.header("Account")
            st.dataframe(account)


elif  navbar == "Update":
    st.title("Gói sản phẩm")
    if st.button("Thêm gói mới"):
        add_package_form()
        

    if st.button("Chỉnh sửa"):
        delete_package_form()
    
    st.title("Quản trị viên")
    if st.button("Thêm admin"):
        add_admin()
    
    st.title("Bác sĩ")
    if st.button("Thêm bác sĩ"):
        add_doctor()


elif navbar == "Logout":
    st.session_state.clear()
    st.switch_page("main.py")

set_sidebar()
