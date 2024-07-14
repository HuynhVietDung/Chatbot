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

    doctor = get_data("Doctor")
    patient = get_data("Patient")
    appointment = get_data("Appointment")
    account = get_data("Account")

    new_appointment = appointment.join(doctor, how= "inner", lsuffix='_appoinment', rsuffix='_doctor').join(patient, how= "inner", lsuffix='_doctor', rsuffix='_patient')

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.header("Danh sách bệnh nhân")
            st.dataframe(patient)
        with st.container():
            st.header("Danh sách bác sĩ")
            st.dataframe(doctor)

    with col2:
        with st.container():
            st.header("Danh sách lịch hẹn")
            st.dataframe(new_appointment)
        with st.container():
            st.header("Danh sách tài khoản")
            st.dataframe(account)


elif  navbar == "Update":
    if "form1_state" not in st.session_state:
        st.session_state.form1_state = False
    st.title("Gói sản phẩm")

    if st.button("Thêm gói mới") or st.session_state.form1_state:
        st.session_state.form1_state = True
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
