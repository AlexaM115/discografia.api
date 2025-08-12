from pydantic import BaseModel, Field
from typing import Optional

class Colaboration(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    id_artist: str
    id_song: str

    class Config:
        allow_population_by_field_name = True