import os
import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = input("Enter your Google API Key: ").strip()

MAX_ATTEMPTS = 3

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0.3
)


class State(TypedDict):
    ingredients: str
    recipe: str
    feedback: str
    approved: bool
    attempts: int


def generate_recipe(state: State):
    response = llm.invoke(f"""
    Create a simple recipe using these ingredients:
    {state["ingredients"]}

    Include ingredient quantities, cooking steps and cooking time.
    Write in English.
    """)

    return {
        "recipe": response.content,
        "attempts": state["attempts"] + 1
    }


def check_recipe(state: State):
    response = llm.invoke(f"""
    Check this recipe:

    Ingredients: {state["ingredients"]}
    Recipe: {state["recipe"]}

    Check if:
    - All ingredients are used
    - Instructions are clear
    - Cooking steps are included
    - Quantities are reasonable
    - Cooking time is included

    Return ONLY valid JSON in this format:
    {{
        "approved": true,
        "feedback": "The recipe is complete."
    }}

    Set approved to false if something is missing.
    Do not include markdown.
    """)

    try:
        text = response.content.strip()
        data = json.loads(text)

        approved = data["approved"]
        feedback = data["feedback"]

        if type(approved) is not bool:
            raise ValueError("Invalid approved value")

    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        approved = False
        feedback = "Review failed. Check and improve the recipe."

    return {
        "approved": approved,
        "feedback": feedback
    }


def improve(state: State):
    response = llm.invoke(f"""
    Improve this recipe based on the feedback.

    Ingredients:
    {state["ingredients"]}

    Current recipe:
    {state["recipe"]}

    Feedback:
    {state["feedback"]}

    Fix all problems.
    Return the complete improved recipe in English.
    """)

    return {
        "recipe": response.content,
        "attempts": state["attempts"] + 1
    }


def decide_next_step(state: State):
    if state["approved"]:
        return "end"

    if state["attempts"] >= MAX_ATTEMPTS:
        return "end"

    return "improve"


graph_builder = StateGraph(State)

graph_builder.add_node("generate_recipe", generate_recipe)
graph_builder.add_node("check_recipe", check_recipe)
graph_builder.add_node("improve", improve)

graph_builder.add_edge(START, "generate_recipe")
graph_builder.add_edge("generate_recipe", "check_recipe")

graph_builder.add_conditional_edges(
    "check_recipe",
    decide_next_step,
    {
        "improve": "improve",
        "end": END
    }
)

graph_builder.add_edge("improve", "check_recipe")

graph = graph_builder.compile()

initial_state = {
    "ingredients": "chicken, rice, onion, tomato",
    "recipe": "",
    "feedback": "",
    "approved": False,
    "attempts": 0
}

result = graph.invoke(initial_state)

print("\nFINAL RECIPE:")
print(result["recipe"])

print("\nFEEDBACK:")
print(result["feedback"])

print("\nAPPROVED:", result["approved"])
print("ATTEMPTS:", result["attempts"])
