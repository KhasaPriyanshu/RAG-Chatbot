from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

def get_conversational_chain(api_key):
    template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details.
    If the answer is not in the provided context, just say "answer is not available in the context"—don't guess.

    Context:
    {context}
    Question:
    {question}
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)
