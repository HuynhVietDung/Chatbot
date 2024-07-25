import streamlit as st
import pandas as pd
from utils.connect import get_data
from utils.crud import find_accountEmail, update_use
import time


def payment():
    df = get_data("Package")
    df = df[df["IsUsed"] == 1]
    if not df.empty:
        n_col = len(df)
        col = st.columns(n_col)

        for i in range(n_col):
            with col[i]:
                placeholder = st.container(border=True)
                with placeholder:

                    st.header(f"**{df.iloc[i]['Name']}**")

                    features = df.iloc[i]["Description"].split("✔️ ")

                    for feature in features[1:]:
                        st.write("✔️ " + feature)

                    st.write(f"Giá: {df.iloc[i]['Price']} VND")

                    # url = df.iloc[i]["Link"]
                    # st.link_button("Mua", url)
                    if st.button("Mua", key=df.iloc[i]["Name"]):
                        st.session_state.Package = df.iloc[i]["ID"]
                        st.switch_page("pages/payment.py")
    else:
        st.error("Lỗi hiển thị. Hãy thử lại sau.")
