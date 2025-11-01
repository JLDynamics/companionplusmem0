import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables from a local `.env` file.
load_dotenv()

# Detect if running on Render cloud
IS_RENDER = os.getenv("RENDER") is not None

# Get Qdrant Cloud credentials (only set in Render environment)
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Configure storage based on environment
if IS_RENDER and QDRANT_URL and QDRANT_API_KEY:
    # ==== RENDER (iPhone) ====
    # Use Qdrant Cloud with separate collection for iPhone
    print("🌐 Render detected - Using Qdrant Cloud for persistent iPhone memories")
    
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=10,  # 10 second timeout for cloud API
    )
    
    COLLECTION_NAME = "companion_memories_iphone"  # Separate collection!
    
    # Create /tmp/.mem0 directory if it doesn't exist
    import os as _os
    _tmp_dir = "/tmp/.mem0"
    _os.makedirs(_tmp_dir, exist_ok=True)
    HISTORY_DB_PATH = "/tmp/.mem0/history_iphone.db"  # Ephemeral, but not critical
    
    print(f"✅ Connected to Qdrant Cloud")
    print(f"📱 iPhone collection: {COLLECTION_NAME}")
    
else:
    # ==== MAC (Local Terminal) ====
    # Use local Qdrant storage with separate collection for Mac
    print("💻 Mac detected - Using local storage for Mac memories")
    
    QDRANT_PATH = os.path.expanduser("~/.mem0/qdrant")
    
    qdrant_client = QdrantClient(
        path=QDRANT_PATH,
        force_disable_check_same_thread=True,
    )
    
    COLLECTION_NAME = "companion_memories_mac"  # Separate collection!
    HISTORY_DB_PATH = os.path.expanduser("~/.mem0/history.db")
    
    print(f"✅ Using local storage: {QDRANT_PATH}")
    print(f"💻 Mac collection: {COLLECTION_NAME}")

# Mem0 configuration
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
            "collection_name": COLLECTION_NAME,  # Different per environment!
            "embedding_model_dims": 1536,
            "client": qdrant_client,
        },
    },
    "history_db_path": HISTORY_DB_PATH,
}

USER_ID = "companion_user"

# Validation
if IS_RENDER and not (QDRANT_URL and QDRANT_API_KEY):
    print("⚠️  WARNING: Running on Render but Qdrant Cloud credentials not found!")
    print("⚠️  Memories will NOT persist. Please set QDRANT_URL and QDRANT_API_KEY.")
