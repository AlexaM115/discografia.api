from fastapi import APIRouter
from pipelines import song_pipeline

router = APIRouter()

@router.get("/song/details")
def get_song_details():
    return song_pipeline.get_song_details()