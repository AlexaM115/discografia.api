from pydantic import BaseModel, Field
from typing import Optional

class ArtistSkill(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    id_artista: str
    id_tipo_artista: str

    class Config:
        allow_population_by_field_name = True