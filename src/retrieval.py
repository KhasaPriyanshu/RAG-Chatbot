def get_retriever(store, k: int = 5):
    """
    Returns a retriever to fetch top-k relevant docs.
    """
    retriever = store.as_retriever(search_kwargs={"k": k})
    return retriever
