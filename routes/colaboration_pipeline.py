from fastapi import APIRouter
from pipelines import colaboration_pipeline

router = APIRouter()

@router.get("/colaboration/details")
def get_colaboration_details():
    return colaboration_pipeline.get_colaboration_details()