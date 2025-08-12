from models.genre import Genre
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("genres")

def create_genre(genero: Genre):
    if collection.find_one({"description": genero.description}):
        raise HTTPException(status_code=400, detail="El género ya existe")
    result = collection.insert_one(genero.dict(by_alias=True, exclude={"id"}))
    return {"message": "Género creado", "id": str(result.inserted_id)}

def get_all_genres():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_genre(id: str):
    genero = collection.find_one({"_id": ObjectId(id)})
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    genero["_id"] = str(genero["_id"])
    return genero

def update_genre(id: str, updated: Genre):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ningún género")
    return {"message": "Género actualizado"}

def delete_genre(id: str):
    songs = get_collection("songs")
    if songs.find_one({"id_genero": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: género en uso")
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return {"message": "Género eliminado"}