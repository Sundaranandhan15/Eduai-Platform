import os
from anthropic import Anthropic
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-api-key-here")

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize Embedder
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# In a real app, chunks would be loaded from a DB or file. 
# Here we mock the text corpus for RAG but we USE the real FAISS and Embedder.
corpus = [
    "Addition is the process of bringing two or more numbers together to make a new total.",
    "Subtraction is taking one number away from another.",
    "Multiplication is essentially repeated addition.",
    "Division is splitting into equal parts or groups.",
    "Fractions represent equal parts of a whole or a collection.",
    "A numerator is the top number of a fraction, representing how many parts we have.",
    "A denominator is the bottom number, representing how many parts make up a whole.",
    "Deep Knowledge Tracing models a student's knowledge over time.",
    "Socratic method involves asking questions to stimulate critical thinking."
]

def get_rag_context(query: str, top_k: int = 3) -> str:
    # Check if index exists, if not build it on the fly
    index_path = os.path.join(os.path.dirname(__file__), "rag", "faiss_index", "index.faiss")
    
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        # Build index
        embeddings = embedder.encode(corpus)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(index, index_path)
    
    query_emb = embedder.encode([query]).astype('float32')
    distances, indices = index.search(query_emb, top_k)
    
    retrieved = [corpus[i] for i in indices[0]]
    return "\n".join(retrieved)

def generate_tutor_response(student_question: str, mastery_prob: float) -> str:
    context = get_rag_context(student_question)
    
    # Logic based on mastery
    if mastery_prob < 0.4:
        instruction = "The student is struggling. Generate a Socratic hint (not the answer)."
    elif mastery_prob <= 0.7:
        instruction = "The student has partial understanding. Generate a guided question to help them realize the next step."
    else:
        instruction = "The student has good mastery. Generate a challenge extension question related to their query."

    system_prompt = (
        "You are an expert educational tutor. Never give the direct answer. "
        "Guide the student using the Socratic method. Use the retrieved context to ground your response.\n\n"
        f"Context:\n{context}\n\n"
        f"Instructions:\n{instruction}"
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=512,
        system=system_prompt,
        messages=[
            {"role": "user", "content": student_question}
        ]
    )
    
    return response.content[0].text
