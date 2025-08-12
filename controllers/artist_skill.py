from models.artist_skill import ArtistSkill
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("artist_skills")
artist_collection = get_collection("artists")
type_collection = get_collection("artist_types")

def create_artist_skill(skill: ArtistSkill):
    if not artist_collection.find_one({"_id": ObjectId(skill.id_artista)}):
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    if not type_collection.find_one({"_id": ObjectId(skill.id_tipo_artista)}):
        raise HTTPException(status_code=404, detail="Tipo de artista no encontrado")
    if collection.find_one({
        "id_artista": skill.id_artista,
        "id_tipo_artista": skill.id_tipo_artista
    }):
        raise HTTPException(status_code=400, detail="Relación ya existe")
    result = collection.insert_one(skill.dict(by_alias=True, exclude={"id"}))
    return {"message": "Relación artista ↔ tipo creada", "id": str(result.inserted_id)}

def get_all_artist_skills():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_artist_skill(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    doc["_id"] = str(doc["_id"])
    return doc

def delete_artist_skill(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"message": "Relación eliminada"}