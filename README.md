# Movie Recommendation System 🎬
![Movie Recommendation Output]![Movie Recommendation Output](https://raw.githubusercontent.com/Prachisinha2005/Movie_Recommendation_system/refs/heads/main/movie%20r%20s.webp)




This is a Python-based movie recommendation system that suggests movies similar to a user's favorite movie. The system uses a similarity matrix to compare movies and recommend the most relevant ones.

![Movie Recommendation System](https://raw.githubusercontent.com/Prachisinha2005/Movie_Recommendation_system/main/images.jpeg)



## Features ✨
- Input a movie title, and the system will recommend similar movies.
- Uses a similarity score based on movie metadata such as genres, ratings, etc.
- Capable of handling close matches even if the user input isn't perfectly accurate.

## How It Works 🔍
1. **User Input**: The user enters their favorite movie.
2. **Find Close Match**: The system finds the closest matching movie in the dataset.
3. **Calculate Similarity**: Using a precomputed similarity matrix, the system calculates similarity scores for other movies.
4. **Recommendation**: It then displays the top 30 similar movies based on the similarity score.

![Movie Recommendation Example](https://raw.githubusercontent.com/Prachisinha2005/Movie_Recommendation_system/refs/heads/main/1718046849736-Untitled%20design%20-%202024-06-11T004357.webp)


## Requirements 🛠️
Before running the code, install the following dependencies:

```bash
pip install pandas
pip install difflib
pip install numpy
