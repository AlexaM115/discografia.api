from pydantic import BaseModel, Field
from typing import Optional

class Album(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    año: int
    descripcion: str
    photo: str
    id_artist: str

    class Config:
        allow_population_by_field_name = True