from fastapi import APIRouter, Request
from models.recording_studio import RecordingStudio
from controllers import recording_studio as controller
from utils.security import validateadmin

router = APIRouter()

@router.post("/recording_studio")
@validateadmin
async def create_studio_route(request: Request, estudio: RecordingStudio):
    return controller.create_studio(estudio)

@router.get("/recording_studio")
def get_all_studios_route():
    return controller.get_all_studios()

@router.get("/recording_studio/{id}")
def get_studio_route(id: str):
    return controller.get_studio(id)

@router.put("/recording_studio/{id}")
@validateadmin
async def update_studio_route(request: Request, id: str, estudio: RecordingStudio):
    return controller.update_studio(id, estudio)

@router.delete("/recording_studio/{id}")
@validateadmin
async def delete_studio_route(request: Request, id: str):
    return controller.delete_studio(id)