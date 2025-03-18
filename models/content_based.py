# 实现内容推荐模型
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def compute_content_similarity(movies):
    tfidf = TfidfVectorizer(stop_words='english')
    movies['Genres'] = movies['Genres'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movies['Genres'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def get_recommendations(title, cosine_sim, movies, top_n=10):
    idx = movies[movies['Title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['Title'].iloc[movie_indices]