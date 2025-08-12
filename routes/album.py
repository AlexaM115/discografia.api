from fastapi import APIRouter, Request
from models.album import Album
from controllers import album as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/album")
@validateadmin
async def create_album_route(request: Request, album: Album):
    return controller.create_album(album)

@router.get("/album")
def get_all_albums_route():
    return controller.get_all_albums()

@router.get("/album/{id}")
def get_album_route(id: str):
    return controller.get_album(id)

@router.get("/artist/{id}/albums")
def get_albums_by_artist_route(id: str):
    return controller.get_albums_by_artist(id)

@router.put("/album/{id}")
@validateadmin
async def update_album_route(request: Request, id: str, album: Album):
    return controller.update_album(id, album)

@router.delete("/album/{id}")
@validateadmin
async def delete_album_route(request: Request, id: str):
    return controller.delete_album(id)