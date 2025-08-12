from pydantic import BaseModel, Field
from typing import Optional

class Genre(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    description: str

    class Config:
        allow_population_by_field_name = True