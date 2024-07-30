import streamlit as st
import pandas as pd
from utils.connect import get_data
from utils.crud import find_accountEmail, update_use, update_flag
import time
from datetime import datetime, timedelta


def payment() -> None:
    df = get_data("Package")
    df = df[df["IsUsed"] == 1]
    df = df.sort_values(by="Duration", key=lambda x: x.astype(int))

    if not df.empty:
        n_col = len(df)
        col = st.columns(n_col)

        for i in range(n_col):
            with col[i]:
                placeholder = st.container(border=True)
                with placeholder:

                    st.header(f"{df.iloc[i]['Name']}")

                    st.write(f"Thời gian sử dụng: {df.iloc[i]['Duration']} ngày")
                    features = df.iloc[i]["Description"].split("✔️ ")

                    for feature in features[1:]:
                        st.write("✔️ " + feature)

                    st.write(f"Giá: {df.iloc[i]['Price']} VND")

                    if st.button("Mua", key=df.iloc[i]["Name"]):
                        st.session_state.Package = df.iloc[i]["ID"]
                        st.switch_page("pages/payment.py")
    else:
        st.error("Lỗi hiển thị. Hãy thử lại sau.")


def update_payment(id: str) -> None:
    all_payment = get_data("Payment")
    try:
        individual_payment = all_payment[
            (all_payment["PatientID"] == id) & (all_payment["Flag"] == 1)
        ].iloc[0]

        # Check duration
        if not individual_payment.empty:
            package = get_data("Package")
            duration = int(
                package[
                    (package["IsUsed"] == 1)
                    & (package["ID"] == individual_payment["PackageID"])
                ].iloc[0]["Duration"]
            )

            try:
                # Parse the datetime string into a datetime object
                exp_date = datetime.strptime(
                    individual_payment["Confirmation"], "%Y-%m-%d %H:%M:%S"
                ) + timedelta(days=duration)

                if datetime.now() > exp_date:
                    update_flag(
                        id=individual_payment["ID"], flag=-2
                    )  # -2 means expiration
                    update_use(
                        id=individual_payment["PatientID"], use=0
                    )  # 0 mean normal account
            except:
                pass
    except:
        pass
