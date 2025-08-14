from pydantic import BaseModel, Field
from typing import Optional

class Artist(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    lastname: str
    gender: str
    date_birth: str
    id_artist_type: str
    description: str
    active: Optional[bool] = True  # 👈 este campo era el que faltaba

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
