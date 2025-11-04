import pandas as pd
import random

movies = pd.DataFrame({
    "movie_id": range(1, 11),
    "title": [f"Movie {i}" for i in range(1, 11)],
    "genres": ["Action|Comedy"]*10,
    "description": ["Lorem ipsum"]*10
})
movies.to_csv("movies.csv", index=False)

ratings = pd.DataFrame({
    "user_id": [random.randint(1,5) for _ in range(30)],
    "movie_id": [random.randint(1,10) for _ in range(30)],
    "rating": [random.randint(1,5) for _ in range(30)],
    "timestamp": [1234567890 + i for i in range(30)]
})
ratings.to_csv("ratings.csv", index=False)
