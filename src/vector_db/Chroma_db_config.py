from langchain_community.vectorstores import Chroma
from src.Ingestion.EmbeddedRetriever import get_embedding_model
from src.config.Settings import DB_DIR

# Create embedding model object
embedding_model = get_embedding_model()

# Create Chroma DB
vectordb = Chroma(
    collection_name="web_rag",
    persist_directory=DB_DIR,
    embedding_function=embedding_model
)


# ----------------------------------------
# Create Vector DB
# ----------------------------------------
def create_vector_db(chunks, url):

    ids = []

    for index, chunk in enumerate(chunks):

        chunk.metadata["source"] = url

        unique_id = f"{url}_{index}"

        ids.append(unique_id)

    vectordb.add_documents(
        documents=chunks,
        ids=ids
    )

    return vectordb


# ----------------------------------------
# Load Existing Vector DB
# ----------------------------------------
def load_vector_db():

    vectordb = Chroma(
        collection_name="web_rag",
        persist_directory=DB_DIR,
        embedding_function=embedding_model
    )

    return vectordb