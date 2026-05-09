from langchain_chroma import Chroma

from src.Ingestion.EmbeddedRetriever import get_embedding_model
from src.config.Settings import DB_DIR

# ----------------------------------------
# Global variables
# ----------------------------------------
embedding_model = None
vectordb = None


# ----------------------------------------
# Load embedding model only once
# ----------------------------------------
def get_embedding():

    global embedding_model

    if embedding_model is None:

        print("Loading embedding model...")

        embedding_model = get_embedding_model()

    return embedding_model


# ----------------------------------------
# Load vector DB only once
# ----------------------------------------
def load_vector_db():

    global vectordb

    if vectordb is None:

        print("Loading ChromaDB...")

        vectordb = Chroma(
            collection_name="web_rag",
            persist_directory=DB_DIR,
            embedding_function=get_embedding()
        )

    return vectordb


# ----------------------------------------
# Insert documents
# ----------------------------------------
def create_vector_db(chunks, url):

    vectordb = load_vector_db()

    ids = []

    for index, chunk in enumerate(chunks):

        chunk.metadata["source"] = url

        unique_id = f"{url}_{index}"

        ids.append(unique_id)

    vectordb.add_documents(
        documents=chunks,
        ids=ids
    )

    print("Documents inserted successfully")

    return vectordb