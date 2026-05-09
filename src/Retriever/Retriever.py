from src.vector_db.Chroma_db_config import load_vector_db

vectordb = load_vector_db()

def retrieve(query: str, k: int = 3):

    retriever = vectordb.as_retriever(
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    return docs