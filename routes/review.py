from fastapi import APIRouter, Request
from models.review import Review
from controllers import review as controller
from utils.security import validateuser, validateadmin

router = APIRouter()

@router.post("/review")
@validateuser
async def create_review_route(request: Request, review: Review):
    return controller.create_review(review)

@router.get("/review")
def get_all_reviews_route():
    return controller.get_all_reviews()

@router.get("/review/{id}")
def get_review_route(id: str):
    return controller.get_review(id)

@router.delete("/review/{id}")
@validateadmin
async def delete_review_route(request: Request, id: str):
    return controller.delete_review(id)