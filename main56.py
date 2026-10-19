
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector import Vector
from pgvector.psycopg import register_vector


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=API_KEY)

EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-2.5-flash"
DIMENSIONS = 768


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME", "hotel_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hotel_chunks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding VECTOR(768) NOT NULL
        )
    """)
    conn.commit()


def get_embedding(text, task_type):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=DIMENSIONS
        )
    )

    return result.embeddings[0].values


def save_chunks(conn):
    file_path = BASE_DIR / "hotel.md"

    loader = UnstructuredMarkdownLoader(
        str(file_path),
        mode="single"
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print(f"\nCreated {len(chunks)} chunks")

    for chunk in chunks:
        content = chunk.page_content

        embedding = get_embedding(
            content,
            "RETRIEVAL_DOCUMENT"
        )

        conn.execute(
            """
            INSERT INTO hotel_chunks (content, embedding)
            VALUES (%s, %s)
            """,
            (content, Vector(embedding))
        )

    conn.commit()

    print("Chunks saved successfully in PostgreSQL!")


def search_similar_chunks(conn, question):
    question_embedding = get_embedding(
        question,
        "RETRIEVAL_QUERY"
    )

    results = conn.execute(
        """
        SELECT
            content,
            1 - (embedding <=> %s) AS similarity
        FROM hotel_chunks
        ORDER BY embedding <=> %s
        LIMIT 3
        """,
        (
            Vector(question_embedding),
            Vector(question_embedding)
        )
    ).fetchall()

    return results


def get_ai_answer(question, results):
    context = "\n\n".join(
        row[0] for row in results
    )

    prompt = f"""
You are a helpful assistant for a hotel.

Answer the question in Georgian.

Use only the context provided below.
Do not invent information.
If the information is not available,
say that it is not mentioned in the hotel information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )

    return response.text


def main():
    with get_connection() as conn:
        conn.execute(
            "CREATE EXTENSION IF NOT EXISTS vector"
        )
        conn.commit()

        register_vector(conn)

        create_table(conn)

        count = conn.execute(
            "SELECT COUNT(*) FROM hotel_chunks"
        ).fetchone()[0]

        if count == 0:
            print("Reading hotel.md...")
            save_chunks(conn)
        else:
            print(f"{count} chunks already stored in PostgreSQL")

        while True:
            question = input(
                "\nEnter your question (exit to stop): "
            ).strip()

            if question.lower() == "exit":
                print("Program finished.")
                break

            if not question:
                continue

            results = search_similar_chunks(
                conn,
                question
            )

            print("\nTOP 3 SIMILAR CHUNKS")

            for index, (content, score) in enumerate(
                results,
                start=1
            ):
                print(f"\nChunk {index}")
                print(f"Similarity: {score:.4f}")
                print(content)
                print("-" * 50)

            answer = get_ai_answer(
                question,
                results
            )

            print("\nGEMINI ANSWER:")
            print(answer)


if __name__ == "__main__":
    main()
