from fastapi import APIRouter, Request
from models.colaboration import Colaboration
from controllers import colaboration as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/colaboration")
@validateadmin
async def create_colaboration_route(request: Request, colab: Colaboration):
    return controller.create_colaboration(colab)

@router.get("/colaboration")
def get_all_colaborations_route():
    return controller.get_all_colaborations()

@router.get("/colaboration/{id}")
def get_colaboration_route(id: str):
    return controller.get_colaboration(id)

@router.delete("/colaboration/{id}")
@validateadmin
async def delete_colaboration_route(request: Request, id: str):
    return controller.delete_colaboration(id)