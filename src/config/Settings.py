from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

DB_DIR = os.getenv("DB_DIR")