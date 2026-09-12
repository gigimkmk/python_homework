from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Movie
from schemas import MovieCreate, MovieResponse, MovieUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Catalog API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


@app.get("/")
def home():
    return {"message": "Movie Catalog API is running"}


@app.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.get("/movies", response_model=list[MovieResponse])
def get_movies(
    genre: Optional[str] = None,
    min_rating: Optional[float] = Query(default=None, ge=0, le=10),
    max_rating: Optional[float] = Query(default=None, ge=0, le=10),
    year: Optional[int] = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_rating cannot be greater than max_rating",
        )

    query = select(Movie)

    if genre is not None:
        query = query.where(Movie.genre.ilike(genre))
    if min_rating is not None:
        query = query.where(Movie.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Movie.rating <= max_rating)
    if year is not None:
        query = query.where(Movie.year == year)

    return db.execute(query).scalars().all()


@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie


@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    update_data = movie_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(Movie, movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return {"detail": f"Movie with id {movie_id} deleted successfully"}


@app.get("/movies/search", response_model=list[MovieResponse])
def search_movies(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    query = select(Movie).where(Movie.title.ilike(f"%{q}%"))
    return db.execute(query).scalars().all()