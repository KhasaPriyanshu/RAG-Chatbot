vector_store.save_local("vectordb/faiss_index")
new_db = FAISS.load_local("vectordb/faiss_index", embeddings, allow_dangerous_deserialization=True)
