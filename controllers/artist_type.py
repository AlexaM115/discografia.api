from models.artist_type import ArtistType
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

collection = get_collection("artist_types")

def create_artist_type(tipo: ArtistType):
    if collection.find_one({"description": tipo.description}):
        raise HTTPException(status_code=400, detail="Tipo de artista ya existe")
    result = collection.insert_one(tipo.dict(by_alias=True, exclude={"id"}))
    return {"message": "Tipo de artista creado", "id": str(result.inserted_id)}

def get_all_artist_types():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_artist_type(id: str):
    tipo = collection.find_one({"_id": ObjectId(id)})
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de artista no encontrado")
    tipo["_id"] = str(tipo["_id"])
    return tipo

def update_artist_type(id: str, tipo: ArtistType):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": tipo.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ningún tipo")
    return {"message": "Tipo de artista actualizado"}

def delete_artist_type(id: str):
    skills = get_collection("artist_skills")
    if skills.find_one({"id_tipo_artista": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: está en uso")
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return {"message": "Tipo de artista eliminado"}