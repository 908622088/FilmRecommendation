# 协同过滤与内容推荐模型
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def compute_user_similarity(user_movie_matrix):
    user_similarity = cosine_similarity(user_movie_matrix.fillna(0))
    user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)
    return user_similarity_df

def compute_item_similarity(user_movie_matrix):
    item_similarity = cosine_similarity(user_movie_matrix.fillna(0).T)
    item_similarity_df = pd.DataFrame(item_similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)
    return item_similarity_df

def predict_user_based_rating(user_id, movie_id, user_similarity_df, user_movie_matrix):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id)
    user_ratings = user_movie_matrix.loc[similar_users.index, movie_id]
    user_ratings = user_ratings[user_ratings.notnull()]
    if user_ratings.empty:
        return 0
    weighted_ratings = user_ratings * similar_users[user_ratings.index]
    return weighted_ratings.sum() / similar_users[user_ratings.index].sum()

def predict_item_based_rating(user_id, movie_id, item_similarity_df, user_movie_matrix):
    user_ratings = user_movie_matrix.loc[user_id]
    similar_movies = item_similarity_df[movie_id].sort_values(ascending=False).drop(movie_id)
    similar_movies = similar_movies[similar_movies > 0]
    if similar_movies.empty:
        return 0
    weighted_ratings = user_ratings[similar_movies.index] * similar_movies[similar_movies.index]
    return weighted_ratings.sum() / similar_movies.sum()

def get_item_based_recommendations(user_id, user_item_matrix, item_similarity_df, movie_df, top_n=5):
    # 获取用户已评分的物品
    user_ratings = user_item_matrix.loc[user_id].dropna()
    
    # 计算每个未评分物品的加权评分
    scores = pd.Series(0, index=user_item_matrix.columns)
    for item, rating in user_ratings.items():
        similar_items = item_similarity_df[item].drop(item)
        scores += similar_items * rating
    
    # 排除用户已评分的物品
    scores = scores.drop(user_ratings.index)
    
    # 返回评分最高的top_n个物品
    recommended_movie_ids = scores.nlargest(top_n).index
    recommended_movies = movie_df[movie_df['MovieID'].isin(recommended_movie_ids)][['MovieID', 'Title']]
    return recommended_movies