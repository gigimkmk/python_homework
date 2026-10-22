
import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


class State(TypedDict):
    product_text: str
    product_info: str
    marketing_text: str
    final_description: str


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.3,
    timeout=30,
    max_retries=1
)


def extract(state: State):
    print("Step 1: Extracting product information...", flush=True)

    prompt = f"""
    Extract the main product information from the text below.

    Organize the information clearly in English.
    Include product name, display, storage, processor,
    camera, connector, battery and colors if available.

    Do not invent missing information.

    Product text:
    {state["product_text"]}
    """

    response = llm.invoke(prompt)

    print("Step 1 completed!", flush=True)

    return {"product_info": response.content}


def marketing(state: State):
    print("Step 2: Creating marketing text...", flush=True)

    prompt = f"""
    Create an attractive marketing description
    for an online store using the information below.

    Write in English.
    Highlight the main product features and benefits.
    Make the description professional and engaging.
    Do not invent specifications.

    Product information:
    {state["product_info"]}
    """

    response = llm.invoke(prompt)

    print("Step 2 completed!", flush=True)

    return {"marketing_text": response.content}


def format_text(state: State):
    print("Step 3: Formatting final description...", flush=True)

    final_text = f"""=== PRODUCT DESCRIPTION ===

{state["marketing_text"]}

=== END ==="""

    print("Step 3 completed!", flush=True)

    return {"final_description": final_text}


graph = StateGraph(State)

graph.add_node("extract", extract)
graph.add_node("marketing", marketing)
graph.add_node("format", format_text)

graph.add_edge(START, "extract")
graph.add_edge("extract", "marketing")
graph.add_edge("marketing", "format")
graph.add_edge("format", END)

app = graph.compile()


initial_state = {
    "product_text": "iphone 15, 6.1 inch oled, 128gb, a16 bionic, 48mp camera, usb-c, battery good, available in black and blue",
    "product_info": "",
    "marketing_text": "",
    "final_description": ""
}


print("Program started...", flush=True)

try:
    result = app.invoke(initial_state)

    print("\nAI finished successfully!\n", flush=True)
    print(result["final_description"])

except Exception as error:
    print("\nERROR:", error, flush=True)
