import streamlit as st
from streamlit_navigation_bar import st_navbar
from utils.connect import create_credentials
from utils.page_functions import (
    set_sidebar,
    add_package_form,
    delete_package_form,
    add_admin,
    add_doctor,
    delete_doctor_form,
    delete_admin_form,
)
from utils.connect import get_data
from utils.crud import find_accountEmail, update_flag, update_use
import time
import pandas as pd

if "ID" not in st.session_state:
    time.sleep(1)
    st.switch_page("main.py")

st.set_page_config(page_title="Doctor AI", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(
    ["Trang chủ", "Cập nhật", "Đăng xuất"],
)
create_credentials()

payment = get_data("Payment")
package = get_data("Package")

if navbar == "Trang chủ":
    try:
        st.title(f"Chào mừng trở lại {find_accountEmail(st.session_state.ID)}.")
    except:
        st.title("Welcome back.")

    n = len(payment[payment["Flag"] == 0])
    if n != 0:
        st.warning(f"Bạn đang có {n} đơn hàng chờ duyệt.")

    st.title("Tra cứu thông tin")

    doctor = get_data("Doctor")
    doctor = doctor[doctor["Flag"] == 1]
    patient = get_data("Patient")
    patient["Phone"] = patient["Phone"].apply(lambda x: "0" + str(x))
    appointment = get_data("Appointment")
    account = get_data("Account")

    merged_appointment = appointment.merge(
        patient, how="left", left_on="PatientID", right_on="ID"
    ).merge(doctor, how="left", left_on="DoctorID", right_on="ID")

    merged_payment = payment.merge(
        patient, how="left", left_on="PatientID", right_on="ID"
    ).merge(package, how="left", left_on="PackageID", right_on="ID")

    successful_payment = merged_payment[merged_payment["Flag"] == 1]
    canceled_payment = merged_payment[merged_payment["Flag"] == -1]

    #### Package
    with st.container():
        st.header("Gói sản phẩm.")
        st.dataframe(
            package[package["IsUsed"] == 1],
            width=700,
            column_config={
                "Name": "Tên",
                "Price": "Giá",
                "Description": "Mô tả tính năng",
                "IsUsed": None,
            },
        )

    #### Patient
    with st.container():
        st.header("Bệnh nhân")
        st.dataframe(
            patient,
            column_config={
                "ID": "Mã số",
                "Email": "Email",
                "Name": "Tên",
                "Age": "Tuổi",
                "Phone": "Số điện thoại",
                "Gender": "Giới tính",
                "Image": "Hình ảnh",
            },
        )

    #### Doctor
    with st.container():
        st.header("Bác sĩ")
        st.dataframe(
            doctor,
            column_config={
                "ID": "Mã số",
                "Name": "Tên",
                "Title": "Chức vụ",
                "Spectiality": "Chuyên ngành",
                "Image": "Hình ảnh",
                "Availability": "Ngày khám",
                "TimeSlots": "Thời gian khám",
            },
        )

    #### Appointment
    with st.container():
        st.header("Lịch hẹn")
        st.dataframe(
            merged_appointment[
                [
                    "ID_x",
                    "PatientID",
                    "Name_x",
                    "DoctorID",
                    "Name_y",
                    "Time",
                    "Description",
                ]
            ],
            column_config={
                "ID_x": "Mã cuộc hẹn",
                "PatientID": "Mã khách hàng",
                "Name_x": "Tên khách hàng",
                "DoctorID": "Mã bác sĩ",
                "Name_y": "Tên bác sĩ",
                "Time": "Thời gian",
                "Description": "Mô tả",
            },
        )

    #### Account
    with st.container():
        st.header("Tài khoản")
        st.dataframe(
            account,
            column_config={
                "ID": "Mã số",
                "Email": "Email",
                "Password": "Mật khẩu",
                "Use": "Loại tài khoản",
                "Role": "Vai trò",
            },
        )

    #### Payment History
    with st.container():
        st.header("Lịch sử thanh toán")
        if not successful_payment.empty:
            st.dataframe(
                successful_payment[
                    [
                        "ID_x",
                        "PatientID",
                        "Name_x",
                        "Email_x",
                        "PackageID",
                        "Name_y",
                        "Time",
                        "Link",
                    ]
                ],
                column_config={
                    "ID_x": "Mã đơn hàng",
                    "PatientID": "Mã khách hàng",
                    "Email_x": "Email",
                    "Name_x": "Tên khách hàng",
                    "PackageID": "Mã gói",
                    "Name_y": "Tên gói",
                    "Time": "Thời gian",
                    "Link": "Hình ảnh",
                },
            )
        else:
            st.info("Chưa có hóa đơn đã thanh toán")

    #### Canceled Payment
    with st.container():
        st.header("Đơn hàng đã hủy")
        if not canceled_payment.empty:
            st.dataframe(
                canceled_payment[
                    [
                        "ID_x",
                        "PatientID",
                        "Name_x",
                        "Email_x",
                        "PackageID",
                        "Name_y",
                        "Time",
                        "Link",
                    ]
                ],
                column_config={
                    "ID_x": "Mã đơn hàng",
                    "PatientID": "Mã khách hàng",
                    "Email_x": "Email",
                    "Name_x": "Tên khách hàng",
                    "PackageID": "Mã gói",
                    "Name_y": "Tên gói",
                    "Time": "Thời gian",
                    "Link": "Hình ảnh",
                },
            )
        else:
            st.info("Chưa có hóa đơn đã thanh toán")

elif navbar == "Cập nhật":

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
                        price = (
                            package[package["ID"] == row["PackageID"]].iloc[0]["Price"]
                            + " VND"
                        )
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
                        del_but = st.button(
                            "Hủy", key=row["ID"] + row["Time"] + row["Link"]
                        )
                        if del_but:
                            update_flag(row["ID"], flag=-1)
                            time.sleep(1)
                            st.rerun()
    else:
        st.info("Hiện không có đơn hàng chờ duyệt")

    st.title("Gói sản phẩm")  ## part 1

    if "form_state" not in st.session_state:
        st.session_state.form_state = False
    if st.button("Thêm gói mới") or st.session_state.form_state:
        st.session_state.form_state = True
        add_package_form()

    if "form2_state" not in st.session_state:
        st.session_state.form2_state = False
    if st.button("Chỉnh sửa", key="package") or st.session_state.form2_state:
        st.session_state.form2_state = True
        delete_package_form()

    st.title("Quản trị viên")  ## part 2

    if "form3_state" not in st.session_state:
        st.session_state.form3_state = False
    if st.button("Thêm admin") or st.session_state.form3_state:
        st.session_state.form3_state = True
        add_admin()

    if "form5_state" not in st.session_state:
        st.session_state.form5_state = False
    if st.button("Chỉnh sửa", key="admin") or st.session_state.form5_state:
        st.session_state.form5_state = True
        delete_admin_form()

    st.title("Bác sĩ")  ## part 3

    if "form4_state" not in st.session_state:
        st.session_state.form4_state = False
    if st.button("Thêm bác sĩ") or st.session_state.form4_state:
        st.session_state.form4_state = True
        add_doctor()

    if "form6_state" not in st.session_state:
        st.session_state.form6_state = False
    if st.button("Chỉnh sửa", key="doctor") or st.session_state.form6_state:
        st.session_state.form6_state = True
        delete_doctor_form()

elif navbar == "Đăng xuất":
    st.session_state.clear()
    st.switch_page("main.py")

set_sidebar()
