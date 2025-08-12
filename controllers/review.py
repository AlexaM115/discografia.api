from models.review import Review
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

collection = get_collection("reviews")
song_collection = get_collection("songs")
user_collection = get_collection("users")

def create_review(review: Review):
    if not song_collection.find_one({"_id": ObjectId(review.id_song)}):
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    if not user_collection.find_one({"_id": ObjectId(review.id_user)}):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    result = collection.insert_one(review.dict(by_alias=True, exclude={"id"}))
    return {"message": "Review creada", "id": str(result.inserted_id)}

def get_all_reviews():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_review(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    doc["_id"] = str(doc["_id"])
    return doc

def delete_review(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review no encontrada")
    return {"message": "Review eliminada"}