from models.artist import Artist
from utils.mongodb import get_collection
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, date

collection = get_collection("artists")

def create_artist(artist: Artist):
    data = artist.model_dump()
    
    # Convertir la fecha de nacimiento a datetime
    if 'date_birth' in data and isinstance(data['date_birth'], date):
        data['date_birth'] = datetime.combine(data['date_birth'], datetime.min.time())

    
    if collection.find_one({"name": artist.name, "lastname": artist.lastname}):
        raise HTTPException(status_code=400, detail="El artista ya existe")

    data = artist.dict(by_alias=True, exclude={"id"})

    if "active" not in data:
        data["active"] = True  # Valor por defecto

    result = collection.insert_one(data)
    return {"message": "Artista creado", "id": str(result.inserted_id)}


def get_all_artists():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

def get_artist(id: str):
    artist = collection.find_one({"_id": ObjectId(id)})
    if not artist:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    artist["_id"] = str(artist["_id"])
    return artist

def update_artist(id: str, updated_artist: Artist):
    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_artist.dict(by_alias=True, exclude={"id"})}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="No se modificó ningún artista")
    return {"message": "Artista actualizado"}

def delete_artist(id: str):
    colabs = get_collection("colaborations")
    if colabs.find_one({"id_artist": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: artista en colaboración")

    skills = get_collection("artist_skills")
    if skills.find_one({"id_artist": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: artista tiene skills")

    albums = get_collection("albums")
    if albums.find_one({"id_artist": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: artista tiene álbumes")

    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return {"message": "Artista eliminado"}