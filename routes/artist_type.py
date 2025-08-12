from fastapi import APIRouter, Request
from models.artist_type import ArtistType
from controllers import artist_type as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/artist_type")
@validateadmin
async def create_artist_type_route(request: Request, tipo: ArtistType):
    return controller.create_artist_type(tipo)

@router.get("/artist_type")
def get_all_artist_types_route():
    return controller.get_all_artist_types()

@router.get("/artist_type/{id}")
def get_artist_type_route(id: str):
    return controller.get_artist_type(id)

@router.put("/artist_type/{id}")
@validateadmin
async def update_artist_type_route(request: Request, id: str, tipo: ArtistType):
    return controller.update_artist_type(id, tipo)

@router.delete("/artist_type/{id}")
@validateadmin
async def delete_artist_type_route(request: Request, id: str):
    return controller.delete_artist_type(id)