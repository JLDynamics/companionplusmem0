from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import os

# Import existing companion functions
from companion import memory, openai_client, SYSTEM_PROMPT, format_memory_context, fetch_relevant_memories
from config import USER_ID

app = FastAPI(
    title="Rudi - AI Companion",
    description="Personal AI companion with memory using Mem0",
    version="1.0.0"
)

# Enable CORS for mobile browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str = USER_ID

class ChatResponse(BaseModel):
    response: str

class MemoriesResponse(BaseModel):
    memories: List[Dict]

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint for uptime monitoring"""
    # Note: SYSTEM_PROMPT is imported from companion.py (Rudi's personality)
    return {"status": "healthy", "service": "rudi-companion"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user message and returns AI response
    Uses existing companion.py logic with memory integration
    """
    try:
        # 1. Fetch relevant memories using existing function
        memories = fetch_relevant_memories(request.message, limit=5)
        memory_context = format_memory_context(memories)
        
        # 2. Build messages with system prompt and memory context
        system_message = f"""{SYSTEM_PROMPT}

Relevant memories about this user:
{memory_context}
"""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": request.message}
        ]
        
        # 3. Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.8,
            max_tokens=2000
        )
        
        assistant_response = response.choices[0].message.content.strip()
        
        # 4. Store conversation in memory
        memory.add(
            messages=[
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": assistant_response}
            ],
            user_id=request.user_id,
            metadata={"source": "web-interface"}
        )
        
        return ChatResponse(response=assistant_response)
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/memories", response_model=MemoriesResponse)
async def get_memories(user_id: str = USER_ID):
    """Retrieve all stored memories for the user"""
    try:
        all_memories = memory.get_all(user_id=user_id)
        return MemoriesResponse(memories=all_memories.get("results", []))
    except Exception as e:
        print(f"Error fetching memories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Memory fetch error: {str(e)}")

# Mount static files (HTML/CSS/JS)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Static directory doesn't exist yet, will be created
    print("Static directory not found, will be created during deployment")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
