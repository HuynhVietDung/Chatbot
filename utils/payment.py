import streamlit as st  
import stripe
import pandas as pd
from utils.connect import get_data 
from utils.crud import find_accountEmail, update_use

def payment():
    df = get_data("Package")
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

                st.write(f"Giá: {df.iloc[i]['Price']}")

                url = df.iloc[i]["Link"]
                st.link_button("Mua", url)

@st.cache_data(ttl=3)
def get_infor_customer():
    stripe.api_key = st.secrets["stripe_api_key"]

    customers = stripe.Customer.list()
    
    transaction = stripe.PaymentIntent.list()
    amount = [c.amount for c in transaction]
    name_customers = [c.name for c in customers]
    id_customers = [c.id for c in customers]
    gmail_customers = [c.email for c in customers]
    df = pd.DataFrame({'ID':id_customers,'Name':name_customers,'Email':gmail_customers,'Amount':amount})
    
    return df

def upgrade_account(ID: str):
    email = find_accountEmail(ID)
    customer = stripe.Customer.list()
    email_customer = [c.email for c in customer]

    if email == email_customer[0]:  
        update_use(ID, 2)  #update use = 2
        st.rerun()


