from pydantic import BaseModel, Field
from typing import Optional

class Song(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    duration: float
    id_artist: str
    id_genre: str
    id_album: str
    id_estudio: str

    class Config:
        allow_population_by_field_name = True