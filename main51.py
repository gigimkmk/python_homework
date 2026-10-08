
import os
from openai import OpenAI

SYSTEM_PROMPT = """
You are an experienced senior software engineer and programming mentor.
Explain technical concepts clearly.
Adapt your explanations to the user's level.
Use practical code examples when appropriate.
Remember the previous conversation and answer follow-up questions.
Stay in the role of Senior Software Engineer and Programming Mentor.
"""

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set.")
        return

    client = OpenAI()

    messages = []

    print("AI Technical Mentor")
    print("Type 'history' to view the conversation.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("\nGoodbye!")
            break

        if user_input.lower() == "history":
            if not messages:
                print("\nNo conversation history.\n")
            else:
                print("\nConversation History:\n")
                for message in messages:
                    print(f"{message['role'].upper()}:")
                    print(message["content"])
                    print()
            continue

        if not user_input:
            continue

        new_message = {
            "role": "user",
            "content": user_input
        }

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                instructions=SYSTEM_PROMPT,
                input=messages + [new_message]
            )

            ai_answer = response.output_text

            print(f"\nAI: {ai_answer}\n")

            messages.append(new_message)
            messages.append({
                "role": "assistant",
                "content": ai_answer
            })

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
