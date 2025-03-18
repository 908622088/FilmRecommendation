# 实现数据加载与预处理
import pandas as pd

def load_data():
    file_path1 = 'data/movies.txt'
    file_path2 = 'data/personalRatings.txt'
    file_pathR1 = 'data/ratings/ratings_1.txt'
    file_pathR2 = 'data/ratings/ratings_2.txt'
    file_pathR3 = 'data/ratings/ratings_3.txt'
    file_pathR4 = 'data/ratings/ratings_4.txt'
    file_pathR5 = 'data/ratings/ratings_5.txt'
    
    movie = pd.read_csv(file_path1, delimiter='::', header=None, names=['MovieID', 'Title', 'Genres'])
    personalRatings = pd.read_csv(file_path2, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    ratings_1 = pd.read_csv(file_pathR1, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    ratings_2 = pd.read_csv(file_pathR2, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    ratings_3 = pd.read_csv(file_pathR3, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    ratings_4 = pd.read_csv(file_pathR4, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    ratings_5 = pd.read_csv(file_pathR5, delimiter='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    
    movie['Genres'] = movie['Genres'].astype(str)
    movie = movie.drop_duplicates().dropna()
    
    personalRatings = personalRatings.drop_duplicates().dropna()
    personalRatings['Timestamp'] = pd.to_datetime(personalRatings['Timestamp'], unit='s')
    
    ratings_1 = ratings_1.drop_duplicates().dropna()
    ratings_1['Timestamp'] = pd.to_datetime(ratings_1['Timestamp'], unit='s')
    
    ratings_2 = ratings_2.drop_duplicates().dropna()
    ratings_2['Timestamp'] = pd.to_datetime(ratings_2['Timestamp'], unit='s')
    
    ratings_3 = ratings_3.drop_duplicates().dropna()
    ratings_3['Timestamp'] = pd.to_datetime(ratings_3['Timestamp'], unit='s')
    
    ratings_4 = ratings_4.drop_duplicates().dropna()
    ratings_4['Timestamp'] = pd.to_datetime(ratings_4['Timestamp'], unit='s')
    
    ratings_5 = ratings_5.drop_duplicates().dropna()
    ratings_5['Timestamp'] = pd.to_datetime(ratings_5['Timestamp'], unit='s')
    
    return {
        'movies': movie,
        'personal_ratings': personalRatings,
        'ratings_1': ratings_1,
        'ratings_2': ratings_2,
        'ratings_3': ratings_3,
        'ratings_4': ratings_4,
        'ratings_5': ratings_5
    }