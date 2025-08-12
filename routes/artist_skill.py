from fastapi import APIRouter, Request
from models.artist_skill import ArtistSkill
from controllers import artist_skill as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/artist_skill")
@validateadmin
async def create_artist_skill_route(request: Request, skill: ArtistSkill):
    return controller.create_artist_skill(skill)

@router.get("/artist_skill")
def get_all_artist_skills_route():
    return controller.get_all_artist_skills()

@router.get("/artist_skill/{id}")
def get_artist_skill_route(id: str):
    return controller.get_artist_skill(id)

@router.delete("/artist_skill/{id}")
@validateadmin
async def delete_artist_skill_route(request: Request, id: str):
    return controller.delete_artist_skill(id)