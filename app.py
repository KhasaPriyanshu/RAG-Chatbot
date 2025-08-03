import streamlit as st
import time

def main():
    st.set_page_config(page_title="RAG Chatbot", layout="wide")
    st.header("RAG Chatbot")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    model_name = st.sidebar.radio("Model:", ("Google AI",))  # only one model for now

    st.sidebar.title("Menu")
    api_key = st.sidebar.text_input("Google API Key")
    st.sidebar.markdown("Get your API key [here](https://ai.google.dev)")

    pdf_docs = st.sidebar.file_uploader("Upload PDFs", accept_multiple_files=True)

    if st.sidebar.button("Submit & Process"):
        if pdf_docs and api_key:
            with st.spinner("Processing files..."):
                st.success("PDFs processed successfully!")
        else:
            st.warning("Please upload PDFs and enter your API key.")

    # Controls
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Reset"):
        st.session_state.conversation_history = []
        st.session_state.user_question = ""

    if col2.button("Rerun"):
        if 'user_question' in st.session_state:
            st.warning("The previous query will be discarded.")
            st.session_state.user_que
            stion = ""
            if st.session_state.conversation_history:
                st.session_state.conversation_history.pop()
        else:
            st.warning("Input field will be cleared.")

    user_question = st.text_input("Ask a question based on the PDFs:")
    if user_question and api_key and pdf_docs:
        user_input(user_question, api_key, pdf_docs, st.session_state.conversation_history)
        st.session_state.user_question = ""

if __name__ == "__main__":
    main()

