from flask import Flask, request, jsonify, render_template
import pandas as pd
from models.data_loader import load_data
from models.collaborative_filtering import compute_user_similarity, compute_item_similarity, predict_user_based_rating, predict_item_based_rating, get_item_based_recommendations
from models.content_based import compute_content_similarity, get_recommendations

app = Flask(__name__)

# 加载数据
dataframes = load_data()
movies = dataframes['movies']
ratings = pd.concat([dataframes['personal_ratings'], dataframes['ratings_1'], dataframes['ratings_2'], 
                     dataframes['ratings_3'], dataframes['ratings_4'], dataframes['ratings_5']])

    
user_movie_matrix = ratings.pivot_table(index='UserID', columns='MovieID', values='Rating')
user_similarity_df = compute_user_similarity(user_movie_matrix)
item_similarity_df = compute_item_similarity(user_movie_matrix)

content_cosine_sim = compute_content_similarity(movies)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_user_based_rating', methods=['POST'])
def predict_user_based_rating_api():
    data = request.json
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = predict_user_based_rating(user_id, movie_id, user_similarity_df, user_movie_matrix)
    return jsonify({'predicted_rating': rating})

@app.route('/predict_item_based_rating', methods=['POST'])
def predict_item_based_rating_api():
    data = request.json
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    rating = predict_item_based_rating(user_id, movie_id, item_similarity_df, user_movie_matrix)
    return jsonify({'predicted_rating': rating})

@app.route('/content_recommendations', methods=['POST'])
def content_recommendations_api():
    data = request.json
    title = data.get('title')
    top_n = data.get('top_n', 10)
    recommendations = get_recommendations(title, content_cosine_sim, movies, top_n)
    return jsonify({'recommendations': recommendations.tolist()})

@app.route('/get_item_based_recommendations', methods=['POST'])
def get_item_based_recommendations_api():
    data = request.json
    user_id = data.get('user_id')
    top_n = data.get('top_n', 5)
    recommendations = get_item_based_recommendations(user_id, user_movie_matrix, item_similarity_df, movies, top_n=top_n)
    return jsonify({'recommendations': recommendations.to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=True)