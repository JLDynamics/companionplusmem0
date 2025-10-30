# Fix readline keybindings on macOS - must be imported before anything else
import sys
import os
try:
    import gnureadline as readline
    sys.modules['readline'] = readline
    readline.read_init_file(os.path.expanduser("~/.inputrc"))
except (ImportError, FileNotFoundError):
    pass

from typing import Dict, List, Tuple

from mem0 import Memory
from openai import OpenAI

from config import MEM0_CONFIG, USER_ID


def _init_clients() -> Tuple[Memory, OpenAI]:
    """Initialize Mem0 memory and OpenAI chat client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a `.env` file with the key or export it in your shell."
        )

    memory_client = Memory.from_config(MEM0_CONFIG)
    llm_client = OpenAI(api_key=api_key)
    return memory_client, llm_client


memory, openai_client = _init_clients()

SYSTEM_PROMPT = (
    "You are a warm, detail-oriented personal companion. Use the provided stored memories to personalize every reply. "
    "If no memories are available, continue the conversation naturally and capture new details for future recall. "
    "Keep responses concise, supportive, and proactive about remembering new facts."
)


def fetch_relevant_memories(query: str, limit: int = 5) -> List[Dict]:
    """Retrieve the most relevant stored memories for the current user."""
    search_response = memory.search(query, user_id=USER_ID, limit=limit)
    return search_response.get("results", [])


def format_memory_context(memories: List[Dict]) -> str:
    """Turn matching memories into a readable context block for the LLM."""
    if not memories:
        return "No stored memories yet."

    formatted = [f"{idx + 1}. {item.get('memory', '').strip()}" for idx, item in enumerate(memories)]
    return "\n".join(formatted)


def chat_with_companion(user_input: str) -> str:
    """Generate a personalized response and persist the interaction in Mem0."""
    memories = fetch_relevant_memories(user_input)
    memory_context = format_memory_context(memories)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Here is the existing memory context for this user:\n"
                f"{memory_context}\n\n"
                f"User says: {user_input}"
            ),
        },
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        temperature=0.2,
        max_tokens=500,
    )

    assistant_message = response.choices[0].message.content.strip()

    memory.add(
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_message},
        ],
        user_id=USER_ID,
        metadata={"source": "companion-chatbot"},
    )

    return assistant_message


def view_all_memories() -> None:
    """Print every stored memory for the current user."""
    memories = memory.get_all(user_id=USER_ID).get("results", [])
    if not memories:
        print("\n📚 No memories stored yet.\n")
        return

    print("\n📚 Your Stored Memories:")
    print("=" * 50)
    for idx, mem in enumerate(memories, start=1):
        print(f"{idx}. {mem.get('memory', '').strip()}")
    print("=" * 50 + "\n")


def main() -> None:
    """Interactive CLI loop for the personal companion chatbot."""
    print("🤖 Personal Companion Chatbot (Mem0 + GPT-4.1-nano)")
    print("=" * 60)
    print("Commands: 'memories' to view | 'exit' to quit")
    print("=" * 60 + "\n")

    while True:
        user_input = input("💭 You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("\n👋 Goodbye!\n")
            break

        if user_input.lower() == "memories":
            view_all_memories()
            continue

        try:
            response = chat_with_companion(user_input)
            print(f"\n🤖 Assistant: {response}\n")
        except Exception as exc:
            print(f"\n❌ Error: {exc}\n")


if __name__ == "__main__":
    main()
