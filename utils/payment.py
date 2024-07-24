import streamlit as st  
import stripe
import pandas as pd
from utils.connect import get_data 
from utils.crud import find_accountEmail, update_use
import time

def payment():
    df = get_data("Package")
    df = df[df['IsUsed'] == 1]
    n_col = len(df)
    col = st.columns(n_col)

    for i in range(n_col):
        with col[i]:
            placeholder = st.container(border= True)
            with placeholder:

                st.header(f"**{df.iloc[i]['Name']}**")
                
                features = df.iloc[i]['Description'].split("✔️ ")
                
                for feature in features[1:]:
                    st.write("✔️ " + feature)

                st.write(f"Giá: {df.iloc[i]['Price']} VND")

                # url = df.iloc[i]["Link"]
                # st.link_button("Mua", url)
                if st.button("Mua", key= df.iloc[i]['Name']):
                    st.session_state.Package = df.iloc[i]["ID"]
                    st.switch_page("pages/payment.py")
                

@st.cache_data(ttl=3)
def get_infor_customer(ID="") -> pd.DataFrame:
    stripe.api_key = st.secrets["stripe_api_key"]

    customers = stripe.Customer.list()
    transaction = stripe.PaymentIntent.list()
    amount = [c.amount for c in transaction]
    name_customers = [c.name for c in customers]
    id_customers = [c.id for c in customers]
    gmail_customers = [c.email for c in customers]
    df = pd.DataFrame({'ID':id_customers,'Name':name_customers,'Email':gmail_customers,'Amount':amount})
    if ID == "":
        return df
    else:
        email = find_accountEmail(ID)
        return df[df["Email"] == email]


def upgrade_account(ID: str) -> None:
    stripe.api_key = st.secrets["stripe_api_key"]
    email = find_accountEmail(ID)
    customer = stripe.Customer.list()
    email_customer = [c.email for c in customer]

    if email == email_customer[0]: 
        df = get_data("Account")
        use = int(df[df["ID"] == st.session_state.ID].iloc[0]["Use"])

        if use !=2:
            try:
                update_use(ID, 2)  #update use = 2
                time.sleep(1)
                st.rerun()
            except:
                st.error("Có lỗi xảy ra trong quá trình xử lý")


