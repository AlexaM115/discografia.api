from fastapi import APIRouter
from pipelines import review_pipeline

router = APIRouter()

@router.get("/review/average")
def get_average_reviews():
    return review_pipeline.get_average_reviews()