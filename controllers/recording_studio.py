from models.recording_studio import RecordingStudio
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException

collection = get_collection("recording_studios")

def create_studio(estudio: RecordingStudio):
    if collection.find_one({"description": estudio.description}):
        raise HTTPException(status_code=400, detail="El estudio ya existe")
    result = collection.insert_one(estudio.dict(by_alias=True, exclude={"id"}))
    return {"message": "Estudio creado", "id": str(result.inserted_id)}

def get_all_studios():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_studio(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

def update_studio(id: str, estudio: RecordingStudio):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": estudio.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ningún estudio")
    return {"message": "Estudio actualizado"}

def delete_studio(id: str):
    songs = get_collection("songs")
    if songs.find_one({"id_estudio": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: estudio en uso")
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    return {"message": "Estudio eliminado"}