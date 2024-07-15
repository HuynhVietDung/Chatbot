import streamlit as st  
import stripe
import pandas as pd
from utils.connect import get_data 
import js2py

def open_url(url):
    code_2 = "function f(x) {window.open('" + url + "', '_blank');}"
    js2py.eval_js(code_2) 

def payment():
    df = get_data("Package")
    n_col = len(df)
    col = st.columns(n_col)

    for i in range(n_col):
        with col[i]:
            placeholder = st.empty()
            with placeholder.form(df.iloc[i]['Name']):

                st.header(f"**{df.iloc[i]['Name']}**")
                
                features = df.iloc[i]['Description'].split("✔️ ")
                
                for feature in features[1:]:
                    st.write("✔️ " + feature)

                st.write(f"Giá: {df.iloc[i]['Price']}")

                submit = st.form_submit_button("Mua")
                if submit:
                    url = df.iloc[i]["Link"]
                    
                    open_url(url)
        

def get_infor_customer():
    stripe.api_key = st.secrets["stripe_api_key"]

    customers = stripe.Customer.list()
    
    transaction = stripe.PaymentIntent.list()
    amount = [c.amount for c in transaction]
    name_customers = [c.name for c in customers]
    id_customers = [c.id for c in customers]
    gmail_customers = [c.email for c in customers]
    df = pd.DataFrame({'ID':id_customers,'Name':name_customers,'Gmail':gmail_customers,'Amount':amount})
    
    return df


