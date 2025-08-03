import os
from .data_processing.py import process_input
from .vector_store import build_vector_store, save_vector_store, load_vector_store
from .retrieval import get_retriever
from .generation import generate_answer

class DocumentQA:
    def __init__(self, persist_dir="vectordb"):
        self.persist_dir = persist_dir
        self.store = None

    def ingest(self, input_type, input_data):
        texts = process_input(input_type, input_data)
        self.store = build_vector_store(texts)
        save_vector_store(self.store, self.persist_dir)

    def load(self, model_name=None):
        from langchain_community.embeddings import HuggingFaceEmbeddings
        hf = HuggingFaceEmbeddings(model_name=model_name, device="cpu")
        self.store = load_vector_store(self.persist_dir, embedding_fn=hf.embed_query)

    def answer(self, query, top_k=5, stream=True):
        retriever = get_retriever(self.store, k=top_k)
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = (
            f"Use only the context below to answer concisely.\n\n"
            f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
        )

        return generate_answer(prompt, stream=stream)
