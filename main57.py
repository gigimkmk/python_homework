

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")


@tool
def search_hotel(city: str) -> str:
    """Search for hotels and their nightly prices in a city."""

    hotels = {
        "tbilisi": [
            "Hotel A - 120 GEL/night",
            "Hotel B - 180 GEL/night",
            "Hotel C - 250 GEL/night",
        ],
        "batumi": [
            "Batumi Hotel - 150 GEL/night",
            "Sea View Hotel - 220 GEL/night",
            "Luxury Hotel - 350 GEL/night",
        ],
        "kutaisi": [
            "Kutaisi Inn - 90 GEL/night",
            "Central Hotel - 140 GEL/night",
            "Grand Hotel - 200 GEL/night",
        ],
    }

    city = city.lower().strip()
    result = hotels.get(city)

    if result:
        return "\n".join(result)

    return f"No hotel information found for {city}."


@tool
def get_exchange_rate(currency: str) -> str:
    """Get the example exchange rate of a currency against GEL."""

    rates = {
        "USD": 2.70,
        "EUR": 3.15,
        "GBP": 3.60,
    }

    currency = currency.upper().strip()
    rate = rates.get(currency)

    if rate is not None:
        return f"1 {currency} = {rate} GEL"

    return f"Exchange rate for {currency} not found."


@tool
def search_attractions(city: str) -> str:
    """Search for popular tourist attractions in a city."""

    attractions = {
        "tbilisi": [
            "Narikala Fortress",
            "Old Tbilisi",
            "Mtatsminda Park",
            "Peace Bridge",
        ],
        "batumi": [
            "Batumi Boulevard",
            "Alphabet Tower",
            "Ali and Nino Statue",
            "Batumi Botanical Garden",
        ],
        "kutaisi": [
            "Bagrati Cathedral",
            "Gelati Monastery",
            "Prometheus Cave",
        ],
    }

    city = city.lower().strip()
    result = attractions.get(city)

    if result:
        return "\n".join(result)

    return f"No attraction information found for {city}."


tools = [
    search_hotel,
    get_exchange_rate,
    search_attractions,
]

tools_by_name = {
    tool_item.name: tool_item
    for tool_item in tools
}

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)

messages = [
    SystemMessage(
        content=(
            "You are a helpful AI Travel Assistant. "
            "Use the available tools when the user asks about "
            "hotels, exchange rates, or tourist attractions. "
            "You may use multiple tools for one question. "
            "The tool data is demo data, not live information. "
            "Never present demo prices or rates as current facts. "
            "Answer in the same language as the user."
        )
    )
]

print("AI Travel Assistant is ready!")
print("Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if not user_input:
        continue

    messages.append(HumanMessage(content=user_input))

    try:
        for _ in range(5):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                print("\nAI:", response.content)
                break

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                print(f"\nSelected Tool: {tool_name}")

                selected_tool = tools_by_name.get(tool_name)

                if selected_tool is None:
                    result = f"Unknown tool: {tool_name}"
                else:
                    try:
                        result = selected_tool.invoke(tool_args)
                    except Exception as error:
                        result = f"Tool error: {error}"

                print("Tool Result:", result)

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )
        else:
            print("\nAI: Tool calling limit reached.")

    except Exception as error:
        print("\nError:", error)
        messages = messages[:1]
