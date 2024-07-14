import streamlit as st  
import webbrowser
import stripe

def payment():
    col1, col2 = st.columns(2)
    with col1:
        placeholder = st.empty()
        with placeholder.form("Gói đăng ký tuần"):
            st.write("**Gói đăng ký tuần**")
            st.write("✔️ Tư vấn y tế cơ bản")
            st.write("✔️ Theo dõi triệu chứng")
            st.write("✔️ Lập kế hoạch sức khỏe cá nhân")
            st.write("✔️ Cảnh báo sức khỏe")
            st.write("✔️ Trả lời câu hỏi không giới hạn trong 1 tuần")
            st.write("✔️ Khuyến mãi 10% cho những lần đăng ký sau")
            st.write("Giá: 300.000")
            submit = st.form_submit_button("Mua")
            if submit:
                url = "https://buy.stripe.com/test_7sIg2dchu5Ae9I4288"
                webbrowser.open_new_tab(url)
           
        
        with col2:
            placeholder = st.empty()
            with placeholder.form("Gói đăng ký tháng"):
                st.write("**Gói đăng ký tháng**")
                st.write("✔️ Tư vấn y tế chuyên sâu")
                st.write("✔️ Theo dõi sức khỏe toàn diện")
                st.write("✔️ Nhắc nhở uống thuốc và kiểm tra định kì")
                st.write("✔️ Cảnh báo sức khỏe và hỗ trợ khẩn cấp")
                st.write("✔️ Tư vấn dinh dưỡng và lối sống lành mạnh")
                st.write("✔️ Trả lời câu hỏi không giới hạn trong 1 tháng")
                st.write("✔️ Khuyến mãi 20% cho những lần đăng ký sau")
                st.write("Giá: 1.000.000")
                submit = st.form_submit_button("Mua")
                if submit:
                    url = "https://buy.stripe.com/test_14k5nzftG9QubQccMN"
                    webbrowser.open_new_tab(url)        



def create_payment_link_week(amount, currency='vnd'):
    stripe.api_key = st.secrets["stripe_api_key"]

    product = stripe.Product.create(name='Gói đăng ký tuần')
        
    # Create a price for the product

    price = stripe.Price.create(
            product=product.id,
            unit_amount=amount,
            currency=currency
        )

        # Create a payment link
    payment_link = stripe.PaymentLink.create(
        line_items=[{
                'price': price.id,
                'quantity': 1,
        }],
        after_completion={
                'type': 'redirect',
                'redirect': {'url': 'https://your-website.com/success'},
        },
    )
    return payment_link['url']

def create_payment_link_mothly(amount, currency='vnd'):
    stripe.api_key = st.secrets["stripe_api_key"]

    product = stripe.Product.create(name='Gói đăng ký tuần')
        
    # Create a price for the product
    price = stripe.Price.create(
            product=product.id,
            unit_amount=amount,
            currency=currency,            
        )

        # Create a payment link
    payment_link = stripe.PaymentLink.create(
        line_items=[{
                'price': price.id,
                'quantity': 1,
        }],
        after_completion={
                'type': 'redirect',
                'redirect': {'url': 'https://your-website.com/success'},
        },
    )
    return payment_link['url']
    


# print(create_payment_link_mothly(amount=1200000))
