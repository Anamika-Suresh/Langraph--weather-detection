import os
import sys
from typing import Annotated, Literal
from typing_extensions import TypedDict

# Ensure UTF-8 output on Windows terminal
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_env_file(filepath=".env"):
    """Load key-value pairs from a .env file if it exists."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = val


load_env_file()

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def get_weather(location: str):
    """Call to get the current weather for a location."""
    loc_lower = location.lower()
    if "yorkshire" in loc_lower:
        return "It's cold and wet (around 11°C with light rain)."
    elif "london" in loc_lower:
        return "It's cloudy and mild (around 16°C)."
    elif "tokyo" in loc_lower:
        return "It's clear and crisp (around 18°C)."
    elif "new york" in loc_lower:
        return "It's sunny with a gentle breeze (around 22°C)."
    else:
        return f"It's warm and sunny in {location} (around 25°C)."


def build_agent():
    """Build and compile the LangGraph workflow."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("⚠️ Warning: GROQ_API_KEY is not set.")
        print("Please set GROQ_API_KEY in your environment or in a .env file.")

    llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7)
    tools = [get_weather]
    llm_with_tools = llm.bind_tools(tools)
    tool_node = ToolNode(tools)

    graph = StateGraph(State)

    def prompt_node(state: State) -> dict:
        """LLM decision node."""
        new_message = llm_with_tools.invoke(state["messages"])
        return {"messages": [new_message]}

    def conditional_edge(state: State) -> Literal["tool_node", "__end__"]:
        """Route to tool_node if tool call requested, else end turn."""
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "tool_node"
        return "__end__"

    graph.add_node("prompt_node", prompt_node)
    graph.add_node("tool_node", tool_node)
    graph.add_conditional_edges("prompt_node", conditional_edge)
    graph.add_edge("tool_node", "prompt_node")
    graph.set_entry_point("prompt_node")

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


def run_interactive_chat():
    """Run interactive terminal chat loop."""
    agent = build_agent()
    session_id = 1
    thread_id = f"user_session_{session_id}"

    print("=" * 65)
    print("🤖 Welcome to the LangGraph Interactive Assistant!")
    print("Ask any question and the system will answer.")
    print("\nExamples:")
    print("  • What is the weather in Yorkshire?")
    print("  • What is the capital of France?")
    print("  • What should I wear there? (it remembers context!)")
    print("\nSpecial commands:")
    print("  • 'exit' or 'quit' -> Close the assistant")
    print("  • 'clear'          -> Start a fresh new conversation")
    print("=" * 65 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! Have a great day! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "q"):
            print("\nGoodbye! Have a great day! 👋")
            break

        if user_input.lower() == "clear":
            session_id += 1
            thread_id = f"user_session_{session_id}"
            print("\n🔄 Conversation memory cleared! Starting a new session.\n")
            continue

        print("\nThinking...", end="", flush=True)

        try:
            config = {"configurable": {"thread_id": thread_id}}
            response = agent.invoke({"messages": [("user", user_input)]}, config=config)
            print("\r                    \r", end="")

            final_message = response["messages"][-1]
            print(f"Assistant: {final_message.content}\n")
            print("-" * 65 + "\n")
        except Exception as e:
            print(f"\n⚠️ Error processing your request: {e}\n")


if __name__ == "__main__":
    run_interactive_chat()
