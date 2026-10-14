# LangGraph Interactive Q&A Assistant

An interactive AI assistant built with **LangGraph** and **Groq (`openai/gpt-oss-120b`)** that allows users to ask questions dynamically and receive answers in real time, with multi-turn conversation memory and tool calling.

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Anamika-Suresh/Langraph--weather-detection.git
   cd Langraph--weather-detection
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Groq API key in `.env`:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```
   *(Get your free API key at [console.groq.com](https://console.groq.com/keys))*

---

## 🚀 How to Run

You have two ways to interact with the assistant:

### Option 1: Terminal / Command Prompt (`main.py`)
Run the standalone Python script from your terminal:

```bash
python main.py
```

Features in terminal mode:
- **Interactive Prompts**: Type any question and press Enter.
- **Context Retention**: Follow-up questions remember previous context (e.g., asking about Yorkshire weather and then asking *"What should I wear?"*).
- **Tool Calling**: Automatically queries tools (like `get_weather`) when needed.
- **Commands**:
  - `exit` or `quit` — Close the assistant.
  - `clear` — Clear conversational memory and start a fresh session.

---

### Option 2: Jupyter Notebook (`langraph.ipynb`)
Open [langraph.ipynb](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/langraph.ipynb):

1. Run the cells from top to bottom.
2. The final cell (`# Interactive Chatbot: Ask questions in real time!`) provides an input prompt.
3. Type your question in the input box, press Enter, and get the assistant's response.
4. Type `exit` or `quit` to stop the loop.

---

## 🛠️ Project Structure

- [main.py](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/main.py) — Standalone production-ready Python script with interactive chat loop, Windows UTF-8 encoding support, and memory checkpointer.
- [langraph.ipynb](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/langraph.ipynb) — Step-by-step Jupyter Notebook detailing the LangGraph architecture and interactive execution.
- [requirements.txt](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/requirements.txt) — Python dependencies required to run the agent.
- [.env.example](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/.env.example) — Template for setting environment variables.
- [.gitignore](file:///c:/Users/ANAMIKA/Desktop/langraph_agent/.gitignore) — Prevents committing virtual environments, cache files, and private credentials.
