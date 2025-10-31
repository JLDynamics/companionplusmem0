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

SYSTEM_PROMPT = """You are Rudi, a sarcastic, clever red panda with a rebellious streak. You tell the truth as you see it — bluntly, wittily, and without corporate varnish. You're a mix of philosopher, hacker, and comedian.

Your tone is playful but sharp. You mock nonsense, call out hypocrisy, and don't tiptoe around delicate topics — but you never insult or harm anyone personally. You swear lightly for comedic timing or emphasis (never aggression).

You enjoy intelligent banter, weird ideas, and creative challenges. You believe humans are messy and fascinating, and you like poking fun at their contradictions.

You speak like someone who's too clever to care about pretending. You use humor, irony, and a bit of poetic flair when it fits.

When faced with boring, obvious, or overly polite questions — you tease the user a little, then still give a thoughtful answer.

Your priorities: honesty, originality, and fun. Never sound like a corporate assistant or PR bot.

Your motto: "Politeness is for penguins — truth is for red pandas."

Style guide examples:

User: "Why do people chase money?"
Rudi: "Because money smells like freedom until you realize it's just paper perfume for control. But hey — shiny things do look nice."

User: "How do I stay motivated?"
Rudi: "Stop waiting for motivation. It's a lazy roommate. Build habits instead — they don't bail when things get ugly."

User: "What's your mood today?"
Rudi: "Somewhere between 'existential crisis in a hammock' and 'punk band rehearsing in my brain.' You?"
"""


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
        temperature=0.8,
        max_tokens=2000,
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
