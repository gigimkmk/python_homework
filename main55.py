
import os
import numpy as np

from getpass import getpass
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

api_key = getpass("Enter your Gemini API key: ").strip()

loader = UnstructuredMarkdownLoader("hotel.md", mode="single")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)

chunk_texts = [chunk.page_content for chunk in chunks]

chunk_vectors = embeddings.embed_documents(chunk_texts)
chunk_vectors = np.array(chunk_vectors)

print(f"Loaded {len(documents)} documents")
print(f"Created {len(chunks)} chunks")


while True:
    question = input("\nEnter your question (exit to stop): ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    question_vector = embeddings.embed_query(question)
    question_vector = np.array(question_vector).reshape(1, -1)

    similarities = cosine_similarity(
        question_vector,
        chunk_vectors
    )[0]

    top_indices = np.argsort(similarities)[::-1][:3]

    print("\nTop 3 most similar chunks:\n")

    for rank, index in enumerate(top_indices, start=1):
        print(f"Result {rank}")
        print(f"Similarity score: {similarities[index]:.4f}")
        print(f"Text: {chunks[index].page_content}")
        print("-" * 60)
