import streamlit as st
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain
from utils.connect import get_data
from utils.crud import update_use
from utils.payment import payment


def chatbot():
    @st.cache_resource(ttl="1d")
    def load_data():
        df = get_data("Doctor")
        df.to_csv("Doctor.csv", index=False)
        loader = CSVLoader(file_path="Doctor.csv", encoding="utf8")
        data = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

        chunks = splitter.split_documents(data)

        embeddings = HuggingFaceEmbeddings()

        vector_index = Chroma.from_documents(chunks, embeddings)
        print("Loading data success..")

        return vector_index, chunks

    def display(vector_index, chunks):
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)

        df = get_data("Account")
        use = int(df[df["ID"] == st.session_state.ID].iloc[0]["Use"])

        if use == 0:
            st.write("Bạn vui lòng thanh toán để được tư vấn tiếp.")
            payment()
            # df = get_infor_customer()
            # if st.session_state.ID == df.iloc[0]["ID"]:
            #     update_use(st.session_state.ID, use=2)

        if use == 1:
            if (
                "messages" not in st.session_state.keys()
            ):  # Initialize the chat message history
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Xin chào ! Tôi có thể giúp gì cho bạn 🧑‍⚕️ ?.",
                    }
                ]

            if (
                "question_count" not in st.session_state
            ):  # Initialize the question count
                st.session_state.question_count = 0

            if question := st.chat_input(
                "Your question"
            ):  # Prompt for user input and save to chat history
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.question_count += 1

            for message in st.session_state.messages:  # Display the prior chat messages
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):

                        if st.session_state.question_count <= 5:
                            prompt_template = """
                        Bạn là một chatbot y tế chuyên nghiệp.
                        Trả lời tự nhiên như 1 người bạn.
                        Trả lời đầy đủ thông tin dựa vào ngữ cảnh.
                        Ngữ cảnh câu hiện tại phải bao gồm ngữ cảnh các câu trước.
                        Tư vấn sức khỏe và đưa ra lời khuyên cho bệnh nhân.
                        Recommend thuốc cho bệnh nhân.
                        Gợi ý một số bác sĩ liên quan đến tình trạng bệnh nhân nếu cần.
                        
                        Context:\n {context}?\n
                        Question: \n {question}\n
                        Answer:
                        """
                            context = vector_index.similarity_search(question, k=3)
                            prompt = PromptTemplate(
                                template=prompt_template,
                                input_variables=["context", "question"],
                            )
                            model = ChatGoogleGenerativeAI(
                                model="gemini-1.5-flash-latest",
                                google_api_key=GOOGLE_API_KEY,
                                temperature=0.3,
                            )
                            chain = load_qa_chain(
                                model, chain_type="stuff", prompt=prompt
                            )
                            response = chain(
                                {"input_documents": chunks, "question": question},
                                return_only_outputs=True,
                            )
                            st.write(response["output_text"])
                            message = {
                                "role": "assistant",
                                "content": response["output_text"],
                            }
                            st.session_state.messages.append(
                                message
                            )  # Add response to message history

                        else:
                            update_use(
                                st.session_state.ID, use=0
                            )  # "0" means cannot using chatbot
                            st.write("Bạn vui lòng thanh toán để được tư vấn tiếp.")
                            payment()

        if use == 2:
            if (
                "messages" not in st.session_state.keys()
            ):  # Initialize the chat message history
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": "Xin chào ! Tôi có thể giúp gì cho bạn 🧑‍⚕️ ?.",
                    }
                ]

            if question := st.chat_input(
                "Your question"
            ):  # Prompt for user input and save to chat history
                st.session_state.messages.append({"role": "user", "content": question})

            for message in st.session_state.messages:  # Display the prior chat messages
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            if st.session_state.messages[-1]["role"] != "assistant":
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):

                        prompt_template = """
                        Bạn là một chatbot y tế chuyên nghiệp.
                        Trả lời tự nhiên như 1 người bạn.
                        Trả lời đầy đủ thông tin dựa vào ngữ cảnh.
                        Ngữ cảnh câu hiện tại phải bao gồm ngữ cảnh các câu trước.
                        Tư vấn sức khỏe và đưa ra lời khuyên cho bệnh nhân.
                        Recommend thuốc cho bệnh nhân.
                        Gợi ý một số bác sĩ liên quan đến tình trạng bệnh nhân nếu cần.
                        
                        Context:\n {context}?\n
                        Question: \n {question}\n
                        Answer:
                        """
                        context = vector_index.similarity_search(question, k=3)
                        prompt = PromptTemplate(
                            template=prompt_template,
                            input_variables=["context", "question"],
                        )
                        model = ChatGoogleGenerativeAI(
                            model="gemini-1.5-flash-latest",
                            google_api_key=GOOGLE_API_KEY,
                            temperature=0.3,
                        )
                        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
                        response = chain(
                            {"input_documents": chunks, "question": question},
                            return_only_outputs=True,
                        )
                        st.write(response["output_text"])
                        message = {
                            "role": "assistant",
                            "content": response["output_text"],
                        }
                        st.session_state.messages.append(
                            message
                        )  # Add response to message history

    vector_index, chunks = load_data()
    display(vector_index, chunks)
