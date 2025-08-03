import os
import json
import faiss
import numpy as np
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load HF token
from dotenv import load_dotenv
load_dotenv()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def process_input(input_type: str, input_data, 
                  chunk_dir="chunks"):
    """
    Reads Link/PDF/TXT/DOCX/Text, splits into chunks, 
    saves each chunk as JSON in chunk_dir, and returns list of texts.
    """
    os.makedirs(chunk_dir, exist_ok=True)

    if input_type == "Link":
        loader = WebBaseLoader(input_data)
        docs = loader.load()
        texts = [doc.page_content for doc in docs]
    else:
        # read raw text
        if input_type == "PDF":
            reader = PdfReader(BytesIO(input_data.read()))
            raw = "".join(p.extract_text() for p in reader.pages)
        elif input_type == "DOCX":
            doc = Document(BytesIO(input_data.read()))
            raw = "\n".join(p.text for p in doc.paragraphs)
        elif input_type == "TXT":
            raw = input_data.read().decode("utf-8")
        elif input_type == "Text":
            raw = input_data
        else:
            raise ValueError(f"Unsupported: {input_type}")

        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = splitter.split_text(raw)

    # save chunks
    for i, txt in enumerate(texts):
        path = os.path.join(chunk_dir, f"chunk_{i:04d}.json")
        with open(path, "w") as f:
            json.dump({"text": txt}, f, ensure_ascii=False)

    return texts
