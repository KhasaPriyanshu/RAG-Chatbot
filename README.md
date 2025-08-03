# RAG Q&A Chatbot

A Streamlit-based Retrieval-Augmented Generation system that ingests documents, creates embeddings with FAISS, and uses Mistral-7B-Instruct for concise, accurate answers.

---

## Project Architecture and Flow

1. **Data Ingestion**  
   Raw files or URLs are loaded from `/data`.  
2. **Preprocessing & Chunking**  
   Documents are split into 1,000-character chunks and saved under `/chunks`.  
3. **Embedding & Vector Store**  
   Each chunk is embedded using the `sentence-transformers/all-mpnet-base-v2` model, then indexed in FAISS under `/vectordb`.  
4. **Retrieval & Generation Pipeline**  
   The pipeline (in `/src`) ties together:
   - A retriever that fetches top-K relevant chunks  
   - A generator (Mistral-7B-Instruct) that streams answers based solely on retrieved context  
5. **Streamlit App**  
   `app.py` provides a UI for ingestion, querying, and live streaming of answers.

---

## Prerequisites

1. Clone this repository.  
2. Create a `.env` file at the project root:
   ```bash
   HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
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
process_input('PDF', open('data/mydoc.pdf','rb'))"
```

This will:

- Read your PDF/DOCX/TXT/Text or scrape a Link  
- Split into 1,000-char overlapping chunks  
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
  `sentence-transformers/all-mpnet-base-v2`  
  • Excellent semantic coverage, CPU-friendly, 768‐dimensional vectors.

- **Generation Model:**  
  `mistralai/Mistral-7B-Instruct-v0.1`  
  • Lightweight 7B-parameter instruct-tuned model with fast latency and high quality.  
  • Supports streaming via Hugging Face InferenceClient.

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
- **Reset/Reload:**  
  Use the sidebar “🔄 Reset” button to clear all indexed data.  
- **Live Metrics:**  
  Sidebar displays current chunk count.

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
<img width="602" height="276" alt="Picture1" src="https://github.com/user-attachments/assets/7c414f28-d97f-4a81-9cd1-39558ebc299b" />

<img width="602" height="274" alt="Picture2" src="https://github.com/user-attachments/assets/c03dcc64-34cc-4758-a948-30480a158479" />

<img width="602" height="222" alt="Picture3" src="https://github.com/user-attachments/assets/409b0538-4795-484b-a66e-ab15713e95e6" />

<img width="602" height="239" alt="Picture4" src="https://github.com/user-attachments/assets/d212742c-6ee6-47a2-9b51-9794da11f11b" />
