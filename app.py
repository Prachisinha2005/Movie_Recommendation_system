from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Get the absolute path to your CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'Movie_Recommendation_system-main', 'tmdb_5000_movies.csv')

# Print current directory and CSV path for debugging
print(f"Current directory: {current_dir}")
print(f"Looking for CSV at: {csv_path}")

# Check if file exists
if not os.path.exists(csv_path):
    # Try alternative path
    csv_path = os.path.join(current_dir, 'tmdb_5000_movies.csv')
    print(f"Trying alternative path: {csv_path}")
    if not os.path.exists(csv_path):
        # List all files in current directory for debugging
        print("Files in current directory:")
        for file in os.listdir(current_dir):
            print(f"- {file}")
        raise FileNotFoundError(f"Could not find CSV file. Please ensure 'tmdb_5000_movies.csv' is in the correct location.")

try:
    # Try to load the dataset
    print(f"Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    print("Dataset loaded successfully!")
    print(f"Number of movies in dataset: {len(df)}")

    # Create a function to combine important features for recommendation
    def combine_features(row):
        try:
            features = []
            if pd.notna(row['title']): features.append(str(row['title']))
            if pd.notna(row['overview']): features.append(str(row['overview']))
            if pd.notna(row['genres']): features.append(str(row['genres']))
            if pd.notna(row['keywords']): features.append(str(row['keywords']))
            return " ".join(features)
        except Exception as e:
            print(f"Error in combine_features: {str(e)}")
            return ""

    # Prepare the data
    print("Preparing data...")
    df['combined_features'] = df.apply(combine_features, axis=1)

    # Create count vectorizer and similarity matrix
    print("Creating similarity matrix...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['combined_features'].fillna('')).toarray()
    similarity = cosine_similarity(vectors)
    print("Similarity matrix created successfully!")

    def get_recommendations(movie_name):
        try:
            # Find the movie in our dataset (case-insensitive)
            movie_index = df[df['title'].str.lower() == movie_name.lower()].index[0]
            
            # Get similarity scores
            distances = similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            
            recommended_movies = []
            for i in movies_list:
                movie_data = {
                    'title': df.iloc[i[0]]['title'],
                    'overview': df.iloc[i[0]]['overview'],
                    'vote_average': round(float(df.iloc[i[0]]['vote_average']), 1),
                    'similarity_score': round(float(i[1] * 100), 1)
                }
                recommended_movies.append(movie_data)
            
            return recommended_movies
        except IndexError:
            return None
        except Exception as e:
            print(f"Error in get_recommendations: {str(e)}")
            return None

except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    raise Exception(f"Failed to load dataset: {str(e)}")

@app.route('/')
def home():
    # Get a list of all movie titles for autocomplete
    movie_titles = sorted(df['title'].tolist())
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    recommendations = get_recommendations(movie_name)
    
    if recommendations:
        return render_template('recommendation.html', 
                             recommendations=recommendations, 
                             movie=movie_name)
    else:
        error_message = f"Sorry, '{movie_name}' not found in our database. Please check the spelling or try another movie."
        return render_template('index.html', 
                             error=error_message, 
                             movie_titles=sorted(df['title'].tolist()))

if __name__ == '__main__':
    app.run(debug=True) 