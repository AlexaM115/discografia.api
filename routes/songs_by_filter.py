from fastapi import APIRouter
from pipelines import songs_by_artist_pipeline, songs_by_album_pipeline

router = APIRouter()

@router.get("/artist/{id}/songs")
def get_songs_by_artist(id: str):
    return songs_by_artist_pipeline.get_songs_by_artist(id)

@router.get("/album/{id}/songs")
def get_songs_by_album(id: str):
    return songs_by_album_pipeline.get_songs_by_album(id)