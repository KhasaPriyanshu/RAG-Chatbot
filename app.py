import streamlit as st
from src.pipeline import DocumentQA

def main():
    st.set_page_config(page_title="📖 RAG Q&A Chatbot", layout="wide")
    st.title("RAG Q&A Chatbot")

    qa = DocumentQA()

    # Sidebar
    with st.sidebar:
        st.header("Info")
        if "ingested" in st.session_state:
            st.write(f"Chunks Indexed: {st.session_state['ingested']}")
        else:
            st.write("No data ingested.")
        if st.button("🔄 Reset"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.experimental_rerun()

    # Ingestion
    input_type = st.selectbox("Select Input Type", ["Link", "PDF", "Text", "DOCX", "TXT"])
    if input_type == "Link":
        url = st.text_input("Enter URL")
    elif input_type == "Text":
        text = st.text_area("Paste text here")
    else:
        file = st.file_uploader("Upload file", type=[input_type.lower()])

    if st.button("➡️ Ingest"):

        data = url if input_type=="Link" else (text if input_type=="Text" else file)
        qa.ingest(input_type, data)
        st.session_state["ingested"] = len(qa.store.docstore.docs)

    # Query
    if "ingested" in st.session_state:
        query = st.text_input("Ask a question:")
        if query and st.button("🤔 Get Answer"):
            placeholder = st.empty()
            answer = ""  # accumulate streamed tokens
            for token in qa.answer(query, stream=True):
                answer += token
                placeholder.markdown(answer)

if __name__ == "__main__":
    main()
