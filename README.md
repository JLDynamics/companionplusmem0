# 🦝 Rudi - Personal AI Companion Chatbot

A sarcastic red panda AI companion with persistent memory, powered by OpenAI GPT-4.1-nano, Mem0, and Qdrant. Features separate storage for Mac terminal and iPhone web interface.

---

## ✨ Features

- 🧠 **Persistent Long-Term Memory** - Remembers your preferences, conversations, and life details
- 🦝 **Sarcastic Red Panda Personality** - Meet Rudi, your sardonic AI companion
- 💻 **Mac Terminal Interface** - Full-featured command-line chatbot
- 📱 **iPhone Web App** - Mobile-optimized dark theme with touch controls
- 🔒 **Privacy-First Design** - Self-hosted with separate Mac/cloud storage (no sync)
- 🌐 **Free Cloud Hosting** - Deployed on Render.com (free tier)
- ⚡ **Cost-Effective** - Uses gpt-4.1-nano for fast, affordable responses
- 🎭 **Rich Personality System** - Context-aware responses with memory-driven conversations
- 📊 **Memory Management** - View, search, and manage stored memories

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Mac Terminal                      │
│   python3 companion.py              │
│   ↓                                 │
│   Local Qdrant                      │
│   ~/.mem0/qdrant/                   │
│   Collection: companion_memories    │
│   ✅ 44+ memories (persistent)      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   iPhone Safari                     │
│   https://your-app.onrender.com     │
│   ↓                                 │
│   Render.com (FastAPI Server)       │
│   ↓                                 │
│   Qdrant Cloud (Free Tier)          │
│   Collection: companion_memories_iphone │
│   ✅ 34+ memories (persistent)      │
└─────────────────────────────────────┘
```

**Storage Strategy:**
- **Mac:** Local Qdrant database (`~/.mem0/qdrant/`) - completely separate
- **iPhone:** Qdrant Cloud (1GB free) - completely separate
- **No sync by design** - keeps personal Mac memories private

---

## 🚀 Quick Start

### Mac Terminal Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JLDynamics/companionplusmem0.git
   cd companionplusmem0/companion-chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```bash
   OPENAI_API_KEY=sk-proj-your-key-here
   ```

4. **Run the chatbot:**
   ```bash
   python3 companion.py
   ```

5. **Chat with Rudi:**
   ```
   You: Hi, my name is Jack
   Rudi: Well hello there, Jack. Ready to grace me with your riveting conversation?
   
   You: Remember that I love pizza
   Rudi: Pizza lover, noted. How original.
   
   You: memories
   # Shows all stored memories
   
   You: exit
   # Saves and exits
   ```

**Commands:**
- `memories` - View all stored memories
- `clear` - Clear conversation history (keeps memories)
- `exit` - Save and quit

---

## 📱 iPhone Web Deployment

### Step 1: Set up Qdrant Cloud (Free)

1. Sign up at [cloud.qdrant.io](https://cloud.qdrant.io) (free, no credit card)
2. Create a cluster:
   - Name: `rudi-memories`
   - Cloud: AWS
   - Region: `us-west-2` (or closest to you)
   - Plan: **Free Tier** (1GB storage)
3. Get credentials:
   - **Cluster URL**: Copy from dashboard (e.g., `https://abc123.aws.cloud.qdrant.io:6333`)
   - **API Key**: Click "API Keys" → "Create" → Copy key

### Step 2: Deploy to Render.com

1. **Push code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Deploy Rudi to Render"
   git push origin main
   ```

2. **Create Render service:**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: `rudi-companion`
     - **Root Directory**: `companion-chatbot`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free

3. **Add environment variables** in Render dashboard:

   | Key | Value |
   |-----|-------|
   | `OPENAI_API_KEY` | `sk-proj-your-openai-key` |
   | `RENDER` | `true` |
   | `QDRANT_URL` | `https://your-cluster.aws.cloud.qdrant.io:6333` |
   | `QDRANT_API_KEY` | `your-qdrant-api-key` |

4. **Deploy** - Wait ~3 minutes for deployment

### Step 3: Access on iPhone

1. Open Safari on iPhone
2. Go to: `https://rudi-companion.onrender.com` (your Render URL)
3. Chat with Rudi!
4. **Add to Home Screen** for app-like experience:
   - Tap Share button → "Add to Home Screen"
   - Removes Safari UI for cleaner interface

**iPhone Features:**
- 💬 Chat interface with auto-scrolling
- 📚 "Memories" button (top right) to view stored memories
- 🌙 Dark theme optimized for mobile
- ⌨️ Auto-resizing text input
- 🔄 Persistent memories (survive app restarts)

---

## 🔧 Configuration

### Personality Customization

Edit `companion.py` to change Rudi's personality:

```python
SYSTEM_PROMPT = """
You are Rudi, a sarcastic red panda AI companion...
[Modify personality traits here]
"""
```

### Model Configuration

Change AI model in `config.py`:

```python
"llm": {
    "provider": "openai",
    "config": {
        "model": "gpt-4.1-nano",  # Change model here
        "temperature": 0.8,        # 0.0 = focused, 1.0 = creative
        "max_tokens": 20000,
    }
}
```

**Supported models:**
- `gpt-4.1-nano` (default, fast & cheap)
- `gpt-4o-mini` (smarter, slightly slower)
- `gpt-4` (most capable, expensive)

### Memory Settings

Adjust memory retrieval in `companion.py`:

```python
relevant_memories = memory.search(
    query=user_input,
    user_id=USER_ID,
    limit=3  # Number of memories to retrieve (3-5 recommended)
)
```

---

## 📂 Project Structure

```
companionplusmem0/
├── companion-chatbot/
│   ├── companion.py          # Main Mac terminal chatbot
│   ├── api.py                # FastAPI server for iPhone
│   ├── config.py             # Configuration & Mem0 setup
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # API keys (gitignored)
│   ├── .env.example          # Environment template
│   ├── static/
│   │   └── index.html        # iPhone web interface
│   ├── export_memories.py    # Export Mac memories to JSON
│   ├── import_memories.py    # Import memories to Qdrant Cloud
│   └── .gitignore
├── README.md
└── DEPLOYMENT.md             # Detailed deployment guide
```

---

## 🔄 Syncing Memories (Optional)

By default, Mac and iPhone memories are **separate**. To copy Mac memories to iPhone:

1. **Export Mac memories:**
   ```bash
   cd companion-chatbot
   python3 export_memories.py
   # Creates: memories_export.json
   ```

2. **Import to Qdrant Cloud:**
   ```bash
   # Set environment variables first:
   export QDRANT_URL="https://your-cluster.aws.cloud.qdrant.io:6333"
   export QDRANT_API_KEY="your-qdrant-api-key"
   export OPENAI_API_KEY="sk-proj-your-key"
   
   python3 import_memories.py
   ```

3. **Verify on iPhone:**
   - Open your app
   - Click "Memories" button
   - See imported memories

**Note:** This is a one-time copy. Future memories stay separate.

---

## 💰 Cost Breakdown

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| **Render.com** | Web hosting (free tier) | $0 |
| **Qdrant Cloud** | 1GB vector storage (free tier) | $0 |
| **OpenAI API** | ~2000 messages with gpt-4.1-nano | ~$1-2 |
| **Total** | | **~$1-2/month** |

**Storage Capacity:**
- 1GB Qdrant Cloud = ~34,000 memories
- At 2000 messages/month = **3+ years** before full

---

## 🐛 Troubleshooting

### Mac Terminal Issues

**Error: "OPENAI_API_KEY is not set"**
```bash
# Create .env file:
echo "OPENAI_API_KEY=sk-proj-your-key" > .env
```

**Error: "Database is locked"**
```bash
# Kill existing process:
pkill -f companion.py
```

**Memory not working:**
```bash
# Check Qdrant data exists:
ls -la ~/.mem0/qdrant/
```

### iPhone/Render Issues

**Error: "Permission denied: '/var/data'"**
- Solution: Make sure `QDRANT_URL` and `QDRANT_API_KEY` are set in Render

**Error: "Unable to open database file"**
- Solution: Redeploy - the latest code creates `/tmp/.mem0/` directory

**Memories not persisting:**
- Check Render logs for "Connected to Qdrant Cloud" message
- Verify `QDRANT_URL` includes `:6333` port
- Check Qdrant dashboard for `companion_memories_iphone` collection

**App won't load:**
```bash
# Check Render logs at:
https://dashboard.render.com → Your Service → Logs
```

---

## 🔒 Security & Privacy

- ✅ **API keys stored in `.env`** (gitignored, never committed)
- ✅ **Separate storage** - Mac and iPhone don't share data
- ✅ **Self-hosted** - You own your data
- ✅ **No analytics** - No tracking or telemetry
- ✅ **Open source** - Audit the code yourself

**Never share your:**
- OpenAI API key
- Qdrant API key
- `.env` file

---

## 📊 Mem0 Research Highlights

- **+26% Accuracy** over OpenAI Memory on LOCOMO benchmark
- **91% Faster Responses** than full-context retrieval
- **90% Lower Token Usage** than full-context, cutting costs
- [Read the full paper](https://mem0.ai/research)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📚 Documentation & Resources

- **Mem0 Docs**: https://docs.mem0.ai
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **OpenAI API**: https://platform.openai.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## 💬 Support & Community

- **GitHub Issues**: [Report bugs](https://github.com/JLDynamics/companionplusmem0/issues)
- **Mem0 Discord**: [Join community](https://mem0.dev/DiG)
- **Email**: licanada2010@gmail.com

---

## 📜 Citation

If you use Mem0 in research:

```bibtex
@article{mem0,
  title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
  author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
  journal={arXiv preprint arXiv:2504.19413},
  year={2025}
}
```

---

## ⚖️ License

Apache 2.0 - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Mem0** - Memory layer framework
- **Qdrant** - Vector database
- **OpenAI** - Language models
- **Render** - Free hosting platform

---

## 🎯 Roadmap

- [ ] Voice input support
- [ ] Image memory (remember photos)
- [ ] Multi-user support
- [ ] Memory export/backup automation
- [ ] Telegram bot integration
- [ ] Android app

---

**Built with ❤️ by Jack | Powered by Mem0, OpenAI, and Qdrant**

**Star ⭐ this repo if you find it helpful!**
   - Go to: `https://your-service.onrender.com`
   - Tap "Add to Home Screen" for app-like experience

##  🔥 Research Highlights
- **+26% Accuracy** over OpenAI Memory on the LOCOMO benchmark
- **91% Faster Responses** than full-context, ensuring low-latency at scale
- **90% Lower Token Usage** than full-context, cutting costs without compromise
- [Read the full paper](https://mem0.ai/research)

# Introduction

[Mem0](https://mem0.ai) ("mem-zero") enhances AI assistants and agents with an intelligent memory layer, enabling personalized AI interactions. It remembers user preferences, adapts to individual needs, and continuously learns over time—ideal for customer support chatbots, AI assistants, and autonomous systems.

### Key Features & Use Cases

**Core Capabilities:**
- **Multi-Level Memory**: Seamlessly retains User, Session, and Agent state with adaptive personalization
- **Developer-Friendly**: Intuitive API, cross-platform SDKs, and a fully managed service option

**Applications:**
- **AI Assistants**: Consistent, context-rich conversations
- **Customer Support**: Recall past tickets and user history for tailored help
- **Healthcare**: Track patient preferences and history for personalized care
- **Productivity & Gaming**: Adaptive workflows and environments based on user behavior

## 🚀 Quickstart Guide <a name="quickstart"></a>

Choose between our hosted platform or self-hosted package:

### Hosted Platform

Get up and running in minutes with automatic updates, analytics, and enterprise security.

1. Sign up on [Mem0 Platform](https://app.mem0.ai)
2. Embed the memory layer via SDK or API keys

### Self-Hosted (Open Source)

Install the sdk via pip:

```bash
pip install mem0ai
```

Install sdk via npm:
```bash
npm install mem0ai
```

### Basic Usage

Mem0 requires an LLM to function, with `gpt-4.1-nano-2025-04-14 from OpenAI as the default. However, it supports a variety of LLMs; for details, refer to our [Supported LLMs documentation](https://docs.mem0.ai/components/llms/overview).

First step is to instantiate the memory:

```python
from openai import OpenAI
from mem0 import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Retrieve relevant memories
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # Generate Assistant response
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}]
    response = openai_client.chat.completions.create(model="gpt-4.1-nano-2025-04-14", messages=messages)
    assistant_response = response.choices[0].message.content

    # Create new memories from the conversation
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()
```

For detailed integration steps, see the [Quickstart](https://docs.mem0.ai/quickstart) and [API Reference](https://docs.mem0.ai/api-reference).

## 🔗 Integrations & Demos

- **ChatGPT with Memory**: Personalized chat powered by Mem0 ([Live Demo](https://mem0.dev/demo))
- **Browser Extension**: Store memories across ChatGPT, Perplexity, and Claude ([Chrome Extension](https://chromewebstore.google.com/detail/onihkkbipkfeijkadecaafbgagkhglop?utm_source=item-share-cb))
- **Langgraph Support**: Build a customer bot with Langgraph + Mem0 ([Guide](https://docs.mem0.ai/integrations/langgraph))
- **CrewAI Integration**: Tailor CrewAI outputs with Mem0 ([Example](https://docs.mem0.ai/integrations/crewai))

## 📚 Documentation & Support

- Full docs: https://docs.mem0.ai
- Community: [Discord](https://mem0.dev/DiG) · [Twitter](https://x.com/mem0ai)
- Contact: founders@mem0.ai

## Citation

We now have a paper you can cite:

```bibtex
@article{mem0,
  title={Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory},
  author={Chhikara, Prateek and Khant, Dev and Aryan, Saket and Singh, Taranjeet and Yadav, Deshraj},
  journal={arXiv preprint arXiv:2504.19413},
  year={2025}
}
```

## ⚖️ License

Apache 2.0 — see the [LICENSE](https://github.com/mem0ai/mem0/blob/main/LICENSE) file for details.