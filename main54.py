
import os
from typing import Literal

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


load_dotenv()


class ProductReview(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    pros: list[str] = Field(description="Positive aspects of the product")
    cons: list[str] = Field(description="Negative aspects of the product")
    summary: str = Field(description="Short summary of the review")
    recommend: bool = Field(description="Whether the product is recommended")


parser = PydanticOutputParser(pydantic_object=ProductReview)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI assistant that analyzes product reviews.

        Analyze the review and determine:
        - sentiment: positive, negative, or neutral
        - pros: positive aspects of the product
        - cons: negative aspects of the product
        - summary: a short summary
        - recommend: true or false

        Base your analysis only on the review.
        Use an empty list if there are no pros or cons.
        Recommend the product based on the overall review.

        Return only the requested structured output.

        {format_instructions}
        """
    ),
    ("human", "Product review: {review}")
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

chain = prompt | model | parser

review = input("Enter product review: ")

try:
    result = chain.invoke({
        "review": review,
        "format_instructions": parser.get_format_instructions()
    })

    print("\nProduct Analysis:")
    print(result)
    print("\nData Type:")
    print(type(result))

except Exception as e:
    print("Error:", e)
