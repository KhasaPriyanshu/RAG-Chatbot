import os
from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def generate_answer(prompt: str, 
                    model="mistralai/Mistral-7B-Instruct-v0.1",
                    max_tokens=256,
                    temperature=0.6,
                    stream: bool = True):
    """
    Yields response chunks if stream=True, else returns full text.
    """
    client = InferenceClient(model=model, token=HF_TOKEN)
    params = dict(
        prompt=prompt,
        max_new_tokens=max_tokens,
        temperature=temperature,
        stream=stream
    )
    response = client.text_generation(**params)

    if not stream:
        return response.text

    # streaming generator
    for chunk in response:
        yield chunk.text
