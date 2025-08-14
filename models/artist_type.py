from pydantic import BaseModel, Field
from typing import Optional

class ArtistType(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    description: str
    active: Optional[bool] = True  # 👈 Esto activa el tipo por defecto

    class Config:
        allow_population_by_field_name = True
