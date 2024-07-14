import streamlit as st  
import webbrowser
import stripe
import pandas as pd
from utils.connect import get_data 


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
                # st.write("✔️ Tư vấn y tế cơ bản")
                # st.write("✔️ Theo dõi triệu chứng")
                # st.write("✔️ Lập kế hoạch sức khỏe cá nhân")
                # st.write("✔️ Cảnh báo sức khỏe")
                # st.write("✔️ Trả lời câu hỏi không giới hạn trong 1 tuần")
                # st.write(f"✔️ Khuyến mãi 10% cho những lần đăng ký sau")
                for feature in feature:
                    st.write(feature)
                    
                st.write(f"Giá: {df.iloc[i]['Price']}")
                submit = st.form_submit_button("Mua")
                if submit:
                    url = df.iloc[i]["Link"]
                    try:
                        webbrowser.open_new_tab(url)
                    except:
                        st.error("Hiện không thể mở link.")
           
        
        # with col2:
        #     placeholder = st.empty()
        #     with placeholder.form("Gói đăng ký tháng"):
        #         # st.write("**Gói đăng ký tháng**")
        #         # st.write("✔️ Tư vấn y tế chuyên sâu")
        #         # st.write("✔️ Theo dõi sức khỏe toàn diện")
        #         # st.write("✔️ Nhắc nhở uống thuốc và kiểm tra định kì")
        #         # st.write("✔️ Cảnh báo sức khỏe và hỗ trợ khẩn cấp")
        #         # st.write("✔️ Tư vấn dinh dưỡng và lối sống lành mạnh")
        #         # st.write("✔️ Trả lời câu hỏi không giới hạn trong 1 tháng")
        #         # st.write(f"✔️ Khuyến mãi 20% cho những lần đăng ký sau")
        #         st.write(f"Giá: {price_2}")
        #         submit = st.form_submit_button("Mua")
        #         if submit:
        #             url = url_2
        #             webbrowser.open_new_tab(url)
                        
        # with col3:
        #     placeholder = st.empty()
        #     with placeholder.form("Gói đăng ký năm"):
        #         # st.write("**Gói đăng ký năm**")
        #         # st.write("✔️ Tư vấn y tế chi tiết")
        #         # st.write("✔️ Theo dõi sức khỏe toàn diện")
        #         # st.write("✔️ Nhắc nhở uống thuốc và kiểm tra định kì")
        #         # st.write("✔️ Lập kế hoạch sức khỏe cá nhân hóa")
        #         # st.write("✔️ Cảnh báo sức khỏe và hỗ trợ khẩn cấp")
        #         # st.write("✔️ Tư vấn dinh dưỡng và lối sống lành mạnh")
        #         # st.write("✔️ Trả lời câu hỏi không giới hạn trong 1 năm")
        #         # st.write(f"✔️ Khuyến mãi 30% cho những lần đăng ký sau")
        #         st.write(f"Giá: {price_3}")
        #         submit = st.form_submit_button("Mua")
        #         if submit:
        #             url = url_3
        #             webbrowser.open_new_tab(url)


def get_infor_customer():
    stripe.api_key = st.secrets["strip_api_key"]

    customers = stripe.Customer.list()
    
    transaction = stripe.PaymentIntent.list()
    amount = [c.amount for c in transaction]
    name_customers = [c.name for c in customers]
    id_customers = [c.id for c in customers]
    gmail_customers = [c.email for c in customers]
    df = pd.DataFrame({'ID':id_customers,'Name':name_customers,'Gmail':gmail_customers,'Amount':amount})
    
    return df


