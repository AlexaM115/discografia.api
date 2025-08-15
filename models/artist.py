from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Artist(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    lastname: str
    gender: str
    date_birth: date
    id_artist_type: str
    active: Optional[bool] = True 

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Juan",
                "lastname": "García",
                "gender": "Masculino",
                "date_birth": "1990-01-01",
                "id_artist_type": "605c5f33e1a3b942509ecf94",
                "description": "Artista versátil y carismático",
                "active": True
            }
        }
