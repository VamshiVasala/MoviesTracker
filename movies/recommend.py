from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommendation(userGenres,userCast,RemMoviesData):
    cast_weight = 0.7
    genre_weight = 0.3
    user_genres_text = " ".join(userGenres)
    user_cast_text = " ".join(userCast)

    # Prepare movie text lists
    movie_genres_texts = [m['genres'] for m in RemMoviesData]
    movie_cast_texts = [m['cast'] for m in RemMoviesData]
    movie_ids = [m['id'] for m in RemMoviesData]

    # TF-IDF separately
    vectorizer = TfidfVectorizer(stop_words="english")

    # Genre vectors
    genre_vectors = vectorizer.fit_transform([user_genres_text] + movie_genres_texts)
    genre_sim = cosine_similarity(genre_vectors[0:1], genre_vectors[1:])[0]

    # Cast vectors
    cast_vectors = vectorizer.fit_transform([user_cast_text] + movie_cast_texts)
    cast_sim = cosine_similarity(cast_vectors[0:1], cast_vectors[1:])[0]

    # Weighted similarity
    final_scores = (cast_weight * cast_sim) + (genre_weight * genre_sim)  
    sorted_indices = final_scores.argsort()[::-1]
    recommended_ids = [movie_ids[i] for i in sorted_indices]

    return recommended_ids
