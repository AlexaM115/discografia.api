from fastapi import APIRouter, Request
from models.artist import Artist
from controllers import artist as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/artist")
@validateadmin
async def create_artist_route(request: Request, artist: Artist):
    return controller.create_artist(artist)

@router.get("/artist")
def get_all_artists_route():
    return controller.get_all_artists()

@router.get("/artist/{id}")
def get_artist_route(id: str):
    return controller.get_artist(id)

@router.put("/artist/{id}")
@validateadmin
def update_artist_route(id: str, artist: Artist):
    return controller.update_artist(id, artist)

@router.delete("/artist/{id}")
@validateadmin
def delete_artist_route(id: str):
    return controller.delete_artist(id)