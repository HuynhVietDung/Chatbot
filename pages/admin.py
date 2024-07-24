import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import  create_credentials
from utils.page_functions import set_sidebar, add_package_form, delete_package_form, add_admin, add_doctor,\
delete_doctor_form, delete_admin_form
from utils.connect import get_data, get_all_data
from utils.crud import find_accountEmail, update_flag, update_use
import time

if "ID" not in st.session_state or "update_data" not in st.session_state:
    time.sleep(1)
    st.switch_page("main.py")

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")

create_credentials()
if st.session_state.update_data == 1:
    get_all_data()
    st.session_state.update_data = 0

payment = get_data("Payment")
package = get_data("Package")    

navbar = st_navbar(
    ["Trang chủ", "Cập nhật", "Đăng xuất"]
)

if navbar == "Trang chủ":
    try:
        st.title(f"Chào mừng trở lại {find_accountEmail(st.session_state.ID)}.")
    except:
        st.title("Welcome back.")

    n = len(payment[payment["Flag"] == 0])
    if n != 0:
        st.warning(f"Bạn đang có {n} đơn hàng chờ duyệt.")

    st.title("Tra cứu thông tin")

    with st.container():
        st.title("Gói sản phẩm.")
        sub_package = package.copy()
        sub_package = sub_package[sub_package["IsUsed"] == 1]
        sub_package.drop(columns=["IsUsed"], inplace= True)
        st.dataframe(sub_package, width= 700)

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

    bill = payment[payment["Flag"] == 1]

    with st.container():
        st.header("Lịch sử thanh toán")
        if not bill.empty:
            st.dataframe(bill)
        else:
            st.info("Chưa có hóa đơn đã thanh toán")

elif  navbar == "Cập nhật":

    st.title("Đơn hàng chờ duyệt")
    bill = payment[payment["Flag"] == 0]
    if not bill.empty:
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
            col1.write("Mã Đơn hàng")
            
            col2.write("Mã Bệnh nhân")

            col3.write("Mã Sản phẩm")

            col4.write("Email")
            
            col5.write("Giá")

            col6.write("Thời gian")
            
            col7.write("Link ảnh")


            for i, row in bill.iterrows():
                with st.container():
                    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
                    
                    col1.write(row["ID"])

                    col2.write(row["PatientID"])

                    col3.write(row["PackageID"])
                    
                    col4.write(row["Email"])

                    try:
                        price = package[package["ID"] == row["PackageID"]].iloc[0]["Price"] + " VND"
                    except:
                        price = None
                        
                    col5.write(price)
                    
                    col6.write(row["Time"])
                    
                    col7.write(row["Link"])

                    with col8:
                        acc_but = st.button("Xác nhận", key=row["ID"] + row["Time"])
                        if acc_but:
                            update_flag(row["ID"])
                            update_use(id=row["PatientID"], use=2)
                            time.sleep(1)
                            st.rerun()
                    
                    with col9:
                        del_but = st.button("Hủy", key=row["ID"] + row["Time"] + row["Link"])
                        if del_but:
                            update_flag(row["ID"], flag =-1)
                            time.sleep(1)
                            st.rerun()
    else:
        st.info("Hiện không có đơn hàng chờ duyệt")

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
