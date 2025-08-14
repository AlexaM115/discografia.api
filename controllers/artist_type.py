from models.artist_type import ArtistType
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

from pipelines.artist_type_pipeline import (
    get_artist_type_pipeline
    , validate_type_is_assigned_pipeline
)

collection = get_collection("artist_types")

def create_artist_type(tipo: ArtistType):
    if collection.find_one({"description": tipo.description}):
        raise HTTPException(status_code=400, detail="Tipo de artista ya existe")
    result = collection.insert_one(tipo.dict(by_alias=True, exclude={"id"}))
    return {"message": "Tipo de artista creado", "id": str(result.inserted_id)}

def get_all_artist_types():
    return [{**doc, "_id": str(doc["_id"])} for doc in collection.find()]

async def get_artist_types() -> list:
    try:
        pipeline = get_artist_type_pipeline()
        catalog_types = list(collection.aggregate(pipeline))
        return catalog_types
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching catalog types: {str(e)}")


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

def deactivate_artist_type(artist_type_id: str) -> dict:
    try:
        pipeline = validate_type_is_assigned_pipeline(artist_type_id)
        assigned = list(collection.aggregate(pipeline))

        if assigned is None:
            raise HTTPException(status_code=404, detail="Artist type not found")

        if assigned[0]["number_of_products"] > 0:
            collection.update_one(
                {"_id": ObjectId(artist_type_id)},
                {"$set": {"active": False}}
            )
            return {"message": "Artist type is assigned to products and has been deactivated"}
        else:
            collection.delete_one({"_id": ObjectId(artist_type_id)})
            return {"message": "Artist type deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating artist type: {str(e)}")
    
def delete_artist_type(id: str):
    # Verifica si hay artistas usando ese tipo
    artists = get_collection("artists")
    if artists.find_one({"id_artist_type": id}):
        raise HTTPException(status_code=400, detail="No se puede eliminar: tipo en uso por artistas")

    # Si no está en uso, se elimina
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")
    return {"message": "Tipo de artista eliminado"}
