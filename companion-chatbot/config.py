import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables from a local `.env` file.
load_dotenv()

# Detect if running on Render cloud
IS_RENDER = os.getenv("RENDER") is not None

# Set appropriate paths based on environment
# Render persistent disk mounted at /var/data
QDRANT_PATH = "/var/data/.mem0/qdrant" if IS_RENDER else os.path.expanduser("~/.mem0/qdrant")
HISTORY_DB_PATH = "/var/data/.mem0/history.db" if IS_RENDER else os.path.expanduser("~/.mem0/history.db")

MEM0_CONFIG = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-nano",
            "temperature": 0.8,
            "max_tokens": 20000,
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": os.getenv("OPENAI_API_KEY"),
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "companion_memories",
            "embedding_model_dims": 1536,
            "client": QdrantClient(
                path=QDRANT_PATH,
                force_disable_check_same_thread=True,
            ),
        },
    },
    "history_db_path": HISTORY_DB_PATH,
}

USER_ID = "companion_user"
