from models.colaboration import Colaboration
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("colaborations")
artist_collection = get_collection("artists")
song_collection = get_collection("songs")

def create_colaboration(colab: Colaboration):
    if not artist_collection.find_one({"_id": ObjectId(colab.id_artist)}):
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    if not song_collection.find_one({"_id": ObjectId(colab.id_song)}):
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    if collection.find_one({"id_artist": colab.id_artist, "id_song": colab.id_song}):
        raise HTTPException(status_code=400, detail="Colaboración ya existe")
    result = collection.insert_one(colab.dict(by_alias=True, exclude={"id"}))
    return {"message": "Colaboración creada", "id": str(result.inserted_id)}

def get_all_colaborations():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_colaboration(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Colaboración no encontrada")
    doc["_id"] = str(doc["_id"])
    return doc

def delete_colaboration(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Colaboración no encontrada")
    return {"message": "Colaboración eliminada"}