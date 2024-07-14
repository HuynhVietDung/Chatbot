import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
import time
import datetime
import random
import string
from utils.connect import get_data
from utils.crud import (
    create_patient_record,
    create_account,
    create_appointment,
    cancel_appointment,
    filter_appointment,
    is_existed,
    is_valid_email,
    find_accountID,
    update_account,
    get_password,
    hash_pass,
    check_pass,
    find_doctor_name,
    find_role,
    create_package,
    delete_package,
    create_doctor
)

def set_sidebar() -> None:
    st.sidebar.image("Image/chusoc.jpg", width=200)
    st.sidebar.title("DoctorAI - Chuyên gia tư vấn sức khỏe dành cho bạn")
    st.sidebar.write("Chat trực tiếp với Doctor AI")
    st.sidebar.header("Các tính năng chính")
    st.sidebar.header("- Chat")
    st.sidebar.header("- Tìm kiếm")
    st.sidebar.header("- Đặt hẹn")

def set_sessionID() -> None:
    if "ID" not in st.session_state:
        st.session_state.ID = None

def set_flag():
    if "is_login" not in st.session_state:
        st.session_state.is_login = True
    if "is_forgotten" not in st.session_state:
        st.session_state.is_forgotten = False
    

def set_default_page(page="Home") -> None:
    if "default_page" not in st.session_state:
        st.session_state.default_page = page
    else:
        st.session_state.default_page = page
    

def home() -> None:
    st.header("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
    st.image("Image/chatbot.jpg", output_format="auto")    
    st.write(
        "Mô Tả: Đưa sức khỏe của bạn vào tay của công nghệ với Doctor AI - chatbot y tế tiên tiến nhất, hỗ trợ bạn từ việc chẩn đoán ban đầu đến quản lý bệnh mãn tính."
    )
    st.header("Doctor AI là gì?")
    st.write(
        "Doctor AI là một chatbot y tế thông minh, được thiết kế để cung cấp cho bạn các lời khuyên y tế chính xác và kịp thời. Với sự hỗ trợ của công nghệ AI tiên tiến, Doctor AI có khả năng chẩn đoán các triệu chứng ban đầu, cung cấp thông tin về các bệnh lý và giúp quản lý các bệnh mãn tính."
    )
    st.image("Image/chatbot2.jpg", output_format="auto")
    st.header("Những Tính Năng Nổi Bật của Doctor AI")
    st.write(
        "+ Chẩn Đoán Ban Đầu: Phân tích các triệu chứng và đưa ra các dự đoán về bệnh lý có thể mắc phải."
    )
    st.write(
        "+ Thông Tin Y Khoa Đầy Đủ: Cung cấp thông tin chi tiết về các bệnh lý, thuốc và phương pháp điều trị."
    )
    st.header("Doctor AI Hoạt Động Như Thế Nào?")
    st.write(
        "Doctor AI sử dụng công nghệ AI tiên tiến để phân tích dữ liệu y tế từ người dùng. Bạn chỉ cần nhập các triệu chứng hoặc câu hỏi của mình, Doctor AI sẽ phân tích và cung cấp câu trả lời chính xác nhất."
    )
    st.image("Image/chatbot3.jpg", output_format="auto")

    st.header("Liên hệ ")
    st.image("Image/chusoc.jpg", width=200)
    st.write("Bác sĩ online")
    st.write("Email: lapduanviet@gmail.com")
    st.write("Số điện thoại: 0918755356")


def register() -> None:
    # form dang ky
    placeholder = st.empty()
    with placeholder.form("Chưa có tài khoản"):
        st.markdown("### Đăng ký")
        email2 = st.text_input(r"$\textsf{\normalsize Email}$:red[$\textsf{\normalsize *}$]")

        characters = string.ascii_letters + string.digits
        id = "".join(random.choice(characters) for i in range(8))
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

        password = st.text_input(
            r"$\textsf{\normalsize Mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password_2 = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        flag = True
        if password != password_2:
            st.warning("Mật khẩu không khớp.")
            flag = False

        # button submit
        submit = st.form_submit_button("Đăng ký")
        if submit:
            if not is_existed(email2) and is_valid_email(email2) and flag:
                time.sleep(0.5)
                hash_pw = hash_pass(password)
                create_account(id, email2, hash_pw)
                create_patient_record(id, email2, name, age, phone, gender)

                st.session_state.ID = id
                st.success("Đăng ký thành công")
                st.switch_page("./pages/page1.py")

            else:
                st.warning("Email/Mật khẩu không hợp lệ")

def reset_password() -> None:
    placeholder = st.empty()

    with placeholder.form("Quên mật khẩu"):
        st.markdown("### Quên mật khẩu")
        email = st.text_input(r"$\textsf{\normalsize Email}$:red[$\textsf{\normalsize *}$]")

        new_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        if password != new_pass:
            st.warning("Mật khẩu không khớp.")

        # button submit
        submit = st.form_submit_button("Hoàn tất")

        if submit:
            if is_existed(email) and password == new_pass:
                id = find_accountID(email)
                update_account(id, password=new_pass)
                st.session_state.ID = id

                time.sleep(1)
                st.success("Đổi mật khẩu thành công")
                st.switch_page("./pages/page1.py")

            else:
                st.warning("Email chưa đăng ký tài khoản")

def login() -> None:    
    # form login
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("### Đăng nhập")
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        # button submit
        submit = st.form_submit_button("Đăng nhập")
        
    if password != "" and email != "": 
        if is_valid_email(email):
            # check email
            if is_existed(email):
                # check password
                actual_pass = get_password(email)
    
                # encode password
                if check_pass(password, actual_pass):
                    st.success("Đăng nhập thành công")
                    user_id = find_accountID(email)
                    time.sleep(0.5)
    
                    st.session_state.ID = user_id
                    if find_role(user_id) == "admin":
                        st.switch_page("./pages/admin.py")
                    else:
                        st.switch_page("./pages/page1.py")
                else:
                    st.error("Email/Mật khẩu không đúng.")
            else:
                st.error("Email chưa được đăng ký tài khoản.")
        else:
            st.error("Email không hợp lệ")

def search_drugs() -> None:
    def find_drug(df, text_search):
        # Filter the dataframe using masks
        if text_search:
            m1 = df["Name"].str.contains(text_search, case=False)
            m2 = df["Brand"].str.contains(text_search, case=False)
            df_search = df[m1 | m2]
            return df_search
        return pd.DataFrame()
    

    st.header("Công Cụ Tìm Kiếm Thuốc")

    # Connect to the drug dataset
    df = get_data("Drug")

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input(
        "Nhập tên thuốc, thương hiệu thuốc hoặc tên bệnh", value=None
    )

    # Show the cards
    N_cards_per_row = 3
    if text_search:
        df_search = find_drug(df, text_search)

        if df_search.empty:
            st.markdown(
                "<h1 style='text-align: center; color: black; font-size: 20px;'>Không tìm thấy sản phẩm phù hợp.</h1>",
                unsafe_allow_html=True,
            )

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")

            # draw the card
            with cols[n_row % N_cards_per_row]:
                name = row["Name"].strip()
                brand = row["Brand"].strip()
                img_link = row["Image Link"].strip()
                drug_link = row["Link"].strip()

                st.image(img_link, use_column_width=True)
                st.write(f"[{name}]({drug_link})")

                if row["Price"] != "['None']":
                    f = "'"
                    price = row["Price"][1:-1].replace(f, "").strip()
                    st.markdown(f"Giá: {price}")


def appointment() -> None:
    def select_name(name):
        st.session_state["selected_name"] = name

    def select_time(slot):
        st.session_state["selected_time"] = slot

    def select_day(day):
        st.session_state["selected_day"] = day
    
    col1, col2, col3 = st.columns([3,3,2])
    with col2:
        st.title("Đặt Lịch Hẹn Bác Sĩ")

    df = get_data("Doctor")

    availability = df["Availability"]
    time_slots = df["TimeSlots"]

    if "selected_time" not in st.session_state:
        st.session_state["selected_time"] = None

    doctor_columns, booking_column = st.columns([4, 3])

    # Doctors' individual information
    with doctor_columns:
        st.header("Thông Tin Bác Sĩ")
        temp_col_1, temp_col_2 = st.columns([1, 1])
        with temp_col_1:
            doctor_name = st.selectbox(
                r"$\textsf{\normalsize Chọn bác sĩ}$:red[$\textsf{\normalsize *}$]",
                df["Name"].to_list(),
            )
            select_name(doctor_name)
        doctor_info = df[df["Name"] == doctor_name]

        col_1, col_2 = st.columns([1, 1])
        with col_1:
            if doctor_info["Image"].values[0] != "None":
                st.image(doctor_info["Image"].values[0], width=250)
            else:
                unknown_doctor = "Image/Unknown_person.jpg"
                st.image(unknown_doctor, width=250)
        with col_2:
            st.subheader(doctor_name)
            st.write(f"*{doctor_info['Title'].values[0]}*")
            st.write(f"*Chuyên Ngành:* {doctor_info['Speciality'].values[0]}")

        # Inject custom CSS for the buttons
        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Days
        st.write(f"*Ngày Khám Trong Tuần:*")
        col = st.columns([1, 1, 1, 1, 1])
        available_days = doctor_info["Availability"].values[0].split(", ")
        unavailable_days = []

        for idx in range(len(available_days)):
            col_idx = idx if idx < 4 else idx - 4
            with col[col_idx]:
                # st.button(available_days[idx])
                if available_days[idx] in unavailable_days:
                    st.button(
                        available_days[idx], disabled=True, key=available_days[idx]
                    )
                else:
                    if st.button(available_days[idx], key=available_days[idx]):
                        select_time(available_days[idx])

        # Available slot
        st.write("*Thời gian khám:*")
        unavailable_slots = []
        available_slots = doctor_info["TimeSlots"].values[0].split(",")
        N_cards_per_row = 4

        for idx in range(len(available_slots)):
            i = idx % N_cards_per_row
            if i == 0:
                cols = st.columns(N_cards_per_row * 2 - 1, gap="small")
            # draw the card
            with cols[idx % N_cards_per_row]:
                if available_slots[idx] in unavailable_slots:
                    st.button(
                        available_slots[idx], key=available_slots[idx], disabled=True
                    )
                else:
                    if st.button(available_slots[idx], key=available_slots[idx]):
                        select_time(available_slots[idx])

    with booking_column:
        st.header("Thông Tin Lịch Hẹn")
        doctor_name = st.session_state["selected_name"]
        date = st.date_input(
            r"$\textsf{\normalsize Chọn ngày khám}$:red[$\textsf{\normalsize *}$]",
            min_value=datetime.date.today(),
        )

        # Determine available slots by excluding unavailable ones
        doctor_info = df[df["Name"] == doctor_name]
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

        # Button to book appointment
        if st.button("Đặt hẹn"):
            characters = string.ascii_letters + string.digits
            ID = "".join(random.choice(characters) for i in range(8))
            PatientID = st.session_state.ID
            DoctorID = doctor_info.iloc[0]["ID"]
            Time = str(date) + " " + selected_time
            Description = f"Triệu chứng: {symptoms}. Ghi chú: {notes}"

            create_appointment(ID, PatientID, DoctorID, Time, Description)

            st.success(
                f"Đặt lịch hẹn thành công với {doctor_name}."
                f" Thời gian {date.strftime('%A, %B %d, %Y')} vào lúc {selected_time}"
            )


def profile() -> None:
    if st.session_state.ID != None:
        df = get_data("Patient")
        user_df = df[df["ID"] == st.session_state.ID].iloc[0]

        Name = user_df["Name"]
        Age = user_df["Age"]
        Email = user_df["Email"]
        Phone = user_df["Phone"]
        Image = user_df["Image"]

        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        ################ Profile ################
        st.title("Thông tin cá nhân")
        col1, col2 = st.columns(2)

        with col1:
            if Image == "":
                st.image("Image/Unknown_person.jpg", width=250)
            else:
                st.image(Image, width=250)
        with col2:
            st.write(f"📝  Tên: {Name}")
            st.write(f"📜  Tuổi: {Age}")
            st.write(f"📧  Email: {Email}")
            st.write(f"📞  SDT: {Phone}")

            col3, col4, col5 = st.columns(3)
            with col3:
                change_info = st.button("Cập nhật")
                if change_info:
                    st.switch_page("./pages/update_info.py")

            with col4:
                change_acc = st.button("Đổi mật khẩu")
                if change_acc:
                    st.switch_page("./pages/update_account.py")

        ################# Appointment #################
        st.header("Lịch hẹn sắp tới 📥")
        appointment = filter_appointment(st.session_state.ID)

        if not appointment.empty:
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])

                # write Header
                col1.write("ID")
                col2.write("Bác sĩ")
                col3.write("Thời gian")
                col4.write("Mô tả")
                

            # write contents
            # Custom CSS to adjust spacing between elements
            st.markdown(
                """
                <style>
                .custom-row-space {
                    margin-bottom: 30px; /* Adjust this value to increase/decrease space */
                }
                </style>
            """,
                unsafe_allow_html=True,
            )

            for i, row in appointment.iterrows():
                with st.container():
                # write contents
                    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])
                    col1.markdown(
                        f'<div class="custom-row-space">{row["ID"]}</div>',
                        unsafe_allow_html=True,
                    )
                    col2.markdown(
                        f'<div class="custom-row-space">{find_doctor_name(row["DoctorID"])}</div>',
                        unsafe_allow_html=True,
                    )
                    col3.markdown(
                        f'<div class="custom-row-space">{row["Time"]}</div>',
                        unsafe_allow_html=True,
                    )
                    col4.markdown(
                        f'<div class="custom-row-space">{row["Description"]}</div>',
                        unsafe_allow_html=True,
                    )

                    with col5:
                        change_but = st.button("Thay đổi", key=i)
                        if change_but:
                            if "app_id" not in st.session_state:
                                st.session_state.app_id = row["ID"]
                            if "app_doctor_id" not in st.session_state:
                                st.session_state.app_doctor_id = row["DoctorID"]
                            st.switch_page("./pages/update_appointment.py")

                    with col6:
                        del_but = st.button("Hủy", key=row["ID"])
                        if del_but:
                            cancel_appointment(row["ID"])
                            st.rerun()

        else:
            st.write("Hiện không có lịch hẹn nào")
    else:
        st.session_state.clear()
        st.switch_page("main.py")


def add_package_form():
    placeholder = st.empty()
    with placeholder.form("Thêm gói"):
        st.markdown("### Thêm gói")
        name = st.text_input(r"$\textsf{\normalsize Tên gói}$:red[$\textsf{\normalsize *}$]")

        characters = string.ascii_letters + string.digits
        id = "".join(random.choice(characters) for i in range(8))

        option = st.selectbox(
            r"$\textsf{\normalsize Thời hạn}$:red[$\textsf{\normalsize *}$]",
            ("Tuần", "Tháng", "Năm")
        )

        price = st.text_input(
            r"$\textsf{\normalsize Giá gói}$:red[$\textsf{\normalsize *}$", type="default"
        )

        description = st.text_area(
            r"$\textsf{\normalsize Mô tả tính năng}$:red[$\textsf{\normalsize *}$",
            height=300
        )

        link = st.text_input(
            r"$\textsf{\normalsize Link thanh toán}$:red[$\textsf{\normalsize *}$", type="default"
        )
        
        # button submit
        submit = st.form_submit_button("Thêm")
        if submit:
            try:
                if name != "" and option != "" and price != "" and description != "" and link != "":
                    create_package(id, name, price, description, link)

                    st.success("Thêm gói thành công")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Điền thiếu thông tin")
            except:
                st.error("Có lỗi xảy ra trong quá trình xử lý")
            


def delete_package_form():
    package = get_data("Package")

    if not package.empty:
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])

            # write Header
            col1.write("ID")
            col2.write("Tên gói")
            col3.write("Giá")
            col4.write("Mô tả")
            col5.write("Link")
                        

        # write contents
        # Custom CSS to adjust spacing between elements
        st.markdown(
            """
            <style>
            .custom-row-space {
                margin-bottom: 30px; /* Adjust this value to increase/decrease space */
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        for i, row in package.iterrows():
            with st.container():
            # write contents
                col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])
                col1.markdown(
                    f'<div class="custom-row-space">{row["ID"]}</div>',
                    unsafe_allow_html=True,
                )
                col2.markdown(
                    f'<div class="custom-row-space">{row["Name"]}</div>',
                    unsafe_allow_html=True,
                )
                col3.markdown(
                    f'<div class="custom-row-space">{row["Price"]}</div>',
                    unsafe_allow_html=True,
                )
                col4.markdown(
                    f'<div class="custom-row-space">{row["Description"]}</div>',
                    unsafe_allow_html=True,
                )

                col5.markdown(
                    f'<div class="custom-row-space">{row["Link"]}</div>',
                    unsafe_allow_html=True,
                )

                with col6:
                    del_but = st.button("Hủy", key=row["ID"])
                    if del_but:
                        delete_package(row["ID"])
                        st.success("Hủy gói thành công")
                        time.sleep(1)
                        st.rerun()

    else:
        st.write("Hiện không có gói nào")

def add_admin():
    # form dang ky
    placeholder = st.empty()
    with placeholder.form("Chưa có tài khoản"):
        st.markdown("### Đăng ký")
        email2 = st.text_input(r"$\textsf{\normalsize Email}$:red[$\textsf{\normalsize *}$]")

        characters = string.ascii_letters + string.digits
        id = "".join(random.choice(characters) for i in range(8))
        name = st.text_input(
            r"$\textsf{\normalsize Tên}$", type="default"
        )
        
        password = st.text_input(
            r"$\textsf{\normalsize Mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password_2 = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        flag = True
        if password != password_2:
            st.warning("Mật khẩu không khớp.")
            flag = False

        # button submit
        submit = st.form_submit_button("Đăng ký")
        if submit:
            if not is_existed(email2) and is_valid_email(email2) and flag:
                hash_pw = hash_pass(password)
                create_account(id, email2, hash_pw, role= "admin")

                st.session_state.ID = id
                st.success("Đăng ký thành công")

                time.sleep(1)
                st.rerun()
            else:
                st.warning("Email/Mật khẩu không hợp lệ")

def add_doctor():
    # form dang ky
    placeholder = st.empty()
    with placeholder.form("Chưa có tài khoản"):
        st.markdown("### Đăng ký")
        name = st.text_input(r"$\textsf{\normalsize Tên}$:red[$\textsf{\normalsize *}$]")

        characters = string.ascii_letters + string.digits
        id = "".join(random.choice(characters) for i in range(8))

        title = st.text_input(
            r"$\textsf{\normalsize Chức vụ}$", type="default"
        )
        spec = st.text_input(
            r"$\textsf{\normalsize Chuyên khoa}$", type="default"
        )
        image = st.text_input(
            r"$\textsf{\normalsize Ảnh}$",
            type="default",
        )

        avai = st.text_input(
            r"$\textsf{\normalsize Ngày khám}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        time = st.text_input(
            r"$\textsf{\normalsize Thời gian khám}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        # button submit
        submit = st.form_submit_button("Đăng ký")
        if submit:
            create_doctor(id, name, title, spec, image, avai, time)
            st.success("Đăng ký thành công")
            time.sleep(1)
            st.rerun()
