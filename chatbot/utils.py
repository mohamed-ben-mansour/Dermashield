# chatbot/utils.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .load_data import load_medical_data

# Load dataset
df = load_medical_data()

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the questions into TF-IDF vectors
tfidf_matrix = vectorizer.fit_transform(df['input'])

def get_answer(user_query, threshold=0.2):
    """
    Get the best matching answer to the user query.
    If the similarity is below the threshold, return a default response.
    
    Parameters:
    - user_query (str): The input query from the user.
    - threshold (float): The minimum similarity score to consider a match.

    Returns:
    - str: The corresponding answer or a default response.
    """
    # Transform the user's question into a TF-IDF vector
    user_query_tfidf = vectorizer.transform([user_query])
    
    # Calculate cosine similarity between the user's query and all questions
    similarities = cosine_similarity(user_query_tfidf, tfidf_matrix)
    
    # Find the highest similarity score and its index
    max_similarity = np.max(similarities)
    index_of_best_match = np.argmax(similarities)
    
    # If the similarity score is below the threshold, return a default response
    if max_similarity < threshold:
        return "I didn't understand you. Could you rephrase?"
    
    # Return the corresponding answer
    return df['output'].iloc[index_of_best_match]