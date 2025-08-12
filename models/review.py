from pydantic import BaseModel, Field
from typing import Optional

class Review(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    id_song: str
    id_user: str
    rating: float
    comment: str

    class Config:
        allow_population_by_field_name = True