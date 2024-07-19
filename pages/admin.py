import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import  create_credentials
from utils.page_functions import set_sidebar, add_package_form, delete_package_form, add_admin, add_doctor,\
delete_doctor_form, delete_admin_form
from utils.connect import get_data
from utils.payment import get_infor_customer
from utils.crud import find_accountEmail

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

create_credentials()
navbar = st_navbar(
    ["Trang chủ ", "Cập nhật", "Đăng xuất"]
)

if navbar == "Trang chủ":
    try:
        st.title(f"Welcome back {find_accountEmail(st.session_state.ID)}.")
    except:
        st.title("Welcome back.")
    
    st.title("Tra cứu thông tin")

    package = get_data("Package")

    with st.container():
        st.title("Gói sản phẩm.")
        st.dataframe(package)

    doctor = get_data("Doctor")
    patient = get_data("Patient")
    appointment = get_data("Appointment")
    account = get_data("Account")

    merged_appointment = appointment.join(doctor, how= "inner", lsuffix='_appointment', rsuffix='_doctor').join(patient, how= "inner", lsuffix='_doctor', rsuffix='_patient')

    new_appointment = merged_appointment[["ID_appointment", "Name_doctor", "Name_patient", "Time", "Description", "PatientID", "DoctorID"]]
    new_appointment.rename(columns={"ID_appointment": "ID", 
                            "Name_doctor": "DoctorName", 
                            "Name_patient" : "PatientName"}, inplace=True)

    col1, col2 = st.columns(2)

    with st.container():
        st.header("Bệnh nhân")
        st.dataframe(patient)

    with st.container():
        st.header("Bác sĩ")
        st.dataframe(doctor)


    with st.container():
        st.header("Lịch hẹn")
        st.dataframe(new_appointment)
    with st.container():
        st.header("Tài khoản")
        st.dataframe(account)

    payment = get_infor_customer()

    with st.container():
        st.header("Lịch sử thanh toán")
        st.dataframe(payment)

elif  navbar == "Cập nhật":
    st.title("Gói sản phẩm") ## part 1

    if "form_state" not in st.session_state:
        st.session_state.form_state = False
    if st.button("Thêm gói mới") or st.session_state.form_state:
        st.session_state.form_state = True
        add_package_form()
        
    if "form2_state" not in st.session_state:
        st.session_state.form2_state = False
    if st.button("Chỉnh sửa", key = "package") or st.session_state.form2_state:
        st.session_state.form2_state = True
        delete_package_form()
    
    st.title("Quản trị viên") ## part 2

    if "form3_state" not in st.session_state:
        st.session_state.form3_state = False
    if st.button("Thêm admin") or st.session_state.form3_state:
        st.session_state.form3_state = True
        add_admin()

    if "form5_state" not in st.session_state:
        st.session_state.form5_state = False
    if st.button("Chỉnh sửa", key = "admin") or st.session_state.form5_state:
        st.session_state.form5_state = True
        delete_admin_form()

    st.title("Bác sĩ") ## part 3

    if "form4_state" not in st.session_state:
        st.session_state.form4_state = False
    if st.button("Thêm bác sĩ") or st.session_state.form4_state:
        st.session_state.form4_state = True
        add_doctor()

    if "form6_state" not in st.session_state:
        st.session_state.form6_state = False
    if st.button("Chỉnh sửa", key = "doctor") or st.session_state.form6_state:
        st.session_state.form6_state = True
        delete_doctor_form()

elif navbar == "Đăng xuất":
    st.session_state.clear()
    st.switch_page("main.py")

set_sidebar()
