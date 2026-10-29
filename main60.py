import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)


class State(TypedDict):
    user_request: str
    destination_info: str
    food_info: str
    budget_info: str
    final_plan: str


def destination_agent(state: State):
    print("Destination Agent is working...")

    response = llm.invoke([
        SystemMessage(content="""
        You are a travel destination expert.

        Analyze the user's destination and interests.
        Recommend attractions and activities.
        Consider the duration of the trip.

        Do not recommend food.
        Do not calculate expenses.
        Do not create a complete travel plan.

        Respond in Georgian.
        """),
        HumanMessage(content=state["user_request"])
    ])

    return {"destination_info": response.content}


def food_agent(state: State):
    print("Food Agent is working...")

    response = llm.invoke([
        SystemMessage(content="""
        You are a food and restaurant expert.

        Recommend traditional local dishes.
        Suggest suitable dining options.
        Consider the user's budget and preferences.

        Do not recommend attractions.
        Do not calculate the total travel budget.
        Do not create a complete travel plan.

        Respond in Georgian.
        """),
        HumanMessage(content=state["user_request"])
    ])

    return {"food_info": response.content}


def budget_agent(state: State):
    print("Budget Agent is working...")

    response = llm.invoke([
        SystemMessage(content="""
        You are a travel budget expert.

        Analyze the destination and trip duration.
        Estimate expenses for:
        - Accommodation
        - Food
        - Transportation
        - Activities

        Calculate the approximate total cost.
        Clearly state that prices are estimates.
        Exclude international flights unless requested.

        Do not create a daily travel itinerary.

        Respond in Georgian.
        """),
        HumanMessage(content=state["user_request"])
    ])

    return {"budget_info": response.content}


def planner_agent(state: State):
    print("Planner Agent is working...")

    response = llm.invoke([
        SystemMessage(content="""
        You are a professional travel planner.

        Combine the information provided by:
        1. Destination Agent
        2. Food Agent
        3. Budget Agent

        Create a complete daily travel itinerary.

        Include:
        - Destination overview
        - Daily activities
        - Food recommendations
        - Budget breakdown
        - Total estimated expenses

        Use only information provided by the agents.
        Do not invent new attractions, restaurants or prices.

        Respond in Georgian.
        """),
        HumanMessage(content=f"""
        User request:
        {state["user_request"]}

        Destination information:
        {state["destination_info"]}

        Food information:
        {state["food_info"]}

        Budget information:
        {state["budget_info"]}

        Combine all information into one travel plan.
        """)
    ])

    return {"final_plan": response.content}


graph = StateGraph(State)

graph.add_node("destination_agent", destination_agent)
graph.add_node("food_agent", food_agent)
graph.add_node("budget_agent", budget_agent)
graph.add_node("planner_agent", planner_agent)

graph.add_edge(START, "destination_agent")
graph.add_edge(START, "food_agent")
graph.add_edge(START, "budget_agent")

graph.add_edge(
    ["destination_agent", "food_agent", "budget_agent"],
    "planner_agent"
)

graph.add_edge("planner_agent", END)

app = graph.compile()


if __name__ == "__main__":

    user_request = input("Enter your travel request: ").strip()

    if not user_request:
        print("Please enter a travel request.")
        raise SystemExit(1)

    initial_state = {
        "user_request": user_request,
        "destination_info": "",
        "food_info": "",
        "budget_info": "",
        "final_plan": ""
    }

    try:
        result = app.invoke(initial_state)

        print("\n========== FINAL TRAVEL PLAN ==========\n")
        print(result["final_plan"])

    except Exception as e:
        print(f"Error: {e}")