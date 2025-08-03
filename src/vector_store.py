import os
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore

def build_vector_store(texts, 
                       model_name="sentence-transformers/all-mpnet-base-v2"):
    """
    Creates FAISS index from list of text chunks.
    """
    hf_embed = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )
    # infer dimension
    dim = np.array(hf_embed.embed_query("test")).shape[0]
    index = faiss.IndexFlatL2(dim)

    store = FAISS(
        embedding_function=hf_embed.embed_query,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    store.add_texts(texts)
    return store

def save_vector_store(store, path="vectordb"):
    os.makedirs(path, exist_ok=True)
    store.save_local(path)

def load_vector_store(path="vectordb", embedding_fn=None):
    """
    embedding_fn: the same function used at build time
    """
    return FAISS.load_local(path, embeddings=embedding_fn)
