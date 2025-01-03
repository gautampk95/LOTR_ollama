from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Query and retrieve relevant chunks, similarity_threshold=0.1 is reasonable, anything above may not result in relevant embeddings
def retrieve_relevant_chunks(query, knowledge_embeddings, top_k=100, similarity_threshold=0.5):
    def normalize(vector):
        return vector / np.linalg.norm(vector)
    normalized_embeddings = [(chunk, normalize(embedding)) for chunk, embedding in knowledge_embeddings]
    query_embedding = normalize(embedding_model.encode(query))

    similarities = [
        (chunk, cosine_similarity([query_embedding], [embedding])[0][0])
        for chunk, embedding in normalized_embeddings
    ]

     # Extract similarity scores
    similarity_scores = np.array([sim for _, sim in similarities])
    
    # Determine a dynamic threshold (e.g., mean + std deviation or median + multiplier)
    threshold = similarity_scores.mean() + similarity_scores.std()
    
    # Filter results above the dynamic threshold
    filtered_similarities = [
        (chunk, similarity) for chunk, similarity in similarities if similarity > threshold
    ]

    sorted_chunks = sorted(filtered_similarities, key=lambda x: x[1], reverse=True)
    # print(sorted_chunks[-1][1])
    # If the highest similarity score is below the threshold, return None (indicating no relevant content)
    if sorted_chunks[0][1] < similarity_threshold:
        return None
    else:
        return [chunk[0] for chunk in sorted_chunks[:top_k]]  # Return top K relevant chunks