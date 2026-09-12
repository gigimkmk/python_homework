from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1)
    genre: str = Field(..., min_length=1)
    year: int = Field(..., gt=0, le=2100)
    rating: float = Field(..., ge=0, le=10)
    description: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    genre: Optional[str] = Field(default=None, min_length=1)
    year: Optional[int] = Field(default=None, gt=0, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    description: Optional[str] = None


class MovieResponse(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
