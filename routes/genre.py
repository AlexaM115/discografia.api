from fastapi import APIRouter, Request
from models.genre import Genre
from controllers import genre as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/genre")
@validateadmin
async def create_genre_route(request: Request, genero: Genre):
    return controller.create_genre(genero)

@router.get("/genre")
def get_all_genres_route():
    return controller.get_all_genres()

@router.get("/genre/{id}")
def get_genre_route(id: str):
    return controller.get_genre(id)

@router.put("/genre/{id}")
@validateadmin
async def update_genre_route(request: Request, id: str, genero: Genre):
    return controller.update_genre(id, genero)

@router.delete("/genre/{id}")
@validateadmin
async def delete_genre_route(request: Request, id: str):
    return controller.delete_genre(id)