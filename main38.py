from fastapi import FastAPI, HTTPException

app = FastAPI()


movies = [
    {
        "id": 1,
        "title": "The Matrix",
        "genre": "sci-fi",
        "year": 1999,
        "rating": 8.7
    },
    {
        "id": 2,
        "title": "Inception",
        "genre": "sci-fi",
        "year": 2010,
        "rating": 8.8
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "genre": "action",
        "year": 2008,
        "rating": 9.0
    },
    {
        "id": 4,
        "title": "The Hangover",
        "genre": "comedy",
        "year": 2009,
        "rating": 7.7
    },
    {
        "id": 5,
        "title": "The Shawshank Redemption",
        "genre": "drama",
        "year": 1994,
        "rating": 9.3
    },
    {
        "id": 6,
        "title": "Parasite",
        "genre": "drama",
        "year": 2019,
        "rating": 8.5
    },
    {
        "id": 7,
        "title": "Joker",
        "genre": "drama",
        "year": 2019,
        "rating": 8.4
    },
    {
        "id": 8,
        "title": "Superbad",
        "genre": "comedy",
        "year": 2007,
        "rating": 7.6
    },
    {
        "id": 9,
        "title": "The Godfather",
        "genre": "drama",
        "year": 1972,
        "rating": 9.2
    },
    {
        "id": 10,
        "title": "The Batman",
        "genre": "action",
        "year": 2022,
        "rating": 7.8
    }
]


@app.get("/movies")
def get_movies(
    genre: str | None = None,
    year: int | None = None,
    min_rating: float | None = None,
    search: str | None = None
):
    result = movies

    if genre:
        result = [
            movie for movie in result
            if movie["genre"].lower() == genre.lower()
        ]

    if year:
        result = [
            movie for movie in result
            if movie["year"] == year
        ]

    if min_rating is not None:
        result = [
            movie for movie in result
            if movie["rating"] >= min_rating
        ]

    if search:
        result = [
            movie for movie in result
            if search.lower() in movie["title"].lower()
        ]

    return result


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )