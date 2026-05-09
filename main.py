from fastapi import FastAPI
from pydantic import BaseModel
import time
from src.Ingestion.ChunkRetriever import ExtractWeb, ChunkContent
from src.vector_db.Chroma_db_config import create_vector_db
from src.db.url_tracker import check_url_exists,insert_url
from src.Retriever.Retriever import retrieve
from src.Generator.Generated import generate_answer

app = FastAPI(
    title="RAG Pipeline API",
    description="Webpage-based RAG API using Groq + ChromaDB",
    version="1.0.0"
)

# -----------------------------
# Global variable
# -----------------------------
ingestion_completed = False


# -----------------------------
# Request Models
# -----------------------------
class IngestRequest(BaseModel):
    url: str


class QueryRequest(BaseModel):
    query: str


# -----------------------------
# Health Check API
# -----------------------------
@app.get("/")
def health_check():

    return {
        "status": "success",
        "message": "RAG API is running"
    }


# -----------------------------
# Ingestion API
# -----------------------------
@app.post("/ingest")
def ingest_webpage(request: IngestRequest):

    global ingestion_completed

    try:
        start_time = time.time()
        if (check_url_exists(request.url)):
            print("URL already processed")
            print("Skipping ingestion...")
            end_time = time.time()
            total_time = end_time - start_time
            print(total_time)
            print(f"Total Time: {total_time:.2f} seconds")
            return {
            "status": "success",
            "message": "Ingestion already exist"
        }
        else:
            # Step 1: Extract webpage
            docs = ExtractWeb(request.url)
            print("Docs part is complete")

            # Step 2: Chunking
            chunks = ChunkContent(docs)
            print("Chunks part is complete")
            # Step 3: Vector DB
            create_vector_db(chunks,request.url)
            print("vectordb part is complete")
            insert_url(request.url)
            ingestion_completed = True
        end_time = time.time()

        total_time = end_time - start_time
        print(total_time)
        print(f"Total Time: {total_time:.2f} seconds")
        return {
            "status": "success",
            "message": "Ingestion completed successfully",
            "url": request.url,
            "total_chunks": len(chunks)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# -----------------------------
# Query API
# -----------------------------
@app.post("/chat")
def chat_with_rag(request: QueryRequest):

    global ingestion_completed

    try:

        if not ingestion_completed:

            return {
                "status": "error",
                "message": "Please ingest webpage first"
            }

        # Step 1: Retrieve relevant chunks
        docs = retrieve(request.query)
        print("Augmentation part is complete")

        # Step 2: Generate answer
        answer = generate_answer(request.query, docs)
        print("generate_answer part is complete")

        return {
            "status": "success",
            "query": request.query,
            "answer": answer
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }