from fastapi import APIRouter, Request
from models.song import Song
from controllers import song as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/song")
@validateadmin
async def create_song_route(request: Request, song: Song):
    return controller.create_song(song)

@router.get("/song")
def get_all_songs_route():
    return controller.get_all_songs()

@router.get("/song/{id}")
def get_song_route(id: str):
    return controller.get_song(id)

@router.put("/song/{id}")
@validateadmin
async def update_song_route(request: Request, id: str, song: Song):
    return controller.update_song(id, song)

@router.delete("/song/{id}")
@validateadmin
async def delete_song_route(request: Request, id: str):
    return controller.delete_song(id)