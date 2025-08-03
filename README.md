# RAG Q&A Chatbot

A Streamlit-based Retrieval-Augmented Generation system that ingests documents, creates embeddings with FAISS, and uses Google Generative AI for concise, accurate answers.

---

## Project Architecture and Flow

1. **Data Ingestion**  
   Raw files or URLs are loaded from `/data`.  
2. **Preprocessing & Chunking**  
   Documents are split into 200-character chunks and saved under `/chunks`.  
3. **Embedding & Vector Store**  
   Each chunk is embedded using the `sentence-transformers/all-mpnet-base-v2` model, then indexed in FAISS under `/vectordb`.  
4. **Retrieval & Generation Pipeline**  
   The pipeline (in `/src`) ties together:
   - A retriever that fetches top-K relevant chunks  
   - A generator (Google Generative AI) that streams answers based solely on retrieved context  
5. **Streamlit App**  
   `app.py` provides a UI for ingestion, querying, and live streaming of answers.

---

## Prerequisites

1. Clone this repository.
   ```bash
   git clone https://github.com/KhasaPriyanshu/RAG-Chatbot
   cd RAG-Chatbot
   ```
2. Setup the environment
   ```bash
   python -m venv myenv
   myenv\Scripts\Activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 1. Preprocessing & Chunk Creation

Run the notebook or script in `/notebooks` to experiment, or call directly from `/src/data_processing.py`:

```bash
python -c "from src.data_processing import process_input; \
process_input('PDF', open('data/AI Training Document.pdf','rb'))"
```

This will:

- Read your PDF/DOCX/TXT/Text or scrape a Link  
- Split into 150-char overlapping chunks  
- Save each chunk as JSON in `/chunks`

---

## 2. Embedding Generation & Vector Store

Use `/src/vector_store.py` to:

1. Load chunk files from `/chunks`  
2. Generate embeddings with `sentence-transformers/all-mpnet-base-v2`  
3. Build a FAISS index and persist it to `/vectordb`  
4. Example:
   ```bash
   python - <<EOF
   from src.vector_store import build_vector_store, save_vector_store
   import json, glob
   texts = [json.load(open(f))['text'] for f in glob.glob('chunks/*.json')]
   store = build_vector_store(texts)
   save_vector_store(store, 'vectordb')
   EOF
   ```

---

## 3. Model & Embedding Choices

- **Embedding Model:**  
  `models/embedding-001`  
  • Excellent semantic coverage, CPU-friendly, 768‐dimensional vectors.

- **Generation Model:**  
  `gemini-1.5-flash`  
  • Lightweight instruct-tuned model with fast latency and high quality.  
  • Supports streaming via `ChatGoogleGenerativeAI`

---

## 4. Building the RAG Pipeline

All logic lives under `/src`:

- `data_processing.py` – ingestion & chunking  
- `vector_store.py` – embedding & FAISS index management  
- `retrieval.py` – top-K document retriever  
- `generation.py` – answer generation with streaming support  
- `pipeline.py` – orchestrates ingest, load, and answer flows

Instantiate and call in Python:
```python
from src.pipeline import DocumentQA

qa = DocumentQA(persist_dir='vectordb')
qa.load(model_name='sentence-transformers/all-mpnet-base-v2')
for token in qa.answer("What is the main idea?", stream=True):
    print(token, end="", flush=True)
```

---

## 5. Running the Chatbot with Streaming

Launch the Streamlit UI to ingest docs and ask questions interactively:
```bash
streamlit run app.py
```

- **Streaming Response:**  
  Answers appear token by token for instant feedback.  
- **Reset/Rerun:**  
  Use the sidebar "Reset” button to rerun the query.
  Use the sidebar "Rerun" button to clear all indexed data.
- **Live Metrics:**  
  Sidebar displays current model in use.

---

## Directory Structure

```
.
├── app.py
├── requirements.txt
├── README.md
├── data/         # raw PDFs, DOCX, TXT, etc.
├── chunks/       # JSON-saved text chunks
├── vectordb/     # persisted FAISS indexes
└── src/          # modular pipeline code
    ├── data_processing.py
    ├── vector_store.py
    ├── retrieval.py
    ├── generation.py
    └── pipeline.py
```



https://github.com/user-attachments/assets/928d8fef-67db-4e99-8c19-67c495ce84b5


