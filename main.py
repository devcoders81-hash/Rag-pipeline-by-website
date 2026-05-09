from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from src.Ingestion.ChunkRetriever import (
    ExtractWeb,
    ChunkContent
)

from src.vector_db.Chroma_db_config import (
    create_vector_db,
    load_vector_db
)

from src.db.url_tracker import (
    check_url_exists,
    insert_url,
    init_db
)

from src.Retriever.Retriever import retrieve
from src.Generator.Generated import generate_answer


# ---------------------------------------------------
# FastAPI App
# ---------------------------------------------------
app = FastAPI(
    title="RAG Pipeline API",
    description="Webpage-based RAG API using Groq + ChromaDB",
    version="1.0.0"
)


# ---------------------------------------------------
# CORS
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------
# Startup Event
# ---------------------------------------------------
@asynccontextmanager
def startup_event():

    print("Initializing application...")

    # Initialize SQLite
    init_db()

    # Load ChromaDB once
    load_vector_db()

    print("Application started successfully")


# ---------------------------------------------------
# Request Models
# ---------------------------------------------------
class IngestRequest(BaseModel):
    url: str


class QueryRequest(BaseModel):
    query: str


# ---------------------------------------------------
# Health Check API
# ---------------------------------------------------
@app.get("/")
def health_check():

    return {
        "status": "success",
        "message": "RAG API is running"
    }


# ---------------------------------------------------
# Ingestion API
# ---------------------------------------------------
@app.post("/ingest")
def ingest_webpage(request: IngestRequest):

    try:

        start_time = time.time()

        # -------------------------------------------
        # Check URL already exists
        # -------------------------------------------
        if check_url_exists(request.url):

            end_time = time.time()

            total_time = end_time - start_time

            return {
                "status": "success",
                "message": "URL already ingested",
                "url": request.url,
                "total_time_seconds": round(total_time, 2)
            }

        # -------------------------------------------
        # Step 1 → Extract webpage
        # -------------------------------------------
        docs = ExtractWeb(request.url)

        print("Docs extraction complete")

        # -------------------------------------------
        # Step 2 → Chunking
        # -------------------------------------------
        chunks = ChunkContent(docs)

        print("Chunking complete")

        # -------------------------------------------
        # Step 3 → Store in Vector DB
        # -------------------------------------------
        create_vector_db(
            chunks=chunks,
            url=request.url
        )

        print("Vector DB insertion complete")

        # -------------------------------------------
        # Step 4 → Save URL in SQLite
        # -------------------------------------------
        insert_url(request.url)

        print("URL stored in SQLite")

        end_time = time.time()

        total_time = end_time - start_time

        return {
            "status": "success",
            "message": "Ingestion completed successfully",
            "url": request.url,
            "total_chunks": len(chunks),
            "total_time_seconds": round(total_time, 2)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ---------------------------------------------------
# Query API
# ---------------------------------------------------
@app.post("/chat")
def chat_with_rag(request: QueryRequest):

    try:

        start_time = time.time()

        # -------------------------------------------
        # Step 1 → Retrieve relevant chunks
        # -------------------------------------------
        docs = retrieve(request.query)

        print("Retrieval complete")

        # -------------------------------------------
        # Step 2 → Generate answer
        # -------------------------------------------
        answer = generate_answer(
            request.query,
            docs
        )

        print("Answer generation complete")

        end_time = time.time()

        total_time = end_time - start_time

        return {
            "status": "success",
            "query": request.query,
            "answer": answer,
            "retrieved_chunks": len(docs),
            "total_time_seconds": round(total_time, 2)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }